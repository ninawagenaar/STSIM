from asyncore import read
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.spatial import distance
plt.rcParams['font.size'] = '12'

class tspProblem:

    def __init__(self, variables, node_coord_section):
        self.name = variables['NAME']
        self.dimension = int(variables['DIMENSION'])
        self.node_coord_section = node_coord_section
        self.distances = self.get_distance_matrix()

    def get_distance_matrix(self):
        '''
        Initialize euclidean distance matrix
        '''
        distances = np.empty((self.dimension, self.dimension))
        for i in self.node_coord_section[:,0]:
            for j in self.node_coord_section[:,0]:
                # Distance is zero for a node to itself
                if i == j:
                    distances[i-1][j-1] = 0
                # Contains some dublication, do we want this gone?
                else:
                    x1 = self.node_coord_section[i-1,1]
                    y1 = self.node_coord_section[i-1,2]
                    coor_node1 = (x1, y1)

                    x2 = self.node_coord_section[j-1,1]
                    y2 = self.node_coord_section[j-1,2] 
                    coor_node2 = (x2, y2)

                    distances[i-1][j-1] = math.dist(coor_node1, coor_node2)
                    distances[i-1][j-1] =  distance.euclidean(coor_node1, coor_node2)
        return distances
                

    def plot_problem(self, pointsize=10):
        plt.figure(figsize=(4, 4), layout="tight")
        plt.scatter(self.node_coord_section[:,1], self.node_coord_section[:,2], s=pointsize)
        plt.xlabel("X coordinate")
        plt.ylabel("Y coordinate")
        plt.title("Vizualization of nodes")
        plt.grid()
        plt.savefig("figs/problem{0}".format(self.dimension))


def read_problem_tsp(filename):
    '''
    Read in problem and initialize an object of the problem class
    '''
    variables = {}
    node_coord_section = []

    with open(filename) as f:
        for line in f:

            line = line.strip()

            if ":" in line: 
                name, value = line.split(":")
                name = name.strip()
                value = value.strip()
                variables[name] = value

            if line[0].isdigit():
                node, xval, yval = line.split()
                node = node.strip()
                xval = xval.strip()
                yval = yval.strip()
                node_coord_section.append([int(float(node)), int(float(xval)), int(float(yval))]) 
    
    node_coord_section = np.asarray(node_coord_section)
    # print(len(node_coord_section[:,0]))	

    return tspProblem(variables, node_coord_section)