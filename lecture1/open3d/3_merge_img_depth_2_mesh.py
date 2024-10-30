import open3d as o3d
import numpy as np
import pyrealsense2 as rs
import cv2
from pyrealsense2 import intrinsics
import os


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

def save_img_depth_intrinsics(path='../data/im_depth/', frame_number=1):
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 15)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 15)
    pipeline.start(config)
    align = rs.align(rs.stream.color)
    count = 0
    while count <= 50 + frame_number:  # skip first X frame for low exposure
    #while True:  # skip first X frame for low exposure
        frames = pipeline.wait_for_frames()
        if count > 50:
            frames = pipeline.wait_for_frames()
            frames = align.process(frames)
            # profile = frames.get_profile()  # 获取相机参数
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            depth_image = np.asanyarray(depth_frame.get_data()).copy()
            color_image = np.asanyarray(color_frame.get_data()).copy()
            # color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)  # opencv bgr
            cv2.imshow("", color_image)
            cv2.waitKey(1)
            cv2.imwrite(path + "/color_%s.png" % str(count).zfill(4), color_image)
            cv2.imwrite(path + "/depth_%s.png" % str(count).zfill(4), depth_image)

        count += 1
    # intrinsics is fixed
    frames = pipeline.wait_for_frames()
    frames = align.process(frames)
    profile = frames.get_profile()
    intrinsics = profile.as_video_stream_profile().get_intrinsics()
    intrinsics_array = [intrinsics.width, intrinsics.height, intrinsics.fx, intrinsics.fy, intrinsics.ppx,
                        intrinsics.ppy]
    np.save(path + "intrinsics_array.npy", intrinsics_array)


def mesh_test(path):
    [width, height, fx, fy, ppx, ppy] = np.load(os.path.join(path, 'intrinsics_array.npy'))
    # print(width, height, fx, fy, ppx, ppy)
    color = cv2.imread(os.path.join(path, 'color_0051.png'))
    depth = cv2.imread(os.path.join(path, 'depth_0051.png'), cv2.IMREAD_UNCHANGED)
    img_depth = o3d.geometry.Image(depth)
    img_color = o3d.geometry.Image(color)

    rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(img_color, img_depth, convert_rgb_to_intensity=False)
    pinhole_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(int(width), int(height), fx, fy, ppx, ppy)
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, pinhole_camera_intrinsic)
    pcd.transform([[1, 0, 0, 0],
                   [0, -1, 0, 0],
                   [0, 0, -1, 0],
                   [0, 0, 0, 1]])

    pc_show([pcd])  # 投影数据变成了只有三层，深度估计错误，难道是存储depth时精度丢失？
    voxel_down_pcd = pcd.voxel_down_sample(voxel_size=0.02)  # 降采样尺度大一点，因为rgbd相对很稠密
    pc_show([voxel_down_pcd])
    alpha = 0.1  #
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(voxel_down_pcd, alpha)

    o3d.visualization.draw_geometries([mesh], width=800, height=800)
    mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh], width=800, height=800)

# step 1
# save_img_depth_intrinsics(r'../data/im_depth/', 5)
save_img_depth_intrinsics(r'../data/seq/', 1)
# step 2
mesh_test(r'../data/seq/')

