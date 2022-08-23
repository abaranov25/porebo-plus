from porebo_plus import f

'''
This script can run OpenBTE Plus on a pore configuration that
threw an error during the trials to find bugs in the OpenBTE
source code. This must be run with the same parameters in params.py
as the original trials, or else the error may not get caught.
'''

num = 0 # Modify for which error sample you want to view in case multiple trials don't work
input = None # the input is the list of coordinates for pore centers followed by the porosity

if input is None:
    with open("errors/error_" + str(num) + "_X.txt") as f:
        coords = f.read().split("\n")
        coords = [float(coord) for coord in coords[:-1]]
else:
    coords = input
    
num_pores = int( (len(coords) - 1)/2 )
porosity = float(coords[-1])

print(num_pores, porosity)


f(coords, num_pores, porosity)