# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 12:59:56 2020

@author: Arnaud
"""

import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

def SeparateAxis(xyz, step):
    x,y,z = [], [], []
    for k in range(0, xyz.shape[0], step):
        x.append(xyz[k,0])
        y.append(xyz[k,1])
        z.append(xyz[k,2])
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    return(x, y, z)


if __name__ == "__main__":

    # Load saved point cloud and visualize it
    pt_cloud = o3d.io.read_point_cloud("C:/Users/Arnaud/EuropaExp/XP1612/Stereo/up_view/beautifulmesh.ply")
    # convert Open3D.o3d.geometry.PointCloud to numpy array
    xyz = np.asarray(pt_cloud.points)
    center = pt_cloud.get_center()
    
    # Translate cneter to (0, 0 ,0)
    for i in range(np.shape(xyz)[0]):
        for j in range(3):
            xyz[i][j] -= center[j]
    center = pt_cloud.get_center()
    
    # Find best fitting plane
    step = 40
    x,y,z = SeparateAxis(xyz, step)
    plane_model, inliers = pt_cloud.segment_plane(distance_threshold=1, ransac_n=3, num_iterations=10)
    [a, b, c, d] = plane_model
    print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
    

    u1 = b/np.sqrt(a**2 + b**2 + c**2)
    u2 = -a/np.sqrt(a**2 + b**2 + c**2)
    cos = c/np.sqrt(a**2 + b**2 + c**2)
    sin = np.sqrt((a**2 + b**2)/(a**2 + b**2 + c**2))
    # Rotation matrix
    Rotator = np.array([[cos+u1**2*(1-cos), u1*u2*(1-cos), u2*sin],
                       [u1*u2*(1-cos), cos+u2**2*(1-cos), -u1*sin],
                       [-u2*sin, u1*sin, cos]])
    # Rotate point cloud
    XYZ = np.dot(np.array([x,y,z]).T, Rotator)
    
    
    
    
    X,Y,Z = SeparateAxis(XYZ, step=1)
    
    ## 3D  Plot 
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, s=0.1, color = "red")
    ax.scatter(X, Y, Z, s=0.1, color = "green")
    # center = pt_cloud.get_center()
    # ax.scatter(center[0], center[1], center[2], s=2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.view_init(azim=100, elev=10)
    plt.show()
