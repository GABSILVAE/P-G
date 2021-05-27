from freenect import sync_get_depth as get_depth
import numpy as np
import cv2
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import time

c = "Capture"
e1 = ".csv"
e2 = ".jpg"
i = 0
n = 1

while i < 7:
    depth = get_depth()[0]
    output = depth.astype(np.uint8)

    n = str(n)
    a = c+n+e1
    b = c+n+e2
    
    cv2.imshow('Depth', output)
    
    mat = pd.DataFrame(data=output)
    mat.to_csv(a,sep=',',header=False,float_format='%d',index=False)

    output = depth.astype(np.uint8)
    cv2.imwrite(b, output)

    n = int(n)
    n += 1
    i += 1
    print(n)
    time.sleep(5)



