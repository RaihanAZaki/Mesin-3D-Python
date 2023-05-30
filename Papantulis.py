print("\033c")       #To close all
import numpy as np
from matplotlib import pyplot as plt

#=====================================================================================
#=================================    USER ENTRIES    ================================
#=====================================================================================
nama_file = "papan"
threshold = 15                               #Threshold for checking a non-black voxel

# THE USER DECIDES THE ROTATION ANGLES IN DEGREE
alfa_start = 0; beta_start = 0
delta_alfa = 6; delta_beta = 6
no_of_rotation = int(15)

#============================================================================================
#=======================   CREATING A 3D MODEL USING GEOMETRICAL SCRIPT   ===================
#============================================================================================
print ("Creating a 3D model...."); print ("")

# THE USER DECIDES THE SIZE OF THE 3D ROOM AND THE 2D SCREEN (MAX 1080 BY 1080)
col, row, length = 200, 200, 200      #Ensure making a cubic 3D space and a square 2D screen.

#Creating The Template Matrix for the 3D Model
voxel  = np.zeros(shape=(row, col, length, 3), dtype=np.uint8)    #Template for the 3D model
buffer = np.zeros(shape=(row, col, length, 3), dtype=np.uint8)    #Template for the 3D buffer
slice = np.zeros(shape=(row, col, 3), dtype=np.uint8)             #Template for the slice cut

batas1 = round(0.10*row); batas1a = round(0.11*row); batas1b = round(0.10*row)
batas2 = round(0.15*row); batas2a = round(0.16*row); batas2b = round(0.11*row)
batas3 = round(0.40*row); batas3a = round(0.20*row);
batas4 = round(0.45*row); batas4b = round(0.47*row); batas4b2 = round(0.48*row)
batas5 = round(0.55*row); batas5b = round(0.51*row); batas5b2 = round(0.49*row)
batas6 = round(0.60*row); batas6a = round(0.65*row); batas6b = round(0.50*row)
batas7 = round(0.85*row); batas7b = round(0.89*row); batas7b2 = round(0.51*row)
batas8 = round(0.90*row); batas8a = round(0.89*row); batas8b = round(0.90*row)

batas_a1 = round(0.14*row)
batas_a2b = round(0.15*row)
batas_a2a = round(0.16*row)
batas_a2 = round(0.40*row)
batas_2b = round(0.41*row)

batas_a3 = round(0.50*row)
batas_a4 = round(0.51*row)

batas_a5 = round(0.48*row)
batas_a6 = round(0.52*row)

batas_a7 = round(0.41*row); batas_a7a = round(0.50*row)
batas_a8 = round(0.66*row);

batas_a9 = round(0.76*row); batas_a92 = round(0.80*row)
batas_a10 = round(0.81*row); batas_a10a = round(0.80*row)

half_length = round(0.5*row)

warna1 = [25, 25, 112]
warna2 = [192, 192, 192]
warna3 = [255, 255, 255]

#Format: voxel[y, x, z]
voxel[batas3:batas7, batas2:batas3a, batas4:batas5, :] = warna1[:]       #Batang panjang 1
voxel[batas3:batas7, batas_a9:batas_a10, batas4:batas5, :] = warna1[:]       #Batang panjang 2

voxel[batas_a2a:batas5b, batas2:batas2a, batas4b2:batas5b, :] = warna2[:]       #kiri papan
voxel[batas_a2a:batas5b, batas_a92:batas_a10, batas4b2:batas5b, :] = warna2[:]       #kanan papan

voxel[batas_a2b:batas_a2a, batas2:batas_a10, batas4b2:batas5b, :] = warna2[:] #Batas atas papan
voxel[batas_a3:batas_a4, batas2:batas_a10, batas4b2:batas5b, :] = warna2[:] #Batas bawah papan


voxel[batas_a2a:batas_a3, batas2a:batas_a10a, batas4b2:batas5b2, :] = warna2[:] #Papan Belakang
voxel[batas_a2a:batas_a3, batas2a:batas_a10a, batas6b:batas7b2, :] = warna3[:] #Papan Depan


#Visualizing the cross slice at the half_length
slice[:, :, :] = voxel[half_length, :, : :]
plt.figure(1); plt.imshow(slice)

