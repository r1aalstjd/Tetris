from copy import deepcopy
import pygame as pg
import numpy as np
import requests, copy, random, time, sys, lxml.html, math
from lxml.html import *
from dataclasses import dataclass
from operator import itemgetter
from pygame.color import THECOLORS
import multiprocessing as mp
from multiprocessing import Pool, Manager

from pprint import pprint

sys.setrecursionlimit(987654321)
clock = pg.time.Clock()

X_INDENT = 10
Y_INDENT = 5
DEBUG = False
INF = np.inf

generation_size = 30
next_gen_p = 5
learning_generation = 100
weight_num = 8

mutation_chance = 0.1
mutation_range = 20

LineWeight = 0
HoleWeight = 1
BlockHoleWeight = 2
MaxLevelWeight = 3
RoofWeight = 4
AdhereWallWeight = 5
AdhereFloorWeight = 6
DenseWeight = 7

#weight = [50, -15, -15, -15, -20, 10, 5, 10]

dfscnt = 0

game_board = [[0 for i in range(30)]for j in range(30)]
board_reset = [[0 for i in range(30)]for j in range(30)]
visit = [[0 for i in range(30)]for j in range(30)]

for j in range(30):
    game_board[25][j] = board_reset[25][j] = visit[25][j] = 1

dx = [0, 1, 1, 1, 0, -1, -1, -1]
dy = [1, 1, 0, -1, -1, -1, 0, 1]

WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]

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

blocks = [block_o, block_i, block_s, block_z, block_l, block_j, block_t]

generation = []

# GENETIC ALGORITHM ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓

def make_next_gen(parents):
    next_generation = []
    for k in range(generation_size):
        child = []
        for n in range(weight_num):
            p = random.randint(0, next_gen_p-1)
            child.append(parents[p][n])
        child.append(0)
        next_generation.append(child)
    return next_generation

def mutate(child):
    for i in range(weight_num):
        chance = random.random()
        if chance < mutation_chance:
            child[i] += random.randint(-mutation_range, mutation_range)
        if i == 0 or i == 5 or i == 6 or i == 7:
            child[i] = abs(child[i])
        else: child[i] = -abs(child[i])
    child[weight_num] = 0
    return child

# GENETIC ALGORITHM ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑

# STARTING WITH SPECIFIC GENE SET ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓

generation = [
    [40, -26, -3, -23, -81, 15, 47, 17, 0],

    [40, -26, -2, -23, -81, 14, 47, 16, 0],

    [40, -26, -4, -23, -81, 14, 47, 20, 0],

    [94, -26, -16, -23, -81, 14, 47, 16, 0],

    [94, -26, -16, -23, -81, 15, 47, 16, 0]
]

generation = make_next_gen(generation)

for i in generation:
    i = mutate(i)

# STARTING WITH SPECIFIC GENE SET ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑

#for i in range(generation_size):
#    gen = [random.randint(-99, 100) for i in range(weight_num)]
#    gen.append(0)
#    generation.append(gen)

def randomblock():
    global blocks
    randomlist = []
    for i in range(7):
        r = random.randint(0,6)
        while r in randomlist: r = random.randint(0,6)
        randomlist.append(r)
    blocklist = []
    while(len(randomlist)):
        blocklist.append(blocks[randomlist[0]])
        del randomlist[0]
    return blocklist

def PPRINT(board): # For debugging
    if DEBUG: return
    for i in range(5,25):
        for j in range(10,20):
            if(board[i][j]):print('■',end='')
            else: print('□',end='')
        print()
    print('- - - - - - - - - -')

#def PRINT_F(board):
#    if DEBUG: return
#    for i in range(5, 25):
#        st = ''
#        for j in range(10, 20):
#            if board[i][j]: st += 'X'
#            else: st += '.'
#        st += '\n'
#        txt.write(st)
#    txt.write('- - - - - - - - - -\n')

