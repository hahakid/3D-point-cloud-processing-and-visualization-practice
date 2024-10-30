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

def single_frame_T_test(path):
    pcd = o3d.io.read_point_cloud(path)
    pcd = recenter(pcd)
    pc_show([pcd])
    # pcd_tx = copy.copy(pcd).translate( (0.1, 0, 0) )
    pcd_tx1 = copy.deepcopy( pcd ).translate( (0.1, 0, 0) )  # meter
    pcd_tx1.paint_uniform_color([0.7, 0, 0])  # as red

    pcd_tx2 = copy.deepcopy( pcd ).translate( (0.2, 0, 0) )  # meter
    pcd_tx2.paint_uniform_color( [0.8, 0, 0] )  # as red

    pcd_tx3 = copy.deepcopy( pcd ).translate( (0.3, 0, 0) )  # meter
    pcd_tx3.paint_uniform_color( [0.9, 0, 0] )  # as red

    # pcd_ty = copy.copy(pcd).translate( (0, 0.1, 0) )
    #pcd_ty = copy.deepcopy( pcd ).translate( (0, 0.1, 0) )
    #pcd_ty.paint_uniform_color( [0, 1, 0] )

    #pcd_tz = copy.deepcopy( pcd ).translate( (0, 0, 0.1) )
    #pcd_tz = copy.copy(pcd).translate( (0, 0, 0.1) )
    #pcd_tz.paint_uniform_color( [0, 0, 1] )
    pc_show( [pcd, pcd_tx1, pcd_tx2, pcd_tx3] )


def single_frame_R_test(path):
    pcd = o3d.io.read_point_cloud(path)
    pcd = recenter(pcd)
    pc_show([pcd])

    R1 = pcd.get_rotation_matrix_from_xyz((1 * np.pi / 8, 0, 0))  # 22.5 degree
    pcd_rx1 = copy.deepcopy(pcd).paint_uniform_color([0, 0.5, 0])  # as green
    pcd_rx1.rotate(R1, center=(0, 0, 0))

    R2 = pcd.get_rotation_matrix_from_xyz((2 * np.pi / 8, 0, 0))  # 45 degree
    pcd_rx2 = copy.deepcopy(pcd).paint_uniform_color([0, 0.7, 0])  # as green
    pcd_rx2.rotate(R2, center=(0, 0, 0))

    R3 = pcd.get_rotation_matrix_from_xyz((3 * np.pi / 8, 0, 0))  # 67.5 degree
    pcd_rx3 = copy.deepcopy(pcd).paint_uniform_color([0, 0.9, 0])  # as green
    pcd_rx3.rotate(R3, center=(0, 0, 0))

    pc_show([pcd, pcd_rx1, pcd_rx2, pcd_rx3])


def single_frame_S_test(path):
    pcd = o3d.io.read_point_cloud(path)
    pcd = recenter(pcd)
    pc_show([pcd])

    pcd_s1 = copy.deepcopy(pcd).translate((0.6, 0, 0))  # rate=0.6
    pcd_s1.scale(0.3, center=pcd_s1.get_center())  # as green
    pcd_s1.paint_uniform_color([0, 0, 0.5])

    pcd_s2 = copy.deepcopy(pcd).translate( (0.4, 0, 0)) # rate=0.4
    pcd_s2.scale( 0.5, center=pcd_s2.get_center() )  # as green
    pcd_s2.paint_uniform_color([0, 0, 0.7])

    pcd_s3 = copy.deepcopy(pcd).translate( (0.2, 0, 0))  # rate=0.2
    pcd_s3.scale( 0.7, center=pcd_s3.get_center() )  # as green
    pcd_s3.paint_uniform_color([0, 0, 0.9])

    pc_show([pcd, pcd_s1, pcd_s2, pcd_s3])

def rigid_body_rotation(path):
    pcd = o3d.io.read_point_cloud(path)
    coord = o3d.geometry.TriangleMesh.create_coordinate_frame(0.3)
    pcd = recenter(pcd)
    # pc_show([pcd])

    T = np.eye(4)  # 空单位阵
    T[:3, :3] = pcd.get_rotation_matrix_from_xyz((np.pi/8, 0, 0))  # R
    T[:3, 3] = np.asarray([0.5, 0, 0]).T  # T, 最后一个固定赋值1，用来构建齐次矩阵。T的最后一行[0,0,0,1]
    print(T)
    pcd_rbr = copy.deepcopy(pcd).transform(T)
    coord_rbr = copy.deepcopy(coord).transform(T)
    pc_show([pcd, coord, pcd_rbr, coord_rbr])

def seq(path, save=False):
    pcd = o3d.io.read_point_cloud(path)
    coord = o3d.geometry.TriangleMesh.create_coordinate_frame(0.3)
    vis = o3d.visualization.Visualizer()
    vis.create_window('rigid body', width=640, height=480)
    vis.add_geometry(pcd)
    vis.add_geometry(coord)

    for i in range(100):
        T = np.eye(4)
        T[:3, :3] = pcd.get_rotation_matrix_from_xyz((np.pi / 16 * i, 0, 0))  # R
        T[:3, 3] = np.asarray([0.1 * i, 0, 0]).T  # T, 最后一个固定赋值1，用来构建齐次矩阵。T的最后一行[0,0,0,1]

        pcd_rbr = copy.copy(pcd)
        coord_rbr = copy.copy(coord)

        pcd_rbr.transform(T)
        coord_rbr.transform(T)
        #pc_show([pcd, coord, pcd_rbr, coord_rbr])

        vis.add_geometry(pcd_rbr)
        vis.add_geometry(coord_rbr)
        vis.update_geometry(pcd_rbr)
        vis.update_geometry(coord_rbr)
        if save:
            vis.capture_screen_image("./temp_%04d.jpg" % i)
        vis.poll_events()
        vis.update_renderer()

    vis.destroy_window()
    del vis

