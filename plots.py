import matplotlib.pyplot as plt
import os
from params import params
from utils import *

'''
This script generates plots for every trial that compares the convergence
between Bayesian Optimization and Random Search for the target kappa. 

It will plot the square error versus iteration for BO and RS given a
porosity and number of pores per quadrant. 
'''

curdir = os.getcwd()
tested_num_pores = params['tested_num_pores']
tested_porosities = params['tested_porosities']
desired_kappa = params['desired_kappa']
display_every_iter = params['display_every_iter']
num_init = params['num_init']
attempt_minimize = params['attempt_minimize']
iterations = list(range(params['num_iters']))



def plot_square_error_per_iteration():
    '''
    Plots the square error and min square error per iteration for
    BO and RS to compare them visually
    
    '''
    for num_pores in tested_num_pores:
        for porosity in tested_porosities:
            # scrape the square error data for bo and random trial
            with open(curdir + '/saved_random_sq_error_per_iteration/num_pores_' + str(num_pores) + '_porosity_' + str(porosity) + '.out') as f:
                random_sq_errors = [float(error) for error in f.read().split('\n') if error != '']
                random_min_sq_errors = min_per_iteration(random_sq_errors)

            with open(curdir + '/saved_bo_sq_error_per_iteration/num_pores_' + str(num_pores) + '_porosity_' + str(porosity) + '.out') as f:
                bo_sq_errors = [float(error) for error in f.read().split('\n') if error != '']
                bo_min_sq_errors = min_per_iteration(bo_sq_errors)

            # generate the plot for min kappa v iteration for both trials
            plt.plot(iterations, random_min_sq_errors, 'y-', label = 'Random Search Min Error')
            plt.plot(iterations, bo_min_sq_errors, 'b-', label = 'Bayesian Optimization Min Error')
            if display_every_iter:
                plt.plot(iterations, random_sq_errors, 'yo', alpha = 0.5, label = 'Random Search Error')
                plt.plot(iterations, bo_sq_errors, 'bo', alpha = 0.5, label = 'Bayesian Optimization Error')
                plt.axvspan(-0.3,num_init - 0.7, alpha = 0.3, color = 'gray', label = 'Initialization for BO')
            plt.title("Convergence Plot")
            plt.xlabel("Number of calls, n")
            plt.ylabel("Minimum Square Error after n calls")
            plt.legend(loc='upper right')
            plt.savefig('./plots/sq_error_convergence_plot_num_pores_' + str(num_pores) + '_porosity_' + str(porosity) +'.png')
            plt.close()



