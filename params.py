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
    desired_kappa (float)           :   The thermal conductivity that we are aiming to reach



All mutable parameters are stored in the below dictionary 
for convenience. Other scripts call on this dictionary for values.
'''


params = {
    'L': 100,
    'step_input': 10,
    'tested_num_pores': [2],
    'tested_porosities': [0.05,0.1],
    'buffer_len': 0.5,
    'num_samples': 30,
    'num_iters': 3,
    'num_init': 1,
    'initialize_folders': True,
    'desired_kappa': 25,
}