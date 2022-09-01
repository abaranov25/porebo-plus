from utils import *
from params import params

'''
This script runs a Random Search for every specified number of pores
and porosity. It does so by grabbing random pore arrangements and finding
the kappa or square error for each, rather than optimizing. This
script uses the same sampler() and f() functions as porebo_plus.
'''



if __name__ == "__main__":
    num_trials = params['num_iters']
    tested_num_pores = params['tested_num_pores']
    tested_porosities = params['tested_porosities']
    desired_kappa_x = params['desired_kappa_x']
    desired_kappa_y = params['desired_kappa_y']

    for num_pores in tested_num_pores:
        for porosity in tested_porosities:
            print("Starting trials for " + str(num_pores) + " pores and " + str(porosity) + " porosity")

            # stores the minimum kappa and pore configuration that produces that kappa
            min_kappa = 0
            config = []
            kappa_per_iteration = []
            trials_left = num_trials

            # Runs some number of samples with random pore configurations
            while trials_left > 0:
                samples = sampler(num_pores, porosity, trials_left)
                if type(samples[0]) != list:
                    samples = [samples]
                for sample in samples:
                    try:
                        kappa = f(sample, num_pores, porosity, desired_kappa_x = desired_kappa_x, desired_kappa_y = desired_kappa_y)
                        kappa_per_iteration.append(kappa)
                        if kappa < min_kappa or not config:
                            min_kappa = kappa
                            config = sample
                        trials_left -= 1
                    except:
                        pass
                print("Trials left: " + str(trials_left))

            print("ybest:", min_kappa)
            print("xbest:", config)

            f(config, num_pores, porosity, save=True, random=True)