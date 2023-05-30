print("\033c")       #To close all
import numpy as np
from matplotlib import pyplot as plt
from skimage.io import imread, imsave
#import cv2

#=====================================================================================
#=================================    USER ENTRIES    ================================
#=====================================================================================
nama_file = "papan"
threshold = 15                               #Threshold for checking a non-black voxel

# PLEASE SPECIFY THESE VALUES EXACTLY THE SAME AS THE ONES USED IN "Create_&_Rotate_Tangga.py".
alfa_start = 0; beta_start = 0
delta_alfa = 6; delta_beta = 6
no_of_rotation = int(15)

cam_focal = 400

# THE USER DECIDES THE CAM P0SITION CONSIDERING THAT
# AT 3D ROOM BORDER Z = 0 AND AT THE LEFTMOST 3D VOXEL, Z = length.
# E.G. CAM_z = -5 * LENGTH MEANS THAT THE CAM RESIDES FAR BEHIND THE 3D ROOM BORDER.
cam_z = -400
print("cam_z =", cam_z)

#=================================================================================================
#========================================    PREPARATION    ======================================
#=================================================================================================
voxel = np.load(nama_file + "_0_0_.npy")
#voxel = voxel.astype(int)

print("pic.shape =", voxel.shape)
maks = max(voxel.shape)
col, row, length = maks, maks, maks   #We ensure making a cubic 3D space and a square 2D screen.

#Preparing the template for 2D screen (initially black)
pixel = np.zeros(shape=(row, col, 3), dtype=np.uint8)         #Template for the 2D screen

print("TO UNDERSTAND THE FOLLOWING MATH OPERATIONS YOU SHALL REFER TO NASUCHA!S GEOMETRIC NOTES")
print('col, row, length =', col, ',', row, ',', length)
cx = round(0.5*col); cy = round(0.5*row)            #The center of 3D room, cam and the 2D screen
print('cx, cy =', cx, ',', cy)

#THE 2D SCREEN POSITION IS FIXED, THAT IS, ANALOGOUS TO REAL SENSORS RESIDING AT THE CAM'S FOCAL
room_border_z = 0                                    #The z position of the 3D room's border is 0.
print('room_border_z =', room_border_z)

#DECIDING THE SIZE OF THE 2D SCREEN
col = col; row = row

#================================================================================================
#======================    DEFINING THE FUNCTION FOR BACKWARD PROJECTION     ====================
#================================================================================================
#FUNCTION TO CORELATE A PIXEL AT THE 2D SCREEN (px,py) TO A VOXEL IN THE 3D ROOM (vx,vy,vz).
def projection (cx, cy, cam_z, screen_z, px, py, vz):
    #You shall refer to Nasucha!s projection geometric notes
    pz = screen_z
    vx = round (cx + (cx-px) * ((vz-cam_z)/(cam_z-pz)) )
    vy = round (cy + (cy-py) * ((vz-cam_z)/(cam_z-pz)) )
    return vx, vy

#============================================================================================
#======================================    MAIN PROGRAM     =================================
#============================================================================================
cam_z = -400 #-420
alfa = alfa_start
beta = beta_start
for i in range (1, no_of_rotation+1):
    pixel[:, :, :] = 0                                     # Put the 2D Screen back to black.
    voxel = np.load(nama_file + "_" + str(alfa) + "_" + str(beta) + "_.npy")
    screen_z = cam_z - cam_focal
    print('cam_z =', cam_z); print('screen_z =', screen_z)
    print('NOW PROJECTING: FROM 2D SCREEN TO CAM TO 3D OBJECT')
    print('Finding vx and vy of the 3D object that corelates with every pixel of 2D sceen.')
    for px in range(0, col):               #x of a pixel of the 2D screen
        print('alfa =', alfa, ', beta =', beta,', px =', px)
        for py in range(0, row):           #y of that pixel
            for vz in range(0, length):    #z of the voxel of the corelating 3D object
                                           #starting from 3D room's border (ringht to left)
                vx, vy = projection (cx, cy, cam_z, screen_z, px, py, vz)        #Projection
                if (vy >= 0 and vy < row and vx >= 0 and vx < col) and \
                    (int(voxel[vy,vx,vz,0]) + int(voxel[vy,vx,vz,1]) + int(voxel[vy,vx,vz,2]) > threshold):
                    pixel[row-py-1,col-px-1,:] = voxel[vy,vx,vz,:]
                    #print('Projecting a voxel and skipping the vz loop')
                    break
    plt.imsave(nama_file + "_" + str(alfa) + ("_") + str(beta) + ("_") + str(cam_z) + "_" + ".jpg", pixel)
    alfa = alfa + delta_alfa
    beta = beta + delta_beta

plt.figure(1)
plt.imshow(pixel)
plt.show()