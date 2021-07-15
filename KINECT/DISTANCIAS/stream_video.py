#Codigo YOLO Python // Hablar con ING Manuel (info)
#Revision estado del arte // Hablar con ING Manuel (recomendaciones)
#Terminar medicion distancia

import cv2
import numpy as np

from frame_convert2 import *
from freenect import sync_get_depth as get_depth

def dist_pixel(imag):
    image_array = np.array(imag)
    a = 0
    y = 0

    for i in range(238,330):
        for j in range(170,270):
            a += 1
            y += image_array[j,i]
    prom = y/a
    return prom

def pol_dod_5(val):
    a = 0.0000000170804376340398 * pow(val, 5)
    b = 0.0000115679971454278 * pow(val, 4)
    c = 0.002933265601153 * pow(val, 3)
    d = 0.32731810765293 * pow(val, 2)
    e = 13.9126049586823 * val
    y = a - b + c - d + e   
    print("pol_dod_5 =", y)
    #print("------------------------------")

def pol_dod_6(val):
    a = 0.000000000222305684221164 * pow(val, 6)
    b = 0.00000019136106547898 * pow(val, 5)
    c = 0.0000655217220984247 * pow(val, 4)
    d = 0.011107202553769 * pow(val, 3)
    e = 0.930454016767366 * pow(val, 2)
    f = 30.367333067039 * val
    y =  a - b + c - d + e - f
    print("pol_dod_6 =", y)
    #print("------------------------------")

def pol_dcd_5(val):
    a = 0.0000000149919615410675 * pow(val, 5)
    b = 0.00000998523171736648 * pow(val, 4)
    c = 0.002489623878325 * pow(val, 3)
    d = 0.27296558147033 * pow(val, 2)
    e = 11.4742200772822 * val
    y = a - b + c - d + e
    print("pol_dcd_5 =", y)
    #print("------------------------------")

def pol_dcd_6(val):
    a = 0.000000000187070887911858 * pow(val, 6)
    b = 0.000000158389104019771 * pow(val, 5)
    c = 0.0000533013556336601 * pow(val, 4)
    d = 0.008866188545258 * pow(val, 3)
    e = 0.727161458340531 * pow(val, 2)
    f = 23.058551860747 * val
    y =  a - b + c - d + e - f
    print("pol_dcd_6 =", y)
    #print("------------------------------")

def pol_ncl_5(val):
    a = 0.0000000153604707187203 * pow(val, 5)
    b = 0.0000102550961463067 * pow(val, 4)
    c = 0.002562964189799 * pow(val, 3)
    d = 0.281730142677474 * pow(val, 2)
    e = 11.860783228931 * val
    y = a - b + c - d + e
    print("pol_ncl_5 =", y)
    #print("------------------------------")

def pol_ncl_6(val):
    a = 0.00000000019146670835859 * pow(val, 6)
    b = 0.000000162757840952639 * pow(val, 5)
    c = 0.0000550372816075057 * pow(val, 4)
    d = 0.009209857387056 * pow(val, 3)
    e = 0.760947609238925 * pow(val, 2)
    f = 24.3756309301879 * val
    y =  a - b + c - d + e - f
    print("pol_ncl_6 =", y)
    #print("------------------------------")

def pol_nsl_5(val):
    a = 0.0000000188003063291798 * pow(val, 5)
    b = 0.0000129509568427124 * pow(val, 4)
    c = 0.003341028347214 * pow(val, 3)
    d = 0.379335200153305 * pow(val, 2)
    e = 16.3242750333465 * val
    y = a - b + c - d + e
    print("pol_nsl_5 =", y)
    #print("------------------------------")

def pol_nsl_6(val):
    a = 0.00000000023078110568243 * pow(val, 6)
    b = 0.00000019902320389213 * pow(val, 5)
    c = 0.0000682169083872867 * pow(val, 4)
    d = 0.011569655063867 * pow(val, 3)
    e = 0.969554910977373 * pow(val, 2)
    f = 31.6974133339278 * val
    y =  a - b + c - d + e - f
    print("pol_nsl_6 =", y)
    #print("------------------------------")        

def pol_todo_5(val):
    a = 0.0000000162385327655822 * pow(val, 5)
    b = 0.00001094084341015 * pow(val, 4)
    c = 0.002760034888734 * pow(val, 3)
    d = 0.306304836461392 * pow(val, 2)
    e = 12.9733974569754 * val
    y = a - b + c - d + e
    print("pol_todo_5 =", y)
    #print("------------------------------")

def pol_todo_6(val):
    a = 0.000000000189559548597579 * pow(val, 6)
    b = 0.00000016033893881767 * pow(val, 5)
    c = 0.0000538908714144491 * pow(val, 4)
    d = 0.008952689404778 * pow(val, 3)
    e = 0.733542744853558 * pow(val, 2)
    f = 23.270668207254 * val
    y =  a - b + c - d + e - f
    print("pol_todo_6 =", y)
    print("------------------------------")  

#def neg(img, prom):


def draw():
    depth = get_depth()[0]
    output = pretty_depth(depth)
    
    prom = dist_pixel(output)
    print("val =",prom)
    pol_dod_5(prom)
    pol_dod_6(prom)
    pol_dcd_5(prom)
    pol_dcd_6(prom)
    pol_ncl_5(prom)
    pol_ncl_6(prom)
    pol_nsl_5(prom)
    pol_nsl_6(prom)
    pol_todo_5(prom)
    pol_todo_6(prom)
    
    output = rectangle(output)
    cv2.imshow('Depth', output)

    output = disp_thresh(output, prom, 5)
    cv2.imshow('Depth2', output)


def loop(function, delay = 5):
    while True:
        function()
        cv2.waitKey(delay)


loop(draw)

