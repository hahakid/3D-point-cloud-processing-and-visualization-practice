import pyrealsense2 as rs
import numpy as np
import cv2
import argparse
import os.path

# Create object for parsing command-line options
parser = argparse.ArgumentParser(description="Read recorded bag file and display depth stream in jet colormap.\
                                Remember to change the stream fps and format to match the recorded.")
# Add argument which takes path to a bag file as an input
parser.add_argument("-i", "--input", type=str, help="Path to the bag file")
# Parse the command line arguments to an object
args = parser.parse_args()
# Safety if no parameter have been given
if not args.input:
    print("No input paramater have been given.")
    print("For help type --help")
    exit()
# Check if the given file have bag extension
if os.path.splitext(args.input)[1] != ".bag":
    print("The given file is not of correct file format.")
    print("Only .bag files are accepted")
    exit()

# Create pipeline
pipeline = rs.pipeline()

# Create a config object
config = rs.config()

# define saved data
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
# enable recording to a bag file
rs.config.enable_record_to_file(config, args.input)

# Start streaming from file
pipeline.start(config)

# Streaming loop
try:
    print('recoding ... press ctrl+C/ESC to stop.')
    while True:
        # Get frameset of depth
        frames = pipeline.wait_for_frames()
        # vis only
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        cv2.imshow("", color_image)
        k = cv2.waitKey(1)
        if k == 27:
            break

except KeyboardInterrupt:
    print("Stop recoding.")

finally:
    pipeline.stop()
