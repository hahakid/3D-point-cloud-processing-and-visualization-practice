import numpy as np
import pyvista as pv
# 均匀栅格

values1 = np.linspace(0, 10, 1000).reshape((20, 5, 10))  #
print(values1.shape)

grid1 = pv.ImageData()
grid1.dimensions = np.array(values1.shape) + 1  # 1 for later data injection

grid1.origin = (100, 33, 55.6)
grid1.spacing = (1, 5, 2)  # 每个轴的 坐标间隔，对应 20/1=20 5/5=1 10/2=5

grid1.cell_data["values"] = values1.flatten(order="F")  # order="F" 按行存储
print(grid1)

#grid.plot(show_edges=True)

values2 = np.linspace(0, 10, 1000).reshape((20, 5, 10))
grid2 = pv.ImageData()
grid2.dimensions = values2.shape

grid2.origin = (100, 33, 55.6)
grid2.spacing = (1, 5, 2)

grid2.point_data['values'] = values2.flatten(order="F")
print(grid2)
#grid.plot(show_edges=True)

# help(pv.ImageData)
pl = pv.Plotter(shape=(1, 2), border=False)
pl.add_mesh(grid1, show_edges=True)
pl.subplot(0, 1)
pl.add_mesh(grid2, show_edges=True)
pl.link_views()
pl.show()

# 50*50*50 三维数组 的随机马赛克
arr = np.random.random((50, 50, 50))
print(arr.shape)
vol = pv.ImageData()
vol.dimensions = arr.shape
vol['array'] = arr.ravel(order='F')

vol.plot()

# 不同可视化下
# 不透明度映射（Opacity mapping）是计算机图形学和可视化中的一种技术，用于根据标量数组的值来调整物体的不透明度。
# 这种方法常用于科学可视化，例如在医学成像、气象模拟和流体动力学等领域，以便更清晰地展示数据中的不同结构和特征。
from pyvista import examples
#vol = examples.download_knee_full(True)
vol = pv.read('../data/vw_knee.slc')
print(vol)
p = pv.Plotter(shape=(1, 2), border=False)
p.add_volume(vol, cmap='bone', opacity='sigmoid')
# p.show()
p.subplot(0, 1)
# custom opacity
opacity = [0, 0, 0, 0.1, 0.3, 0.6, 1]

#vol = pv.Wavelet()
p.add_volume(vol, cmap='bone', opacity=opacity)
p.link_views()
p.show()










