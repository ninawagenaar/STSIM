import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
plt.rcParams['font.size'] = '12'

def plot_cost_over_iter(cost_over_iter):
    # Get x and y
    mean_cost = np.mean(cost_over_iter, axis=0)
    print(mean_cost)
    iterations = range(len(mean_cost))

    #95% confidence interval
    cis = [st.t.interval(alpha=0.95, df=len(iter)-1, loc=np.mean(iter), scale=st.sem(iter)) for iter in cost_over_iter.T]
    cis_lower = [i[0] for i in cis]
    cis_higher = [i[1] for i in cis]  

    # Make plot
    plt.plot(iterations, mean_cost)
    plt.fill_between(iterations, cis_lower, cis_higher, color='blue', alpha=0.2)
    plt.xlabel("Iteration")
    plt.ylabel("Distance of circuit")
    plt.title("Distance of circuit over iterations")
    plt.grid()
    plt.show()