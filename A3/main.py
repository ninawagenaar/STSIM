import matplotlib.pyplot as plt
import numpy as np
import read_tsp as tsp
import solution_search as sol
            

def main():
    filename = 'eil51.tsp.txt'
    problem = tsp.read_problem_tsp(filename) 
    #problem.plot_problem()
    solution = sol.solution("hillclimbing", len(problem.node_coord_section[:,0]))
    solution.hillclimbing(problem)

if __name__ == "__main__":
    main()
