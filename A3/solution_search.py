import numpy as np
import read_tsp as tsp
import random
import math

class search_alg:

    def __init__(self, name, length, max_iter):
        self.name = name 
        self.length = length
        self.circuit = None
        self.current_cost = None
        self.history_cost = np.zeros(max_iter+1)

    def initialize_circuit(self, tspProblem):
        # Make a randomn circuit
        circuit = tspProblem.node_coord_section[:,0]
        random.shuffle(circuit)
        self.circuit = circuit

    def two_opt(self, i, k):
        new_circuit = np.zeros(self.length)
        new_circuit[0:i] = self.circuit[0:i]
        new_circuit[i:k] = np.flip(self.circuit[i:k])
        new_circuit[k:self.length] = self.circuit[k:self.length]
        return new_circuit

    def get_cost(self, circuit, tspProblem):
        cost = 0
        for idx in range(self.length):
            node1 = int(circuit[idx-1])
            node2 = int(circuit[idx])
            cost += tspProblem.distances[node1-1, node2-1]
        return cost

    def simulatedannealing(self, tspProblem, max_iter, probability, temperature):

        # Initialize randomn solution
        self.initialize_circuit(tspProblem)
        self.cost = self.get_cost(self.circuit, tspProblem)

        # Save initial cost
        self.history_cost[0] = self.cost
    
        for iter in range(max_iter):
            # Select two edges two swap
            i = random.randint(0, self.length)
            k = random.randint(0, self.length)
            j = i
            # The last node in the array is adjacent to the first node 
            if k == self.length:
                j = -1

            # The first edge must occur first in the list, the edges cannot be adjacent nor the same edge
            while (abs(i-k) == 1 or (i == k) or abs(i-j) == 1) or (i > k):
                i = random.randint(0, self.length)
                k = random.randint(0, self.length)
                if k == self.length:
                    j = -1

            # Swap the selected edges
            potential_circuit = self.two_opt(i, k)
            potential_cost = self.get_cost(potential_circuit, tspProblem)
            if potential_cost < self.cost:
                self.circuit = potential_circuit
                self.cost = potential_cost
            elif random.random() < probability: 
                self.circuit = potential_circuit
                self.cost = potential_cost

            # Reduce probability    
            probability = probability * temperature

            # Save result iteration 
            self.history_cost[iter+1] = self.cost

            

            

        
        



                              


