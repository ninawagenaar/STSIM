"""
GIVE EXPLANATION OF WHAT THIS DOC DOES
"""
import random
import simpy
import numpy as np

class Servers(object):
    """
    
    """
    def __init__(self, env, num_servers, capacity):
        self.env = env
        self.machine = simpy.Resource(env, num_servers)
        self.capacity = capacity

    def serve(self, name):
        """
        
        """
        servetime = random.expovariate(self.capacity)
        yield self.env.timeout(servetime)


def customer(env, name, s, wait_times):
    """

    """
    with s.machine.request() as request:
        start_wait = env.now
        #print('%s enters the at %.2f.' % (name, env.now))
        yield request
        end_wait = env.now
        #print('%s served at %.2f.' % (name, env.now))
        wait_time = [end_wait - start_wait]
        # Record witing time
        wait_times.append(wait_time)

        yield env.process(s.serve(name))
        #print('%s leaves at %.2f.' % (name, env.now))



def setup(env, num_servers, num_customers, capacity, arrival_rate, wait_times):
    """

    """
    # Create the carwash
    servers = Servers(env, num_servers, capacity)

    # Create n initial customers
    for i in range(num_servers):
        env.process(customer(env, 'Customer %d' % i, servers, wait_times))

    # Create more cars while the sicapacitylation is running
    for i in range(num_servers, num_customers):
        arrival_time = random.expovariate(arrival_rate)
        yield env.timeout(arrival_time)
        i += 1
        env.process(customer(env, 'Customer %d' % i, servers, wait_times))


def run_simulation(num_servers, num_simulations, num_customers, capacity, arrival_rate):
    avg_wait_times = np.zeros((len(num_servers), num_simulations))

    for idx_n in range(len(num_servers)):
        for sim in range(num_simulations):
            wait_times = []
            arrival_rate_n = arrival_rate * num_servers[idx_n]
            # Create an environment and start the setup process
            env = simpy.Environment()
            env.process(setup(env, num_servers[idx_n], num_customers, capacity, arrival_rate_n, wait_times))
            # Execute!
            env.run()
            avg_wait_times[idx_n][sim] = np.mean(wait_times)

    return avg_wait_times

num_servers = [1,2,4]
num_simulations = 100
num_customers = 50
capacity = 2
arrival_rate = 1.9
avg_wait_times = run_simulation(num_servers, num_simulations, num_customers, capacity, arrival_rate)

# Results
mean_over_sim = [np.mean(result_n_servers) for result_n_servers in avg_wait_times]
print(mean_over_sim)