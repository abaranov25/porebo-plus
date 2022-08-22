import matplotlib.pyplot as plt
import os
from params import params
import numpy as np


curdir = os.getcwd()
tested_num_pores = params['tested_num_pores']
tested_porosities = params['tested_porosities']
iterations = list(range(params['num_iters']))


def min_per_iteration(kappas):
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
        with open(curdir + '/saved_random_kappa_v_iteration/num_pores_' + str(num_pores) + '_porosity_' + str(porosity) + '.out') as f:
            random_kappas = [float(kappa) for kappa in f.read().split('\n')]
            random_kappas = min_per_iteration(random_kappas)


        with open(curdir + '/saved_bo_kappa_v_iteration/num_pores_' + str(num_pores) + '_porosity_' + str(porosity) + '.out') as f:
            bo_kappas = [float(kappa) for kappa in f.read().split('\n')]
            bo_kappas = min_per_iteration(bo_kappas)


        # generate the plot for min kappa v iteration for both trials
        plt.plot(iterations, random_kappas, 'yo-', label = 'Random Search')
        plt.plot(iterations, bo_kappas, 'bo-', label = 'Bayesian Optimization')
        plt.title("Convergence Plot")
        plt.xlabel("Number of calls, n")
        plt.ylabel("Minimum error after n calls")
        plt.legend(loc='upper right')
        plt.savefig('./plots/convergence_plot_num_pores_' + str(num_pores) + '_porosity_' + str(porosity) +'.png')