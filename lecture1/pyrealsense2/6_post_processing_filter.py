import time

import numpy as np
import matplotlib.pyplot as plt
import pyrealsense2 as rs
from matplotlib.animation import FuncAnimation

pipe = rs.pipeline()
cfg = rs.config()
cfg.enable_device_from_file("../data/20241020_171946.bag")  # 复用上一步采集的bag
profile = pipe.start(cfg)

# Skip 5 first frames to give the Auto-Exposure time to adjust
for x in range(5):
    pipe.wait_for_frames()

# Store next frameset for later processing:
frameset = pipe.wait_for_frames()
depth_frame = frameset.get_depth_frame()

# Cleanup:
pipe.stop()
print("Frames Captured")

colorizer = rs.colorizer()
colorized_depth = np.asanyarray(colorizer.colorize(depth_frame).get_data())
plt.subplot(1, 3, 1)
plt.title('raw')
plt.rcParams["axes.grid"] = False
# plt.rcParams['figure.figsize'] = [16, 4]
plt.imshow(colorized_depth)


# Decimation
# z-accuracy is related to original spacial resolution.
# If you are satisfied with lower spatial resolution,
# the Decimation Filter will reduce spatial resolution
# preserving z-accuracy and performing some rudamentary hole-filling.
plt.subplot(1, 3, 2)
plt.title('decimation_filter')
decimation = rs.decimation_filter()
decimation.set_option(rs.option.filter_magnitude, 4)
decimated_depth = decimation.process(depth_frame)
colorized_depth = np.asanyarray(colorizer.colorize(decimated_depth).get_data())
plt.imshow(colorized_depth)


# Spatial Filter is a fast implementation of Domain-Transform Edge Preserving Smoothing
plt.subplot(1, 3, 3)
plt.title('Spatial Filter')
spatial = rs.spatial_filter()

# 提升 smooth_alpha and smooth_delta
spatial.set_option(rs.option.filter_magnitude, 5)
spatial.set_option(rs.option.filter_smooth_alpha, 1)
spatial.set_option(rs.option.filter_smooth_delta, 50)

# hole filling
spatial.set_option(rs.option.holes_fill, 5)

filtered_depth = spatial.process(depth_frame)
colorized_depth = np.asanyarray(colorizer.colorize(filtered_depth).get_data())
plt.imshow(colorized_depth)

plt.show()



# Temporal Filter, only used for multi-frame

profile = pipe.start(cfg)

frames = []
for x in range(10, 100, 1):
    frameset = pipe.wait_for_frames()
    frames.append(frameset.get_depth_frame())

pipe.stop()
print("Frames Captured")

colorizer = rs.colorizer()
colorized_depth = np.asanyarray(colorizer.colorize(depth_frame).get_data())
raw = colorized_depth

temporal = rs.temporal_filter()
hole_filling = rs.hole_filling_filter()

'''
for x in range(10):
    temp_filtered = temporal.process(frames[x])
colorized_depth = np.asanyarray(colorizer.colorize(temp_filtered).get_data())
plt.subplot(1, 3, 2)
plt.title('Temporal Filter')
plt.imshow(colorized_depth)

# hole fill

filled_depth = hole_filling.process(depth_frame)
colorized_depth = np.asanyarray(colorizer.colorize(filled_depth).get_data())
plt.subplot(1, 3, 3)
plt.title('Temporal Filter with hole fill')
plt.imshow(colorized_depth)
plt.show()
'''

depth_to_disparity = rs.disparity_transform(True)
disparity_to_depth = rs.disparity_transform(False)


d1, d2, d3 = [], [], []
fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

#ax1.title('raw')
#ax2.title('Temporal Filter')
#ax3.title('Temporal Filter with hole fill')
colorized_depth = np.asanyarray(colorizer.colorize(frames[0]).get_data())
im1 = ax1.imshow(colorized_depth)
im2 = ax2.imshow(colorized_depth)
im3 = ax3.imshow(colorized_depth)

plt.ion()
plt.show()

for x, _ in enumerate(frames):
    frame = frames[x]
    frame = decimation.process(frame)
    frame = depth_to_disparity.process(frame)
    frame = spatial.process(frame)
    frame = temporal.process(frame)
    frame = disparity_to_depth.process(frame)
    # aaa =np.asarray(frame)
    im1.set_data(colorized_depth)
    im2.set_data(np.asarray(frame.data))
    frame = hole_filling.process(frame)
    im3.set_data(np.asarray(frame.data))

    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.2)





