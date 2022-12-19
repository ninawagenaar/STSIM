import numpy as np
import read_tsp as tsp
import random
import math
import matplotlib.pyplot as plt

class search_alg:

    # a is the scaling constant for T0
    def __init__(self, name, length, max_iter, a=0.1, cooling_scheme='logarithmic'):
        self.name = name 
        self.length = length
        self.max_iter = max_iter
        self.a = a
        self.cooling_scheme = cooling_scheme
        self.circuit = None
        self.current_cost = None
        self.history_cost = np.zeros(max_iter+1)
        self.temperatures = np.empty(max_iter+1)
        

    def initialize_circuit(self, tspProblem):
        # Make a randomn circuit
        circuit = tspProblem.node_coord_section[:,0]
        random.shuffle(circuit)
        self.circuit = circuit
        

    # Fills the temperatures array with temperatures at each iteration i
    # purpose: save time, especially with logarithmic cooling
    def get_temperatures(self):

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

        # plt.figure(figsize=(5, 5), layout="tight")
        # plt.plot(self.temperatures)
        # plt.xlabel("Iteration")
        # plt.ylabel("Temperature")
        # plt.title("The {} \n cooling schedule".format(self.cooling_scheme))
        # # plt.savefig("figs/temperature_{0}cooling_{1}T0".format(self.cooling_scheme, self.temperatures[0]))
        # plt.show()

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

    def simulatedannealing(self, tspProblem, max_iter):

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
            
        self.localmin = np.min(self.history_cost)


            

            

        
        



                              


