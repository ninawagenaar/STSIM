import matplotlib.pyplot as plt
import numpy as np
import read_tsp as tsp
import solution_search as sol
import plotting as plotting
import sys
import time
import analyze as anlz
import optimal_tours as opt

def run_simulations(tspProblem, simulations, max_iter, a=0.005, cooling_scheme='linear', markov_chain=1):
    cost_over_iter = []
    minima = []
    time_sim = []
    for _ in range(simulations):
        search_alg_sa = sol.search_alg("simulatedannealing", tspProblem.dimension, max_iter, a=a, cooling_scheme=cooling_scheme, markov_chain=markov_chain)
        start = time.time()
        search_alg_sa.simulatedannealing(tspProblem, max_iter)
        end = time.time()
        minima.append(search_alg_sa.localmin)
        cost_over_iter.append(search_alg_sa.history_cost)
        time_sim.append(end-start)
   
    filename_min = "results/min_dim{2}_a{0}_{1}cooling_60000maxiter_mc{3}.txt".format(search_alg_sa.a, search_alg_sa.cooling_scheme, search_alg_sa.length, search_alg_sa.markov_chain)
    filename_time = "running_times/min_dim{2}_a{0}_{1}cooling_60000maxiter_mc{3}.txt".format(search_alg_sa.a, search_alg_sa.cooling_scheme, search_alg_sa.length, search_alg_sa.markov_chain)
    
    with open (filename_min ,'w') as f:
       for min in minima:
        f.write(f"{min}\n")

    with open (filename_time ,'w') as f:
       for t in time_sim:
        f.write(f"{t}\n")

    cost_over_iter = np.asarray(cost_over_iter)
    return cost_over_iter, minima


