import numpy as np
import os
import cv2

ipl_name = 'harddrop.ipl'
dir = 'C:/Users/jsheo/Desktop/TetrisOnlinePoland/skin/specialfx/default'

for i in range(7):
    path = os.path.join(dir, ipl_name+'_{}.png'.format(i))
    print(path)
    image_np = cv2.imread(path,cv2.IMREAD_UNCHANGED)
    image_np = np.zeros_like(image_np)
    cv2.imwrite(path,image_np)
