import cv2
import freenect
import numpy as np

from morphology.processing import dilatation, erosion
from frame_convert2 import video_cv


def green():
    video, timestamp = freenect.sync_get_video()
    video = video_cv(video)
    video2 = video
    R = video[:,:,0]
    G = video[:,:,1]
    B = video[:,:,2]
    for i in range(641):
        if(i == 213 or i == 214 or i == 427 or i == 428):
            x = i
            R[:,x] = 0
            G[:,x] = 255
            B[:,x] = 0
    R[240,:] = 0
    G[240,:] = 255
    B[240,:] = 0
    video2[:,:,0] = R
    video2[:,:,1] = G
    video2[:,:,2] = B
    cv2.imshow('video', video2)


def pol_ncl_5(val):
    a = 0.0000000153604707187203 * pow(val, 5)
    b = 0.0000102550961463067 * pow(val, 4)
    c = 0.002562964189799 * pow(val, 3)
    d = 0.281730142677474 * pow(val, 2)
    e = 11.860783228931 * val
    y = a - b + c - d + e
    return y


def disp_thresh(lower, upper):
    depth, timestamp = freenect.sync_get_depth()
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = 255 * np.logical_and(depth > lower, depth < upper)
    depth = depth.astype(np.uint8)
    cv2.imshow('Depth', depth)
    
    filter = np.array( [[1,1,1,1,1],
                        [1,1,1,1,1],
                        [1,1,1,1,1],
                        [1,1,1,1,1],
                        [1,1,1,1,1]])                  
    
    output_erosion = erosion(depth, filter)
    output_erosion = output_erosion.astype(np.uint8)
    #output_dilatation = dilatation(output_erosion, filter)
    #output_dilatation = output_dilatation.astype(np.uint8)
    output_erosion = erosion(output_erosion, filter)
    output_erosion = output_erosion.astype(np.uint8)
    cv2.imshow('Apertura', output_erosion)
    cv2.waitKey(10)
    return output_erosion


def objs(img):
    filas, columnas = img.shape
    matriz = 1 * img.astype(np.bool)

    numeroIslas=2

    for i in range(filas-1):
        for j in range(columnas-1):
            valorPos=matriz[i][j]
            dirN=i+1
            dirS=i-1
            dirD=j+1
            dirI=j-1
            if(dirN<0 or dirN>9):
                posN=0
            else:
                posN=matriz[dirN][j]
            
            if(dirS<0 or dirS>10):
                posS=0
            else:
                posS=matriz[dirS][j]
            
            if(dirD<0 or dirD>9):
                posD=0
            else:
                posD=matriz[i][dirD]
            
            if(dirI<0 or dirI>10):
                posI=0
            else:
                posI=matriz[i][dirI]
            
            if (valorPos==1):
                if(posD==1 or posD==0):
                    matriz[i][j]=numeroIslas
                    if(posN==1):
                        matriz[i+1][j]=numeroIslas
                    if(posS==1):
                        matriz[i-1][j]=numeroIslas
                    if(posD==1):
                        matriz[i][j+1]=numeroIslas
                    if(posI==1):
                        matriz[i][j-1]=numeroIslas
                    numeroIslas=numeroIslas+1
                if(posD>1):
                    matriz[i][j]=posD
                    if(posN==1):
                        matriz[i+1][j]=posD
                    if(posS==1):
                        matriz[i-1][j]=posD
                    if(posD==1):
                        matriz[i][j+1]=posD
                    if(posI==1):
                        matriz[i][j-1]=posD

            if(valorPos!=0 and valorPos!=1):
                if(posN==1):
                    matriz[i+1][j]=valorPos
                if(posS==1):
                    matriz[i-1][j]=valorPos
                if(posD==1):
                    matriz[i][j+1]=valorPos
                if(posI==1):
                    matriz[i][j-1]=valorPos
    numeroIslas=numeroIslas-2
    print("numero de islas = %s" %numeroIslas)
    return numeroIslas