def main():
    # These parameters remain constant for all experiments 
    simulations = 25
    max_iter = 60000

    # These lists enable us to iterate through these files if needed
    files = ['eil51.tsp.txt', 'a280.tsp.txt', 'pcb442.tsp.txt']
    filename_sols = ['eil51.opt.tour.txt', 'a280.opt.tour.txt', 'pcb442.opt.tour.txt']
    cooling_schedules = ['logarithmic', 'linear', 'quadratic']
    param_a = [0.005, 0.05, 0.5]
    markov_chain_lengths = [1,5,10]

    # Optimal cost and optimal tour
    for filename_problem, filename_sol in zip(files, filename_sols):
        problem = tsp.read_problem_tsp(filename_problem) 
        circuit = opt.read_sol_tsp(filename_sol) 
        print(opt.get_cost(circuit, problem))
        plotting.plot_optimal_path(circuit, problem)

    # Make plots problems
    for file in files:
        tspProblem = tsp.read_problem_tsp(file)
        tspProblem.plot_problem()

    
    # Make plots cooling schedules 
    for schedule in cooling_schedules:
       plotting.plot_cooling(1500, 10000, cooling_scheme=schedule)
    
    
    # Get plots and analysis of effect problem size
    cost_over_iter_arr = []
    for file in files:
        # Set param experiment
        a = 0.005
        cooling_schedule = 'logarithmic'
        markov_chain = 1

        # Set up problem and run experiment
        tspProblem = tsp.read_problem_tsp(file)
        cost_over_iter, _ = run_simulations(tspProblem, simulations, max_iter, a, cooling_scheme=cooling_schedule, markov_chain=markov_chain)
        cost_over_iter_arr.append(cost_over_iter)
        labels = ["dim 51", "dim 280", "dim 442"]
        plotting.plot_cost_several_problems(cost_over_iter_arr, labels)
        plotting.plot_cost_several_problems(cost_over_iter_arr[:2], labels[:2])
    
    data_51_0005_lg_1 = anlz.read_file_results('results\min_dim51_a0.005_logarithmiccooling_60000maxiter_mc1.txt')
    data_280__0005_lg_1 = anlz.read_file_results('results\min_dim280_a0.005_logarithmiccooling_60000maxiter_mc1.txt')
    data_442__0005_lg_1 = anlz.read_file_results('results\min_dim442_a0.005_logarithmiccooling_60000maxiter_mc1.txt')
    anlz.mean_std(data_51_0005_lg_1)
    anlz.mean_std(data_280__0005_lg_1)
    anlz.mean_std(data_442__0005_lg_1)
    

    
    # Get plots for effect initial temperature and cooling schedule
    tspProblem = tsp.read_problem_tsp('a280.tsp.txt')
    markov_chain = 1
    for schedule in cooling_schedules:
        cost_over_iter_arr = []
        minima_arr = []
        for a in param_a:
            cost_over_iter, minima = run_simulations(tspProblem, simulations, max_iter, a, cooling_scheme=schedule, markov_chain=markov_chain)
            cost_over_iter_arr.append(cost_over_iter)
            minima_arr.append(minima)
        plotting.plot_cost_over_iter(cost_over_iter_arr, minima_arr, schedule, mode = 'a', param_a = param_a)
    
    
    # Get analysis for effect initial temperature and cooling schedule
    data_log_0005_lg1 = anlz.read_file_results('results\min_dim280_a0.005_logarithmiccooling_60000maxiter_mc1.txt')
    data_log_005_lg1 = anlz.read_file_results('results\min_dim280_a0.05_logarithmiccooling_60000maxiter_mc1.txt')
    data_log_05_lg1 = anlz.read_file_results('results\min_dim280_a0.5_logarithmiccooling_60000maxiter_mc1.txt')

    data_lin_0005_lg1 = anlz.read_file_results('results\min_dim280_a0.005_linearcooling_60000maxiter_mc1.txt')
    data_lin_005_lg1 = anlz.read_file_results('results\min_dim280_a0.05_linearcooling_60000maxiter_mc1.txt')
    data_lin_05_lg1 = anlz.read_file_results('results\min_dim280_a0.5_linearcooling_60000maxiter_mc1.txt')

    data_qua_0005_lg1 = anlz.read_file_results('results\min_dim280_a0.005_quadraticcooling_60000maxiter_mc1.txt')
    data_qua_005_lg1 = anlz.read_file_results('results\min_dim280_a0.05_quadraticcooling_60000maxiter_mc1.txt')
    data_qua_05_lg1 = anlz.read_file_results('results\min_dim280_a0.5_quadraticcooling_60000maxiter_mc1.txt')
    
    
    data_test_log = [data_log_0005_lg1, data_log_005_lg1, data_log_05_lg1]
    names_test_log = ["data_log_0005_lg1", "data_log_005_lg1", "data_log_05_lg1"]
    anlz.t_test(data_test_log, names_test_log)
    

    data_test_lin = [data_lin_0005_lg1, data_lin_005_lg1, data_lin_05_lg1]
    names_test_lin = ["data_lin_0005_lg1", "data_lin_005_lg1", "data_lin_05_lg1"]
    anlz.t_test(data_test_lin, names_test_lin)
    

    data_test_qua = [data_qua_0005_lg1, data_qua_005_lg1, data_qua_05_lg1]
    names_test_qua = ["data_lin_0005_lg1", "data_lin_005_lg1", "data_lin_05_lg1"]
    anlz.t_test(data_test_qua, names_test_qua)
    

    data_test_0005 = [data_log_0005_lg1, data_lin_0005_lg1, data_qua_0005_lg1]
    names_test_0005 = ["data_log_0005_lg1", "data_lin_0005_lg1", "data_qua_0005_lg1"]
    anlz.t_test(data_test_0005, names_test_0005)
    


    # Get plots for effect markov chain and cooling schedule
    tspProblem = tsp.read_problem_tsp('a280.tsp.txt')
    a = .005
    for schedule in cooling_schedules:
        cost_over_iter_arr = []
        minima_arr = []
        for k in  markov_chain_lengths:
            cost_over_iter, minima = run_simulations(tspProblem, simulations, max_iter, a, cooling_scheme=schedule, markov_chain=k)
            cost_over_iter_arr.append(cost_over_iter)
            minima_arr.append(minima)
        plotting.plot_cost_over_iter(cost_over_iter_arr, minima_arr, schedule, mode = 'markov', markov_chain_lengths=markov_chain_lengths)

    # Get analysis for effect temperature length and cooling schedule
    data_log_0005_lg1 = anlz.read_file_results('results\min_dim280_a0.005_logarithmiccooling_60000maxiter_mc1.txt')
    data_log_0005_lg5 = anlz.read_file_results('results\min_dim280_a0.005_logarithmiccooling_60000maxiter_mc5.txt')
    data_log_0005_lg10 = anlz.read_file_results('results\min_dim280_a0.005_logarithmiccooling_60000maxiter_mc10.txt')

    data_lin_0005_lg1 = anlz.read_file_results('results\min_dim280_a0.005_linearcooling_60000maxiter_mc1.txt')
    data_lin_0005_lg5 = anlz.read_file_results('results\min_dim280_a0.005_linearcooling_60000maxiter_mc5.txt')
    data_lin_0005_lg10 = anlz.read_file_results('results\min_dim280_a0.005_linearcooling_60000maxiter_mc10.txt')

    data_qua_0005_lg1 = anlz.read_file_results('results\min_dim280_a0.005_quadraticcooling_60000maxiter_mc1.txt')
    data_qua_0005_lg5 = anlz.read_file_results('results\min_dim280_a0.005_quadraticcooling_60000maxiter_mc5.txt')
    data_qua_0005_lg10 = anlz.read_file_results('results\min_dim280_a0.005_quadraticcooling_60000maxiter_mc10.txt')

    
    data_test_log = [data_log_0005_lg1, data_log_0005_lg5, data_log_0005_lg10]
    names_test_log = ['data_log_0005_lg1', 'data_log_0005_lg5', 'data_log_0005_lg10']
    anlz.t_test(data_test_log, names_test_log)
    
    
    data_test_lin = [data_lin_0005_lg1, data_lin_0005_lg5, data_lin_0005_lg10]
    names_test_lin = ['data_lin_0005_lg1', 'data_lin_0005_lg5', 'data_lin_0005_lg10']
    anlz.t_test(data_test_lin, names_test_lin)
    

    data_test_qua = [data_qua_0005_lg1, data_qua_0005_lg5, data_qua_0005_lg10]
    names_test_qua = ['data_qua_0005_lg1', 'data_qua_0005_lg5', 'data_qua_0005_lg10']
    anlz.t_test(data_test_qua, names_test_qua)
   
    # Analyze running time for different k
    time_log_0005_lg1 = anlz.read_file_results('running_times\min_dim280_a0.005_logarithmiccooling_60000maxiter_mc1.txt')
    time_log_0005_lg5 = anlz.read_file_results('running_times\min_dim280_a0.005_logarithmiccooling_60000maxiter_mc5.txt')
    time_log_0005_lg10 = anlz.read_file_results('running_times\min_dim280_a0.005_logarithmiccooling_60000maxiter_mc10.txt')

    time_lin_0005_lg1 = anlz.read_file_results('running_times\min_dim280_a0.005_linearcooling_60000maxiter_mc1.txt')
    time_lin_0005_lg5 = anlz.read_file_results('running_times\min_dim280_a0.005_linearcooling_60000maxiter_mc5.txt')
    time_lin_0005_lg10 = anlz.read_file_results('running_times\min_dim280_a0.005_linearcooling_60000maxiter_mc10.txt')

    time_qua_0005_lg1 = anlz.read_file_results('running_times\min_dim280_a0.005_quadraticcooling_60000maxiter_mc1.txt')
    time_qua_0005_lg5 = anlz.read_file_results('running_times\min_dim280_a0.005_quadraticcooling_60000maxiter_mc5.txt')
    time_qua_0005_lg10 = anlz.read_file_results('running_times\min_dim280_a0.005_quadraticcooling_60000maxiter_mc10.txt')

    anlz.mean_std(time_log_0005_lg1)
    anlz.mean_std(time_log_0005_lg5)
    anlz.mean_std(time_log_0005_lg10)

    anlz.mean_std(time_lin_0005_lg1)
    anlz.mean_std(time_lin_0005_lg5)
    anlz.mean_std(time_lin_0005_lg10)

    anlz.mean_std(time_qua_0005_lg1)
    anlz.mean_std(time_qua_0005_lg5)
    anlz.mean_std(time_qua_0005_lg10)
    

if __name__ == "__main__":
    main()
