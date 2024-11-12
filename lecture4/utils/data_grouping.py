
import os
import shutil

import numpy as np


def load_point_list(config):
    point_list = sorted(os.listdir(os.path.join(config, "velodyne")))
    for idx in range(len(point_list)):
        point_list[idx] = config + "/" + "velodyne/" +point_list[idx]

    return point_list


def load_label_list(config):
    label_list = sorted(os.listdir(os.path.join(config, "labels")))
    for idx in range(len(label_list)):
        label_list[idx] = config + "/" + "labels/" +label_list[idx]

    return label_list


def convert_crlf_to_lf(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'rb') as f:
                content = f.read()
            # 替换CRLF为LF
            content = content.replace(b'\r\n', b'\n')
            # 写入文件
            with open(file_path, 'wb') as f:
                f.write(content)
            #print(f"Converted {filename} to LF format.")




if __name__ == "__main__":
    data_path = "C:/Users/Z/Desktop/work/课程/三维点云/lesson4/R1kitti32"

    target_path = r"C:\Users\Z\Desktop\work\课程\三维点云\lesson4\dataset"

    DATASIZE = 133



    point_list = load_point_list(data_path)
    label_list = load_label_list(data_path)

    poses = np.loadtxt(data_path+"/poses.txt")
    #with open(os.path.join(data_path, "poses.txt"), "r") as file:
    #file = open(os.path.join(data_path, "poses.txt"), "r")
    #lines = file.readlines()



    for i in range(10):
        now_path = os.path.join(target_path, "group" + str(i))


        #
        os.mkdir(os.path.join(now_path))
        os.mkdir(os.path.join(now_path, "velodyne"))
        #os.mkdir(os.path.join(now_path, "labels"))

        pose = []

        for iter in range(DATASIZE):


            #velodyne
            shutil.copy(point_list[i*DATASIZE + iter], os.path.join(now_path, "velodyne", str(iter).zfill(6)+".bin"))

            #label
            #shutil.copy(label_list[i * DATASIZE + iter], os.path.join(now_path, "labels", str(i).zfill(6) + ".txt"))

            #pose
            pose.append(poses[i * DATASIZE + iter])
            #print(pose)

        #pose = np.array(pose, dtype=np.float32)
        np.savetxt(now_path+"/poses.txt", pose, fmt="%s")
        convert_crlf_to_lf(now_path)

        shutil.copy(os.path.join(data_path, "calib.txt"), now_path+"/calib.txt")









    print()