def seq1(path, save=False):
    point_cloud_combined = o3d.geometry.PointCloud()

    pcd = o3d.io.read_point_cloud(path)
    coord = o3d.geometry.TriangleMesh.create_coordinate_frame(0.3)
    # 一次性绕， Green
    T1 = np.eye(4)
    T1[:3, :3] = pcd.get_rotation_matrix_from_xyz((np.pi / 6, np.pi / 6, np.pi / 6))  # R
    T1[:, 3] = np.asarray([0, 0, 0, 1.0]).T  # T, 最后一个固定赋值1，用来构建齐次矩阵。T的最后一行[0,0,0,1]

    pcd_rbr1 = copy.copy(pcd)
    coord_rbr1 = copy.copy(coord)

    pcd_rbr1.transform(T1)
    pcd_rbr1.paint_uniform_color([0, 0, 0.9])
    coord_rbr1.transform(T1)
    # 依次绕， blue
    base_matrix = np.asarray([[np.pi / 6, 0, 0],
                              [0, np.pi / 6, 0],
                              [0, 0, np.pi / 6]])
    arr = np.asarray([0, 1, 2])
    np.random.shuffle(arr)
    print(arr)
    pcd_rbr2 = copy.copy(pcd)
    pcd_rbr2.paint_uniform_color([0, 0.8, 0])
    #coord_rbr2 = copy.copy(coord)

    for i in arr:
        temp_T = np.eye(4)
        deg = base_matrix[i] * i
        temp_T[:3, :3] = pcd.get_rotation_matrix_from_xyz(deg)  # R
        temp_T[:3, 3] = np.asarray([0, 0, 0]).T
        pcd_rbr2.transform(temp_T)
        #coord_rbr2.transform(temp_T)
    pc_show([pcd, pcd_rbr1, pcd_rbr2])
    point_cloud_combined += pcd
    point_cloud_combined += pcd_rbr1
    point_cloud_combined += pcd_rbr2
    o3d.io.write_point_cloud("test1.pcd", point_cloud_combined)


def pc_show_seq(pcd, coord, arr, base_matrix, save):
    seq_arr = ['x', 'y', 'z']
    vis = o3d.visualization.Visualizer()
    vis.create_window('rigid body', width=640, height=480)
    vis.add_geometry(pcd)
    vis.add_geometry(coord)
    point_cloud_combined = o3d.geometry.PointCloud()
    point_cloud_combined += pcd
    for i in arr:

        # point_cloud_combined += coord
        T = np.eye(4)
        deg = base_matrix[i] * i  # rotate order

        T[:3, :3] = pcd.get_rotation_matrix_from_xyz(deg)  # R
        T[:3, 3] = np.asarray([0.1 * i, 0, 0]).T  # T, 最后一个固定赋值1，用来构建齐次矩阵。T的最后一行[0,0,0,1]

        pcd_rbr = copy.copy(pcd)
        coord_rbr = copy.copy(coord)

        pcd_rbr.transform(T)
        coord_rbr.transform(T)
        # pc_show([pcd, coord, pcd_rbr, coord_rbr])
        point_cloud_combined += pcd_rbr
        vis.add_geometry(pcd_rbr)
        vis.add_geometry(coord_rbr)
        vis.update_geometry(pcd_rbr)
        vis.update_geometry(coord_rbr)
        if save:
            vis.capture_screen_image("./temp_%04d.jpg" % i)
        # sleep(1)
        vis.poll_events()
        vis.update_renderer()

    vis.destroy_window()
    del vis
    o3d.io.write_point_cloud("order-%s-%s-%s.pcd"%(seq_arr[arr[0]], seq_arr[arr[1]], seq_arr[arr[2]]), point_cloud_combined)


def seq(path):
    pcd = o3d.io.read_point_cloud(path)
    coord = o3d.geometry.TriangleMesh.create_coordinate_frame(0.3)

    seq_arr = ['x', 'y', 'z']
    base_matrix = np.asarray([[np.pi / 16, 0, 0],
                   [0, np.pi / 16, 0],
                   [0, 0, np.pi / 16]])

    arr = np.asarray([0, 1, 2])  # np.random.randint(0, 3, size=3)
    print('\nOrder1:', seq_arr[arr[0]], seq_arr[arr[1]], seq_arr[arr[2]])
    save = False
    pc_show_seq(pcd, coord, arr, base_matrix, save)

    arr1 = np.random.permutation(arr)
    while np.array_equal(arr1, arr):
        arr1 = np.random.permutation(arr)

    print('\nOrder1:', seq_arr[arr1[0]], seq_arr[arr1[1]], seq_arr[arr1[2]])
    pc_show_seq(pcd, coord, arr1, base_matrix, save)




# single_frame_T_test('./data/cropped_pcd/0013.pcd')
# single_frame_R_test('./data/cropped_pcd/0013.pcd')
# single_frame_S_test('./data/cropped_pcd/0013.pcd')
# rigid_body_rotation('./data/cropped_pcd/0013.pcd')

# seq('./data/cropped_pcd/0013.pcd')  # 3次旋转，顺序随机
seq1('./data/cropped_pcd/0013.pcd')  # 1次旋转 vs. 3次旋转


