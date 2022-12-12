import matplotlib.pyplot as plt
import numpy as np
import read_tsp as tsp
import solution_search as sol
import plotting as plotting

def run_simulations(tspProblem, simulations, max_iter, probability, temperature):
    cost_over_iter = []
    for simulation in range(simulations):

        print("simulation:", simulation)

        search_alg_sa = sol.search_alg("simulatedannealing", tspProblem.dimension, max_iter)
        search_alg_sa.simulatedannealing(tspProblem, max_iter, probability, temperature)
        cost_over_iter.append(search_alg_sa.history_cost)

    cost_over_iter = np.asarray(cost_over_iter)
    plotting.plot_cost_over_iter(cost_over_iter)
    

def main():
    filename = 'eil51.tsp.txt'
    tspProblem = tsp.read_problem_tsp(filename) 
    #problem.plot_problem()

    max_iter = 10000
    simulations = 20
    temperature = 0.9
    probability = 0.3
    run_simulations(tspProblem, simulations, max_iter, probability, temperature)


if __name__ == "__main__":
    main()
