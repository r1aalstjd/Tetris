import numpy as np
from random import *
from pprint import pprint
from operator import itemgetter
import matplotlib
import matplotlib.pyplot as plt

debug = True

generation_size = 50
next_gen_p = 5
learning_generation = 100
weight_num = 7

mutation_chance = 0.2
mutation_range = 50

LineWeight = 0
HoleWeight = 1
MaxLevelWeight = 2
RoofWeight = 3
AdhereWallWeight = 4
AdhereFloorWeight = 5

weight = [0 for i in range(weight_num)]

goal = [10, 47, 48, -943, 32, 1, 331]

generation = []
empty_list = []

graph_x = [i for i in range(learning_generation)]
graph_y = []

def play_game(weight):
    score = 0
    for i in range(weight_num):
        score += abs(goal[i] - weight[i])
    return score

def make_next_gen(parents):
    next_generation = []
    for k in range(generation_size):
        child = []
        for n in range(weight_num):
            p = randint(0, next_gen_p-1)
            child.append(parents[p][n])
        child.append(0)
        next_generation.append(child)
    return next_generation

def mutate(child):
    for i in range(weight_num):
        chance = random()
        if chance < mutation_chance:
            child[i] += randint(-mutation_range, mutation_range)
    child[weight_num] = 0
    return child


for i in range(generation_size):
    gen = [randint(-999, 1000) for i in range(weight_num)]
    gen.append(0)
    generation.append(gen)

pprint(generation)
print('- - - - - - - - - - - parents')

for gen in range(learning_generation):
    play_score = []
    next_gen = []

    for child in range(generation_size):
        generation[child][weight_num] = play_game(generation[child])
        play_score.append(generation[child])

    play_score.sort(key=itemgetter(weight_num))

    #pprint(generation)
    #print('- - - - - - - - - - - gen : %d' % gen)

    graph_y.append(play_score[0][weight_num])
    pprint(play_score[0])

    for child in range(next_gen_p):
        next_gen.append(play_score[child])

    generation = make_next_gen(next_gen)

    for child in generation:
        mutate(child)

print('- - - - - - - - - - -')
pprint(goal)

plt.plot(graph_x, graph_y)
plt.show()

