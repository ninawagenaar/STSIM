import plotting as plotting


def read_sol_tsp(filename):
    tour = []
    with open(filename) as f:
        for line in f:

            line = line.strip()

            if line[0].isdigit():
                node = line
                tour.append(node)
    
    return tour


def get_cost(circuit, tspProblem):
    cost = 0
    for idx in range(tspProblem.dimension):
        node1 = int(circuit[idx-1])
        node2 = int(circuit[idx])
        cost += tspProblem.distances[node1-1, node2-1]
    return cost
