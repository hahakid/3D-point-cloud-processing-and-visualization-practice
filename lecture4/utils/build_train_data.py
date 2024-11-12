# encoding=utf-8


import os
import shutil
import numpy as np

def load_point_list(path):
    point_list = sorted(os.listdir(os.path.join(path, "velodyne")))
    for idx in range(len(point_list)):
        point_list[idx] = path+ "/" + "velodyne/" +point_list[idx]

    return point_list






if __name__ == "__main__":




    target_path = "/media/z/Share/study/dataset/train_data"
    source_path = "/media/z/Share/study/dataset/R1kitti32"

    print("构建中,请等待...")

    if os.path.exists(target_path):
        shutil.rmtree(target_path)

    os.mkdir(target_path)

    point_list = load_point_list(source_path)

    train_list = []
    test_list = []

    i = 0
    for file_path in point_list:
        if i % 10 == 0:
            test_list.append(file_path)
        else:
            train_list.append(file_path)
        i+=1


    # calib
    os.mkdir(target_path + "/calib")
    os.mkdir(target_path + "/calib/00")
    os.mkdir(target_path + "/calib/01")

    shutil.copy(source_path + "/calib.txt", target_path + "/calib/00/calib.txt")
    shutil.copy(source_path + "/calib.txt", target_path + "/calib/01/calib.txt")


    #pose
    os.mkdir(target_path + "/poses/")
    train_pose = []
    test_pose = []
    with open(os.path.join(source_path, "poses.txt"), "r") as file:
        lines = file.readlines()

        i = 0
        for line in lines:
            if i % 10 == 0:
                test_pose.append(line.strip())
            else:
                train_pose.append(line.strip())
            i += 1




    np.savetxt(target_path + "/poses/" + "00.txt", train_pose, fmt="%s")
    np.savetxt(target_path + "/poses/" + "01.txt", test_pose, fmt="%s")



    #bin
    # trainset:
    os.mkdir(target_path + "/velodyne/")
    os.mkdir(target_path+"/velodyne/00")
    for i in range(len(train_list)):
        shutil.copy(train_list[i], target_path+"/velodyne/00/"+str(i).zfill(6) + ".bin")

    # testset:
    os.mkdir(target_path + "/velodyne/01")
    for i in range(len(test_list)):
        shutil.copy(test_list[i], target_path + "/velodyne/01/" + str(i).zfill(6) + ".bin")



    #label
    # trainset:
    os.mkdir(target_path + "/labels/")
    os.mkdir(target_path+"/labels/00")
    for i in range(len(train_list)):
        shutil.copy(train_list[i].replace(".bin",".label").replace("velodyne", "labels"), target_path+"/labels/00/"+str(i).zfill(6) + ".label")

    # testset:
    os.mkdir(target_path + "/labels/01")
    for i in range(len(test_list)):
        shutil.copy(test_list[i].replace(".bin",".label").replace("velodyne", "labels"), target_path + "/labels/01/" + str(i).zfill(6) + ".label")




    print("构建已完成，输出路径：",target_path)