#Visualizing the cross slice at the half_length
slice[:, :, :] = voxel[:, half_length, :, :]
plt.figure(2); plt.imshow(slice)

#Visualizing the cross slice at the half_length
slice[:, :, :] = voxel[:, :, half_length, :]
plt.figure(3); plt.imshow(slice)

plt.ion()
plt.show()
plt.pause(1)

np.save(nama_file + "_0_0_.npy", voxel)

#================================================================================================
#=================    DEFINING FUNCTION FOR DEGREE CONVERSION AND ROTATION    ===================
#================================================================================================
# Converting degree unit of alfa and beta to radiant unit
def degree_to_rad (alfa, beta):
    alfa_rad = (alfa / 180) * np.pi  # Converting degree to rad
    beta_rad = (beta / 180) * np.pi  # Converting dgreee to rad
    return alfa_rad, beta_rad

#FUNCTION TO ROTATE A VOXEL (xx,xv,vz) ABOUT A DEFINED CENTER (cx,cy,cz) AS MUCH AS ALFA RAD
#AROUND Z-AXIS THEN AS MUCH AS BETA RAD AROUND X-AXIS
def rotate(vx,vy,vz,cx,cy,cz,alfa_rad,beta_rad):
    #Converting point's coordinate to be relative to the rotation center
    #so that the rotation matrix can be applied correctly.
    vx=vx-cx; vy=vy-cy; vz=vz-cz

    k = 0.6                                      #Correction factor
    # ROTATION 1 - Rotating the point as much as alfa around z-axis
    vx = int( np.cos(alfa_rad*k) * vx + np.sin(alfa_rad*k) * vy)
    vy = int(-np.sin(alfa_rad*k) * vx + np.cos(alfa_rad*k) * vy)
    vz = vz                                   #The z-coordinate of the voxel does not change.
    # ROTATION 2 - Rotating the point as much as beta around x-axis
    vz = int( np.cos(beta_rad*k) * vz + np.sin(beta_rad*k) * vy)
    vy = int(-np.sin(beta_rad*k) * vz + np.cos(beta_rad*k) * vy)
    vx = vx                                   #The x-coordinate of the voxel does not change.

    # Converting point's coordinate back, relative to (0,0,0)
    vx = vx + cx; vy = vy + cy; vz = vz + cz

    return vx, vy, vz  #Variabel input: vx,vy,vz, nama untuk variabel output tetap vx, vy, vz.

#============================================================================================
#==========================   MAIN PROGRAM TO ROTATE THE 3D OBJECT   ========================
#============================================================================================
#The object is rotated with the same angle over and over again acc. to number of rotations.
cx = round(col/2); cy = round(row/2); cz = round(length/2)      #Center of 3D object rotation

alfa = alfa_start
beta = beta_start
for r in range (1, no_of_rotation+1):
    alfa = alfa + delta_alfa
    beta = beta + delta_beta
    alfa_rad, beta_rad = degree_to_rad(alfa, beta)                #Convert degree to rad.
    voxel = np.load(nama_file + "_0_0_.npy")                #Always reads original model.

    for i in range (0, col):                              #Rotating te whole voxel[:,:,:]
        print('alfa =', alfa, ', beta =', beta,', now rotating voxels in column', i, '.')
        for j in range (0, row):
            for k in range (0, length):
                cek1 = int(voxel[i,j,k,0])
                cek2 = int(voxel[i,j,k,1])
                cek3 = int(voxel[i,j,k,2])
                if  (cek1 + cek2 + cek3) > threshold:
                    u, v, w = rotate(i,j,k,cx,cy,cz,alfa_rad,beta_rad) #Rotate every voxel
                    buffer[u,v,w,:] = voxel[i,j,k,:]
                    voxel[i,j,k,:] = 0                         #Must be put back to black.
    #Result of one time rotation of the object is ready for next rotation
    np.save(nama_file + "_" + str(alfa) + "_" + str(beta) + "_" + ".npy", buffer)
    voxel[:, :, :] = 0                                      #Must be put back to black.
    buffer[:, :, :] = 0                                     #Must be put back to black.

plt.show()