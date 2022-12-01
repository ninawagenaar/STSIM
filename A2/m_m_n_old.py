import simpy
import numpy as np
import random 
import scipy.stats as st
import matplotlib.pyplot as plt


def customer(env, name, bcs, lambd, mu, wait_times, queue_type = "FIFO"):
    # Arrivals occur at rate λ according to a Poisson proces

    #print('%s arriving at %d' % (name, start_wait))

    # Waiting room
    with bcs.request() as req:
        # Service times have an exponential distribution with rate parameter μ
        start_wait = env.now
        yield req
        end_wait = env.now  

        service_time = random.expovariate(mu)

        print("wait", end_wait-start_wait, start_wait, end_wait)
        wait_times.append(end_wait-start_wait)
        #print('%s being served %s' % (name, end_wait))
        yield env.timeout(service_time)
        #print('%s leaving the bcs at %s' % (name, env.now))


def setup(env, n_customers, bcs, lambd_n, mu, wait_times):
    for i in range(2):
        env.process(customer(env, 'Customer %d' % i, bcs, lambd_n, mu, wait_times))
        print("here")

    for customer in range(2, n_customers):
        time_before_arrival = random.expovariate(lambd_n)
        yield env.timeout(time_before_arrival)
        env.process(customer(env, 'Customer %d' % i, bcs, lambd_n, mu, wait_times))


def run_simulation(n_simulations, n_customers, lambd, mu, n):

    avg_waits_n = np.empty((3,n_simulations))

    for idx in range(len(n)):
        print("n", n[idx])

        lambd_n = (lambd * n[idx])
        rho = lambd_n / ( n[idx] * mu)

        for sim in range(n_simulations):
            env = simpy.Environment()
            bcs = simpy.Resource(env, capacity = n[idx])
            wait_times = []
            setup(env, n_customers, bcs, lambd_n, mu, wait_times)
            env.run()
            avg_wait = np.mean(wait_times)
            avg_waits_n[idx][sim] = avg_wait

    return avg_waits_n

def plot_dep_servers(n, avg_wait_times):
    means = [np.mean(list) for list in avg_wait_times]
    print(len(avg_wait_times[0])-1)
    print(avg_wait_times.shape)
    print(len(avg_wait_time_n) for avg_wait_time_n in avg_wait_times)
    ci = [st.t.interval(confidence=0.95, df=len(avg_wait_time_n)-1, loc=np.mean(avg_wait_time_n), scale=st.sem(avg_wait_time_n)) for avg_wait_time_n in avg_wait_times]
    ci_lower = [i[0] for i in ci]
    ci_higher = [i[1] for i in ci]  
    plt.fill_between(n, ci_lower, ci_higher, color='blue', alpha=0.2)
    plt.title("Relation between number of servers and average wait time")
    plt.xlabel("Number of servers")
    plt.ylabel("Average wait time")
    plt.plot(n, means)
    plt.show()

def plot_dep_customers(n_customers, means):
    plt.title("Relation between number of customers and average wait time") 
    plt.xlabel("Number of servers")
    plt.ylabel("Average wait time")
    plt.plot(np.arange(0, n_customers), means[0, :], label = "n = 1")
    plt.plot(np.arange(0, n_customers), means[1, :], label = "n = 2")
    plt.plot(np.arange(0, n_customers), means[2, :], label = "n = 4")
    plt.legend()
    plt.show()

def main():
    n_simulations = 100
    ## Experiment data                         
    n_customers = 1000
    # number of servers = n
    n = [1]
    # parameter for poisson proces
    lambd = 1
    # parameter for exponential distribution
    mu = 2

    avg_wait_times = run_simulation(n_simulations, n_customers, lambd, mu, n)

    #Make plots
    #plot_dep_servers(n, avg_wait_times)

if __name__ == "__main__":
    main()  



