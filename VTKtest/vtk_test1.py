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

def plot_press(m, dims):
    """ Plot pressure data  """
    N3, N2, N1 = dims
    coords = m.points
    x = coords[:, 0].reshape((N3, N2, N1))
    y = coords[:, 1].reshape((N3, N2, N1))
    z = coords[:, 2].reshape((N3, N2, N1))
    rho = m.point_data['Pressure']
    val = rho.reshape((N3, N2, N1))

    plt.pcolormesh(x[:, 0, :], y[:, 0, :], val[:, 0, :], shading='gouraud', cmap='jet')
    plt.colorbar()
    plt.show()

def main():
    """ Main function to execute the script functionality. """
    fp = '/home/joseph/Downloads/VTKtest/NRotSphere001N000.vtk'

    # Load and display mesh
    m = load_mesh(fp)
    print_mesh_info(m)

    # Plotting
    dims = get_dims(m)
    plot_press(m, dims)

if __name__ == "__main__":
    main()
