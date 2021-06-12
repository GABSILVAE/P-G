import numpy as np
import pandas as pd
import numpy as np

from freenect import sync_get_depth as get_depth
from matplotlib import pyplot as plt


depth = get_depth()[0]
mat = pd.DataFrame(data = depth)
mat.to_csv("1depth.csv",sep=',',header=False,float_format='%d',index=False)

np.clip(depth, 0, 2**9 - 1, depth)
mat = pd.DataFrame(data = np.clip(depth, 0, 2**10 - 1, depth))
mat.to_csv("2clip.csv",sep=',',header=False,float_format='%d',index=False)

depth >>= 2
mat = pd.DataFrame(data = depth)
mat.to_csv("3despla.csv",sep=',',header=False,float_format='%d',index=False)

depth = depth.astype(np.uint8)
mat = pd.DataFrame(data = depth)
mat.to_csv("4out.csv",sep=',',header=False,float_format='%d',index=False)
