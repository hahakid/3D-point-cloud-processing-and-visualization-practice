import open3d as o3d
import numpy as np
import pyrealsense2 as rs
import cv2
from pyrealsense2 import intrinsics
import os
import glob
import copy
import random
from tenacity import sleep

# 限制最大转角和最大位移
max_degree = np.pi/8  # [-max, max]
max_dis = 0.15  #0.05  # [-max, max]


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

def recenter(pcd):
    points = np.asarray( pcd.points )
    center = points.mean( axis=0 )
    translation_vector = -center
    points_translated = points + translation_vector
    pcd.points = o3d.utility.Vector3dVector( points_translated )
    return pcd

def ideal_ICP_test(path):
    pcd = o3d.io.read_point_cloud(path)
    coord = o3d.geometry.TriangleMesh.create_coordinate_frame(0.3)
    pcd = recenter(pcd)
    # pc_show([pcd])

    # normal
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

    T = np.eye(4)  # 空单位阵
    R = np.random.uniform(-max_degree, max_degree, size=3)
    T[:3, :3] = pcd.get_rotation_matrix_from_xyz(R)  # R
    t = np.random.uniform(-max_dis, max_dis, size=3)
    T[:3, 3] = np.asarray(t).T  # 不然旋转太远
    print(T)
    pcd2 = copy.deepcopy(pcd).transform(T)
    pcd2.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))


    #pcd2.estimate_point_covariances(search_param=o3d.geometry.KDTreeSearchParamKNN(knn = 50))
    # pcd2.paint_uniform_color([0.9, 0, 0])
    coord2 = copy.deepcopy(coord).transform(T)
    # before ICP
    pc_show([pcd, coord, pcd2, coord2])

    source = copy.deepcopy(pcd2)
    target = copy.deepcopy(pcd)

    # source.estimate_point_covariances(target, search_param=o3d.geometry.KDTreeSearchParamKNN(knn=50))
    # target.estimate_point_covariances(source, search_param=o3d.geometry.KDTreeSearchParamKNN(knn=50))
    # 静止
    target.paint_uniform_color([0, 0.9, 0])  # green
    source.paint_uniform_color([0, 0, 0.9])

    threshold = 0.02
    trans_init = np.eye(4)
    reg_p2p = o3d.pipelines.registration.registration_icp(
        source, target, threshold, trans_init,
    #o3d.pipelines.registration.TransformationEstimationPointToPoint(),  # point 2 point
        o3d.pipelines.registration.TransformationEstimationPointToPlane(),  # point 2 plane
        #o3d.pipelines.registration.TransformationEstimationForGeneralizedICP(),
        #o3d.pipelines.registration.TransformationEstimationForColoredICP(),
    o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=500))
    print(reg_p2p)
    print(reg_p2p.transformation)

    source.transform(reg_p2p.transformation)

    pc_show([pcd, pcd2, source, target])
    pc_show([pcd, target])


def ideal_colored_ICP_test(path):
    pcd = o3d.io.read_point_cloud(path)
    coord = o3d.geometry.TriangleMesh.create_coordinate_frame(0.3)
    pcd = recenter(pcd)
    # pc_show([pcd])

    # normal
    #pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

    T = np.eye(4)  # 空单位阵
    R = np.random.uniform(-max_degree, max_degree, size=3)
    T[:3, :3] = pcd.get_rotation_matrix_from_xyz(R)  # R
    t = np.random.uniform(-max_dis, max_dis, size=3)
    T[:3, 3] = np.asarray(t).T  # 不然旋转太远
    print(T)
    pcd2 = copy.deepcopy(pcd).transform(T)
    #pcd2.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

    coord2 = copy.deepcopy(coord).transform(T)
    # before ICP
    pc_show([pcd, coord, pcd2, coord2])

    source = copy.deepcopy(pcd2)
    target = copy.deepcopy(pcd)
    voxel_radius = [0.04, 0.02, 0.01]  # 分三轮，渐进迭代，每次粒度更细，迭代次数更少
    max_iter = [50, 30, 14]
    # threshold = 0.02
    current_transformation = np.eye(4)  # init T

    for scale in range(3):
        iter = max_iter[scale]
        radius = voxel_radius[scale]
        print([iter, radius, scale])
        print("3-1. Downsample with a voxel size %.2f" % radius)
        source_down = source.voxel_down_sample(radius)
        target_down = target.voxel_down_sample(radius)

        print("3-2. Estimate normal.")
        source_down.estimate_normals(
            o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 4, max_nn=30))
        target_down.estimate_normals(
            o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 4, max_nn=30))

        print("3-3. Applying colored point cloud registration")
        result_icp = o3d.pipelines.registration.registration_colored_icp(
            source_down, target_down, radius, current_transformation,
            o3d.pipelines.registration.TransformationEstimationForColoredICP(),
            o3d.pipelines.registration.ICPConvergenceCriteria(relative_fitness=1e-6,
                                                              relative_rmse=1e-6,
                                                              max_iteration=iter))
        current_transformation = result_icp.transformation
        print(result_icp)
        print(result_icp.transformation)

        source.transform(result_icp.transformation)
        # pc_show([pcd, pcd2, source, target])
        pc_show([source, target])

# ideal_ICP_test('./data/cropped_pcd/0013.pcd')

ideal_colored_ICP_test('./data/cropped_pcd/0011.pcd')



