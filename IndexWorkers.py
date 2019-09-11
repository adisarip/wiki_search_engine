#!/usr/bin/env python

# Test script to show how to invoke multiple processes

import multiprocessing as mp
import time

def calc_square(queue):
    while not queue.empty():
        try:
            num = queue.get(False)
            print(mp.current_process().name, " Square of", num, "=", num*num)
            time.sleep(1)
        except:
            pass

if __name__ == "__main__":
    queue = mp.Queue()
    [queue.put(x) for x in range(1, 10)]
    l_processes = [mp.Process(target=calc_square,
                              args=(queue,))
                              for x in range(5)]

    for p in l_processes:
        p.start()

    for p in l_processes:
        p.join()