def PRINT_VISIT(board):
    if DEBUG: return
    for i in range(5, 25):
        for j in  range(10, 20):
            print(board[i][j], end = ' ')
        print()
    print('- - - - - - - - - -')

def getdensity(board, priv_board):
    cnt = 0
    for i in range(5, 25):
        for j in range(10, 20):
            if priv_board[i][j]:
                for k in range(0, 4):
                    n = k*2
                    p = i + dx[n]
                    q = j + dy[n]
                    if not priv_board[p][q] and board[p][q]: cnt += 1
    return cnt

def removeline(board):
    line = 0
    i = 24
    while i>4:
        cnt = 0
        for j in range(10, 20):
            cnt += board[i][j]
        if cnt == 10:
            line += 1
            for j in range(10,20):
                board[i][j] = 0
            t = i
            while t>0:
                for j in range(10, 20):
                    board[t][j], board[t-1][j] = board[t-1][j], board[t][j]
                t -= 1
            i = 25
        i -= 1
    return board, line

def dfs(x, y, board, visit, n):
    if x < X_INDENT or x > X_INDENT+9 or y > 24 or y < 0: return
    if visit[y][x] or board[y][x]: return
    global dfscnt
    visit[y][x] = n
    dfscnt += 1
    for i in range(4):
        k = i*2
        p = x + dx[k]
        q = y + dy[k]
        if not visit[q][p] and not board[q][p]:
            dfs(p, q, board, visit, n)

def collision(board, block_type, x, y): # Checks whether a block collides or not
    for i in range(y, y+4):
        for j in range(x, x+4):
            if board[i][j] != 0 and block_type[i-y][j-x] != 0: return 1
    return 0

def finding_void(block_type): # Returns the length of a block's left side void, making the block dropped from the left side of a board
    for x in range(4):
        for y in range(4):
            if block_type[y][x]: return x

def length_block(block_type): # Returns the horizonal length of a state of a block
    l = 0
    for x in range(4):
        for y in range(4):
            if block_type[y][x]:
                l += 1
                break
    return l

def block_drop(board, block_type, x): # Make a block be dropped on the board. Needs the x coord to use
    x += X_INDENT
    x -= finding_void(block_type)
    y = 0
    while True:
        if(collision(board, block_type, x, y)): break
        y += 1
    y -= 1
    for p in range(x, x+4):
        for q in range(y, y+4):
            if board[q][p] == 0: board[q][p] = block_type[q-y][p-x]

    return board

def getmaxlevel(board):
    maxlevel = 0
    for i in range(5, 25):
        cnt = 0
        for j in range(10,20):
            cnt += board[i][j]
        if cnt:
            return i
    return 24

