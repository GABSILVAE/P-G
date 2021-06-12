import numpy as np
import frame_convert2
import pandas as pd
import numpy as np
import time
import cv2

from freenect import sync_get_depth as get_depth
from matplotlib import pyplot as plt

c = "Capture_kc2_50cm"
e1 = ".csv"
e2 = ".jpeg"
i = 0
n = 1

while i < 6:
    depth = get_depth()[0]
    output = frame_convert2.pretty_depth_cv(depth)

    n = str(n)
    a = c+n+e1
    b = c+n+e2
    
    cv2.imshow('Depth', output)
    
    mat = pd.DataFrame(data=output)
    mat.to_csv(a,sep=',',header=False,float_format='%d',index=False)

    cv2.imwrite(b, output)

    n = int(n)
    n += 1
    i += 1
    print(n)
    time.sleep(1)



