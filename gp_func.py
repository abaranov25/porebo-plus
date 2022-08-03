from openbte import Geometry, Solver, Material, Plot
from openbte.utils import *
from os import mkdir
import numpy as np

def reflect(x_shift: float, y_shift: float, side_len: float, len_x: float, len_y: float) -> list:
    """
    x_shift: float
        Translation from the square to the origin along x [nm]
    y_shift: float
        Translation from the square to the origin along y [nm]
    side_len: float
        Length of the pores [nm]
    len_x: float
        Length of the geometry along x direction [nm]
    len_y: float
        Length of the geometry along y direction [nm]
    """

    poly_list = []

    # If the polygon wraps around in x-axis, move the center to the left

    if x_shift + side_len / 2 > len_x / 2:

        return reflect(x_shift = x_shift - len_x / 2, y_shift = y_shift, side_len = side_len, len_x = len_x, len_y = len_y)

    # If the polygon wraps around in y-axis, move the center down

    elif y_shift + side_len / 2 > len_y/ 2:

        return reflect(x_shift = x_shift, y_shift = y_shift - len_y/ 2, side_len = side_len, len_x = len_x, len_y = len_y)

    # This case represents the polygon going over the y-axis but not x-axis

    if x_shift - side_len / 2 < 0 and 0 < y_shift - side_len / 2:

        poly_list.append([[x_shift + side_len / 2, y_shift + side_len / 2],
                          [x_shift + side_len / 2, y_shift - side_len / 2],
                          [-x_shift - side_len / 2, y_shift - side_len / 2],
                          [-x_shift - side_len / 2, y_shift + side_len / 2]])

        poly_list.append([[x_shift + side_len / 2, -y_shift - side_len / 2],
                          [x_shift + side_len / 2, -y_shift + side_len / 2],
                          [-x_shift - side_len / 2, -y_shift + side_len / 2],
                          [-x_shift - side_len / 2, -y_shift - side_len / 2]])

        poly_list.append([[len_x / 2 + x_shift - side_len / 2, y_shift + side_len / 2],
                          [len_x / 2 + x_shift - side_len / 2, y_shift - side_len / 2],
                          [len_x / 2 - x_shift + side_len / 2, y_shift - side_len / 2],
                          [len_x / 2 - x_shift + side_len / 2, y_shift + side_len / 2]])

        poly_list.append([[len_x / 2 + x_shift - side_len / 2, -y_shift - side_len / 2],
                          [len_x / 2 + x_shift - side_len / 2, -y_shift + side_len / 2],
                          [len_x / 2 - x_shift + side_len / 2, -y_shift + side_len / 2],
                          [len_x / 2 - x_shift + side_len / 2, -y_shift - side_len / 2]])

    # This case represents the polygon going over the x-axis but not y-axis

    elif 0 < x_shift - side_len / 2 and 0 > y_shift - side_len / 2:

        poly_list.append([[x_shift + side_len / 2, y_shift + side_len / 2],
                          [x_shift + side_len / 2, -y_shift - side_len / 2],
                          [x_shift - side_len / 2, -y_shift - side_len / 2],
                          [x_shift - side_len / 2, y_shift + side_len / 2]])

        poly_list.append([[-x_shift - side_len / 2, y_shift + side_len / 2],
                          [-x_shift - side_len / 2, -y_shift - side_len / 2],
                          [-x_shift + side_len / 2, -y_shift - side_len / 2],
                          [-x_shift + side_len / 2, y_shift + side_len / 2]])

        poly_list.append([[x_shift + side_len / 2, len_y/ 2 + y_shift - side_len / 2],
                          [x_shift - side_len / 2, len_y/ 2 + y_shift - side_len / 2],
                          [x_shift - side_len / 2, len_y/ 2 - y_shift + side_len / 2],
                          [x_shift + side_len / 2, len_y/ 2 - y_shift + side_len / 2]])

        poly_list.append([[-x_shift - side_len / 2, len_y/ 2 + y_shift - side_len / 2],
                          [-x_shift + side_len / 2, len_y/ 2 + y_shift - side_len / 2],
                          [-x_shift + side_len / 2, len_y/ 2 - y_shift + side_len / 2],
                          [-x_shift - side_len / 2, len_y/ 2 - y_shift + side_len / 2]])

    # This case represents the polygon going over the x-axis and y-axis

    elif 0 > x_shift - side_len / 2 and 0 > y_shift - side_len / 2:

        poly_list.append([[x_shift + side_len / 2, y_shift + side_len / 2],
                          [x_shift + side_len / 2, -y_shift - side_len / 2],
                          [-x_shift - side_len / 2, -y_shift - side_len / 2],
                          [-x_shift - side_len / 2, y_shift + side_len / 2]])

        poly_list.append([[x_shift + side_len / 2, len_y/ 2 + y_shift - side_len / 2],
                          [x_shift + side_len / 2, len_y/ 2 - y_shift + side_len / 2],
                          [-x_shift - side_len / 2, len_y/ 2 - y_shift + side_len / 2],
                          [-x_shift - side_len / 2, len_y/ 2 + y_shift - side_len / 2]])

        poly_list.append([[len_x / 2 + x_shift - side_len / 2, y_shift + side_len / 2],
                          [len_x / 2 + x_shift - side_len / 2, -y_shift - side_len / 2],
                          [len_x / 2 - x_shift + side_len / 2, -y_shift - side_len / 2],
                          [len_x / 2 - x_shift + side_len / 2, y_shift + side_len / 2]])

        poly_list.append([[len_x / 2 + x_shift - side_len / 2, len_y/ 2 + y_shift - side_len / 2],
                          [len_x / 2 + x_shift - side_len / 2, len_y/ 2 - y_shift + side_len / 2],
                          [len_x / 2 - x_shift + side_len / 2, len_y/ 2 - y_shift + side_len / 2],
                          [len_x / 2 - x_shift + side_len / 2, len_y/ 2 + y_shift - side_len / 2]])

    # This case represents the polygon not going over either the x-axis or y-axis

    else:

        poly_list.append([[x_shift - side_len / 2, y_shift - side_len / 2],
                          [x_shift + side_len / 2, y_shift - side_len / 2],
                          [x_shift + side_len / 2, y_shift + side_len / 2],
                          [x_shift - side_len / 2, y_shift + side_len / 2]])

        poly_list.append([[x_shift - side_len / 2, -y_shift + side_len / 2],
                          [x_shift + side_len / 2, -y_shift + side_len / 2],
                          [x_shift + side_len / 2, -y_shift - side_len / 2],
                          [x_shift - side_len / 2, -y_shift - side_len / 2]])

        poly_list.append([[-x_shift + side_len / 2, -y_shift + side_len / 2],
                          [-x_shift - side_len / 2, -y_shift + side_len / 2],
                          [-x_shift - side_len / 2, -y_shift - side_len / 2],
                          [-x_shift + side_len / 2, -y_shift - side_len / 2]])

        poly_list.append([[-x_shift + side_len / 2, y_shift - side_len / 2],
                          [-x_shift - side_len / 2, y_shift - side_len / 2],
                          [-x_shift - side_len / 2, y_shift + side_len / 2],
                          [-x_shift + side_len / 2, y_shift + side_len / 2]])

    return poly_list

