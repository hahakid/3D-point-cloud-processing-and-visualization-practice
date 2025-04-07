import pyvista as pv
from pyvista import examples
import numpy as np


points = np.random.rand(300, 3)
print(points[:5, :])  # 打印前5个点的坐标
print(points.shape)  # 打印点的数量和维度
# vertices
mesh = pv.PolyData(points)  # no connection between points
print(mesh)
mesh.plot(point_size=10, style='points')

# meshgrid and points
mesh_example = examples.load_hexbeam()
cpos = [(6.2, 3., 7.5), (0.16, 0.13, 2.65), (-0.28, 0.94, -0.21)]

pl = pv.Plotter()
pl.add_mesh(mesh_example, style='surface', show_edges=True, color='yellow', opacity=0.5) #, render_lines_as_tubes=True)
pl.add_points(mesh_example.points, color='red', point_size=20, render_points_as_spheres=True)
pl.camera_position = cpos
pl.show()


# bunny_coarse = examples.download_bunny_coarse()  # vpn
bunny_coarse = pv.read('../data/Bunny.vtp')
pl = pv.Plotter()
pl.add_mesh(bunny_coarse, show_edges=True, color='gray')  # 三角剖分的颜色
pl.add_points(bunny_coarse.points, color='green', point_size=10, render_points_as_spheres=True)
pl.camera_position = cpos = [(0.02, 0.3, 0.73), (0.02, 0.03, -0.022), (-0.03, 0.94, -0.34)]
pl.show()



# cell 定义mesh中points的连接性，也就是拓扑几何关系
# 实际上就是通过edges关联点

cell_example = examples.load_hexbeam()

pl = pv.Plotter()  # new plotter
pl.add_mesh(cell_example, show_edges=True, color='white')  # 三角剖分的颜色
pl.add_points(cell_example.points, color='red', point_size=20)

single_cell = cell_example.extract_cells(cell_example.n_cells - 1)  # 提取最后一个cell
pl.add_mesh(single_cell, color='green', edge_color="blue", line_width=5, show_edges=True) # , opacity=0.9)  # 渲染效果似乎有点问题，单独显示最后一个cell

pl.camera_position = cpos = [(6.2, 3., 7.5), (0.16, 0.13, 2.65), (-0.28, 0.94, -0.21)]
pl.show()

# data attributes

cell_example.point_data['my point values'] = np.arange(cell_example.n_points)
cell_example.plot(scalars='my point values', cpos=cpos, show_edges=True)

cell_example.cell_data['my cell values'] = np.arange(cell_example.n_cells)  # 每个cell的值
cell_example.plot(scalars='my cell values', cpos=cpos, show_edges=True)


uni = examples.load_uniform()
pl = pv.Plotter(shape=(1, 2), border=False)
pl.add_mesh(uni, scalars='Spatial Point Data', show_edges=True)
pl.subplot(0, 1)
pl.add_mesh(uni, scalars='Spatial Cell Data', show_edges=True)
# pl.link_views()
pl.show()

# Field data
mesh_field = pv.Cube()
mesh_field.field_data['metadata'] = ['str1', 'str2']
print(mesh_field.field_data['metadata'])

cube = pv.Cube()
print(cube)
cube.cell_data['myscalars'] = range(6)

other_cube = cube.copy()
print(other_cube)
other_cube.point_data['myscalars'] = range(8)


pl = pv.Plotter(shape=(1, 2), border_width=1)
pl.add_mesh(cube, cmap='coolwarm')

pl.subplot(0, 1)
pl.add_mesh(other_cube, cmap='coolwarm')
pl.link_views()
pl.show()














