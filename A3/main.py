import matplotlib.pyplot as plt
import numpy as np
import read_tsp as tsp
import solution_search as sol
import plotting as plotting
plt.rcParams['font.size'] = '12'

def run_simulations(tspProblem, simulations, max_iter, a=1, cooling_scheme='logarithmic'):
    cost_over_iter = []
    minima = []
    for simulation in range(simulations):

        # print("simulation:", simulation)

        search_alg_sa = sol.search_alg("simulatedannealing", tspProblem.dimension, max_iter, a=a, cooling_scheme=cooling_scheme)
        search_alg_sa.simulatedannealing(tspProblem, max_iter)
        minima.append(search_alg_sa.localmin)
        cost_over_iter.append(search_alg_sa.history_cost)
        # print("final result", search_alg_sa.history_cost[-1])

    cost_over_iter = np.asarray(cost_over_iter)
    plotting.plot_cost_over_iter(cost_over_iter, search_alg_sa)
    print("The costs of all minima of these simulations are: ", minima)
    

def main():
    # These lists enable us to iterate through these files if needed
    files = ['eil51.tsp.txt', 'a280.tsp.txt', 'pcb442.tsp.txt']
    cooling_schedules = ['logarithmic', 'linear', 'quadratic']

    
     
    # problem.plot_problem() # default size of point is 10, use pointsize=X for another size.



    max_iter = 10000
    simulations = 100

    # to test the different sizes
    for filename in files:
        tspProblem = tsp.read_problem_tsp(filename)

        # to test the cooling schedules
        for cool in cooling_schedules:

            # to test the starting temperatures
            for a in [0.005, 0.01, 0.05, 0.1, 0.5]:
                print(tspProblem.dimension, cool, a )
                run_simulations(tspProblem, simulations, max_iter, a=a, cooling_scheme=cool)


if __name__ == "__main__":
    main()
