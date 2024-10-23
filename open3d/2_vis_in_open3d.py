import pyrealsense2 as rs
import numpy as np  # 1.24.0
import cv2
import open3d as o3d
import datetime

# print and record the device parameters for settings first.
# o3d.t.io.RealSenseSensor.list_devices()

'''
[Open3D INFO] [0] Intel RealSense D435I: 239122073486
[Open3D INFO] 	color_format: [RS2_FORMAT_BGR8 | RS2_FORMAT_BGRA8 | RS2_FORMAT_RAW16 | RS2_FORMAT_RGB8 | RS2_FORMAT_RGBA8 | RS2_FORMAT_Y16 | RS2_FORMAT_YUYV]
[Open3D INFO] 	color_resolution: [1280,720 | 1920,1080 | 320,180 | 320,240 | 424,240 | 640,360 | 640,480 | 848,480 | 960,540]
[Open3D INFO] 	color_fps: [15 | 30 | 6 | 60]
[Open3D INFO] 	depth_format: [RS2_FORMAT_Z16]
[Open3D INFO] 	depth_resolution: [1280,720 | 256,144 | 424,240 | 480,270 | 640,360 | 640,480 | 848,100 | 848,480]
[Open3D INFO] 	depth_fps: [100 | 15 | 30 | 300 | 6 | 60 | 90]
[Open3D INFO] 	visual_preset: []
[Open3D INFO] Open3D only supports synchronized color and depth capture (color_fps = depth_fps).
'''
# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 6)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 6)

# Start streaming
pipeline.start(config)
align = rs.align(rs.stream.color)
# for point cloud
vis = o3d.visualization.Visualizer()
vis.create_window('Open3d-pc', width=640, height=480)
# for mesh
#vis1 = o3d.visualization.Visualizer()
#vis1.create_window('Open3d-mesh', width=640, height=480)

# updatable
pointcloud = o3d.geometry.PointCloud()
#Mesh = o3d.geometry.MeshBase()
geom_added = False

while True:
    dt0 = datetime.datetime.now()
    frames = pipeline.wait_for_frames()
    frames = align.process(frames)
    profile = frames.get_profile()  # 获取相机参数
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    if not depth_frame or not color_frame:
        continue

    # Convert images to numpy arrays
    depth_image = np.asanyarray(depth_frame.get_data()).copy()  # 16-bit
    color_image = np.asanyarray(color_frame.get_data()).copy()

    # release buffer, or lead to block
    # depth_image = depth_image.copy()
    # color_image = color_image.copy()

    o3d_color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)  # opencv bgr


    img_depth = o3d.geometry.Image(depth_image)
    img_color = o3d.geometry.Image(o3d_color_image)

    rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(img_color, img_depth, convert_rgb_to_intensity=False)

    intrinsics = profile.as_video_stream_profile().get_intrinsics()  # camera intrinsics

    pinhole_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(intrinsics.width, intrinsics.height, intrinsics.fx, intrinsics.fy, intrinsics.ppx, intrinsics.ppy)
    # print(intrinsics.width, intrinsics.height, intrinsics.fx, intrinsics.fy, intrinsics.ppx, intrinsics.ppy)
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, pinhole_camera_intrinsic)

    # 旋转，因为相机坐标(0,0)=up-left
    pcd.transform([[1, 0,  0, 0],
                   [0, -1, 0, 0],
                   [0, 0, -1, 0],
                   [0, 0,  0, 1]])
    voxel_down_pcd = pcd.voxel_down_sample(voxel_size=0.05)

    #alpha = 0.1  #
    #mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(voxel_down_pcd, alpha)
    #mesh.compute_vertex_normals()

    # update pointcloud for vis
    pointcloud.points = pcd.points
    pointcloud.colors = pcd.colors

    if geom_added == False:
        vis.add_geometry(pointcloud)

        geom_added = True

    vis.update_geometry(pointcloud)
    vis.poll_events()
    vis.update_renderer()

    color_image = cv2.resize(color_image, dsize=None, fx=0.5, fy=0.5)
    cv2.imshow('Opencv', color_image)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    # cal FPS
    process_time = datetime.datetime.now() - dt0
    print("FPS: " + str(1 / process_time.total_seconds()))

# o3d.io.write_triangle_mesh("output2.ply", mesh)
pipeline.stop()
cv2.destroyAllWindows()
vis.destroy_window()
del vis