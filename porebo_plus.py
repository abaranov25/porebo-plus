import os
from openbteplus.workflows import wf_4
from optim import BOMinimizer
import numpy as np
import gp_func
from plot_kappa_v_iteration import plot
import time
from params import params

"""
Parameters
    L: float
        Length of the geometry along x and y directions [nm]
    num_pores: int
        Number of pores in each quadrant
    porosity: float
        Percentage of the total geometry covered by pores
    step_input: float
        step size for the BTE solver (smaller means more accurate but slower)
    side_len: float
        Length of the pores [nm]. Calculated based on the given porosity and number of pores.
    buffer_len: float
        Minimum distance that pores must be from each other and from the walls of the geometry [nm] —
        set this parameter to 0 if a buffer is not needed

Depreciated sys inputs
    [ 'porebo.py' , num_pores , 100 * porosity ]
"""
kappa_per_iteration = []
tested_num_pores = params['tested_num_pores']
tested_porosities = params['tested_porosities']
given_L = params['L']
step_input = params['step_input']
buffer_len = params['buffer_len']
num_iters = params['num_iters']
num_init = params['num_init']
initialize_folders = params['initialize_folders']


def f(x, num_pores, given_porosity, save = False, random = False):
    '''
    Runs the BTE solver on the given sample of pore centers.
    '''
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
        mesh_size = 7,\
        shape     = 'square')

    time2 = time.time()
    print("Took ", time2-time1, " sec")

    # Saves the kappa value for the given sample of pore centers if save is True
    if save:
        if random:
            np.savetxt('./saved_random_kappas/num_pores_' + str(num_pores) + '_porosity_' + str(given_porosity) + '.out', [results.bte.kappa_eff])
            np.savetxt('./saved_random_poly_lists/poly_list_num_pores_' + str(num_pores) + '_porosity_' + str(given_porosity) + '.out', x)        
        else:
            np.savetxt('./saved_bo_kappas/num_pores_' + str(num_pores) + '_porosity_' + str(given_porosity) + '.out', [results.bte.kappa_eff])
            np.savetxt('./saved_bo_poly_lists/poly_list_num_pores_' + str(num_pores) + '_porosity_' + str(given_porosity) + '.out', x)

    kappa_per_iteration.append(results.bte.kappa_eff)
    return results.bte.kappa_eff



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
    dirNames = ['./saved_bo_kappas', './saved_bo_poly_lists', './saved_random_kappas', './saved_random_poly_lists', './plots']
    for dirName in dirNames:
        try:    
            os.mkdir(dirName)    
            print('Directory ', dirName, ' Created')    
        except FileExistsError:
            pass



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
            BO_obj = BOMinimizer(f=f, bounds=[(-0.5, 0.5)] * 2 * num_pores, n_init=num_init, n_calls=num_iters, n_sample=300, sampler=sampler, noise=1e-3, kernel="Matern", acq="EI", num_pores = num_pores, porosity = porosity)

            Xbest, ybest = BO_obj.minimize()
            print("ybest:", ybest)
            print("xbest:", Xbest)

            plot(kappa_per_iteration, num_init, num_pores, porosity, num_iters, algorithm = "porebo")
    
            f(Xbest, num_pores, porosity, save=True)