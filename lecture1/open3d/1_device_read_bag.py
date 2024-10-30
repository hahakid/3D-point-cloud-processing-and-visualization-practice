import open3d as o3d
import numpy as np
import pyrealsense2 as rs
import matplotlib.pyplot as plt
import cv2

# 获取连接设备信息
o3d.t.io.RealSenseSensor.list_devices()

# bag read and play
def realsense_bag_test(path):
    bag_reader = o3d.t.io.RSBagReader()
    bag_reader.open(path)
    count = 0
    while not bag_reader.is_eof():
        print(count)
        im_rgbd = bag_reader.next_frame()
        if not im_rgbd.color or not im_rgbd.depth:
            continue

        rgb_im = np.asarray(im_rgbd.color)
        rgb_im = cv2.cvtColor(rgb_im, cv2.COLOR_BGR2RGB)
        depth_im = np.asarray(im_rgbd.depth)

        if 10 < count < 20:
            plt.subplot(1, 2, 1)
            plt.title('rgb')
            plt.imshow(rgb_im)
            plt.subplot(1, 2, 2)
            plt.title('depth')
            plt.imshow(depth_im)
            plt.show()

        count += 1
    bag_reader.close()

realsense_bag_test(r'../data/d415.bag')
