import matplotlib.pyplot as plt
import os
from params import params
import numpy as np

'''
This script generates plots for every trial that compares the convergence
between Bayesian Optimization and Random Search for the target kappa. 

It will plot the square error versus iteration for BO and RS given a
porosity and number of pores per quadrant. 
'''

curdir = os.getcwd()
tested_num_pores = params['tested_num_pores']
tested_porosities = params['tested_porosities']
iterations = list(range(params['num_iters']))


def min_per_iteration(kappas):
    '''
    Given a list of kappa values (or square errors) per iteration, returns a new
    list of the minimum kappa (or square error) up to that iteration.
    '''
    min_kappa_per_iteration = []
    for kappa in kappas:
        if (min_kappa_per_iteration and kappa < min_kappa_per_iteration[-1]) or not min_kappa_per_iteration:
            min_kappa_per_iteration.append(kappa)
        else:
            min_kappa_per_iteration.append(min_kappa_per_iteration[-1])
    return min_kappa_per_iteration


for num_pores in tested_num_pores:
    for porosity in tested_porosities:
        # scrape the kappa data for bo and random trial
        with open(curdir + '/saved_random_kappa_per_iteration/num_pores_' + str(num_pores) + '_porosity_' + str(porosity) + '.out') as f:
            random_kappas = [float(kappa) for kappa in f.read().split('\n') if kappa != '']
            random_kappas = min_per_iteration(random_kappas)

        with open(curdir + '/saved_bo_kappa_per_iteration/num_pores_' + str(num_pores) + '_porosity_' + str(porosity) + '.out') as f:
            bo_kappas = [float(kappa) for kappa in f.read().split('\n') if kappa != '']
            bo_kappas = min_per_iteration(bo_kappas)

        # generate the plot for min kappa v iteration for both trials
        plt.plot(iterations, random_kappas, 'yo-', label = 'Random Search')
        plt.plot(iterations, bo_kappas, 'bo-', label = 'Bayesian Optimization')
        plt.title("Convergence Plot")
        plt.xlabel("Number of calls, n")
        if params['desired_kappa'] == 0:
            y_label = "Minimum Kappa after n calls"
        else:
            y_label = "Minimum error after n calls"
        plt.ylabel(y_label)
        plt.legend(loc='upper right')
        plt.savefig('./plots/convergence_plot_num_pores_' + str(num_pores) + '_porosity_' + str(porosity) +'.png')
        plt.close()