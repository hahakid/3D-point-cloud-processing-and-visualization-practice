
import os
import numpy as np
import yaml
import open3d as o3d

# data组织形式: 需要data数据集


# 工具函数：
# compute_label_kinds(label_list)  参数导入一组label_list绝对地址标签

# continus_project_show(config,0, 7825, point_list, label_list, pose_list, filter=False)
#   参数：     config   yaml类数据
#             start    起始帧
#             end      结束帧
#             point_list    点云绝对路径
#             label_list    标签绝对路径
#             pose_list     位姿绝对路径




def load_point_list(config):
    point_list = sorted(os.listdir(os.path.join(config["root_path"], "velodyne/01")))
    for idx in range(len(point_list)):
        point_list[idx] = config["root_path"]+ "/" + "velodyne/01/" +point_list[idx]

    return point_list


def load_label_list(config):
    path = ""
    if config["show_kind"] == "ground_truth":
        path = config["ground_truth_label_path"]
    elif config["show_kind"] == "predict":
        path = config["predict_label_path"]



    label_list = sorted(os.listdir(path))


    for idx in range(len(label_list)):
        label_list[idx] = path + "/"  +label_list[idx]

    return label_list

def load_pointcloud(filename):
    scan = np.fromfile(filename, dtype=np.float32)
    scan = scan.reshape((-1, 4))
    return scan


def load_label(config, filename):
    remap = config["learning_map"]


    label = np.fromfile(filename, dtype=np.uint32)
    label = label.reshape((-1))
    # upper_half = label >> 16  # get upper half for instances
    lower_half = label & 0xFFFF  # get lower half for semantics
    lower_half = remap[lower_half]
    return lower_half

def load_label_unremap(config, filename):
    remap = config["learning_map"]


    label = np.fromfile(filename, dtype=np.uint32)
    label = label.reshape((-1))
    # upper_half = label >> 16  # get upper half for instances
    lower_half = label & 0xFFFF  # get lower half for semantics
    #lower_half = remap[lower_half]
    return lower_half

def load_pcl(config, idx, label_list, point_list):
    pc = load_pointcloud(point_list[idx])

    if config["show_kind"] == "ground_truth":
        lb = load_label(config, label_list[idx])
    elif config["show_kind"] == "predict":
        lb = np.load(label_list[idx])


    lb = lb.reshape((-1, 1), order='F')
    assert len(pc[:, 0]) == len(lb)
    return np.hstack((pc,lb))


def parase_config(_path):
    with open(_path, 'r') as file:
        # 加载YAML文件内容
        return yaml.safe_load(file)


def compute_label_kinds(label_list):
    all_label = np.array([0]).astype(dtype=np.uint32)

    num_point = 0

    for l_path in label_list:
        label = load_label_unremap(config, l_path)
        unique_arr, indices, counts = np.unique(label, return_index=True, return_counts=True)
        num_point += np.sum(counts)

        # all_label =
        all_label = np.concatenate((all_label, unique_arr))
        all_label = np.unique(all_label)

        print(l_path)

    print(num_point, all_label)
    return num_point,all_label





def load_learning_map(config):
    remapdict = config["learning_map"]

    max_key = max(remapdict.keys())

    label_map = np.zeros(max_key+1, dtype=np.uint32)
    label_map[list(remapdict.keys())] = list(remapdict.values())


    return label_map

def load_color_map(config):
    remapdict = config["color_map"]

    max_key = max(remapdict.keys())

    color_map = np.zeros((max_key+1, 3))
    color_map[list(remapdict.keys())] = list(remapdict.values())
    color_map = color_map / 255.0

    return color_map


def show_pcl(config, pcl):

    colormap = config["color_map"]
    color = []
    labels = pcl[:, 4]
    for l in labels:
        color.append(colormap[int(l)])
    color = np.asarray(color)
    colored_pointcloud = o3d.geometry.PointCloud()
    colored_pointcloud.points = o3d.utility.Vector3dVector(pcl[:, 0:3])
    colored_pointcloud.colors = o3d.utility.Vector3dVector(color)


    ##  baocun
    #o3d.io.write_point_cloud("00.ply", colored_pointcloud)

    vis = o3d.visualization.Visualizer()
    vis.create_window(width=800, height=600)
    opt = vis.get_render_option()  # render意为渲染
    opt.point_size = 1  # 设置点的大小
    vis.add_geometry(colored_pointcloud)  # 添加点云
    vis.run()  # 运行
    vis.destroy_window()  # 关闭窗口

    return colored_pointcloud

# def pose_init(data_root, train_set):
#     calib = {}
#     pose = []
#     seq_pos_list = {}
#     for seq in train_set:
#         calib_path = os.path.join(data_root, "calib", seq, "calib.txt")
#         calib[seq] = parse_calibration(calib_path)
#
#         seq_pos_list[seq] = parse_poses(os.path.join(data_root, 'poses', seq + ".txt"), calib[seq])
#         pose +=  seq_pos_list[seq]
#     return pose, seq_pos_list

