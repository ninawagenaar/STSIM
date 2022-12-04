import m_m_n as simulate
import plotting

#First experiment: waiting time for customer number

def exp_queue_position(num_servers, num_customers, wait_times_cust):
    plotting.plot_dep_customers(num_servers, num_customers, wait_times_cust)

def exp_dep_servers(num_servers, avg_wait_times):
    plotting.plot_dep_servers_box(num_servers, avg_wait_times)

def exp_dep_rho(num_servers, num_simulations, num_customers, capacity):

    if len(num_servers) != 3:
        print("Please provide a list of 3 for the number of servers")
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

def exp_queue_dep(num_servers, avg_wait_times_FIFO, avg_wait_times_SJFS):
    plotting.plot_dep_queue(num_servers, avg_wait_times_FIFO, avg_wait_times_SJFS)



#Default variables
num_servers = [1,2,4]
num_simulations = 200
num_customers = 200
capacity = 2
arrival_rate = 1.9

#Experiment to carry out
avg_wait_times_FIFO, wait_times_cust_FIFO = simulate.run_simulation(num_servers, num_simulations, num_customers, capacity, arrival_rate)
avg_wait_times_FIFO = avg_wait_times_FIFO[:20]
#exp_queue_position(num_servers, num_customers, wait_times_cust)
#exp_dep_servers(num_servers, avg_wait_times_FIFO)
#exp_dep_rho(num_servers, num_simulations, num_customers, capacity)
avg_wait_times_SJFS, _ = simulate.run_simulation(num_servers, num_simulations, num_customers, capacity, arrival_rate, "SJFS")
avg_wait_times_SJFS = avg_wait_times_SJFS[:20]
exp_queue_dep(num_servers, avg_wait_times_FIFO, avg_wait_times_SJFS)