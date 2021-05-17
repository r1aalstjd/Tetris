import multiprocessing as mp
from multiprocessing import Manager
import time


def g(k):
    return k*10000, (k+1)*10000

def f(k, result):
    a, b = g(k)
    for i in range(a, b):
        result.append(i)
    return result

if __name__ == '__main__':
    begin = time.time()
    manager = Manager()
    result = manager.list()
    procs = []

    for i in range(1, 6):
        proc = mp.Process(target=f, args=(i, result))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
    #print(result)
    print(float(time.time()-begin))
    l = list(result)
    print(len(l))

    begin = time.time()
    p = []
    for i in range(0, 60000):
        p.append(i)
    print(float(time.time()-begin))