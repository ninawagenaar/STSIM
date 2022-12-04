import m_m_n as simulate
import plotting

#First experiment: waiting time for customer number

def exp_queue_position(num_servers, num_customers, wait_times_cust):
    plotting.plot_dep_customers(num_servers, num_customers, wait_times_cust)

def exp_dep_servers(num_servers, avg_wait_times):
    plotting.plot_dep_servers_line(num_servers, avg_wait_times[:,20:])
    plotting.plot_dep_servers_histo(num_servers, avg_wait_times[:,20:])

''''
def exp_rho_dep(num_servers, num_simulations, num_customers, capacity):
    arrival_rates = [1.1 ,1.3 ,1.5 ,1.7 ,1.9]
    for arrival_rate in arrival_rates:
        avg_wait_times, _ = simulate.run_simulation(num_servers, num_simulations, num_customers, capacity, arrival_rate)
        plotting.plot_avg_wait_times()
'''


#Default variables
num_servers = [1,2,4]
num_simulations = 5000
num_customers = 2000
capacity = 2
arrival_rate = 1.9

#Experiment to carry out
avg_wait_times, wait_times_cust = simulate.run_simulation(num_servers, num_simulations, num_customers, capacity, arrival_rate)
#exp_queue_position(num_servers, num_customers, wait_times_cust)
exp_dep_servers(num_servers, avg_wait_times)