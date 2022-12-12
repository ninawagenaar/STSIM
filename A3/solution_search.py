import numpy as np
import read_tsp as tsp
import random

class solution:

    def __init__(self, name, length):
        self.name = name 
        self.length = length
        self.circuit = None

    def initialize_circuit(self, tspProblem):
        # Make a randomn circuit
        circuit = tspProblem.node_coord_section[:,0]
        random.shuffle(circuit)
        self.circuit = circuit

    def two_opt(self, i, k):
        print(i, k)
        new_circuit = np.zeros(self.length)
        new_circuit[0:i] = self.circuit[0:i]
        new_circuit[i:k] = np.flip(self.circuit[i:k])
        new_circuit[k:self.length] = self.circuit[k:self.length]
        self.solution = new_circuit
        
    def hillclimbing(self, tspProblem):
        # Initialize randomn solution
        self.initialize_circuit(tspProblem)

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
        self.two_opt(i, k)

        
        



                              


