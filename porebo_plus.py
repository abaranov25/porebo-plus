import os
from openbteplus.workflows import wf_4
from optim import BOMinimizer
import numpy as np
import gp_func
import time
from params import params
import matplotlib.pyplot as plt

"""
This script runs the trials for Bayesian Optimization with the parameters
defined in params.py. 

Inside this script are f(), sampler(), and initialize(), all of which are explained further below
"""

# Initializing values for the trials
kappa_per_iteration = []
tested_num_pores = params['tested_num_pores']
tested_porosities = params['tested_porosities']
given_L = params['L']
step_input = params['step_input']
buffer_len = params['buffer_len']
num_iters = params['num_iters']
num_init = params['num_init']
num_samples = params['num_samples']
initialize_folders = params['initialize_folders']
desired_kappa = params['desired_kappa']



def f(x, num_pores, given_porosity, save = False, random = False, desired_kappa = 0):
    '''
    Runs the BTE solver on the given sample of pore centers.
    '''
    global kappa_per_iteration
    # Creates the list of edges used to generate the pore geometry
    poly_list = []
    for i in range(0, len(x)-1, 2):
        x_shift = x[i]
        y_shift = x[i+1]
        for x_val in [-x_shift, x_shift]:
            for y_val in [-y_shift, y_shift]:
                poly_list.append([x_val, y_val])

    # Uses OpenBTEPlus to calculate the associated kappa value with the geometry
    time1 = time.time()
    results = wf_4.run(L = given_L,\
        material  = 'Si_rta',\
        porosity  = given_porosity,\
        positions = poly_list,\
        mesh_size = step_input,\
        shape     = 'square')
    time2 = time.time()
    print("Took ", time2-time1, " sec")

    # updated_kappa is the square error between measured thermal conductivity and the desired thermal conductivity
    if desired_kappa != 0:
        updated_kappa = (desired_kappa - results.bte.kappa_eff) ** 2 
    else:
        updated_kappa = results.bte.kappa_eff

    # Saves the kappa value for the given sample of pore centers if save is True
    if save:
        if random:
            np.savetxt('./saved_random_kappas/num_pores_' + str(num_pores) + '_porosity_' + str(given_porosity) + '.out', [updated_kappa])
            np.savetxt('./saved_random_poly_lists/poly_list_num_pores_' + str(num_pores) + '_porosity_' + str(given_porosity) + '.out', x)  
            np.savetxt('./saved_random_kappa_per_iteration/num_pores_' + str(num_pores) + '_porosity_' + str(given_porosity) + '.out', kappa_per_iteration)      
        else:
            np.savetxt('./saved_bo_kappas/num_pores_' + str(num_pores) + '_porosity_' + str(given_porosity) + '.out', [updated_kappa])
            np.savetxt('./saved_bo_poly_lists/poly_list_num_pores_' + str(num_pores) + '_porosity_' + str(given_porosity) + '.out', x)
            np.savetxt('./saved_bo_kappa_per_iteration/num_pores_' + str(num_pores) + '_porosity_' + str(given_porosity) + '.out', kappa_per_iteration)
        kappa_per_iteration = []
    else:
        kappa_per_iteration.append(updated_kappa)

    return updated_kappa



def sampler(num_pores, porosity, n=1):
    '''
    For every n, sampler creates a sample of pore centers, given in coordinates, and returns a 1-D list containing them. 
    The output will be a 2-D list containing n 1-D lists of samples. These samples are randomly generated.
    '''
    samples = []
    side_len = (porosity * given_L ** 2/(4*num_pores)) ** 0.5 

    for i in range(n):
        poly_centers = gp_func.config(x_len=given_L, y_len=given_L, side_len=side_len,
                                num_pores=num_pores, buffer_len=buffer_len, return_poly_list=False)

        # To polish the list of pore center's coordinates, we first sort it by the x coordinate, and then we flatten it
        poly_centers.sort()
        poly_centers = [coordinate for pore in poly_centers for coordinate in pore]

        samples.append(poly_centers)

    if len(samples) == 1:
        return samples[0]
    else:
        return samples



def initialize():
    '''
    If initialize_folders is set to True in params.py, we create directories
    to store the results.
    '''
    dirNames = ['./saved_bo_kappa_per_iteration', './saved_random_kappa_per_iteration', './saved_bo_kappas', './saved_bo_poly_lists', './saved_random_kappas', './saved_random_poly_lists', './plots', './errors']
    for dirName in dirNames:
        try:    
            os.mkdir(dirName)
            print('Directory ', dirName, ' Created')    
        except FileExistsError:
            pass



def plot(kappas, num_init, num_pores, porosity, num_iters, algorithm):
    '''
    Given a list of kappa values corresponding to each iteration, 
    plots these kappa values and also the minimum kappa value that 
    occurs after every iteration.
    '''
    min_kappa_per_iteration = []

    # Adds either the current value to kappa or the previous minimum
    for kappa in kappas:
        if (min_kappa_per_iteration and kappa < min_kappa_per_iteration[-1]) or not min_kappa_per_iteration:
            min_kappa_per_iteration.append(kappa)

        else:
            min_kappa_per_iteration.append(min_kappa_per_iteration[-1])
    
    iterations = list(range(num_iters))

    # labels the graph depending on whether we are finding the minimum
    # kappa or optimizing for a specific kappa
    if params['desired_kappa'] == 0:
        label_kappa = "Kappa Per Iteration"
        label_min_kappa = "Minimum Kappa Per Iteration"
        y_label = "Kappa"
        title = "Kappa v Iteration"
    else:
        label_kappa = "Square Error Per Iteration"
        label_min_kappa = "Minimum Square Error Per Iteration"
        y_label = "Square Error"
        title = "Convergence Plot"

    plt.plot(iterations, kappas, 'ro-', alpha = 0.7, label = label_kappa)
    plt.plot(iterations, min_kappa_per_iteration, 'bo-', label = label_min_kappa)
    if algorithm == 'porebo':
        plt.axvspan(-0.3,num_init - 0.7, alpha = 0.4, color = 'gray', label = 'Initialization')
    plt.xlabel('Iteration')
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend(loc='upper right')
    plt.savefig('plots/' + algorithm + '_num_pores_' + str(num_pores) + '_porosity_' + str(porosity) +'.png')
    plt.close()



if __name__ == "__main__":
    '''
    If running this file, perform the Bayesian Optimization and return the minimum kappa pore configuration
    '''
    if initialize_folders:
        initialize()

    for num_pores in tested_num_pores:
        for porosity in tested_porosities:
            kappa_per_iteration = []
            print("Starting trials for " + str(num_pores) + " pores and " + str(porosity) + " porosity")
            BO_obj = BOMinimizer(f=f, bounds=[(-0.5, 0.5)] * 2 * num_pores, n_init=num_init, n_calls=num_iters, n_sample=num_samples, sampler=sampler, noise=1e-3, kernel="Matern", acq="EI", num_pores = num_pores, porosity = porosity, desired_kappa = desired_kappa)

            Xbest, ybest = BO_obj.minimize()
            print("ybest:", ybest)
            print("xbest:", Xbest)

            plot(kappa_per_iteration, num_init, num_pores, porosity, num_iters, algorithm = "porebo")
    
            f(Xbest, num_pores, porosity, desired_kappa = desired_kappa, save=True)