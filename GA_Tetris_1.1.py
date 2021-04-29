from copy import deepcopy
import pygame as pg
import numpy as np
import requests, copy, random, time, sys, lxml.html, math
from lxml.html import *
from dataclasses import dataclass
from operator import itemgetter
from pygame.color import THECOLORS

from pprint import pprint

sys.setrecursionlimit(987654321)

X_INDENT = 10
Y_INDENT = 5
DEBUG = False
INF = np.inf

generation_size = 30
next_gen_p = 5
learning_generation = 100
weight_num = 9

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
ComboWeight = 8

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
        if i == LineWeight or i == AdhereWallWeight or i == AdhereFloorWeight or i == DenseWeight or i == ComboWeight:
            child[i] = abs(child[i])
        else: child[i] = -abs(child[i])
    child[weight_num] = 0
    return child

# GENETIC ALGORITHM ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑ ↑

# STARTING WITH SPECIFIC GENE SET ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓

generation = [
    [40, -26, -3, -23, -81, 15, 47, 17, 89, 0],

    [40, -26, -2, -23, -81, 14, 47, 16, 31, 0],

    [40, -26, -3, -23, -81, 14, 47, 17, 95, 0],

    [40, -26, -2, -23, -81, 14, 47, 16, 3, 0],

    [94, -26, -4, -23, -81, 15, 47, 20, 43, 0]
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
    for i in range(15,25):
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
    global board_reset
    visit = deepcopy(board_reset)
    cnt = 0
    for i in range(5, 25):
        for j in range(10, 20):
            if priv_board[i][j]:
                for k in range(0, 4):
                    n = k*2
                    p = i + dx[n]
                    q = j + dy[n]
                    if not priv_board[p][q] and board[p][q] and not visit[p][q]:
                        cnt += 1
                        visit[p][q] = 1;
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

def evaluation(board, priv_board, weight, block_shape, combo): # Evaluates a state of a block by certain factors
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
    ComboAlive = False

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

    #if block_shape == block_j or block_shape == block_l or block_shape == block_s or block_shape == block_z:
    #    score += (LineFill * weight[LineWeight]) // 2
    
    score += (LineFill ** 2) * weight[LineWeight]

    #if block_shape == block_j or block_shape == block_l or block_shape == block_s or block_shape == block_z:
    #    score += Holecnt * weight[HoleWeight] * 2

    score += Holecnt * weight[HoleWeight]

    score += BlockHole * weight[BlockHoleWeight]

    score += AdhereWall * weight[AdhereWallWeight]

    score += AdhereFloor * weight[AdhereFloorWeight]

    score += Roof * weight[RoofWeight]

    score += MaxLevel * weight[MaxLevelWeight]

    score += Density * weight[DenseWeight]

    if combo and LineFill:
        score += weight[ComboWeight]
        ComboAlive = True

    if 0:
        print('LineFill : %d' % LineFill)
        print('Holecnt : %d' % Holecnt)
        print('BlockHole : %d' % BlockHole)
        print('AdhereWall : %d' % AdhereWall)
        print('AdhereFloor : %d' % AdhereFloor)
        print('Roof : %d' % Roof)
        print('MaxLevel : %d' % MaxLevel)
        print('Density : %d' % Density)
        print('Combo :', ComboAlive)
        print(score)
        #st = 'L H HC  B AW AF R  M D\n'
        #st += '%d %d %2d %2d %2d %2d %d %2d %d\n%d\n' % (LineFill, Hole, Holecnt, BlockHole, AdhereWall, AdhereFloor, Roof, MaxLevel, Density, score)
        #txt.write(st)
    dfscnt = 0
    if MaxLevel >= 20: return -INF, False
    return score, ComboAlive

def best_location(board, block_shape, weight, combo): # Finding the best location and shape for a block, by simulating all 40(can be lower) situations
    best_possible = []
    comboalive = False

    for i in range(len(block_shape)):
        block_type = block_shape[i]
        void_front = finding_void(block_type)
        for x in range(0, 11 - length_block(block_type)):
            next_board = deepcopy(board)
            next_board = block_simulate(next_board, block_type, x)
            score, comboalive = evaluation(next_board, board, weight, block_shape, combo)
            score_set = [score, i, x, comboalive]
            best_possible.append(score_set)
    
    best_possible.sort(key=itemgetter(3), reverse=True)
    best_possible.sort(key=itemgetter(0), reverse=True)
    return best_possible[0]

def block_simulate(board, block_type, x):
    board = block_drop(board, block_type, x)
    if 0:
        PPRINT(board)
    return board

def play_game(weight, gen, child):
    gen += 1
    child += 1
    global game_board
    line_del = 0
    line_score = 0
    Combo = 0
    game_board = deepcopy(board_reset)

    pg.init()
    pg.display.set_caption('Tetris')
    icon = pg.image.load('../etc/1.png')
    pg.display.set_icon(icon)
    screen = pg.display.set_mode([270, 320])
    screen.fill([255, 255, 255])

    font = pg.font.SysFont('consolas', 30, True, False)
    font2 = pg.font.SysFont('consolas', 20, True, False)

    string1 = font.render("Next:", True, BLACK)
    string2 = font2.render('Gen ', True, BLACK)
    string_gen = font2.render(str(gen), True, BLACK)
    string_child = font.render('%2d' % child + '/' + str(generation_size), True, BLACK)
    string3 = font2.render('Score', True, BLACK)
    string_score = font2.render(str(line_score), True, BLACK)
    string4 = font2.render('Combo', True, BLACK)
    string_combo = font2.render(str(Combo), True, BLACK)

    screen.blit(string1, [185, 5])
    screen.blit(string2, [185, 95])
    screen.blit(string_gen, [235, 95])
    screen.blit(string_child, [185, 125])
    screen.blit(string3, [185, 185])
    screen.blit(string_score, [185, 215])
    screen.blit(string4, [185, 245])
    screen.blit(string_combo, [185, 275])

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
        next_place = best_location(game_board, next_blocks[0], weight, Combo)
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

        game_board, line_del = removeline(game_board)
        line_score += line_del ** 2
        string_score = font2.render(str(line_score), True, BLACK)
        if line_del: Combo += 1
        else: Combo = 0
        
        # Screen Clearing
        for i in range(5, 25):
            for j in range(X_INDENT, X_INDENT+10):
                pg.draw.rect(screen, WHITE,[5+15*(j-9), 5+15*(i-5), 15, 15])

        pg.draw.rect(screen, WHITE, [185, 215, 100, 30])

        for i in range(5, 25):
            for j in range(X_INDENT, X_INDENT+10):
                if game_board[i][j]:
                    pg.draw.rect(screen, [128, 128, 128], [5+15*(j-9), 5+15*(i-5), 12, 12], 1)

        screen.blit(string_score, [185, 215])

        string_combo = font2.render(str(Combo), True, BLACK)

        pg.draw.rect(screen, WHITE, [185, 275, 100, 30])

        screen.blit(string_combo, [185, 275])

        pg.display.flip()

        if(getmaxlevel(game_board)) <= 5:
            running = False
            print('Gen #%d, Child #%d, Score : %d' % (gen, child, line_score))
            break

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                print('Gen #%d, Child #%d (Terminated), Score : %d' % (gen, child, line_score))
                break

        del next_blocks[0]
        #time.sleep(0.01)
    return line_score

for gen in range(learning_generation):
    play_score = []
    next_gen = []

    for child in range(generation_size):
        generation[child][weight_num] = play_game(generation[child], gen, child)
        play_score.append(generation[child])

    play_score.sort(key=itemgetter(weight_num), reverse=True)

    txt = open('./Weights_1.1.txt', 'a')
    pprint(play_score[0])
    for nxt in range(0,5):
        st = ''
        for i in play_score[nxt]:
            st += '%7d,' % i
        txt.write('[ ' + st + ' ] #' + str(gen+1) + '\n')
    txt.write('- - - - - - - - - - - - - - - - - - - - - - - - - #' + str(gen+1) + '\n\n')

    for child in range(next_gen_p):
        next_gen.append(play_score[child])
    txt.close()

    generation = make_next_gen(next_gen)

    for child in generation:
        mutate(child)