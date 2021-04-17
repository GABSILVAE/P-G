from freenect import sync_get_depth as get_depth
from functools import partial
import numpy as np
import cv2
import os


class Video:
    FILE_OUTPUT = 'output.avi'
    dimensions = (640, 480)
    
    def __init__(self):
        self.clean()
        # codec. Podes probar otros como 'X264'
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')  
        self.out = cv2.VideoWriter(self.FILE_OUTPUT, fourcc, 30, self.dimensions, True)

    def write(self, image):
        self.out.write(image)

    def clean(self):
        if os.path.isfile(self.FILE_OUTPUT):
            os.remove(self.FILE_OUTPUT)
            
    def __del__(self):
        self.out.release()


class App:
    def __init__(self):
        self.screenOut = Output(partial(cv2.imshow, 'Screen Output'))
        self.videoOut = Video()

    def draw(self):
        depth = get_depth()[0]
        output = depth.astype(np.uint8)
        output = cv2.cvtColor(output, cv2.COLOR_GRAY2RGB)

        self.screenOut.write(output)
        self.videoOut.write(output)

    def __del__(self):
        cv2.destroyAllWindows()


class Output:
    def __init__(self, device):
        self.device = device

    def write(self, output):
        self.device(output)


def loop(function, delay=5):
    while True:
        function()
        cv2.waitKey(delay)


app = App()
loop(app.draw)