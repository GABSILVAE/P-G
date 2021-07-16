import cv2
import freenect
import numpy as np
import collections

from morphology.processing import dilatation, erosion
from frame_convert2 import video_cv
from image import array2vector_gray


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

    islas=2
    filas, columnas = matriz.shape
    adv = False

    for i in range(filas - 2):
        for j in range(columnas - 2):

            if(i == 0 and j == 0 and matriz[i+1,j+1] == 1):
                matriz[i+1,j+1] = islas
            
            if(matriz[i+1,j+1] == 1):
                adv = False
                for m in range(3):
                    for n in range(3):
                        if(matriz[i+m,j+n] != 1 and matriz[i+m,j+n] != 0):
                            adv = True
                if(adv):
                    matriz[i+1,j+1] = islas
                    adv = False
                else:
                    islas += 1
                    matriz[i+1,j+1] = islas

            if(matriz[i+1,j+1] != 1 and matriz[i+1,j+1] != 0):
                for k in range(3):
                    for l in range(3):
                        if(matriz[i+k,j+l] == 1):
                            matriz[i+k,j+l] = matriz[i+1,j+1]
    
    cantidad = array2vector_gray(matriz)
    cantidad = collections.Counter(cantidad)
    print(cantidad)
    
    islas -= 1
    print('islas = %d' % (islas))