def pose_init(data_root):
    calib_path = os.path.join(data_root,"calib/01/calib.txt")
    calib = parse_calibration(calib_path)

    seq_pos_list = parse_poses(os.path.join(data_root, "poses",'01'+ ".txt"), calib)
    return seq_pos_list


def parse_calibration(filename):
    """ read calibration file with given filename

        Returns
        -------
        dict
            Calibration matrices as 4x4 numpy arrays.
    """
    calib = {}

    calib_file = open(filename)
    for line in calib_file:
        key, content = line.strip().split(":")
        values = [float(v) for v in content.strip().split()]

        pose = np.zeros((4, 4))
        pose[0, 0:4] = values[0:4]
        pose[1, 0:4] = values[4:8]
        pose[2, 0:4] = values[8:12]
        pose[3, 3] = 1.0

        calib[key] = pose

    calib_file.close()

    return calib

def parse_poses(filename, calibration):
    """ read poses file with per-scan poses from given filename

        Returns
        -------
        list
            list of poses as 4x4 numpy arrays.
    """
    file = open(filename)

    poses = []

    Tr = calibration["Tr"]
    Tr_inv = np.linalg.inv(Tr)

    for line in file:
        values = [float(v) for v in line.strip().split()]

        pose = np.zeros((4, 4))
        pose[0, 0:4] = values[0:4]
        pose[1, 0:4] = values[4:8]
        pose[2, 0:4] = values[8:12]
        pose[3, 3] = 1.0

        poses.append(np.matmul(Tr_inv, np.matmul(pose, Tr)))

    return poses


def j_to_i_project(point_j, pose_j, pose_i):
    diff_pose = np.matmul(np.linalg.inv(pose_i), pose_j)
    pc_j = rigid_translate(point_j, diff_pose)
    return pc_j

def rigid_translate(pc_input, extrinsic):
    # projection
    pc = np.hstack((pc_input[:, :3], np.ones_like(pc_input[:, 0]).reshape(-1, 1)))  # label=1
    pc = np.matmul(extrinsic, pc.T).T  # np.matmul(extrinsic, pc).T
    pcl = np.hstack((pc[:, :3], pc_input[:, 3:]))
    return pcl

def continus_project2(start, end, plist, llist, polist, filter=False):
    # plist = seq_point_list[seq]
    # llist = seq_lable_list[seq]
    # polist = seq_pos_list[seq]
    all_point = np.array([]).reshape((0, 5))




    #all_point = np.concatenate((all_point,),)
    for idx in range(start, end):
        #pcl1 = load_pcl(plist[idx], llist[idx], remap)
        pcl1 = load_pcl(config, idx, llist, plist)

        # 点过滤
        # if filter == True:
        #     pcl1 = filter_point(pcl1, obj)

        pose1 = polist[idx]
        pose2 = polist[start]

        pcl1 = j_to_i_project(pcl1, pose1, pose2)

        all_point = np.concatenate((all_point, pcl1), axis=0)

        print(idx)

    show_pcl(config, all_point)

def continus_project_show(config, start, end, plist, llist, polist, filter=False):
    # plist = seq_point_list[seq]
    # llist = seq_lable_list[seq]
    # polist = seq_pos_list[seq]
    sample_rate = config["down_sample_rate"]


    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name='Open3D Fullscreen Visualization',width=2560, height=1440)


    #all_point = np.array([]).reshape((0, 5))

    #pcl = load_pcl(config, start, label_list, point_list)



    #   add point open3d


    #all_point = np.concatenate((all_point,),)
    for idx in range(start, end):







        #pcl1 = load_pcl(plist[idx], llist[idx], remap)
        pcl = load_pcl(config, idx, llist, plist)

        #  显示轨迹
        #nav = np.random.uniform(low=0, high=1, size=(1000, 5))
        #nav[:, 4] = 8
        #pcl = np.concatenate((pcl,nav))


        # 点过滤
        # if filter == True:
        #     pcl1 = filter_point(pcl1, obj)

        pose1 = polist[idx]
        pose2 = polist[start]

        pcl = j_to_i_project(pcl, pose1, pose2)

        #===========================================================
        #删除  0 1标签  和天花板
        #pcl = pcl[(pcl[:,4]!=0)&(pcl[:,4]!=5)&(pcl[:,4]!=1)&(pcl[:,4]!=7)]
        #pcl = pcl[(pcl[:, 4] != 0)&(pcl[:,4]!=2)]
        pcl = pcl[(pcl[:, 4] != 0)]







        #all_point = np.concatenate((all_point, pcl1), axis=0)

        colormap = config["color_map"]
        color = []
        labels = pcl[:, 4]
        for l in labels:
            color.append(colormap[int(l)])
        color = np.asarray(color)
        colored_pointcloud = o3d.geometry.PointCloud()
        colored_pointcloud.points = o3d.utility.Vector3dVector(pcl[:, 0:3])
        colored_pointcloud.colors = o3d.utility.Vector3dVector(color)

        #voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(colored_pointcloud, 0.1)   #只能改体素大小
        if sample_rate != 0 :
            colored_pointcloud = colored_pointcloud.voxel_down_sample(sample_rate)

        vis.add_geometry(colored_pointcloud)

        # 视角
        view_control = vis.get_view_control()

        # 设置相机参数
        #view_control.set_zoom(0.8)  # 缩放视角（0-1 之间）
        #view_control.rotate(10.0, 0.0)  # 旋转视角（水平和垂直方向）
        view_control.set_front([0, 0, -1])  # 设置前视方向（向量）
        #view_control.set_lookat([0, 0, 0])  # 设置视点位置
        #view_control.set_up([0, -1, 0])  # 设置向上的方向








        vis.poll_events()
        vis.update_renderer()


        print(idx)

    while vis.poll_events():  # 继续处理事件直到窗口关闭
        vis.update_renderer()
    #show_pcl(config, all_point)
    #vis.destroy_window()




