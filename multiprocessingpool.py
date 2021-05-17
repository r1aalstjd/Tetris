import multiprocessing as mp
from multiprocessing import Pool
import os

def g(k):
    return k*10000, (k+1)*10000

def f(a, b):
    #a, b = g(k)
    t = []
    for i in range(a, b):
        t.append(i)
    print(os.getpid())
    return t

if __name__ == '__main__':
    m = mp.Manager()
    result = m.list()
    cores = 5
    pool = mp.Pool(cores)
    result = pool.starmap(f, [(i*10000, (i+1)*10000) for i in range(1, 21)])
    pool.close()
    pool.join()
    print()
    print(len(list(result)))
    for i in result:
        print(len(i), i[0], i[len(i)-1])