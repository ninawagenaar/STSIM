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

    # Even kijken welke implementatie beter is voor in het algoritme
    def linear_cooling1(self, Ti, a):
        Tnew = Ti - a

        if Tnew <= 0:
            return 0
        else:
            return Tnew

    def linear_cooling2(self, T0, iter, a):
        Tnew = T0 - iter*a

        if Tnew <= 0:
            return 0
        else:
            return Tnew

    def lundy_mees_cooling(self, Ti, a, b):
        if (a + b * Ti) < Ti:
            print("a and b are not selected properly")
            return ValueError
        else:
            return Ti / (a + b * Ti)


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

            # Update temperature using function
            Tk = T0 / (1+np.log(1+iter))
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

            

            

        
        



                              


