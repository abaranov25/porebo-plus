from porebo_plus import f

num = 0 # Modify for which error sample you want to view in case multiple trials don't work
input = [2.950811556269384184e+01,
2.573554318554741016e+01,
0.15,
] # the input is the list of coordinates for pore centers followed by the porosity

if input is None:
    with open("errors/error_" + str(num) + "_X.txt") as f:
        coords = f.read().split("\n")
        coords = [float(coord) for coord in coords[:-1]]
else:
    coords = input
    
num_pores = int( (len(coords) - 1)/2 )
porosity = float(coords[-1])

print(num_pores, porosity)


f(coords, num_pores, porosity, save=False, random=True)