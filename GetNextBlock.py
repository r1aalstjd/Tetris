# GetNextBlock

import pyautogui as pag
from PIL import Image as img
import numpy as np

from pprint import pprint

debug = False

#pag.screenshot('./temp.png', region = (1145,270,160,90))
#
#blockimg=img.open('./temp.png')
#blockimg=np.array(blockimg)

block_o = [
    [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]
]

block_i = [
    [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ]
]

block_s = [
    [
        [0, 0, 0, 0],
        [0, 0, 1, 1],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ],
    [
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ]
]

block_z = [
    [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 0]
    ],
    [
        [0, 0, 0, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ],
]

block_l = [
    [
        [0, 0, 0, 1],
        [0, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 0]
    ],
    [
        [0, 0, 0, 0],
        [0, 1, 1, 1],
        [0, 1, 0, 0],
        [0, 0, 0, 0]
    ],
    [
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ]
]

block_j = [
    [
        [0, 1, 0, 0],
        [0, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    [
        [0, 0, 1, 1],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ],
    [
        [0, 0, 0, 0],
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ],
    [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]
]

block_t = [
    [
        [0, 0, 1, 0],
        [0, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    [
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ],
    [
        [0, 0, 0, 0],
        [0, 1, 1, 1],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ],
    [
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ]
]

def getnextblock():
    global debug
    pag.screenshot('./temp.png', region = (1145,270,160,90))
    blockimg=img.open('./temp.png')
    blockimg=np.array(blockimg)

    pixel_x = 80
    pixel_y = 45
    breaker = False

    for i in range(pixel_y - 8, pixel_y + 9):
        for j in range(pixel_x - 5, pixel_x + 6):
            if (49<blockimg[i][j][0] and blockimg[i][j][0]<76) and (133<blockimg[i][j][1] and blockimg[i][j][1]<206) and (104<blockimg[i][j][2] and blockimg[i][j][2]<158):
                if debug:
                    print('I block')
                    breaker = True
                    break
                return block_i

            elif (83<blockimg[i][j][0] and blockimg[i][j][0]<122) and (68<blockimg[i][j][1] and blockimg[i][j][1]<104) and (125<blockimg[i][j][2] and blockimg[i][j][2]<213):
                if debug:
                    print('J block')
                    breaker = True
                    break
                return block_j

            elif (177<blockimg[i][j][0] and blockimg[i][j][0]<201) and (101<blockimg[i][j][1] and blockimg[i][j][1]<119) and (55<blockimg[i][j][2] and blockimg[i][j][2]<78):
                if debug:
                    print('L block')
                    breaker = True
                    break
                return block_l

            elif (162<blockimg[i][j][0] and blockimg[i][j][0]<209) and (146<blockimg[i][j][1] and blockimg[i][j][1]<170) and (55<blockimg[i][j][2] and blockimg[i][j][2]<78):
                if debug:
                    print('O block')
                    breaker = True
                    break
                else: return block_o

            elif (125<blockimg[i][j][0] and blockimg[i][j][0]<160) and (180<blockimg[i][j][1] and blockimg[i][j][1]<207) and (50<blockimg[i][j][2] and blockimg[i][j][2]<93):
                print('S block')
                breaker = True
                break

            elif (148<blockimg[i][j][0] and blockimg[i][j][0]<213) and (60<blockimg[i][j][1] and blockimg[i][j][1]<104) and (144<blockimg[i][j][2] and blockimg[i][j][2]<183):
                if debug:
                    print('T block')
                    breaker = True
                    break
                return block_t

            elif (164<blockimg[i][j][0] and blockimg[i][j][0]<210) and (55<blockimg[i][j][1] and blockimg[i][j][1]<96) and (60<blockimg[i][j][2] and blockimg[i][j][2]<82):
                if debug:
                    print('Z block')
                    breaker = True
                    break
                return block_z
            
        if breaker == True :
            break

if __name__ == '__main__':
    debug = True
    getnextblock()