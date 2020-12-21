# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 12:59:56 2020

@author: Arnaud
"""


import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__ == "__main__":

    # Load saved point cloud and visualize it
    pt_cloud = o3d.io.read_point_cloud("C:/Users/Arnaud/EuropaExp/XP1612/Stereo/up_view/8.ply")
    #o3d.visualization.draw_geometries([pcd_load])

    # convert Open3D.o3d.geometry.PointCloud to numpy array
    xyz = np.asarray(pt_cloud.points)

    
    x,y,z = [], [], []
    for k in range(0, xyz.shape[0], 1000):
        x.append(xyz[k,0])
        y.append(xyz[k,1])
        z.append(xyz[k,2])
    
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(x, y, -z, zdir='z',s=0.1)
    # ax.view_init(azim=180, elev=10)
    # plt.show()
    
    # # rotate the axes and update
    # for angle in range(0, 360):
    #     ax.view_init(30, angle)
    #     plt.draw()
    #     plt.pause(.001)
    
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(y[:],z[:],s=0.2)
    plt.show()