import simulation as simulate
import plotting
import scipy.stats as stats


#First experiment: waiting time for customer number

def exp_queue_position(num_servers, num_customers, wait_times_cust):
    """
    Experiment to see how the queue position affects the average waiting time
    """
    plotting.plot_dep_customers(num_servers, num_customers, wait_times_cust)


def exp_dep_servers(num_servers, avg_wait_times):
    """
    Experiment to see if the average waiting time is dependent on the number of servers
    """
    plotting.plot_dep_servers_box(num_servers, avg_wait_times)

    print('')
    print("Results for the experiment on influence number of servers")

    print("Results T-test to see if mean n= 1 is greater than n=2")
    print(stats.ttest_ind(avg_wait_times[0], avg_wait_times[1], alternative="greater"))

    print("Results T-test to see if mean n= 1 is greater than n=4")
    print(stats.ttest_ind(avg_wait_times[0], avg_wait_times[2], alternative="greater"))


def exp_dep_rho(num_servers, num_simulations, num_customers, capacity):
    """
    Experiment to see how the average waiting time depends on rho for different number of servers
    """

    if len(num_servers) != 3:
        print("Please provide a list of 3 for number of servers")
        return

    arrival_rates = [1.1 ,1.3 ,1.5 ,1.7 ,1.9]
    rhos = [arrival_rate / capacity for arrival_rate in arrival_rates]
    data_n1 = []
    data_n2 = []
    data_n4 = []
    data_all = []
    for arrival_rate in arrival_rates:
        avg_wait_times, _ = simulate.run_simulation(num_servers, num_simulations, num_customers, capacity, arrival_rate)
        data_n1.append(avg_wait_times[0])
        data_n2.append(avg_wait_times[1])
        data_n4.append(avg_wait_times[2])
    data_all = [data_n1, data_n2, data_n4]
    plotting.plot_dep_rho(num_servers, rhos, data_all)

def exp_dep_queue_struct(num_servers, avg_wait_times_FIFO, avg_wait_times_SJFS):
    """
    Experiment to see how the average waiting time depends on the queue structure
    """
    plotting.plot_dep_queue_struct(num_servers, avg_wait_times_FIFO, avg_wait_times_SJFS)

    print('')
    print("Results for the experiment on queue structure")

    print("Results T-test to see if mean FIFO is greater than mean SJFS for n = 1")
    print(stats.ttest_ind(avg_wait_times_FIFO[0], avg_wait_times_SJFS[0], alternative="greater"))

    print("Results T-test to see if mean FIFO is greater than mean SJFS for n = 2")
    print(stats.ttest_ind(avg_wait_times_FIFO[1], avg_wait_times_SJFS[1], alternative="greater"))

    print("Results T-test to see if mean FIFO is greater than mean SJFS for n = 4")
    print(stats.ttest_ind(avg_wait_times_FIFO[2], avg_wait_times_SJFS[2], alternative="greater"))


def exp_dep_queue_type(num_servers, avg_wait_times_m_m_n, avg_wait_times_m_d_n, avg_wait_times_lt, structure):
    """"
    Experiment to see how the average waiting time depends on the service rate distribution
    """
    plotting.plot_dep_queue_type(num_servers, avg_wait_times_m_m_n, avg_wait_times_m_d_n, avg_wait_times_lt, structure)

    print('')
    print(f"Results for the experiment on queue types using structure {structure}")

    print("results to see if mean m_m_n queue is different from m_d_n queue for n = 1")
    print(stats.ttest_ind(avg_wait_times_m_m_n[0], avg_wait_times_m_d_n[0]))

    print("results to see if mean m_m_n queue is different from m_d_n queue for n = 2")
    print(stats.ttest_ind(avg_wait_times_m_m_n[1], avg_wait_times_m_d_n[1]))

    print("results to see if mean m_m_n queue is different from m_d_n queue for n = 4")
    print(stats.ttest_ind(avg_wait_times_m_m_n[2], avg_wait_times_m_d_n[2]))

    print("results to see if mean m_m_n queue is different from long-tailed queue for n = 1")
    print(stats.ttest_ind(avg_wait_times_m_m_n[0], avg_wait_times_lt[0]))

    print("results to see if mean m_m_n queue is different from long-tailed queue for n = 2")
    print(stats.ttest_ind(avg_wait_times_m_m_n[0], avg_wait_times_lt[0]))

    print("results to see if mean m_m_n queue is different from long-tailed queue for n = 4")
    print(stats.ttest_ind(avg_wait_times_m_m_n[0], avg_wait_times_lt[0]))



#Default variables
num_servers = [1,2,4]
num_simulations = 2000
num_customers = 4000
capacity = 2
arrival_rate = 1.9
throwaway = 1000

# Get some initial results to limit the amount of dublicate computations needed for experiments

avg_wait_times_FIFO_m_m_n, wait_times_cust_FIFO_m_m_n = simulate.run_simulation(num_servers, num_simulations, num_customers, capacity, arrival_rate)
avg_wait_times_FIFO_m_m_n = avg_wait_times_FIFO_m_m_n[:throwaway]
avg_wait_times_SJFS_m_m_n, _ = simulate.run_simulation(num_servers, num_simulations, num_customers, capacity, arrival_rate, "SJFS")
avg_wait_times_SJFS_m_m_n = avg_wait_times_SJFS_m_m_n[:throwaway]

avg_wait_times_FIFO_m_d_n, _ = simulate.run_simulation(num_servers, num_simulations, num_customers, capacity, arrival_rate, "FIFO", "m_d_n")
avg_wait_times_FIFO_m_d_n = avg_wait_times_FIFO_m_d_n[:throwaway]
avg_wait_times_SJFS_m_d_n, _ = simulate.run_simulation(num_servers, num_simulations, num_customers, capacity, arrival_rate, "SJFS", "m_d_n")
avg_wait_times_SJFS_m_d_n = avg_wait_times_SJFS_m_d_n[:throwaway]

avg_wait_times_FIFO_lt, _ = simulate.run_simulation(num_servers, num_simulations, num_customers, capacity, arrival_rate, "FIFO", "long_tailed")
avg_wait_times_FIFO_lt = avg_wait_times_FIFO_lt[:throwaway]
avg_wait_times_SJFS_lt, _ = simulate.run_simulation(num_servers, num_simulations, num_customers, capacity, arrival_rate, "SJFS", "m_d_n")
avg_wait_times_SJFS_lt = avg_wait_times_SJFS_m_d_n[:throwaway]

# Experiments to carry out

# Question 2
exp_queue_position(num_servers, num_customers, wait_times_cust_FIFO_m_m_n)
exp_dep_servers(num_servers, avg_wait_times_FIFO_m_m_n)
exp_dep_rho(num_servers, num_simulations, num_customers, capacity)

# Question 3
exp_dep_queue_struct(num_servers, avg_wait_times_FIFO_m_m_n, avg_wait_times_SJFS_m_m_n)

# Question 4
exp_dep_queue_type(num_servers, avg_wait_times_FIFO_m_m_n, avg_wait_times_FIFO_m_d_n, avg_wait_times_FIFO_lt, "FIFO")
exp_dep_queue_type(num_servers, avg_wait_times_SJFS_m_m_n, avg_wait_times_FIFO_m_d_n, avg_wait_times_SJFS_lt, "SJFS")