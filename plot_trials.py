import matplotlib.pyplot as plt
import os

curdir = os.getcwd()

kappa_plots = []
for porosity in [0.05,0.1,0.15]:
    temp_kappas = []
    for num_pores in [1,2,3,4,5]:
        with open(curdir + '/saved_bo_kappas/num_pores_' + str(num_pores) + '_porosity_' + str(porosity) + '.out') as f:
            kappa = float(f.read())
            temp_kappas.append(kappa)
    kappa_plots.append(temp_kappas)

for i, kappa_plot in enumerate(kappa_plots):
    plt.plot([1,2,3,4,5], kappa_plot, label = "Porosity = " + str(0.05 * i))

plt.legend(loc='upper right')
plt.xlabel('# of Pores')
plt.ylabel('Min Kappa')
plt.savefig('plot_trials_bo.png')

kappa_plots = []
for porosity in [0.05,0.1,0.15]:
    temp_kappas = []
    for num_pores in [1,2,3,4,5]:
        with open(curdir + '/saved_random_kappas/num_pores_' + str(num_pores) + '_porosity_' + str(porosity) + '.out') as f:
            kappa = float(f.read())
            temp_kappas.append(kappa)
    kappa_plots.append(temp_kappas)

for i, kappa_plot in enumerate(kappa_plots):
    plt.plot([1,2,3,4,5], kappa_plot, label = "Porosity = " + str(0.05 * i))

plt.legend(loc='upper right')
plt.xlabel('# of Pores')
plt.ylabel('Min Kappa')
plt.savefig('plot_trials_random.png')