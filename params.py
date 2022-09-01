'''
The parameters for the model are as follows:



    L (float)                       :   The total length of the geometry along the x and y directions [nm]
    step_input (float)              :   The step size for the BTE solver (smaller means more accurate but slower)
    tested_num_pores (list)         :   A list of the amount of pores to be placed in each quadrant for every trial
    tested_porosities (list)        :   A list of the porosities (percentage of total geometry covered by the pores)
                                        to be tested in the trials
    buffer_len (float)              :   The minimum distance pores must have between each other and walls [nm]
    num_samples (int)               :   The number of pore configurations to be generated after every iteration of
                                        Bayesian Optimization, from which only one sample will be chosen to run 
                                        OpenBTE Plus on
    num_iters (int)                 :   The number of total calls to the OpenBTE Plus solver for every trial
    num_init (int)                  :   The number of random pore configurations tested before using Bayesian 
                                        Optimization to select the next pore configuration
    initialize_folders (bool)       :   Set to True if you want the relevant folders storing results to be initialized
    desired_kappa (float)           :   The thermal conductivity that we are aiming to reach. If desired_kappa = 0, then
                                        we are finding the minimum kappa. Otherwise, it will try to optimize for the 
                                        given value.
    *display_every_iter (bool)      :   If set to True, will plot a scatter of kappa per iteration for all plots
    *attempt_minimize (bool)        :   If set to True, will ignore the desired kappa and try instead to minimize
                                        kappa for every trial. This will produce additional plots in the plots folder
                                        called plot_trials_random.png and plot_trials_bo.png



* These were added since the last Github push



All mutable parameters are stored in the below dictionary 
for convenience. Other scripts call on this dictionary for values.
'''


params = {
    'L': 100,
    'step_input': 10,
    'tested_num_pores': [4],
    'tested_porosities': [0.05],
    'buffer_len': 0.5,
    'num_samples': 200,
    'num_iters': 25,
    'num_init': 5,
    'initialize_folders': True,
    'desired_kappa_x': 31,
    'desired_kappa_y': 38,
    'display_every_iter': True,
    'attempt_minimize': False,
}