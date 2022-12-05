import random
import simpy
import numpy as np
import scipy.stats as st
import plotting

class Servers(object):
    """
    A class for the servers that serve the customers
    """
    def __init__(self, env, num_servers, capacity):
        self.env = env
        self.machine = simpy.PriorityResource(env, num_servers)
        self.capacity = capacity
        self.servetime = None

    def set_servetime(self, queue_type):
        """
        Set a servetime based on the service rate distribution used
        """
        if queue_type == "m_m_n":
            self.servetime = random.expovariate(self.capacity)
        if queue_type == "m_d_n":
            self.servetime = 1 / self.capacity
        if queue_type == "long_tailed":
            if np.random.rand() < 0.75:
                self.servetime = random.expovariate(1)
            else:
                self.servetime = random.expovariate(5)


def customer(env, name, s, wait_times, queue_structure, queue_type):
    """
    Function that simulates a customer standing in a queue and them being served
    """
    s.set_servetime(queue_type)
    servetime = s.servetime

    # If the queue structure is SJFS, priority is based on low servetime
    if queue_structure == "SJFS":
        priority = servetime
    else:
        priority = None

    # Stand in queue
    with s.machine.request(priority) as request:
        start_wait = env.now
        yield request

        # Leave queue
        end_wait = env.now
        wait_time = end_wait - start_wait
        wait_times.append(wait_time)
        yield env.timeout(servetime)



def setup(env, num_servers, num_customers, capacity, arrival_rate, wait_times, queue_structure, queue_type):
    """
    Setup the simulation by creating the servers and customers
    """
    # Create the servers
    servers = Servers(env, num_servers, capacity)

    # Create n initial customers
    for i in range(num_servers):
        env.process(customer(env, 'Customer %d' % i, servers, wait_times, queue_structure, queue_type))

    # Create more customers while the sicapacitylation is running
    for i in range(num_servers, num_customers):
        arrival_time = random.expovariate(arrival_rate)
        yield env.timeout(arrival_time)
        i += 1
        env.process(customer(env, 'Customer %d' % i, servers, wait_times, queue_structure, queue_type))


def run_simulation(num_servers, num_simulations, num_customers, capacity, arrival_rate, queue_structure = "FIFO", queue_type = "m_m_n"):
    """
    Run simulation n times and return the average waiting times recorded for each simulation
    """
    avg_wait_times = np.empty((len(num_servers), num_simulations))
    wait_times_cust = []
    for idx_n in range(len(num_servers)):
        wait_times_cust_n = []
        for sim in range(num_simulations):
            wait_times = []
            arrival_rate_n = arrival_rate * num_servers[idx_n]

            # Create an environment and start the setup process
            env = simpy.Environment()
            env.process(setup(env, num_servers[idx_n], num_customers, capacity, arrival_rate_n, wait_times, queue_structure, queue_type))

            # Execute!
            env.run()
            avg_wait_times[idx_n][sim] = np.mean(wait_times)
            wait_times_cust_n.append(wait_times)
        wait_times_cust.append(wait_times_cust_n)

    wait_times_cust = np.array(wait_times_cust)
    return avg_wait_times, wait_times_cust