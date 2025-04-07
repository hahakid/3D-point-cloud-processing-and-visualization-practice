import numpy as np
import pyvista as pv
from pyvista import examples

def show_mesh(mesh):
    plotter = pv.Plotter()
    plotter.add_mesh(mesh, point_size=1, color='blue')# Plot the mesh
    plotter.show()  # Display the plot

def generate_points(subset=0.05):
    # Load a sample mesh
    dataset = examples.download_lidar()
    # Generate a random subset of points from the dataset
    ids = np.random.randint(low=0, high=dataset.n_points-1, size=int(dataset.n_points * subset))
    # Return the subset of points
    return dataset.points[ids]

points = generate_points()
print(points[0:5, :])

# 基于points 生成mesh
point_cloud = pv.PolyData(points)
show_mesh(point_cloud)  # 看起来像航空雷达拍摄效果
print(np.allclose(points, point_cloud.points))

# 基于EDL的点云可视化技术，增强点云的可视性
# https://docs.pyvista.org/examples/02-plot/edl.html
point_cloud.plot(eye_dome_lighting=True)

# 增加一列与现在point_cloud相同规模的数据

data = points[:, -1]  # z-axis
point_cloud["elevation"] = data  # 定义为高度

point_cloud.plot(render_points_as_spheres=True, point_size=5, cmap="coolwarm",
                 scalars="elevation")

# 增加多维数据
points = np.random.rand(100, 3)
point_cloud = pv.PolyData(points)

def compute_vector(mesh):
    origin = mesh.center
    vectors = mesh.points - origin  # 中心归一化
    return vectors / np.linalg.norm(vectors, axis=1)[:, None]  # 归一化

vectors = compute_vector(point_cloud)
print(vectors[0:5, :])  # 同样打印部分

point_cloud["vectors"] = vectors

arrows = point_cloud.glyph(orient="vectors", scale=False, factor=0.15)

plotter = pv.Plotter()
plotter.add_mesh(point_cloud, color="maroon", point_size=10, render_points_as_spheres=True)
plotter.add_mesh(arrows, color="lightblue")
plotter.show_grid()
plotter.show()















