import numpy as np
import scipy as sp

def read_file_results(filename):
    '''
    Read result files
    '''
    data = np.loadtxt(filename)
    return data

def mean_std(array):
    '''
    Given an array, print mean and std
    '''
    mean = np.mean(array)
    std = np.std(array)
    print('The mean is:', mean)
    print('The std is:', std)

def t_test(data, names):
    '''
    Perform a two sided t-test for each combination of results in data
    '''
    for i in range(len(data)):
        for j in range(len(data)):
            if j > i:
                print("t-test between {0} and {1}".format(names[i], names[j]))
                print(sp.stats.ttest_ind(data[i], data[j]))




