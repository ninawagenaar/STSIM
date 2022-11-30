import simpy
import numpy as np
from random import expovariate
import scipy.stats as st


def customer(env, name, bcs, lambd, mu, wait_times):

    # Arrivals occur at rate λ according to a Poisson proces
    time_before_arr = np.random.poisson(lambd, size=None)
    yield env.timeout(time_before_arr)
    start_wait = env.now
    print('%s arriving at %d' % (name, start_wait))

    # Waiting room
    with bcs.request() as req:
        # Service times have an exponential distribution with rate parameter μ
        yield req
        service_time = expovariate(1.0/mu)
        end_wait = env.now  
        wait_times.append(end_wait-start_wait)
        print('%s being served %s' % (name, end_wait))
        yield env.timeout(service_time)
        print('%s leaving the bcs at %s' % (name, env.now))

def main():
    ## Experiment data                         
    no_customers = 100
    # number of servers = n
    no_servers = 10
    # parameter for poisson proces
    lambd = 1.9
    # parameter for exponential distribution
    mu = 2
    rho = lambd / (no_servers * mu)
    print("rho:", rho)

    env = simpy.Environment()
    bcs = simpy.Resource(env, capacity=no_servers)
    wait_times = []
    for i in range(no_customers):
        env.process(customer(env, 'Customer %d' % i, bcs, lambd, mu, wait_times))
    env.run()
    avg_wait = np.mean(wait_times)
    print("average wait time:", avg_wait)

    #create 95% confidence interval for population mean weight
    ci = st.t.interval(confidence=0.95, df=len(wait_times)-1, loc=np.mean(wait_times), scale=st.sem(wait_times)) 
    print("95 percent confidence interval:", ci)

if __name__ == "__main__":
    main()  



