import matplotlib.pyplot as plt
import numpy as np

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

def read_problem_tsp(filename):
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
