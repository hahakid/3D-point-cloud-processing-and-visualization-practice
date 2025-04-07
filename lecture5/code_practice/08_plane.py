# 平面组件
# 通过平面旋转，平移 切割进行剖面展示

import pyvista as pv
from pyvista import examples

vol =  pv.read("../data/brain.vtk") # examples.download_brain()

p = pv.Plotter()
p.add_mesh_clip_box(vol)
p.show()

print(p.plane_clipped_meshes)

#  单一维度平面切分,可通过法向控制剖面方向
p = pv.Plotter()
p.add_mesh_slice(vol, normal='x')
p.show()