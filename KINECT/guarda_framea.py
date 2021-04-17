from freenect import sync_get_depth as get_depth
import numpy as np
import cv2
from matplotlib import pyplot as plt

depth = get_depth()[0]

output = depth.astype(np.uint8)
cv2.imshow('Depth', output)

cv2.imwrite('Capture.jpg', output)

img = cv2.imread('Capture.jpg')
 
blur = cv2.blur(img,(3,3))
 
plt.subplot(121),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(blur),plt.title('Difuminada')
plt.xticks([]), plt.yticks([])
plt.show()

cv2.waitKey(0) # se espera a que se presione cualquier tecla
cv2.destroyAllWindows() # un clean up no está de más