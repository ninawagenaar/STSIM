from re import T
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = '14'
import numpy as np

def lundy_mees_cooling(Ti, a, b):
        if (a + b * Ti) > Ti:
            print("a and b are not selected properly")
            return ValueError
        else:
            return Ti / (a + b * Ti)

def linear_cooling1(Ti, a):
        Tnew = Ti - a

        if Tnew <= 0:
            return 0
        else:
            return Tnew

def linear_cooling2(T0, iter, a):
        Tnew = T0 - iter*a

        if Tnew <= 0:
            return 0
        else:
            return Tnew

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
    T = 400
    iters = 1000
    a = T/iters
    b = a
    
    x = np.arange(iters)
    y = np.empty(iters)

    for i in range(iters):
        y[i] = T
        T = lundy_mees_cooling(T, a, b)
    
    plt.plot(x, y)
    plt.show()

    T = 400
    a = T/iters
    for i in range(iters):
        y[i] = T
        T = linear_cooling1(T, a)
    
    plt.plot(x, y)
    plt.show()

    



if __name__ == "__main__":
    main()

