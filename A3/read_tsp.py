from asyncore import read
import matplotlib.pyplot as plt
import numpy as np
import math
plt.rcParams['font.size'] = '16'

class tspProblem:

    def __init__(self, variables, node_coord_section):
        self.name = variables['NAME']
        self.dimension = int(variables['DIMENSION'])
        self.node_coord_section = node_coord_section
        self.distances = self.get_distance_matrix()

    def get_distance_matrix(self):
        distances = np.empty((self.dimension, self.dimension))
        for i in self.node_coord_section[:,0]:
            for j in self.node_coord_section[:,0]:
                if i == j:
                    distances[i-1][j-1] = 0
                else:
                    x1 = self.node_coord_section[i-1,1]
                    y1 = self.node_coord_section[i-1,2]
                    coor_node1 = (x1, y1)

                    x2 = self.node_coord_section[j-1,1]
                    y2 = self.node_coord_section[j-1,2] 
                    coor_node2 = (x2, y2)

                    distances[i-1][j-1] = math.dist(coor_node1, coor_node2)
        return distances
                

    def plot_problem(self):
        plt.figure(figsize=(4, 4), layout="tight")
        plt.scatter(self.node_coord_section[:,1], self.node_coord_section[:,2], s=10)
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

if __name__ == "__main__":
    config51 = read_problem_tsp("eil51.tsp.txt")
    config51.plot_problem()

    config280 = read_problem_tsp("a280.tsp.txt")
    config280.plot_problem()
    
    config442 = read_problem_tsp("pcb442.tsp.txt")
    config442.plot_problem()