def evaluation(board, priv_board, weight, block_shape): # Evaluates a state of a block by certain factors
    global dfscnt
    score = 0
    LineFill = 0
    Hole = 0
    Holecnt = 0
    BlockHole = 0
    AdhereWall = 0
    AdhereFloor = 0
    Roof = 0
    MaxLevel = 0
    Density = 0

    board, LineFill = removeline(board)
    
    temp_visit = deepcopy(board_reset)
    dfs(10, 0, board, temp_visit, 1)
    
    for i in range(24, 0, -1):
        cnt = 0
        for j in range(10, 20):
            if board[i][j]: cnt += 1
            elif not board[i][j] and not temp_visit[i][j]:
                dfscnt = 0
                Hole += 1
                dfs(j, i, board, temp_visit, 2)
                Holecnt += dfscnt
        if cnt == 10: LineFill += 1
        elif cnt == 0:
            MaxLevel = 24 - i
            break
    
    #PRINT_VISIT(temp_visit)

    for i in range(5, 25):
        AdhereWall += board[i][X_INDENT]
        AdhereWall += board[i][X_INDENT+9]
    for j in range(10,20):
        AdhereFloor += board[24][j]

    temp_visit2 = deepcopy(temp_visit)
    temp_visit = deepcopy(board_reset)

    for i in range(24, 4, -1):
        for j in range(10, 20):
            if not board[i][j] and not temp_visit[i][j] and temp_visit2[i][j] == 2:
                t = i
                while not board[t][j] and not temp_visit[t][j] and temp_visit2[t][j] == 2 and t >= MaxLevel:
                    temp_visit[t][j] = 1
                    t -= 1
                while board[t][j] and not temp_visit[t][j] and t >= MaxLevel:
                    temp_visit[t][j] = 1
                    t -= 1
                    BlockHole += 1

    Density = getdensity(board, priv_board)

    temp_visit = deepcopy(board_reset)

    for i in range(24, 4, -1):
        for j in range(10, 20):
            if not board[i][j] and not temp_visit[i][j] and temp_visit2[i][j] == 1:
                t = i
                while not board[t][j] and not temp_visit[t][j] and temp_visit2[t][j] == 1 and t > 0:
                    temp_visit[t][j] = 1
                    t -= 1
                while board[t][j] and not temp_visit[t][j] and t > 0:
                    temp_visit[t][j] = 1
                    t -= 1
                    Roof += 1


    score += LineFill * weight[LineWeight]

    score += Holecnt * weight[HoleWeight]

    score += BlockHole * weight[BlockHoleWeight]

    score += AdhereWall * weight[AdhereWallWeight]

    score += AdhereFloor * weight[AdhereFloorWeight]

    score += Roof * weight[RoofWeight]

    score += MaxLevel * weight[MaxLevelWeight]

    score += Density * weight[DenseWeight]

    if 0:
        print('L H HC  B AW AF R  M D')
        print('%d %d %2d %2d %2d %2d %d %2d %d' % (LineFill, Hole, Holecnt, BlockHole, AdhereWall, AdhereFloor, Roof, MaxLevel, Density))
        print(score)
        #st = 'L H HC  B AW AF R  M D\n'
        #st += '%d %d %2d %2d %2d %2d %d %2d %d\n%d\n' % (LineFill, Hole, Holecnt, BlockHole, AdhereWall, AdhereFloor, Roof, MaxLevel, Density, score)
        #txt.write(st)
    dfscnt = 0
    if MaxLevel >= 20: return -INF
    return score

def best_location(board, block_shape, weight): # Finding the best location and shape for a block, by simulating all 40(can be lower) situations
    best_possible = []

    for i in range(len(block_shape)):
        block_type = block_shape[i]
        void_front = finding_void(block_type)
        for x in range(0, 11 - length_block(block_type)):
            next_board = deepcopy(board)
            next_board = block_simulate(next_board, block_type, x)
            score = evaluation(next_board, board, weight, block_shape)
            score_set = [score, i, x]
            best_possible.append(score_set)
    
    best_possible.sort(key=itemgetter(0), reverse=True)
    return best_possible[0]

def block_simulate(board, block_type, x):
    board = block_drop(board, block_type, x)
    if 0:
        PPRINT(board)
        #PRINT_F(board)
    return board

#game_board = block_drop(game_board, block_i[1], 0)
#game_board = block_drop(game_board, block_i[1], 3)
#game_board = block_drop(game_board, block_i[0], 0)
#
#best_location(game_board, block_t)


