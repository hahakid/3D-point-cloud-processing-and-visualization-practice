import pyvista as pv
#import os
import numpy as np
from pyvista import examples
#os.environ['PYVISTA_USERDATA_PATH'] = './data/'
mesh1 = examples.download_lucy(True)
mesh2 = examples.download_bunny(True)
#dataset.plot(smooth_shading=True, color='white')
#mesh1.plot(cpos='xy')  # 基于模型的坐标系进行投影可视化，x轴=X，y轴=Y
#mesh2.plot(cpos='yz')  # x-axis=Y, y-axis=Z


# 着色点云可视化，
points = np.random.random((1000, 3))
pc = pv.PolyData(points)
#pc.plot(scalars=points[:, 2], point_size=5.0, cmap='jet')  # z-轴作为颜色值，colormap

# pv支持的形状
cyl = pv.Cylinder(capping=False)  # 圆柱体
arrow = pv.Arrow()  # 箭头
sphere = pv.Sphere()  # 球体
plane = pv.Plane()  # 平面
line = pv.Line()  # 线段
box = pv.Box()  # 矩形
cone = pv.Cone()  # 圆锥
ploy = pv.Polygon()  # 多边形
disc = pv.Disc()  # 圆盘

p = pv.Plotter(shape=(3, 3))  # 创建一个3*3的子图
p.subplot(0, 0)  # 第一个子图，第一行第一列 ，0，0
p.add_mesh(cyl, color='blue', show_edges=True, nan_opacity=0.8)  # 输入参数的数据结构十分长，多元化可控性高

p.subplot(0, 1)  # 第一个子图，第一行第一列 ，0，0
p.add_mesh(arrow, color='tan', show_edges=True, line_width=5.3)  # 输入参数的数据结构十分长，多元化可控性高

p.subplot(0, 2)  # 第一个子图，第一行第一列 ，0，0
p.add_mesh(sphere, color='tan', show_edges=True, style='points_gaussian')  # 输入参数的数据结构十分长，多元化可控性高


p.subplot(1, 0)  # 第一个子图，第一行第一列 ，0，0
p.add_mesh(plane, color='tan', show_edges=True)  # 输入参数的数据结构十分长，多元化可控性高

p.subplot(1, 1)  # 第一个子图，第一行第一列 ，0，0
p.add_mesh(line, color='tan', line_width=3)  # show_edges=True)  # 输入参数的数据结构十分长，多元化可控性高

p.subplot(1, 2)  # 第一个子图，第一行第一列 ，0，0
p.add_mesh(box, color='tan', show_edges=True)  # 输入参数的数据结构十分长，多元化可控性高


p.subplot(2, 0)  # 第一个子图，第一行第一列 ，0，0
p.add_mesh(cone, color='tan', show_edges=True)  # 输入参数的数据结构十分长，多元化可控性高

p.subplot(2, 1)  # 第一个子图，第一行第一列 ，0，0
p.add_mesh(ploy, color='tan', show_edges=True)  # 输入参数的数据结构十分长，多元化可控性高

p.subplot(2, 2)  # 第一个子图，第一行第一列 ，0，0
p.add_mesh(disc, color='tan', show_edges=True)  # 输入参数的数据结构十分长，多元化可控性高

p.show()  # 显示 ,类似 matplotlib



