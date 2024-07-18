import sys
import numpy as np
import matplotlib.pyplot as plt
import os
import pyvista as pv

def load_mesh(fp):
    """ load VTK file  """
    if not os.path.exists(fp):
        print(f"Error: File not found at {fp}")
        sys.exit(1)

    return pv.read(fp)

def print_mesh_info(m):
    """ Print mesh info. """
    print(m)
    if m.point_data:
        print("Point Data:")
        for n in m.point_data:
            print(f"  - {n}: {m.point_data[n].shape}")

def get_dims(m):
    return m.dimensions

def slicer(m, dims, parameters, slices, dimensions):
    """
    Function to plot slices of the parameters data given along any of the 3 axis at any length.
    Currently only supporting 3D arrays from vtk files
    Args:
        m (pyvista.core.grid.ImageData): The array of data containing all the data and info about the simulation (output from 'load_mesh' function)
        dims (tuple of int): Number of cells in each direction (output from get_dims function)
        parameters (tuple of str): Name of data parameters to plot a slice of
        slices (tuple of int): Lengths at which a slice plot will be made given in cell numbers NOT physical length
        dimensions (tuple of str): Dimensions along a slice will be made. Valide options are: 'x', 'y', 'z'
    Notes: The length of parameters, slices and dimensions tuples has to be the same.
    """
    if not len(parameters)==len(slices)==len(dimensions):
        print(f"Error: Size of parameters, slices and dimensions arrays not equal")
        sys.exit(1)
        
    N3, N2, N1 = dims
    coords = m.points
    num_of_plots = len(parameters)
    plt_lay = 110*int(np.ceil(np.sqrt(num_of_plots)))+1
    x = coords[:, 2].reshape((N3, N2, N1))
    y = coords[:, 1].reshape((N3, N2, N1))
    z = coords[:, 0].reshape((N3, N2, N1))
    fig = plt.figure()
    for i in range(num_of_plots):
        arr_to_plot = m.point_data[parameters[i]]
        vals_to_plot = arr_to_plot.reshape((N3, N2, N1))
        ax = plt.subplot(plt_lay+i)
        if dimensions[i] == 'x':
            pl = ax.pcolormesh(y[slices[i],:,slices[i]],z[slices[i],slices[i],:],vals_to_plot[slices[i],:,:],cmap='jet')
        elif dimensions[i] == 'y':
            pl = ax.pcolormesh(x[:,slices[i],slices[i]],z[slices[i],slices[i],:],vals_to_plot[:,slices[i],:],cmap='jet')
        elif dimensions[i] == 'z':
            pl = ax.pcolormesh(x[:,slices[i],slices[i]],y[slices[i],:,slices[i]],vals_to_plot[:,:,slices[i]],cmap='jet')
        fig.colorbar(pl)
        ax.set_title(parameters[i])
    plt.tight_layout()
    plt.show()
#    print(m.point_data)
#    plt.pcolormesh(x[:,slc,slc], y[slc,:,slc],val[:, slc, :], cmap='jet')
    #plt.gca().set_aspect('equal')
#    plt.colorbar()
#    plt.show()
    
def main():
    """ Main function to execute the script functionality. """
    fp = 'EP3DV50.vtk'

    # Load and display mesh
    m = load_mesh(fp)
    print(type(m.dimensions))
    print_mesh_info(m)

    # Plotting
    dims = get_dims(m)
    par = ['Density','Pressure','Density','Pressure']
    dimen = ['x','x','x','x']
    sly = [28,36,28,36]
    slicer(m, dims,par,sly,dimen)

if __name__ == "__main__":
    main()
