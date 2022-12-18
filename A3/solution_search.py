import numpy as np
import read_tsp as tsp
import random
import math

class search_alg:

    # a is the scaling constant for T0
    def __init__(self, name, length, max_iter, a=1):
        self.name = name 
        self.length = length,
        self.max_iter = max_iter
        self.a = a
        self.circuit = None
        self.current_cost = None
        self.history_cost = np.zeros(max_iter+1)
        self.temperatures = np.empty(max_iter+1)
        

    def initialize_circuit(self, tspProblem):
        # Make a randomn circuit
        circuit = tspProblem.node_coord_section[:,0]
        random.shuffle(circuit)
        self.circuit = circuit
        self.temperatures[0] = self.a * self.get_cost(circuit, tspProblem)
        print(self.temperatures[0])

    # Fills the temperatures array with temperatures at each iteration i
    # purpose: save time, especially with logarithmic cooling
    def get_temperatures(self, cooling_scheme='linear'):

        if cooling_scheme == 'linear':
            c = self.temperatures[0] / self.max_iter
            for i in range(1, self.max_iter+1):
                self.temperatures[i] = self.temperatures[i-1] - c

        elif cooling_scheme == 'logarithmic':
            for i in range(1, self.max_iter+1):
                self.temperatures[i] = self.temperatures[0] / (1+np.log(1+i))
            
        elif cooling_scheme == 'quadratic':
            a = self.temperatures[0] / self.max_iter**2
            b = 2* -self.temperatures[0] / self.max_iter
            c = self.temperatures[0]
            for i in range(1, self.max_iter+1):
                self.temperatures[i] = a * i**2 + b*i + c

        else:
            raise ValueError("Cooling Scheme incorrectly provided: try 'linear', 'logarithmic' or 'quadratic'. ")

    #     return True

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

    # TODO: iets toevoegen waardoor er ipv 1 een i aantal oplossingen
    # gemaakt wordt voor elke temperatuur.
    # de lengte van de markovchain is dan n*i
    # waarbij n maximale iteraties is.

    def simulatedannealing(self, tspProblem, max_iter, T0):

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
            delta = potential_cost - self.cost

            # # Update temperature using function
            # Tk = T0 / (1+np.log(1+iter))
            
            # I updated this to an array with the temperatures at each iter
            self.temperatures
            if delta < 0:
                self.circuit = potential_circuit
                self.cost = potential_cost
            elif delta >= 0: 
                probability = math.exp( -delta / Tk)
                if random.random() < probability:
                    self.circuit = potential_circuit
                    self.cost = potential_cost

            # Save result iteration 
            self.history_cost[iter+1] = self.cost

            

            

        
        



                              