def config(x_len: float, y_len: float, side_len: float, num_pores: int, buffer_len: float, return_poly_list: bool = True) -> list:

    """
        x_len: float
            Length of the geometry along x direction [nm]
        y_len: float
            Length of the geometry along y direction [nm]
        side_len: float
            Length of the pores [nm]
        num_pores: int
            Number of pores
        buffer_len: float
            Minimum distance that pores must be from each other and from the walls of the geometry [nm] —
            set this parameter to 0 if a buffer is not needed
    """

    poly_centers = []  # This represents the pores configurations as a list of lists
    reflected_poly = []
    trial_count = 0

    # Generate "num_pores" pores such that they do not overlap

    while len(poly_centers) < num_pores:

        trial_count += 1
        if trial_count > 1000:
            print('Pore configuration failed, trying again')
            trial_count = 0
            poly_centers = []
            reflected_poly = []
        

        is_valid = True
        x_shift = np.random.uniform(0, x_len/2)
        y_shift = np.random.uniform(0, y_len/2)

        if (abs(x_shift) > x_len/2 - side_len - buffer_len or abs(y_shift) > y_len/2 - side_len - buffer_len or abs(x_shift) < side_len + buffer_len or abs(y_shift) < side_len + buffer_len):
            is_valid = False
        # check to see if the pore overlaps with any other square

        for poly in poly_centers:

            xpore_ctr = poly[0]
            ypore_ctr = poly[1]

            if (side_len + buffer_len > abs(x_shift - xpore_ctr) or
                side_len + buffer_len > abs(x_shift - xpore_ctr - x_len/2) or
                side_len + buffer_len > abs(x_shift - xpore_ctr + x_len/2)) and (side_len + buffer_len > abs(y_shift - ypore_ctr) or
                side_len + buffer_len > abs(y_shift - ypore_ctr - y_len/2) or
                side_len + buffer_len > abs(y_shift - ypore_ctr + y_len/2)
                ):
                is_valid = False

        if  is_valid: # If the pore does not overlap with any other pore, then add the pore to the list of pores

            poly_centers.append([x_shift, y_shift])
            if return_poly_list:

                for poly in reflect(x_shift=x_shift, y_shift=y_shift, side_len=side_len, len_x=x_len, len_y=y_len):

                    reflected_poly.append(poly)

    # Saves each polygon in a separate file

    dir_name = 'Poly_list'
    try:
        mkdir(dir_name)
        print("Directory ", dir_name, " Created ")

    except FileExistsError:
        pass

    for i in range(num_pores):

      filename = dir_name + '/poly_list_' + str(i) + '.out'
      np.savetxt(filename, poly_centers[i])

    if return_poly_list:
        return reflected_poly, poly_centers
    else:
        return poly_centers

if __name__ == '__main__':

    x_length = 200
    y_length = 170
    side_length = 8
    number_pores = 15
    buffer_length = 5
    step = 10

    poly_list, poly_centers = config(x_len=x_length, y_len=y_length, side_len=side_length,
                       num_pores=number_pores, buffer_len=buffer_length)

    # Create the geometry
    geo = Geometry(model='custom', lx=x_length, ly=y_length, step=step, polygons=poly_list,
                   applied_gradient=[1,0], boundary=['Periodic', 'Periodic'],
                   relative=False, delete_gmsh_files=False)

    # Create the material
    mat = Material(source='database',model='rta2DSym',filename='rta_Si_300',temperature=300)

    # Solve BTE
    sol = Solver(verbose=True,max_bte_iter=30,only_fourier=False)

    # Plot the outputs
    plot_bte = Plot(model='solver',show=False)

    # Returns kappa
    np.savetxt('kappa.out', sol['kappa'])