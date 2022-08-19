from pandas_datareader import test
from porebo_plus import sampler, f
from plot_kappa_v_iteration import plot
from params import params

num_trials = params['num_iters']
tested_num_pores = params['tested_num_pores']
tested_porosities = params['tested_porosities']

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
            for sample in samples:
                try:
                    kappa = f(sample, num_pores, porosity)
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
        plot(kappa_per_iteration, 0, num_pores, porosity, num_trials, algorithm = "random")