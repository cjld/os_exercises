import threading as th
import random

num_a, num_b = 0, 0

n,m = 10, 5

cond = th.Condition()

def run_cond(next_status):
    while 1:
        cond.acquire()
        new_a, new_b = next_status(num_a, num_b)
        if ck_cond(new_a, new_b):
            num_a, num_b = new_a, new_b
            cond.notify()
        else:
            cond.wait()
        cond.release()

def save_a():
    run_cond(lambda x,y: (x+1,y))

def save_b():
    run_cond(lambda x,y: (x,y+1))

def getab():
    run_cond(lambda x,y: (x-1,y-1))

func_list = [save_a, save_b, getab]
threads = []

for i in range(0,100):
    threads.append(th.Thread(target = func_list[random.randint(0,2)]))

for t in threads: t.start()

for t in threads: t.join()
