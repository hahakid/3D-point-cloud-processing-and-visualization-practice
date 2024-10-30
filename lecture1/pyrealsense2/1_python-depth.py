import pyrealsense2 as rs

try:
    # Create a context object. This object owns the handles to all connected realsense devices
    pipeline = rs.pipeline()

    # Configure streams
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    # Start streaming
    pipeline.start(config)

    while True:
        # This call waits until a new coherent set of frames is available on a device
        # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()
        if not depth:
            continue

        # Print a simple text-based representation of the image, by breaking it into 10x20 pixel regions and approximating the coverage of pixels within one meter
        coverage = [0] * 64  # 列分成10块，每块64像素，累加统计
        str_img = []
        for y in range(480):  # size = 480*640
            for x in range(640):
                dist = depth.get_distance(x, y)  # get depth
                if 0 < dist < 1:  # filtering background >1 太远的
                    coverage[x//10] += 1  # index 注意修改, 累加
            
            if y % 20 == 19:  # 每行分成20块，每块24像素，基于coverage统计，进行可视化
                line = ""
                for c in coverage:
                    line += " .:!@#$%…&"[c // 25]  # 按c(最大为10)的密度映射
                str_img.append(line)
                coverage = [0] * 64  # init
                print(line[::-1])  # 逆序

        for l in str_img:
            print(''.join(l))
    exit(0)

except Exception as e:
    print(e)
    pass
