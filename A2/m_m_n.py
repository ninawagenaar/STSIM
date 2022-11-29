import simpy
import numpy as np
from random import expovariate


def customer(env, name, bcs, lambd, mu):
    # Arrivals occur at rate λ according to a Poisson proces
    time_before_arr = np.random.poisson(lambd, size=None)
    yield env.timeout(time_before_arr)
    print('%s arriving at %d' % (name, env.now))


    # Waiting room
    with bcs.request() as req:
        # Service times have an exponential distribution with rate parameter μ
        yield req
        service_time = expovariate(1.0/mu)  
        print('%s being served %s' % (name, env.now))
        yield env.timeout(service_time)
        print('%s leaving the bcs at %s' % (name, env.now))

def main():
    ## Experiment data 
    maxTime = 100.0                           
    no_customers = 4
    no_servers = 1
    lambd = 0.9
    mu = 10


    env = simpy.Environment()
    bcs = simpy.Resource(env, capacity=no_servers)

    for i in range(no_customers):
        env.process(customer(env, 'Customer %d' % i, bcs, lambd, mu))
    env.run(until=maxTime)

if __name__ == "__main__":
    main()  



