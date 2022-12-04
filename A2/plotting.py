import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import seaborn as sns

def plot_dep_customers(num_servers, num_customers, wait_times_cust):
    for idx_n in range(len(num_servers)):
        n = num_servers[idx_n]
        xdata = np.arange(0, num_customers)
        ydata = wait_times_cust[idx_n].T

        avg_ydata = [np.mean(data) for data in ydata]

        ci = [st.t.interval(confidence=0.95, df=len(data)-1, loc=np.mean(data), scale=st.sem(data)) for data in ydata]
        ci_lower = [i[0] for i in ci]
        ci_higher = [i[1] for i in ci]  

        line, = plt.plot(xdata, avg_ydata, label = f"number of servers =  {n}")
        plt.fill_between(xdata, ci_lower, ci_higher, color=line.get_color(), alpha=0.2)
        plt.legend()
        plt.gca().yaxis.grid()

    plt.title("Relation between number of customers and average wait time") 
    plt.xlabel("Queue position customer")
    plt.ylabel("Average wait time")
    plt.show()  

def plot_dep_servers_line(num_servers, avg_wait_times):
    xdata = num_servers
    ydata = avg_wait_times
    avg_ydata  = [np.mean(list) for list in avg_wait_times]

    # Make line plot
    ci = [st.t.interval(confidence=0.95, df=len(data)-1, loc=np.mean(data), scale=st.sem(data)) for data in ydata]
    ci_lower = [i[0] for i in ci]
    ci_higher = [i[1] for i in ci]  
   
    plt.title("Relation between number of servers and average wait time")
    plt.xlabel("Number of servers")
    plt.ylabel("Average wait time")
    line, = plt.plot(xdata, avg_ydata)
    plt.fill_between(xdata, ci_lower, ci_higher, color=line.get_color(), alpha=0.2)
    plt.gca().yaxis.grid()
    plt.show()

def plot_dep_servers_histo(num_servers, avg_wait_times):
    for idx_n in range(len(num_servers)):
        n = num_servers[idx_n]
        sns.distplot(avg_wait_times[idx_n], hist=True, kde=True, 
             bins=100, kde_kws={'linewidth': 2}, label=f"number of servers =  {n}")
        plt.legend()
        plt.gca().yaxis.grid()

    plt.title("Density Distribution of Average Wait Time per No. of Servers") 
    plt.ylabel("Average wait time")
    plt.show()  

    
    


    
