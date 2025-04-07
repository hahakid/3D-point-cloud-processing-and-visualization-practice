import pyvista as pv
from pyvista import examples
import numpy as np
import meshio
import open3d as o3d
from joblib import Parallel, delayed
import time

'''
# from github source
saddle = examples.download_saddle_surface()
print(saddle)
saddle.plot()

frog = examples.download_frog()
print(frog)
frog.plot(volume=True)

# read from local
# file format = [vtk, meshio]
local = pv.read('../data/bunny.ply')
print(local)
local.plot()
'''

# show bin in open3d vs. pyvista
def pc_show(pc, norm_flag=False):
    vis = o3d.visualization.Visualizer()
    vis.create_window(width=800, height=800)
    opt = vis.get_render_option()
    opt.point_size = 2
    opt.point_show_normal = norm_flag
    for p in pc:
        vis.add_geometry(p)
    vis.run()
    vis.destroy_window()

def npy2pcd(pcd_np):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pcd_np[:, :3])
    return pcd

def load_pc(bin_file_path):
    """
    load pointcloud file (velodyne format)
    :param bin_file_path: 点云文件路径
    :return: 点云数据
    """
    pc = np.fromfile(bin_file_path, dtype=np.float32).reshape((-1, 4))
    return pc[:, :3]

#def load_pc_parallel(bin_file_path):
#    pc = np.fromfile(bin_file_path, dtype=np.float32).reshape((-1, 4))
#    return pc[:, :3]
#t1 = time.time()
lidar = load_pc('../data/000210.bin')
#t2 = time.time()

#def parallel_process():
#    lidar = Parallel(n_jobs=-1)(delayed(load_pc_parallel)('../data/000210.bin') for _ in range(1))[0]
#    return lidar
#lidar = parallel_process()

#t3 = time.time()
#print(t3 - t2, t2 - t1)

cells = [("vertex", np.arange(len(lidar)).reshape(-1, 1))]
z_values = lidar[:, 2]
z_normalized = (z_values - z_values.min()) / (z_values.max() - z_values.min())
color = np.zeros((len(lidar), 3))
color[:, 0] = z_normalized
color[:, 2] = 1 - z_normalized

mesh = meshio.Mesh(points=lidar, cells=cells, point_data={"colors": color})
mesh.write("../data/output.vtk")

# show in pyvista
points = pv.read('../data/output.vtk')
print(points)
points.plot()
#points.plot(scalars='colors', rgb=True)

# show in open3d
pcd = npy2pcd(lidar)
pc_show([pcd])


