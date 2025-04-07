import pyvista as pv
from pyvista import examples
# 读取 python虚拟环境中，安装的pyvista库中的示例文件
filename = examples.planefile
print(filename)

mesh = pv.read(filename)

cpos = mesh.plot()  # 绘制
print(mesh.points[:3, :])

print(mesh.faces.reshape(-1, 4)[:, 1:])

############################

# read STL file， 读取官方github上的stl文件
mesh = pv.read('../data/42400-IDGH.stl')  # examples.download_cad_model()
cpos = [(107, 68, 204), (128, 86, 223), (0, 0, 0)]
# print(mesh)
mesh.plot(cpos=cpos, show_edges=True, show_grid=True, show_axes=True)

# read obj  file
mesh = examples.download_doorman()
mesh.plot(cpos='xy')

#read BYU file
mesh = examples.download_teapot()
mesh.plot(cpos=[-1, 2, -5], show_edges=True)

#read VTK file
mesh = examples.download_bunny_coarse()
mesh.plot(cpos='xy', show_edges=True, color=True)

# download different types of above 3D file, and plot



