import numpy as np
import pyvista as pv

x = np.arange(-10, 10, 0.5)
y = np.arange(-10, 10, 0.5)
x, y = np.meshgrid(x, y)
r = np.sqrt(x**2 + y**2)
z = np.sin(r)

grid = pv.StructuredGrid(x, y, z)

# 定义绘制格式
plotter = pv.Plotter(notebook=False, off_screen=True)
plotter.add_mesh(grid,
                 scalars=z.ravel(),
                 lighting=False,
                 show_edges=True,
                 scalar_bar_args={"title": "Height"},
                 clim=[-1, 1],)
# 文件名
plotter.open_gif("wave.gif")
pts = grid.points.copy()

nframe = 15
#[0, 2*pi] / 15
for phase in np.linspace(0, 2 * np.pi, nframe + 1)[:nframe]:
    print(phase)
    z = np.sin(r + phase)
    grid.points[:, -1] = z.ravel()
    # plotter.update_coordinates(pts, render=False)
    grid.point= pts
    plotter.write_frame()

plotter.close()






