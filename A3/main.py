import matplotlib.pyplot as plt
import numpy as np
import read_tsp as tsp
import solution_search as sol
import plotting as plotting
plt.rcParams['font.size'] = '12'

def run_simulations(tspProblem, simulations, max_iter, temperature):
    cost_over_iter = []
    for simulation in range(simulations):

        print("simulation:", simulation)

        search_alg_sa = sol.search_alg("simulatedannealing", tspProblem.dimension, max_iter)
        search_alg_sa.simulatedannealing(tspProblem, max_iter, temperature)
        cost_over_iter.append(search_alg_sa.history_cost)
        print("final result", search_alg_sa.history_cost[-1])

    cost_over_iter = np.asarray(cost_over_iter)
    plotting.plot_cost_over_iter(cost_over_iter)
    

def main():
    # These lists enable us to iterate through these files if needed
    files = ['eil51.tsp.txt', 'a280.tsp.txt', 'pcb442.tsp.txt']
    cooling_schedules = ['logarithmic', 'linear', 'quadratic']
    filename = files[0]
    tspProblem = tsp.read_problem_tsp(filename) 
    # problem.plot_problem() #default size of point is 10, use pointsize=X for another size.



    max_iter = 10000
    simulations = 20
    temperature = 0.9
    run_simulations(tspProblem, simulations, max_iter, temperature)


if __name__ == "__main__":
    main()
