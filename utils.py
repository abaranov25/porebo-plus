import os
from openbteplus.workflows import wf_4
from optim import BOMinimizer
import numpy as np
import gp_func
import time
from params import params
import matplotlib.pyplot as plt

given_L = params['L']
step_input = params['step_input']
buffer_len = params['buffer_len']
initialize_folders = params['initialize_folders']
attempt_minimize = params['attempt_minimize']

kappa_x_per_iteration = []
kappa_y_per_iteration = []
norm_error_per_iteration = []
kappa_norm_per_iteration = []



def f(x, num_pores, given_porosity, save = False, random = False, desired_kappa_x = 0, desired_kappa_y = 0):
    '''
    Runs the BTE solver on the given sample of pore centers.
    '''
    global kappa_x_per_iteration
    global kappa_y_per_iteration
    global norm_error_per_iteration
    global kappa_norm_per_iteration
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
    res_x, res_y = wf_4.run(L = given_L,\
        material  = 'Si_rta',\
        porosity  = given_porosity,\
        positions = poly_list,\
        mesh_size = step_input,\
        shape     = 'square')
    time2 = time.time()
    print("Took ", time2-time1, " sec")

    # norm error is the error between the result kappa and desired kappa
    kappa_x = res_x.bte.kappa_eff
    kappa_y = res_y.bte.kappa_eff
    kappa_norm = (kappa_x ** 2 + kappa_y ** 2) ** 0.5
    norm_error = ((kappa_x - desired_kappa_x) ** 2 + (kappa_y - desired_kappa_y) ** 2) ** 0.5

    # Saves the kappa value for the given sample of pore centers if save is True
    if save:
        if random:
            algo = 'random'
        else:
            algo = 'bo'
        np.savetxt('./saved_' + algo + '_kappa_x_per_iteration/num_pores_' + str(num_pores) + '_porosity_' + str(given_porosity) + '.out', kappa_x_per_iteration)
        np.savetxt('./saved_' + algo + '_kappa_y_per_iteration/num_pores_' + str(num_pores) + '_porosity_' + str(given_porosity) + '.out', kappa_y_per_iteration)
        np.savetxt('./saved_' + algo + '_poly_lists/poly_list_num_pores_' + str(num_pores) + '_porosity_' + str(given_porosity) + '.out', x)
        np.savetxt('./saved_' + algo + '_kappas/num_pores_' + str(num_pores) + '_porosity_' + str(given_porosity) + '.out', [kappa_x, kappa_y])
        np.savetxt('./saved_' + algo + '_sq_error_per_iteration/num_pores_' + str(num_pores) + '_porosity_' + str(given_porosity) + '.out', norm_error_per_iteration)
        np.savetxt('./saved_' + algo + '_kappa_norm_per_iteration/num_pores_' + str(num_pores) + '_porosity_' + str(given_porosity) + '.out', kappa_norm_per_iteration)
        kappa_x_per_iteration = []
        kappa_y_per_iteration = []
        norm_error_per_iteration = []
        kappa_norm_per_iteration = []
    else:
        kappa_x_per_iteration.append(kappa_x)
        kappa_y_per_iteration.append(kappa_y)
        norm_error_per_iteration.append(norm_error)
        kappa_norm_per_iteration.append(kappa_norm)

    if attempt_minimize:
        # If we want to minimize, we return the norm of kappa
        return kappa_norm
    else:
        # Otherwise, we return the distance between kappa and desired kappa
        return norm_error



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
    dirNames = ['./saved_bo_sq_error_per_iteration/', 
                './saved_random_sq_error_per_iteration/', 
                './saved_bo_kappa_x_per_iteration', 
                './saved_bo_kappa_y_per_iteration', 
                './saved_random_kappa_x_per_iteration', 
                './saved_random_kappa_y_per_iteration', 
                './saved_bo_kappa_norm_per_iteration',
                './saved_random_kappa_norm_per_iteration',
                './saved_bo_kappas', 
                './saved_bo_poly_lists', 
                './saved_random_kappas', 
                './saved_random_poly_lists', 
                './plots', 
                './errors']
    for dirName in dirNames:
        try:    
            os.mkdir(dirName)
            print('Directory ', dirName, ' Created')    
        except FileExistsError:
            pass



def min_per_iteration(items):
    '''
    Given a list of square errors per iteration, returns a new
    list of the minimum square error up to that iteration.
    '''
    min_per_iteration = []
    for item in items:
        if (min_per_iteration and item < min_per_iteration[-1]) or not min_per_iteration:
            min_per_iteration.append(item)
        else:
            min_per_iteration.append(min_per_iteration[-1])
    return min_per_iteration



def closest_per_iteration(items, desired):
    '''
    Given a list of kappa values per iteration, returns a new
    list of the kappa value closest to the desired kappa
    up to that iteration.
    '''
    closest_kappas = []
    for item in items:
        if not closest_kappas or abs(item - desired) < abs(closest_kappas[-1] - desired):
            closest_kappas.append(item)
        else:
            closest_kappas.append(closest_kappas[-1])

    return closest_kappas



if __name__ == "__main__":
    if initialize_folders:
        initialize()