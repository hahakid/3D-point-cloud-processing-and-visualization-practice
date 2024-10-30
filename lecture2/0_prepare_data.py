import open3d as o3d
import numpy as np
import pyrealsense2 as rs
import cv2
from pyrealsense2 import intrinsics
import os
import glob

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

def save_img_depth_intrinsics(path='../data/im_depth/'):
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    pipeline.start(config)
    align = rs.align(rs.stream.color)
    count = 0
    while True:  # skip first X frame for low exposure
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
            k = cv2.waitKey(1)
            if k == ord("s"):
                cv2.imwrite(path + "/color_%s.png" % str(count).zfill(4), color_image)
                cv2.imwrite(path + "/depth_%s.png" % str(count).zfill(4), depth_image)
                print("frame %s saved"%str(count).zfill(4))
                print(path + "/depth_%s.png")
            if k in (27, ord("q")):
                break
        count += 1
    # intrinsics is fixed
    frames = pipeline.wait_for_frames()
    frames = align.process(frames)
    profile = frames.get_profile()
    intrinsics = profile.as_video_stream_profile().get_intrinsics()
    intrinsics_array = [intrinsics.width, intrinsics.height, intrinsics.fx, intrinsics.fy, intrinsics.ppx,
                        intrinsics.ppy]
    np.save(path + "intrinsics_array.npy", intrinsics_array)

    cv2.destroyAllWindows()

def generate_pcd(path):
    [width, height, fx, fy, ppx, ppy] = np.load(os.path.join(path, 'intrinsics_array.npy'))
    print(width, height, fx, fy, ppx, ppy)
    file_list = glob.glob(os.path.join(path, 'color*.png'))
    for i, f in enumerate(file_list):
        color = cv2.imread(f)
        color = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)
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
        pc_show([pcd])
        o3d.io.write_point_cloud(os.path.join(path, 'pcd/'+str(i).zfill(4) + '.pcd'), pcd, write_ascii=False, compressed=True)


# step 1
# save frame with key=s
# save_img_depth_intrinsics(r'./data/')
# step 2
# generate_pcd('./data')

# show final pcd
pc = './data/GT.pcd'
pcd_gt = o3d.io.read_point_cloud(pc)
pc_show([pcd_gt])