import numpy as np
import read_tsp as tsp
import random
import math
import matplotlib.pyplot as plt

class search_alg:

    # a is the scaling constant for T0
    def __init__(self, name, length, max_iter, a=0.1, cooling_scheme='logarithmic', markov_chain=1):
        self.name = name 
        self.length = length
        self.max_iter = max_iter
        self.a = a
        self.cooling_scheme = cooling_scheme
        self.circuit = None
        self.current_cost = None
        self.history_cost = np.zeros(max_iter+1)
        self.temperatures = np.empty(max_iter+1)
        self.markov_chain = markov_chain
        

    def initialize_circuit(self, tspProblem):
        '''
        Initialize a random circuit
        '''
        circuit = tspProblem.node_coord_section[:,0]
        random.shuffle(circuit)
        self.circuit = circuit
        


    def get_temperatures(self):
        '''
        Fills the temperatures array with temperatures at each iteration i
        Purpose: save time, especially with logarithmic cooling
        '''
        if self.cooling_scheme == 'linear':
            c = self.temperatures[0] / self.max_iter
            for i in range(1, self.max_iter+1):
                self.temperatures[i] = self.temperatures[i-1] - c

        elif self.cooling_scheme == 'logarithmic':
            for i in range(1, self.max_iter+1):
                self.temperatures[i] = self.temperatures[0] / (1+np.log(1+i))
            
        elif self.cooling_scheme == 'quadratic':
            aa = self.temperatures[0] / self.max_iter**2
            b = 2* -self.temperatures[0] / self.max_iter
            c = self.temperatures[0]
            for i in range(1, self.max_iter+1):
                self.temperatures[i] = aa * i**2 + b*i + c

        else:
            raise ValueError("Cooling Scheme incorrectly provided: try 'linear', 'logarithmic' or 'quadratic'. ")


    def two_opt(self, i, k):
        '''
        Input: a circuit and two edges
        Removes two edges and reconnects the nodes to form a new circuit
        '''
        new_circuit = np.zeros(self.length)
        if i > k:
            i,k = k,i
        new_circuit[0:i] = self.circuit[0:i]
        new_circuit[i:k] = np.flip(self.circuit[i:k])
        new_circuit[k:self.length] = self.circuit[k:self.length]
        return new_circuit

    def get_cost(self, circuit, tspProblem):
        '''
        Input: a circuit
        Output: cost of the circuit using Euclidean distance
        Uses a look-up matrix for efficiency 
        '''
        cost = 0
        for idx in range(self.length):
            node1 = int(circuit[idx-1])
            node2 = int(circuit[idx])
            cost += tspProblem.distances[node1-1, node2-1]
        return cost

    def simulatedannealing(self, tspProblem, max_iter):
        '''
        Implementation of the simulated annealing algorithm
        Aim: find a (global) minimal solution to the given TSP problem
        '''

        # Initialize randomn solution
        self.initialize_circuit(tspProblem)
        self.cost = self.get_cost(self.circuit, tspProblem)
        # print(self.cost)

        # T0 aanmaken met self.cost*a
        self.temperatures[0] = self.a * self.cost
        self.get_temperatures()

        # Save initial cost
        self.history_cost[0] = self.cost
    
        for iter in range(max_iter):
            for _ in range(self.markov_chain):
                i = 0
                j = 1
                l = 0

                # The first edge must occur first in the list, the edges cannot be adjacent nor the same edge
                while (abs(i-j) == 1 or abs(i-l) == 1 or abs(j-l) == 1):
                    # Select two edges two swap
                    edges = np.random.choice(self.length, 2, replace=False)
                    i = edges[0]
                    j = edges[1]

                    # The last node in the array is adjacent to the first node 
                    if j == self.length:
                        l = -1

                    if i == self.length:
                        l = -1
                        
                # Swap the selected edges
                potential_circuit = self.two_opt(i, j)
                potential_cost = self.get_cost(potential_circuit, tspProblem)
                delta = potential_cost - self.cost

                if delta < 0:
                    self.circuit = potential_circuit
                    self.cost = potential_cost
                elif delta >= 0: 
                    probability = math.exp( -delta / self.temperatures[iter])
                    if random.random() < probability:
                        self.circuit = potential_circuit
                        self.cost = potential_cost

            # Save result iteration 
            self.history_cost[iter+1] = self.cost
                
        # Keep track of minimal solution of this simulation
        self.localmin = np.min(self.history_cost)


            

            

        
        



                              