def continus_project_show_nav(config, start, end, plist, llist, polist, filter=False):
    # plist = seq_point_list[seq]
    # llist = seq_lable_list[seq]
    # polist = seq_pos_list[seq]
    sample_rate = config["down_sample_rate"]


    vis = o3d.visualization.Visualizer()
    vis.create_window()


    #all_point = np.array([]).reshape((0, 5))

    #pcl = load_pcl(config, start, label_list, point_list)



    #   add point open3d


    #all_point = np.concatenate((all_point,),)
    for idx in range(start, end):







        #pcl1 = load_pcl(plist[idx], llist[idx], remap)
        #pcl = load_pcl(config, idx, llist, plist)

        #pcl = np.random.normal(size=(1000, 5))

        pcl = np.random.uniform(low=0, high=1, size=(1000, 5))
        #pcl = np.random.normal(loc=0, scale=0.5, size=(1000, 5))

        pcl[:,4] = 0


        # 点过滤
        # if filter == True:
        #     pcl1 = filter_point(pcl1, obj)

        pose1 = polist[idx]
        pose2 = polist[start]

        pcl = j_to_i_project(pcl, pose1, pose2)

        #===========================================================
        #删除  0 1标签  和天花板
        #pcl = pcl[(pcl[:,4]!=0)&(pcl[:,4]!=5)&(pcl[:,4]!=1)]
        #pcl = pcl[(pcl[:, 4] != 0)&(pcl[:,4]!=2)]







        #all_point = np.concatenate((all_point, pcl1), axis=0)

        colormap = config["color_map"]
        color = []
        labels = pcl[:, 4]
        for l in labels:
            color.append(colormap[int(l)])
        color = np.asarray(color)
        colored_pointcloud = o3d.geometry.PointCloud()
        colored_pointcloud.points = o3d.utility.Vector3dVector(pcl[:, 0:3])
        colored_pointcloud.colors = o3d.utility.Vector3dVector(color)

        #voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(colored_pointcloud, 0.1)   #只能改体素大小
        if sample_rate != 0 :
            colored_pointcloud = colored_pointcloud.voxel_down_sample(sample_rate)

        vis.add_geometry(colored_pointcloud)

        # 视角
        view_control = vis.get_view_control()

        # 设置相机参数
        #view_control.set_zoom(0.8)  # 缩放视角（0-1 之间）
        #view_control.rotate(10.0, 0.0)  # 旋转视角（水平和垂直方向）
        view_control.set_front([0, 0, -1])  # 设置前视方向（向量）
        #view_control.set_lookat([0, 0, 0])  # 设置视点位置
        #view_control.set_up([0, -1, 0])  # 设置向上的方向







        vis.poll_events()
        vis.update_renderer()


        print(idx)

    while vis.poll_events():  # 继续处理事件直到窗口关闭
        vis.update_renderer()
    #show_pcl(config, all_point)
    #vis.destroy_window()


def print_z_max_min_value(point_list):
    for file_path in point_list:
        point = load_pointcloud(file_path)
        z = point[...,2]
        max = np.max(z)
        min = np.min(z)

        print(max,min)



def create_zero_as_nav(num_point):
    pass








if __name__ == "__main__":

    config = parase_config("R132_test_pridict.yaml")



    #init--------------------------

    point_list = load_point_list(config)
    label_list = load_label_list(config)
    config["learning_map"] = load_learning_map(config)
    config["color_map"] = load_color_map(config)
    pose_list = pose_init(config["root_path"])


    num_frame = len(point_list)
    # init_end--------------------------

    # 显示两帧叠加 & 显示单帧点云
    #pcl = load_pcl(config, 1, label_list, point_list)
    #pcl2 = load_pcl(config, 2, label_list, point_list)
    #pcl = j_to_i_project(pcl2, pose_list[2],pose_list[1] )

    #show_pcl(config, pcl)


    # 计算标签
    #compute_label_kinds(label_list)


    #  叠图
    #continus_project2(0, 10, point_list, label_list, pose_list, filter=False)
    #continus_project_show(config,0, num_frame, point_list, label_list, pose_list, filter=False)


    continus_project_show(config, 0, num_frame, point_list, label_list, pose_list, filter=False)


    # 输出z轴最大值最小值
    #print_z_max_min_value(point_list)


    #num_point, all_label = compute_label_kinds(label_list)










    #print(num_point,"\n",all_label)