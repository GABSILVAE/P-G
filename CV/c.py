import numpy as np
import cv2 as cv

img = cv2.imread("figContorno.png", cv2.IMREAD_GRAYSCALE)
src = cv2.cuda_GpuMat()
src.upload(img)
 
clahe = cv2.cuda.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
dst = clahe.apply(src, cv2.cuda_Stream.Null())
 
result = dst.download()
 
cv2.imshow("result", result)
cv2.waitKey(0)
