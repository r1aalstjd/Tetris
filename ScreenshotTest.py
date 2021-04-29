# getnextblock

import pyautogui as pag
from PIL import Image as img
import numpy as np

from pprint import pprint

pag.screenshot('./temp.png', region = (1145,270,160,90))

blockimg=img.open('./temp.png')
blockimg=np.array(blockimg)

pixel_x = 80
pixel_y = 45

#check=blockimg[45][80]
#
#print(check)

breaker = False

for i in range(pixel_y - 2, pixel_y + 3):
    for j in range(pixel_x - 2, pixel_x + 3):
        if (49<blockimg[i][j][0] and blockimg[i][j][0]<76) and (133<blockimg[i][j][1] and blockimg[i][j][1]<206) and (104<blockimg[i][j][2] and blockimg[i][j][2]<158):
            print('I block')
            breaker = True
            break

        elif (83<blockimg[i][j][0] and blockimg[i][j][0]<122) and (68<blockimg[i][j][1] and blockimg[i][j][1]<104) and (125<blockimg[i][j][2] and blockimg[i][j][2]<213):
            print('J block')
            breaker = True
            break

        elif (177<blockimg[i][j][0] and blockimg[i][j][0]<201) and (101<blockimg[i][j][1] and blockimg[i][j][1]<119) and (55<blockimg[i][j][2] and blockimg[i][j][2]<78):
            print('L block')
            breaker = True
            break

        elif (162<blockimg[i][j][0] and blockimg[i][j][0]<209) and (146<blockimg[i][j][1] and blockimg[i][j][1]<170) and (55<blockimg[i][j][2] and blockimg[i][j][2]<78):
            print('O block')
            breaker = True
            break

        elif (125<blockimg[i][j][0] and blockimg[i][j][0]<160) and (180<blockimg[i][j][1] and blockimg[i][j][1]<207) and (50<blockimg[i][j][2] and blockimg[i][j][2]<93):
            print('S block')
            breaker = True
            break

        elif (148<blockimg[i][j][0] and blockimg[i][j][0]<213) and (60<blockimg[i][j][1] and blockimg[i][j][1]<104) and (144<blockimg[i][j][2] and blockimg[i][j][2]<183):
            print('T block')
            breaker = True
            break

        elif (164<blockimg[i][j][0] and blockimg[i][j][0]<210) and (55<blockimg[i][j][1] and blockimg[i][j][1]<96) and (60<blockimg[i][j][2] and blockimg[i][j][2]<82):
            print('Z block')
            breaker = True
            break
    
    if breaker == 1 :
        break