import open3d as o3d
import numpy as np
import pyrealsense2 as rs
import cv2
from pyrealsense2 import intrinsics
import os
import glob
import matplotlib.pyplot as plt
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

def save_test(path):
    [width, height, fx, fy, ppx, ppy] = np.load(os.path.join(path, 'intrinsics_array.npy'))
    print(width, height, fx, fy, ppx, ppy)

    file_list = glob.glob(os.path.join(path, 'color*.png'))
    for f in file_list:
        print(f)
        color = cv2.imread(f)
        depth = cv2.imread(f.replace('color_', 'depth_'), cv2.IMREAD_UNCHANGED)
        img_depth = o3d.geometry.Image(depth)
        img_color = o3d.geometry.Image(color)

        rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(img_color, img_depth, convert_rgb_to_intensity=False)
        pinhole_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(int(width), int(height), fx, fy, ppx, ppy)
        pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, pinhole_camera_intrinsic)
        pcd.transform([[1, 0, 0, 0],
                       [0, -1, 0, 0],
                       [0, 0, -1, 0],
                       [0, 0, 0, 1]])
        print(f.replace('color_', '').replace('.png', '1.pcd'))
        o3d.io.write_point_cloud(f.replace('color_', '').replace('.png', '_1.pcd'),
                                 pcd, write_ascii=False, compressed=False, print_progress=True)

        o3d.io.write_point_cloud(f.replace('color_', '').replace('.png', '_2.pcd'),
                                 pcd, write_ascii=True, compressed=False, print_progress=True)

        o3d.io.write_point_cloud(f.replace('color_', '').replace('.png', '_3.pcd'),
                                 pcd, write_ascii=True, compressed=True, print_progress=True)

        o3d.io.write_point_cloud(f.replace('color_', '').replace('.png', '_4.pcd'),
                                 pcd, write_ascii=False, compressed=True, print_progress=True)


        '''
        pc_show([pcd])  # 投影数据变成了只有三层，深度估计错误，难道是存储depth时精度丢失？
        voxel_down_pcd = pcd.voxel_down_sample(voxel_size=0.02)  # 降采样尺度大一点，因为rgbd相对很稠密
        pc_show([voxel_down_pcd])
        alpha = 0.1  #
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(voxel_down_pcd, alpha)

        o3d.visualization.draw_geometries([mesh], width=800, height=800)
        mesh.compute_vertex_normals()
        o3d.visualization.draw_geometries([mesh], width=800, height=800)
        '''

def plane_detection(path):
    pcd = o3d.io.read_point_cloud(os.path.join(path, '0001_1.pcd'))
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.3, max_nn=30))
    pc_show([pcd])

    downpcd = pcd.voxel_down_sample(voxel_size=0.02)
    pc_show([downpcd])


    downpcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.3, max_nn=30))
    pc_show([downpcd], norm_flag=True)


    #'''
    downpcd.paint_uniform_color([1, 0, 0])  # rgb \in [0, 1] 归一化的， red
    pc_show([downpcd])

    aabb = downpcd.get_axis_aligned_bounding_box()
    aabb.color = (1, 0, 0)
    obb = downpcd.get_oriented_bounding_box()
    obb.color = (0, 1, 0)
    pc_show([downpcd, aabb, obb])
    
    # 生成一个最小凸多边形闭包
    # The convex hull of a point cloud is the smallest convex set that contains all points.
    hull, _ = downpcd.compute_convex_hull()
    hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull)
    hull_ls.paint_uniform_color((1, 0, 0))
    pc_show([downpcd, hull_ls])
    
    
    #'''
    #'''
    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
        labels = np.array(pcd.cluster_dbscan(eps=0.02, min_points=10, print_progress=True))
    max_label = labels.max()
    print(f"point cloud has {max_label + 1} clusters")
    colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
    colors[labels < 0] = 0
    pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
    pc_show([pcd])
    #'''
    # 错误也来自于错误的法向估计
    oboxes = pcd.detect_planar_patches(
        normal_variance_threshold_deg=60,
        coplanarity_deg=75,
        outlier_ratio=0.75,
        min_plane_edge_length=0,
        min_num_points=0,
        search_param=o3d.geometry.KDTreeSearchParamKNN(knn=20))

    print("Detected {} patches".format(len(oboxes)))

    geometries = []
    for obox in oboxes:
        mesh = o3d.geometry.TriangleMesh.create_from_oriented_bounding_box(obox, scale=[1, 1, 0.0001])
        mesh.paint_uniform_color(obox.color)
        geometries.append(mesh)
        geometries.append(obox)
    geometries.append(pcd)

    pc_show(geometries)



# step 1
# save_img_depth_intrinsics(r'../data/im_depth/', 5)
# step 2
# save_test(r'../data/seq/')
plane_detection(r'../data/seq/')
