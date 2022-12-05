import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import seaborn as sns

def plot_dep_customers(num_servers, num_customers, wait_times_cust):
    """
    Plot the dependency of the average waiting time of the count that the customer enters the queue
    So the 1000th customer is the 1000th person that has entered that queue
    """
    for idx_n in range(len(num_servers)):
        n = num_servers[idx_n]
        xdata = np.arange(0, num_customers)
        ydata = wait_times_cust[idx_n].T

        avg_ydata = [np.mean(data) for data in ydata]

        # Calculate 95% confidence intervals
        ci = [st.t.interval(confidence=0.95, df=len(data)-1, loc=np.mean(data), scale=st.sem(data)) for data in ydata]
        ci_lower = [i[0] for i in ci]
        ci_higher = [i[1] for i in ci]  

        line, = plt.plot(xdata, avg_ydata, label = f"number of servers =  {n}")
        plt.fill_between(xdata, ci_lower, ci_higher, color=line.get_color(), alpha=0.2)
        plt.legend()

    plt.gca().yaxis.grid()
    plt.title("Relation between number of customers and average wait time") 
    plt.xlabel("Queue position customer")
    plt.ylabel("Average waiting time")

    plt.show()


def plot_dep_servers_box(num_servers, avg_wait_times):
    """
    Plot boxplot of the average waiting time as a function of the number of servers
    """
    plt.title("Relation between number of servers and average wait time")
    plt.xlabel("Number of servers")
    plt.ylabel("Average waiting time")

    ax = plt.boxplot(avg_wait_times.T, patch_artist=True, labels=num_servers)
    # fill with colors
    colors = ['pink', 'lightblue', 'lightgreen']
    for patch, color in zip(ax['boxes'], colors):
         patch.set_facecolor(color)

    plt.gca().yaxis.grid()
    plt.show()



def plot_dep_rho(num_servers, rhos, avg_wait_times):
    """
    Plot a lineplot where the average wait time is a function of rho
    """
    for idx_n in range(len(num_servers)):
        n = num_servers[idx_n]
        xdata = rhos
        ydata = avg_wait_times[idx_n]

        avg_ydata = [np.mean(data) for data in ydata]

        #  Calculate 95% confidence intervals
        ci = [st.t.interval(confidence=0.95, df=len(data)-1, loc=np.mean(data), scale=st.sem(data)) for data in ydata]
        ci_lower = [i[0] for i in ci]
        ci_higher = [i[1] for i in ci]  

        line, = plt.plot(xdata, avg_ydata, label = f"number of servers =  {n}")
        plt.fill_between(xdata, ci_lower, ci_higher, color=line.get_color(), alpha=0.2)
        plt.legend()

    plt.title("Relation between Rho and average wait time") 
    plt.xlabel("Rho")
    plt.ylabel("Average waiting time")

    plt.gca().yaxis.grid()
    plt.show()


def plot_dep_queue_struct(num_servers, avg_wait_times_FIFO, avg_wait_times_SJFS):
    """
    Plot 2 boxplots, one for the average waiting time of a FIFO queue and one of a SJFS queue
    """
    labels = ["FIFO", "SJFS"]

    for idx_n in range(len(num_servers)):
        data = np.array([avg_wait_times_FIFO[idx_n], avg_wait_times_SJFS[idx_n]])

        plt.title(f"Comparison of queue structures using {num_servers[idx_n]} servers")
        plt.xlabel("Queue structure")
        plt.ylabel("Average waiting time")

        ax = plt.boxplot(data.T, patch_artist=True, labels=labels)

        # fill with colors
        colors = ['pink', 'lightblue']
        for patch, color in zip(ax['boxes'], colors):
            patch.set_facecolor(color)

        plt.gca().yaxis.grid()
        plt.show()


def plot_dep_queue_type(num_servers, avg_wait_times_m_m_n, avg_wait_times_m_d_n, avg_wait_times_lt, structure):
    """
    Plot boxplots for the average waiting time depending on the service rate distributions
    """
    labels = ["m_m_n", "m_d_n", "long-tailed"]

    for idx_n in range(len(num_servers)):
        data = np.array([avg_wait_times_m_m_n[idx_n], avg_wait_times_m_d_n[idx_n], avg_wait_times_lt[idx_n]])
        plt.title(f"Comparison of queue types using {num_servers[idx_n]} servers and a {structure} structure")
        plt.xlabel("Queue type")
        plt.ylabel("Average waiting time")

        ax = plt.boxplot(data.T, patch_artist=True, labels=labels)

        # fill with colors
        colors = ['pink', 'lightblue', 'lightgreen']
        for patch, color in zip(ax['boxes'], colors):
            patch.set_facecolor(color)

        plt.gca().yaxis.grid()
        plt.show()

        





    


    
