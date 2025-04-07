import pyvista as pv
from pyvista import examples

dataset = pv.read('../data/Bunny.vtp')  # examples.download_bunny_coarse()
print(dataset)

# 使用平面裁剪，取y轴负方向的数据, True表示取反
clipped = dataset.clip('y', invert=False)
inv_clipped = dataset.clip('y', invert=True)
print(clipped)
print(inv_clipped)

p = pv.Plotter(shape=(1, 2))
p.add_mesh(dataset, style="wireframe", color='lightblue', label="Input")
p.add_mesh(clipped, color='red', label="Clipped")
p.show_axes_all()
p.show_bounds()
p.add_legend()

p.subplot(0, 1)
p.add_mesh(dataset, style="wireframe", color='lightblue', label="Input")
p.add_mesh(inv_clipped, color='red', label="Clipped")
p.show_axes_all()
p.show_bounds()
p.add_legend()

p.link_views()
p.show()

# clip_box
dataset = examples.download_office()
bounds = [1, 2, 3, 4, 0, 3]  # xmin, xmax, ymin, ymax, zmin, zmax
clipped = dataset.clip_box(bounds, invert=True)
inv_clipped = dataset.clip_box(bounds, invert=False)
print(clipped)

p = pv.Plotter(shape=(1, 2))
# p.add_mesh(dataset, style="wireframe", color='lightblue', label="Input")
p.add_mesh(clipped, color='red', label="Clipped", show_edges=True, opacity=0.40)
p.show_bounds()
p.show_axes_all()
p.add_legend()

p.subplot(0, 1)
p.add_mesh(dataset, style="wireframe", color='lightblue', label="Input")
p.add_mesh(inv_clipped, color='blue', label="Clipped")
p.show_bounds()
p.show_axes_all()
p.add_legend()
p.link_views()
p.show()

#  rotate clip box
mesh = examples.load_airplane()

# Use `pv.Box()` or `pv.Cube()` to create a region of interest
# center, x_length, y_length, z_length
roi = pv.Cube(center=(0.9e3, 0.2e3, mesh.center[2]), x_length=500, y_length=500, z_length=500)
roi.rotate_z(45, inplace=True)  # 旋转 ROI, False不旋转

p = pv.Plotter()
p.add_mesh(roi, opacity=0.75, color="red")
p.add_mesh(mesh, opacity=0.5)
p.show_bounds()
p.show()

# 反转裁剪， ROI以外
extracted = mesh.clip_box(roi, invert=False)  # 裁剪
inv_extracted = mesh.clip_box(roi, invert=True)  # 裁剪box以外的

p = pv.Plotter(shape=(1, 3))
p.add_mesh(roi, opacity=0.75, color="red")
p.add_mesh(mesh)
p.show_bounds()

p.subplot(0, 1)
p.add_mesh(extracted)
p.add_mesh(roi, opacity=0.75, color="red")
p.show_bounds()

p.subplot(0, 2)
p.add_mesh(inv_extracted)
# p.view_isometric()
p.link_views()
p.show()



#  crinkle
mesh = pv.Wavelet()
normal = (1, 1, 1)  # 法向
plane = pv.Plane(i_size=30, j_size=30, direction=normal)  # 平面
clipped = mesh.clip(normal=normal)  # 裁剪

crinkled = mesh.clip(normal=normal, crinkle=True)  # 裁剪

p = pv.Plotter(shape=(1, 2))
p.add_mesh(clipped, show_edges=True)
p.add_mesh(plane.extract_feature_edges(), color="r")
p.show_bounds()

p.show_axes_all()
p.subplot(0, 1)
p.add_mesh(crinkled, show_edges=True)
p.add_mesh(plane.extract_feature_edges(), color="r")
p.show_bounds()
p.show_axes_all()
p.link_views()
p.show()







