import numpy as np
import pyvista as pv
from scipy.interpolate import griddata


def get_colors(n):
    """A helper function to get n colors."""
    from itertools import cycle
    import matplotlib as mpl

    cycler = mpl.rcParams["axes.prop_cycle"]
    colors = cycle(cycler)
    return [next(colors)["color"] for i in range(n)]


# Create a grid to interpolate to
xmin, xmax, ymin, ymax = 0, 100, 0, 100
x = np.linspace(xmin, xmax, num=25)
y = np.linspace(ymin, ymax, num=25)
xx, yy, zz = np.meshgrid(x, y, [0])

# Make sure boundary conditions exist
boundaries = np.array([[xmin, ymin, 0], [xmin, ymax, 0], [xmax, ymin, 0], [xmax, ymax, 0]])

# Create the PyVista mesh to hold this grid
surf = pv.StructuredGrid(xx, yy, zz)

# Create some initial perturbations
# - this array will be updated inplace
points = np.array([[33, 25, 45], [70, 80, 13], [51, 57, 10], [25, 69, 20]])

# Create an interpolation function to update that surface mesh
def update_surface(point, i) -> None:
    points[i] = point
    tp = np.vstack((points, boundaries))
    # @ points @ data values @ Points at which to interpolate data. @ 插值算法
    zz = griddata(tp[:, 0:2], tp[:, 2], (xx[:, :, 0], yy[:, :, 0]), method="cubic")
    surf.points[:, -1] = zz.ravel(order="F")

# Get a list of unique colors for each widget
colors = get_colors(len(points))
# vis
p = pv.Plotter()

# Add the surface to the scene
p.add_mesh(surf, color=True)

# Add the widgets which will update the surface
p.add_sphere_widget(update_surface, center=points, color=colors, radius=3)
# Add axes grid
p.show_grid()

# Show it!
p.show()