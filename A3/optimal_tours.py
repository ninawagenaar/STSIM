
import read_tsp as tsp
import matplotlib.pyplot as plt


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

def plot_optimal_path(circuit, tspProblem):
    plt.rcParams["figure.figsize"] = [4, 4]
    plt.rcParams["figure.autolayout"] = True
    for idx in range(tspProblem.dimension):
        node1 = int(circuit[idx-1])
        node2 = int(circuit[idx])
        x1 = tspProblem.node_coord_section[node1-1,1]
        x2 = tspProblem.node_coord_section[node2-1,1]
        y1 = tspProblem.node_coord_section[node1-1,2]
        y2 = tspProblem.node_coord_section[node2-1,2]

        x_values = [x1, x2]
        y_values = [y1, y2]
        plt.plot(x_values, y_values, color='blue', markersize=2, marker='o', linestyle="--", markerfacecolor='green')
        
    plt.title("Vizualization of path")
    plt.grid()
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.show()

def main():
    filename_problems = ['eil51.tsp.txt', 'a280.tsp.txt', 'pcb442.tsp.txt']
    filename_sols = ['eil51.opt.tour.txt', 'a280.opt.tour.txt', 'pcb442.opt.tour.txt']
    for filename_problem, filename_sol in zip(filename_problems, filename_sols):
        problem = tsp.read_problem_tsp(filename_problem) 
        circuit = read_sol_tsp(filename_sol) 
        print(get_cost(circuit, problem))
        plot_optimal_path(circuit, problem)


if __name__ == "__main__":
    main()
