import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt
'''
n = 20
# 线性离散 + 小随机噪声
x = np.linspace(-200, 200, n) + np.random.uniform(-5, 5, n)
y = np.linspace(-200, 200, n) + np.random.uniform(-5, 5, n)
xx, yy = np.meshgrid(x, y)
A, b = 100, 100  #归一化参数

# 负负得正，会导致原本为凸的漏斗型 变成四角翘起，全为正
zz = A * np.sin(np.sqrt(xx**2 + yy**2) / b)

# 2D scatter plot
plt.scatter(xx, yy, s=5)
plt.xlabel("X")
plt.ylabel("Y")
plt.show()

# 3D point cloud
points = np.c_[xx.reshape(-1), yy.reshape(-1), zz.reshape(-1)]  # N*3
print(points[:5, :])

cloud = pv.PolyData(points)
cloud.plot(point_size=5)

# help(cloud.delaunay_2d)

surf = cloud.delaunay_2d()
surf.plot(show_edges=True)  # , line_width=5, color=True, opacity=0.5)

'''

x = np.arange(10, dtype=float)
xx, yy, zz = np.meshgrid(x, x, [0])
points = np.column_stack((xx.ravel(order='F'), yy.ravel(order='F'), zz.ravel(order='F')))
# 抖动
points[:, 0] += np.random.rand(len(points))  * 0.3
points[:, 1] += np.random.rand(len(points))  * 0.3

cloud = pv.PolyData(points)
print(cloud)  # 打印数据结构

cloud.plot(cpos='xy', point_size=10)
surf = cloud.delaunay_2d()
surf.plot(cpos='xy', show_edges=True)  # , line_width=5, color=True, opacity=0.5)
surf = cloud.delaunay_2d(alpha=1, tol=0.1)
surf.plot(cpos="xy", show_edges=True)
















