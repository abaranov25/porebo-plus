import matplotlib.pyplot as plt
import os
from params import params

curdir = os.getcwd()
tested_num_pores = params['tested_num_pores']
tested_porosities = params['tested_porosities']

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