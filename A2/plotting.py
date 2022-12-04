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


def plot_dep_servers_box(num_servers, avg_wait_times):
    plt.title("Relation between number of servers and average wait time")
    plt.xlabel("Number of servers")
    plt.ylabel("Average wait time")
    ax = plt.boxplot(avg_wait_times.T, patch_artist=True, labels=num_servers)
    # fill with colors
    colors = ['pink', 'lightblue', 'lightgreen']
    for patch, color in zip(ax['boxes'], colors):
         patch.set_facecolor(color)
    plt.show()  

def plot_dep_rho(num_servers, rhos, avg_wait_times):
    for idx_n in range(len(num_servers)):
        n = num_servers[idx_n]
        xdata = rhos
        ydata = avg_wait_times[idx_n]

        avg_ydata = [np.mean(data) for data in ydata]

        ci = [st.t.interval(confidence=0.95, df=len(data)-1, loc=np.mean(data), scale=st.sem(data)) for data in ydata]
        ci_lower = [i[0] for i in ci]
        ci_higher = [i[1] for i in ci]  

        line, = plt.plot(xdata, avg_ydata, label = f"number of servers =  {n}")
        plt.fill_between(xdata, ci_lower, ci_higher, color=line.get_color(), alpha=0.2)
        plt.legend()
        plt.gca().yaxis.grid()

    plt.title("Relation between Rho and average wait time") 
    plt.xlabel("Rho")
    plt.ylabel("Average wait time")
    plt.show()  



    


    