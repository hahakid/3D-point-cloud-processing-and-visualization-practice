import pyvista as pv
from pyvista import examples

mesh = pv.Wavelet()

# 新建画布，并添加mesh数据
p = pv.Plotter()
p.add_mesh(mesh)  # , show_edges=True, color='w')
p.show()

# 修改绘制的色彩配图，
# 一般是对灰度图进行彩色着色，因为灰度或者单一维度数值只有一个维度
# colormap 就是完成将 单一维度数值进行三通道0-255区间映射
# 这里注意参数 cmap是colormap着色策略，color是单一配色
p = pv.Plotter(shape=(1, 2))
p.subplot(0, 0)
p.add_mesh(mesh, cmap='coolwarm')

p.subplot(0, 1)
p.add_mesh(mesh, color='w')
p.link_views()
p.show()

#显示mesh的边缘
p = pv.Plotter()
p.add_mesh(mesh, show_edges=True)
p.show()

#不透明度对比
mesh = examples.download_st_helens().warp_by_scalar()
p = pv.Plotter(shape=(5, 1))
p.subplot(0, 0)
p.add_mesh(mesh, cmap='terrain')

p.subplot(1, 0)
p.add_mesh(mesh, cmap='terrain', opacity='linear')

p.subplot(2, 0)
p.add_mesh(mesh, cmap='terrain', opacity='linear_r')

p.subplot(3, 0)
p.add_mesh(mesh, cmap='terrain', opacity='geom')

p.subplot(4, 0)
p.add_mesh(mesh, cmap='terrain', opacity='geom_r')

p.link_views()
p.view_isometric()  # 等角视图
p.show()

# 在单个画布上绘制多个mesh

kinds = ['tetrahedron', 'cube', 'octahedron', 'dodecahedron', 'icosahedron']
centers = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0)]

solids = [pv.PlatonicSolid(kind, radius=0.4, center=center) for kind, center in zip(kinds, centers)]

p = pv.Plotter(window_size=[1000, 1000])
for _ind, solid in enumerate(solids):
    p.add_mesh(solid, color='silver', specular=1.0, specular_power=10)
p.view_vector((5.0, 2, 3))
p.add_floor("-z", lighting=True, color="tan", pad=1.0)
p.enable_shadows()
p.show()