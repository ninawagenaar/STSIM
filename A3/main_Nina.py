from re import T
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = '16'
import numpy as np


def plot_cooling(T0, max_iter, cooling_scheme='linear'):
    temperatures = np.zeros(max_iter+1)
    temperatures[0] = T0

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

    plt.figure(figsize=(5, 5), layout="tight")
    plt.plot(temperatures)
    plt.xlabel("Iteration")
    plt.ylabel("Temperature")
    plt.title("The {} \n cooling schedule".format(cooling_scheme))
    plt.savefig("figs/temperature_{0}cooling_{1}T0".format(cooling_scheme, T0))
    plt.show()

class tspProblem:

    def __init__(self, variables, node_coord_section):
        self.variables = variables
        self.node_coord_section = node_coord_section

    def plot_problem(self):
        plt.scatter(self.node_coord_section[:,1], self.node_coord_section[:,2])
        plt.xlabel("X coordinate")
        plt.ylabel("Y coordinate")
        plt.title("Vizualization of nodes")
        plt.grid()
        plt.show()

    def solve(self, T_init):
        self.T = T_init
        



def read_files_tsp(filename):
    variables = {}
    node_coord_section = []

    with open(filename) as f:
        for line in f:

            if " : " in line: 
                name, value = line.split(" : ")
                value = value.rstrip()
                variables[name] = value

            if line[0].isdigit():
                node, xval, yval = line.split(" ")
                yval = yval.rstrip()
                node_coord_section.append([int(node), int(xval), int(yval)]) 

    node_coord_section = np.asarray(node_coord_section)

    return tspProblem(variables, node_coord_section)
            

def main():
    # filename = 'eil51.tsp.txt'
    # problem = read_files_tsp(filename) 
    # problem.plot_problem()
    cooling_schedules = ['logarithmic', 'linear', 'quadratic']
    for schedule in cooling_schedules:
        plot_cooling(500, 10000, cooling_scheme=schedule)


if __name__ == "__main__":
    main()

