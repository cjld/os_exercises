import threading as th
import random

num_a, num_b = 0, 0

n,m = 10, 5

sa, sb = th.Semaphore(0), th.Semaphore(0)

def save_a():
    sa.release()
def save_b():
    sb.release()
def getab():
    sa.acquire(), sb.acquire()


func_list = [save_a, save_b, getab]
threads = []

for i in range(0,100):
    threads.append(th.Thread(target = func_list[random.randint(0,2)]))

for t in threads: t.start()

for t in threads: t.join()