def plot_kappa_per_iteration():
    '''
    Plots the kappa and closest kappa per iteration for
    BO and RS to compare them visually
    '''
    for num_pores in tested_num_pores:
        for porosity in tested_porosities:
            # scrape the kappa data for bo and random trial
            with open(curdir + '/saved_random_kappa_per_iteration/num_pores_' + str(num_pores) + '_porosity_' + str(porosity) + '.out') as f:
                random_kappas = [float(kappa) for kappa in f.read().split('\n') if kappa != '']
                random_kappas_closest = closest_per_iteration(random_kappas)
                random_kappas_min = min_per_iteration(random_kappas)

            with open(curdir + '/saved_bo_kappa_per_iteration/num_pores_' + str(num_pores) + '_porosity_' + str(porosity) + '.out') as f:
                bo_kappas = [float(kappa) for kappa in f.read().split('\n') if kappa != '']
                bo_kappas_closest = closest_per_iteration(bo_kappas)
                bo_kappas_min = min_per_iteration(bo_kappas)


            if not attempt_minimize:
                # generate the plot for closest kappa v iteration for both trials
                plt.plot(iterations, random_kappas_closest, 'yo-', label = 'Random Search Closest')
                plt.plot(iterations, bo_kappas_closest, 'bo-', label = 'Bayesian Optimization Closest')
                plt.plot(iterations, desired_kappa * len(iterations), 'r--', label = 'Desired Kappa')
                if display_every_iter:
                    plt.plot(iterations, random_kappas, 'yo', alpha = 0.5, label = 'Random Search Kappas')
                    plt.plot(iterations, bo_kappas, 'bo', alpha = 0.5, label = 'Bayesian Optimization Kappas')
                    plt.axvspan(-0.3,num_init - 0.7, alpha = 0.3, color = 'gray', label = 'Initialization for BO')
                plt.title("Convergence Plot")
                plt.xlabel("Number of calls, n")
                plt.ylabel("Closest Kappa after n calls")
                plt.legend(loc='upper right')
                plt.savefig('./plots/kappa_convergence_plot_num_pores_' + str(num_pores) + '_porosity_' + str(porosity) +'.png')
                plt.close()

            else:
                # generate the plot for min kappa v iteration for both trials
                plt.plot(iterations, random_kappas_min, 'yo-', label = 'Random Search Minimum')
                plt.plot(iterations, bo_kappas_min, 'bo-', label = 'Bayesian Optimization Minimum')
                if display_every_iter:
                    plt.plot(iterations, random_kappas, 'yo', alpha = 0.5, label = 'Random Search Kappas')
                    plt.plot(iterations, bo_kappas, 'bo', alpha = 0.5, label = 'Bayesian Optimization Kappas')
                    plt.axvspan(-0.3,num_init - 0.7, alpha = 0.3, color = 'gray', label = 'Initialization for BO')
                plt.title("Minimum Kappa Per Iteration")
                plt.xlabel("Number of calls, n")
                plt.ylabel("Min Kappa after n calls")
                plt.legend(loc='upper right')
                plt.savefig('./plots/min_plot_num_pores_' + str(num_pores) + '_porosity_' + str(porosity) +'.png')
                plt.close()



def plot_trends_for_trials():
    '''
    This script can be used to plot the minimum value of kappa for every trial 
    to compare between Bayesian Optimization and Random Search.

    It will generate one plot for each of BO and RS for every specified
    amount of number of pores and porosity.
    '''
    kappa_plots = []
    for porosity in tested_porosities:
        temp_kappas = []
        for num_pores in tested_num_pores:
            with open(curdir + '/saved_bo_kappas/num_pores_' + str(num_pores) + '_porosity_' + str(porosity) + '.out') as f:
                kappa = float(f.read())
                temp_kappas.append(kappa)
        kappa_plots.append(temp_kappas)

    for i, kappa_plot in enumerate(kappa_plots):
        plt.plot(tested_num_pores, kappa_plot, 'o-', label = "Porosity = " + str(tested_porosities[i]))

    plt.legend(loc='upper right')
    plt.title('Kappa vs Number of Pores and Porosity')
    plt.xlabel('# of Pores')
    plt.ylabel('Min Kappa')
    plt.savefig('plots/plot_trials_bo.png')
    plt.close()

    kappa_plots = []
    for porosity in tested_porosities:
        temp_kappas = []
        for num_pores in tested_num_pores:
            with open(curdir + '/saved_random_kappas/num_pores_' + str(num_pores) + '_porosity_' + str(porosity) + '.out') as f:
                kappa = float(f.read())
                temp_kappas.append(kappa)
        kappa_plots.append(temp_kappas)

    for i, kappa_plot in enumerate(kappa_plots):
        plt.plot(tested_num_pores, kappa_plot, 'o-', label = "Porosity = " + str(tested_porosities[i]))

    plt.legend(loc='upper right')
    plt.xlabel('# of Pores')
    plt.ylabel('Min Kappa')
    plt.title('Kappa vs Number of Pores and Porosity')
    plt.savefig('plots/plot_trials_random.png')



if __name__ == '__main__':
    plot_kappa_per_iteration()
    if attempt_minimize:
        plot_trends_for_trials()
    else:
        plot_square_error_per_iteration()
