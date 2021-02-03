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
    return(np.array(x), np.array(y), np.array(z))

def RotationMatrixFromVectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return(rotation_matrix)

def PlotPointCloud(xyz):
    """3D plot of a point cloud"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d') 
    x,y,z = SeparateAxis(xyz, step=200)
    ax.scatter(x, y, z, s=0.1, color = "red")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_zlim(-40, 40)
    ax.view_init(azim=100, elev=10)
    plt.show()
    return(None)

def PlotCrossSection(xyz, x0 = 0, thresh = 0.1):
    """2D plot of a Cross Section"""
    # Find points near line
    Y, Z = [], []
    for point in xyz:
        x, y, z = point
        if x > x0-thresh and x < x0+thresh:
            Z.append(z)
            Y.append(y)
    # 2D plot
    fig, ax = plt.subplots()
    #ax.scatter(Y, Z, s=0.1, label = f"{x0}")
    ax.plot(Y, Z, label = f"x = {100+x0} mm")
    ax.set_ylim(-40, 40)
    ax.set_ylabel("y (mm)")
    ax.set_xlabel("z (mm)")
    plt.title("Cross section of 3D point cloud")
    plt.legend()
    plt.show()
    return(None)

def GenerateDepthMap(xyz, nx = 1000):
    """Returns a 2D array to plot depth map"""
    dx = (np.max(xyz[:,0])-np.min(xyz[:,0]))/nx
    dy = dx
    #ny = int((np.max(xyz[:,1])-np.min(xyz[:,1]))/dx)
    minx = np.min(xyz[:,0])
    miny = np.min(xyz[:,1])
    Map  = np.zeros((nx+1,nx+1))
    for point in xyz:
        x, y, z = point
        i = int((x+abs(minx))/dx)
        j = int((y+abs(miny))/dy)
        Map[i][j] = z
    return(Map)

def PlotDepthMap(Map):
    """Plot the map surface"""
    fig, ax = plt.subplots()
    cmap = ax.pcolormesh(Map)
    ax.set_ylabel("y")
    ax.set_xlabel("x")
    fig.colorbar(cmap, label = "z (mm)")
    plt.show()
    return(None)

def Translate2Origin(xyz, center):
    """Translate center of point cloud to (0, 0 ,0)"""
    for i in range(np.shape(xyz)[0]):
        for j in range(3):
            xyz[i][j] -= center[j]
    return(xyz)

def Rotate2Horizontal(pt_cloud, xyz):
    """"
    Rotate point cloud to the xy plane.
    1) Find the best fitting plane of the point cloud.
    2) Rotate pt cloud so that fitted plane normal becomes axis z = (0,0,1).
    Returns: Rotated point cloud xyz
    """
    # Find best fitting plane
    plane_model, inliers = pt_cloud.segment_plane(distance_threshold=10, ransac_n=100000, num_iterations=50)
    [a, b, c, d] = plane_model
    print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
    # Apply Rotation
    vect_z = np.array([0, 0, 1]) # vecteur z
    vect_normal = np.array([a, b, c]) # vecteur normal au plan
    R = RotationMatrixFromVectors(vect_normal, vect_z) # matrice de rotation
    xyz = np.dot(xyz, R.T) 
    return(xyz)

if __name__ == "__main__":

    # Load saved point cloud and visualize it
    ply_path = "C:/Users/Cyril/Documents/Work/PLR1/EuropaExp/XP2611/set_GCP/7.ply"
    pt_cloud = o3d.io.read_point_cloud(ply_path)
    center = pt_cloud.get_center()
    # Convert to array
    xyz = np.asarray(pt_cloud.points)
    # Translate center
    Translate2Origin(xyz, center)
    # Rotation to horizontal
    Rotate2Horizontal(pt_cloud, xyz)
    
    # # ## 3D  Plot 
    PlotPointCloud(xyz)
    # # # # 2D Plot
    PlotCrossSection(xyz)
    
    # Create Depth map
    Map = GenerateDepthMap(xyz, nx=1000)
    #P Plot Depth map
    PlotDepthMap(Map)

    

    
    # nx = 1000
    # dx = (np.max(xyz[:,0])-np.min(xyz[:,0]))/nx
    # yticks = [k*100 for k in range(Map.shape[1])]
    # ax.set_yticks(yticks)
    # ax.set_yticklabels([str(int(y*dx)) for y in yticks])
    # xticks = [k*100 for k in range(6)]
    # ax.set_xticks(xticks)
    # ax.set_xticklabels([str(int(x*dx)) for x in xticks])

    