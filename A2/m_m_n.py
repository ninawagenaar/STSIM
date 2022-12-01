"""
GIVE EXPLANATION OF WHAT THIS DOC DOES
"""
import random
import simpy
import numpy as np


RANDOM_SEED = 42
SIM_TIME = 2000


class Servers(object):
    """
    
    """
    def __init__(self, env, num_servers, capacity):
        self.env = env
        self.machine = simpy.Resource(env, num_servers)
        self.capacity = capacity

    def serve(self):
        """
        
        """
        servetime = random.expovariate(self.capacity)
        yield self.env.timeout(servetime)

def customer(env, name, s, wait_times):
    """

    """
    with s.machine.request() as request:
        start_wait = env.now
        yield request
        end_wait = env.now
        wait_time = [end_wait - start_wait]

        # Record witing time
        wait_times.append(wait_time)

        yield env.process(s.serve())



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


def run_simulation(num_servers, num_customers, capacity, arrival_rate):
    avg_wait_times = np.empty(len(num_servers))
    for idx_n in range(len(num_servers)):
        arrival_rate = arrival_rate * num_servers[idx_n]
        wait_times = []
        # Create an environment and start the setup process
        env = simpy.Environment()
        env.process(setup(env, num_servers[idx_n], num_customers, capacity, arrival_rate, wait_times))
        # Execute!
        env.run()
        avg_wait_times[idx_n] = np.mean(wait_times) 

    # Print record
    print(avg_wait_times)

random.seed(RANDOM_SEED)  # This helps reproducing the results 
num_servers = [1, 2, 4]
num_customers = 30000
capacity = 2
arrival_rate = 1.9
run_simulation(num_servers, num_customers, capacity, arrival_rate)