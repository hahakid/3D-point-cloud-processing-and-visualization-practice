import numpy as np
import pyvista as pv
from pyvista import examples

# help(pv.Plotter.add_point_labels)
# 随机生成10个点云
poly = pv.PolyData(np.random.rand(10, 3))

# 定义 等长 label #
#poly["mylabels"] = [f"Label {i}" for i in range(poly.n_points)]
poly["mylabels"] = [f"Label ({', '.join(map(lambda x: f'{x:.3f}', tuple(poly.points[i])))})" for i in range(poly.n_points)]
print(poly)

plotter = pv.Plotter()
plotter.add_point_labels(poly, "mylabels", point_size=20, font_size=16)
plotter.show()


grid = pv.UnstructuredGrid(examples.hexbeamfile)
plotter = pv.Plotter()
plotter.add_mesh(grid, show_edges=True, color='tan')
points = grid.points
mask = points[:, 0] == 0  # 选择x=0的点云
plotter.add_point_labels(points[mask], points[mask].tolist(), point_size=20, font_size=16)
plotter.show()


mesh = examples.load_uniform().slice()
p = pv.Plotter()
p.add_mesh(mesh, scalars="Spatial Point Data", show_edges=True)
p.add_point_scalar_labels(mesh, "Spatial Point Data", point_size=20, font_size=16)

p.show()






