def play_game(weight):
    global game_board
    line_del = 0
    line_score = 0
    game_board = deepcopy(board_reset)

    sprintbegin = time.time()

    pg.init()
    pg.display.set_caption('Tetris')
    icon = pg.image.load('../etc/1.png')
    pg.display.set_icon(icon)
    screen = pg.display.set_mode([270, 320])
    screen.fill([255, 255, 255])

    font = pg.font.SysFont('consolas', 30, True, False)
    font2 = pg.font.SysFont('consolas', 20, True, False)

    string1 = font.render("Next:", True, BLACK)
    string2 = font.render('Score', True, BLACK)
    string3 = font.render(str(line_score), True, BLACK)
    string4 = font2.render('Time', True, BLACK)
    string_time = font2.render('0:00:00', True, BLACK)

    screen.blit(string1, [185, 5])
    screen.blit(string2, [185, 95])
    screen.blit(string3, [185, 125])
    screen.blit(string4, [185, 230])
    screen.blit(string_time, [185, 260])

    for i in range(1, 22):
        pg.draw.rect(screen, [0, 0, 0], [5, 5+15*(i-1), 12, 12], 0)
        pg.draw.rect(screen, [0, 0, 0], [170, 5+15*(i-1), 12, 12], 0)

    for j in range(1, 11):
        pg.draw.rect(screen, [0, 0, 0], [5+15*j, 305, 12, 12], 0)

    pg. display.flip()

    running = True
    next_blocks = randomblock()
    while running:
        if len(next_blocks) <= 3:
            next_blocks.extend(randomblock())
        next_place = best_location(game_board, next_blocks[0], weight)
        #print(next_place)
        game_board = block_drop(game_board, next_blocks[0][next_place[1]], next_place[2])

        #Screen Clearing
        for i in range(5, 25):
            for j in range(X_INDENT, X_INDENT+10):
                pg.draw.rect(screen, WHITE,[5+15*(j-9), 5+15*(i-5), 15, 15])

        for i in range(0,4):
            for j in range(0,4):
                    pg.draw.rect(screen, WHITE, [185+15*j, 35+15*i, 15, 15], 0)

        # Next Block
        for i in range(0,4):
            for j in range(0,4):
                if next_blocks[1][0][i][j]:
                    pg.draw.rect(screen, BLUE, [185+15*j, 35+15*i, 12, 12], 0)

        # Game Board
        for i in range(5, 25):
            for j in range(X_INDENT, X_INDENT+10):
                if game_board[i][j]:
                    pg.draw.rect(screen, [128, 128, 128], [5+15*(j-9), 5+15*(i-5), 12, 12], 1)

        pg.display.flip()
        #time.sleep(0.15)

        game_board, line_del = removeline(game_board)
        line_score += line_del ** 2

        string3 = font.render(str(line_score), True, BLACK)

        current_time = round(time.time() - sprintbegin, 2)
        if current_time >= 3600: str_time = '59:59:99'
        else:
            current_min = round(current_time//60)
            current_sec = np.floor(current_time%60)
            current_milsec = round((current_time%1), 2) * 100
            str_time = '%02d' % current_min + ':' +'%02d' % current_sec + ':' + '%02d' % current_milsec
        
        string_time = font2.render(str_time, True, BLACK)
        
        for i in range(5, 25):
            for j in range(X_INDENT, X_INDENT+10):
                pg.draw.rect(screen, WHITE,[5+15*(j-9), 5+15*(i-5), 15, 15])

        pg.draw.rect(screen, WHITE, [185, 125, 100, 100])
        pg.draw.rect(screen, WHITE, [185, 260, 100, 30])

        for i in range(5, 25):
            for j in range(X_INDENT, X_INDENT+10):
                if game_board[i][j]:
                    pg.draw.rect(screen, [128, 128, 128], [5+15*(j-9), 5+15*(i-5), 12, 12], 1)

        screen.blit(string3, [185, 125])
        screen.blit(string_time, [185, 260])

        pg.display.flip()

        if(getmaxlevel(game_board)) <= 5:
            running = False
            print('Game Over\nBest Score : %d' % (line_score))
            break

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                print('Game has been Terminated\nScore : %d' % (line_score))
                break

        del next_blocks[0]
        #time.sleep(0.15)
    return line_score

Gene = [40, -26, -2, -23, -71, 14, 33, 16]
Gene = [94, -35, -16, -23, -81, 15, 47, 16]

if __name__ == '__main__':
    manager = mp.Manager()
    res = manager.list()
    cores = 5
    pool = mp.Pool(cores)
    result = pool.map(play_game, [(Gene) for i in range(0, 5)])
    pool.close()
    pool.join()
    print(list(result))