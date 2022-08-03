from porebo_plus import sampler, f
import sys
from plot_kappa_v_iteration import plot

num_trials = 50


for num_pores in [1,2,3,4,5]:
    for porosity in [0.05,0.1,0.15]:
        print("Starting trials for " + str(num_pores) + " pores and " + str(porosity) + " porosity")

        # stores the minimum kappa and pore configuration that produces that kappa
        min_kappa = 0
        config = []
        kappa_per_iteration = []

        # Runs some number of samples with random pore configurations
        samples = sampler(num_pores, porosity, num_trials)
        for sample in samples:
            kappa = f(sample, num_pores, porosity)
            kappa_per_iteration.append(kappa)
            if kappa < min_kappa or not config:
                min_kappa = kappa
                config = sample

        print("ybest:", min_kappa)
        print("xbest:", config)

        f(config, num_pores, porosity, save=True, random=True)
        plot(kappa_per_iteration, 0, num_pores, porosity, num_trials, algorithm = "random")