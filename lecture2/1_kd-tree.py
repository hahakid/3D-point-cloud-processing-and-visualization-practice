import numpy as np
from binarytree import tree, build
import time

point_number=30
point_degree=6
#print(np.floor(time.time()))
rng=np.random.default_rng(int(time.time()))
X=np.floor(rng.random((point_number, point_degree)) * 10) #

tree_nodes = []

def findSplit(data):
    """
        使用递归的方式分割数据，使其构建出二叉树结构。选择方差最大列的中位数值作为分割点。
    """
    if data.size == 0:
        return None

    colidx = np.argmax(np.var(data, axis=0))
    sortdata = data[data[:, colidx].argsort()]  # 按方差最大排序

    med = len(sortdata) // 2  # 中位数
    divide = sortdata[med]
    left, right = sortdata[:med], sortdata[med+1:]

    tree_nodes.append(divide)  # 添加当前分割节点

    # 递归
    findSplit(left)
    findSplit(right)

def showtree(dataarray):
    """
       显示树结构：首先显示每个数据点的索引，然后调用 findSplit 构建树结构。
    """

    for i, data in enumerate(dataarray):
        print(f"{i}: {data}")
    # build binary-tree
    findSplit(dataarray)

    treeidx=[j for i in tree_nodes for j, d in enumerate(dataarray) if np.array_equal(d, i)]

    root = build(treeidx)
    print("Tree structure:", root)


data1 = np.asarray([[2., 3.],
                    [5., 4.],
                    [9., 6.],
                    [4., 7.],
                    [8., 1.],
                    [7., 2.]])

data2 = np.asarray([[5, 7, 6],
                    [5, 4, 6],
                    [4, 8, 9],
                    [3, 7, 5],
                    [5, 9, 0],
                    [0, 0, 8],  # ])
                    [7, 8, 9],
                    [7, 4, 7],
                    [1, 6, 1],
                    [9, 5, 4]])

data3 = np.asarray([[4., 7., 0.],
                    [3., 1., 0.],
                    [1., 3., 3.],
                    [5., 4., 6.],
                    [2., 8., 0.],
                    [6., 4., 5.],
                    [1., 1., 8.],
                    [9., 3., 6.],
                    [8., 8., 0.],
                    [0., 1., 8.]])

showtree(data1)
showtree(data2)
showtree(data3)