import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
plt.rcParams['font.size'] = '14'


def plot_cost_over_iter(cost_over_iter_arr, minima_arr, cooling_scheme, mode= "a",  param_a=[0.005], markov_chain_lengths = [1]):
    '''
    Make figure with thee subplots for three different parameter settings
    '''

    # using the variable axs for multiple Axes
    fig, axs = plt.subplots(1, 3, figsize=(15, 5), layout="tight", sharex=True, sharey=True)

    # Get mean for every iter
    mean_cost_iter = []
    cis_iter_low = []
    cis_iter_high = []
    for cost_over_iter in cost_over_iter_arr:
        mean_cost_iter.append(np.mean(cost_over_iter, axis=0))
        ci_iter = [st.t.interval(alpha=0.95, df=len(iter)-1, loc=np.mean(iter), scale=st.sem(iter)) for iter in cost_over_iter.T]
        cis_iter_low.append([i[0] for i in ci_iter])
        cis_iter_high.append([i[1] for i in ci_iter])

    # Get mean of min
    mean_cost_min = []
    cis_min_low = []
    cis_min_high = []
    for minima in minima_arr:
        mean_cost_min.append(np.mean(minima, axis=0))
        ci_min = st.t.interval(alpha=0.95, df=len(minima)-1, loc=np.mean(minima), scale=st.sem(minima))
        cis_min_low.append(ci_min[0])
        cis_min_high.append(ci_min[1])

    # Get x
    iterations = range(len(mean_cost_iter[0]))

    # Make plots
    for idx in range(len(cost_over_iter_arr)):

        axs[idx].plot(iterations, mean_cost_iter[idx])
        axs[idx].fill_between(iterations, cis_iter_low[idx], cis_iter_high[idx], color='red', alpha=0.2)

        axs[idx].axhline(y = mean_cost_min[idx], color = 'green', linestyle = '--')
        axs[idx].fill_between(iterations, cis_min_low[idx], cis_min_high[idx], color='green', alpha=0.2)
        if mode == 'a':
            axs[idx].set_title("a = {0}".format(param_a[idx]))
        else:
            axs[idx].set_title("temp length = {0}".format(markov_chain_lengths[idx]))            
        axs[idx].grid()


    fig.text(0.5, 0.01, 'Iteration', ha='center')
    fig.text(0.001, 0.5, 'Distance of circuit', va='center', rotation='vertical')
    fig.suptitle("Distance of circuit over iterations, using {0} cooling schedule".format(cooling_scheme))
    if mode == 'a':
        plt.savefig("figs/costoveriter_{0}cooling__mc{1}.png".format(cooling_scheme, markov_chain_lengths[0]))
    else:
        plt.savefig("figs/costoveriter_{0}cooling__a{1}.png".format(cooling_scheme, param_a[0]))
    plt.close()

def plot_cooling(T0, max_iter, cooling_scheme='linear'):
    '''
    Plot the cooling function over iterations
    '''
    
    plt.figure(figsize=(5, 5), layout="tight")

    for aa in [0.005, 0.01, 0.05, 0.1, 0.5]:
        temperatures = np.zeros(max_iter+1)
        temperatures[0] = round(T0*aa, 1)

        if cooling_scheme == 'linear':
            c = temperatures[0] / max_iter
            for i in range(1, max_iter+1):
                temperatures[i] = temperatures[i-1] - c

        elif cooling_scheme == 'logarithmic':
            for i in range(1, max_iter+1):
                temperatures[i] = temperatures[0] / (1+np.log(1+i))
            
        elif cooling_scheme == 'quadratic':
            a = temperatures[0] / max_iter**2
            b = 2* -temperatures[0] / max_iter
            c = temperatures[0]
            for i in range(1, max_iter+1):
                temperatures[i] = a * i**2 + b*i + c

        plt.plot(temperatures, label="T0 = {}".format(round(T0*aa, 1)))
        
    plt.xlabel("Iteration")
    plt.ylabel("Temperature")
    plt.legend()
    plt.title("The {} \n cooling schedule".format(cooling_scheme))
    plt.savefig("figs/temperature_{0}cooling_{1}T0.png".format(cooling_scheme, T0))
    plt.close()


def plot_cost_several_problems(cost_over_iter_arr, labels):
    '''
    Plot the cost of solutions over iterations for several problem size'
    '''
    plt.figure(figsize=(5, 5), layout="tight")
    
    for cost_over_iter, label in zip(cost_over_iter_arr, labels):
        mean_cost = np.mean(cost_over_iter, axis=0)
        iterations = range(len(mean_cost))

        #95% confidence interval mean
        cis = [st.t.interval(alpha=0.95, df=len(iter)-1, loc=np.mean(iter), scale=st.sem(iter)) for iter in cost_over_iter.T]
        cis_lower = [i[0] for i in cis]
        cis_higher = [i[1] for i in cis]  

        # Make plotS
        plt.plot(iterations, mean_cost, label = label)
        plt.fill_between(iterations, cis_lower, cis_higher, alpha=0.2)

    plt.xlabel("Iteration")
    plt.ylabel("Distance of circuit")
    plt.title("Distance of circuit over iterations")
    plt.legend()
    plt.grid()
    plt.savefig("figs/costoveriter_allcities_a0.005_logarithmiccooling_60000maxiter_mc_len{0}.png".format(len(cost_over_iter_arr)))
    plt.close()
    #plt.show()

def plot_optimal_path(circuit, tspProblem):
    '''
    Vizualize a route given the circuit
    '''
    plt.rcParams["figure.figsize"] = [4, 4]
    plt.rcParams["figure.autolayout"] = True
    for idx in range(tspProblem.dimension):
        node1 = int(circuit[idx-1])
        node2 = int(circuit[idx])
        x1 = tspProblem.node_coord_section[node1-1,1]
        x2 = tspProblem.node_coord_section[node2-1,1]
        y1 = tspProblem.node_coord_section[node1-1,2]
        y2 = tspProblem.node_coord_section[node2-1,2]

        x_values = [x1, x2]
        y_values = [y1, y2]
        plt.plot(x_values, y_values,  markersize=2.5, marker='o', linestyle="-")
        
    plt.title("Vizualization of path")
    plt.grid()
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.savefig("figs/problem{0}".format(tspProblem.dimension))


