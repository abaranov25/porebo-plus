import matplotlib.pyplot as plt

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

    plt.plot(iterations, kappas, 'ro-', alpha = 0.7, label = "Kappa Per Iteration")
    plt.plot(iterations, min_kappa_per_iteration, 'bo-', label = "Minimum Kappa Per Iteration")
    if algorithm == 'porebo':
        plt.axvspan(-0.3,num_init - 0.7, alpha = 0.4, color = 'gray', label = 'Initialization')
    plt.xlabel('Iteration')
    plt.ylabel('Kappa')
    plt.title('Kappa vs Iteration')
    plt.legend(loc='upper right')
    plt.savefig('plots/' + algorithm + '_num_pores_' + str(num_pores) + '_porosity_' + str(porosity) +'.png')
    plt.close()

