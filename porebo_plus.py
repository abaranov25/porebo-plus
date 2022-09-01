from optim import BOMinimizer
from params import params
from utils import *

"""
This script runs the trials for Bayesian Optimization with the parameters
defined in params.py. It first initializes by using random search for a
certain number of trials, and then proceeds by 
"""



if __name__ == "__main__":
    # Initializing values for the trials
    tested_num_pores = params['tested_num_pores']
    tested_porosities = params['tested_porosities']
    num_iters = params['num_iters']
    num_init = params['num_init']
    num_samples = params['num_samples']
    desired_kappa_x = params['desired_kappa_x']
    desired_kappa_y = params['desired_kappa_y']
    for num_pores in tested_num_pores:
        for porosity in tested_porosities:
            kappa_per_iteration = []
            print("Starting trials for " + str(num_pores) + " pores and " + str(porosity) + " porosity")
            BO_obj = BOMinimizer(f=f, bounds=[(-0.5, 0.5)] * 2 * num_pores, n_init=num_init, n_calls=num_iters, n_sample=num_samples, sampler=sampler, noise=1e-3, kernel="Matern", acq="EI", num_pores = num_pores, porosity = porosity, desired_kappa_x = desired_kappa_x, desired_kappa_y = desired_kappa_y)

            Xbest, ybest = BO_obj.minimize()
            print("ybest:", ybest)
            print("xbest:", Xbest)

            f(Xbest, num_pores, porosity, desired_kappa_x = desired_kappa_x, desired_kappa_y = desired_kappa_y, save=True)