import numpy as np
import pyvista as pv

# Create a triangle surface
surf = pv.PolyData()
surf.points = np.array(
    [
        [-10, -10, -10],
        [10, 10, -10],
        [-10, 10, 0],
    ]
)
surf.faces = np.array([3, 0, 1, 2])  # triangle face, 连接顺序 0, 1, 2

p = pv.Plotter()


def callback(point) -> None:
    surf.points[0] = point

p.add_sphere_widget(callback)
p.add_mesh(surf, color=True)

p.show_grid()
p.show()

surf = pv.PolyData()
surf.points = np.array(
    [
        [-10, -10, -10],
        [10, 10, -10],
        [-10, 10, 0],
    ]
)
surf.faces = np.array([3, 0, 1, 2])  # triangle face, 连接顺序 0, 1, 2

p = pv.Plotter()

def callback(point, i) -> None:
    surf.points[i] = point

p.add_sphere_widget(callback, center=surf.points)
p.add_mesh(surf, color=True)

p.show_grid()
p.show()