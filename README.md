# porebo-plus
Testing whether Bayesian Optimization is better than random search in finding pore arrangements that minimize thermal conductivity.

To perform the tests, simply open the bash file named "run_scripts.sh".

The results will be printed onto the terminal and also saved as plots in the "plots" folder.

Changes made since last update:
  - Added more mutable parameters in params.py
  - Removed plot_kappa_v_iteration.py and moved it to porebo_plus.py
  - Added an option to tune thermal transport to a specific value
  - Added folders to save kappa values or square error per iteration
