import open3d as o3d
import numpy as np
import pyrealsense2 as rs
import cv2
from pyrealsense2 import intrinsics
import os
import glob
import copy

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


# single_frame_T_test('./data/cropped_pcd/0013.pcd')
# single_frame_R_test('./data/cropped_pcd/0013.pcd')
# single_frame_S_test('./data/cropped_pcd/0013.pcd')
# rigid_body_rotation('./data/cropped_pcd/0013.pcd')





