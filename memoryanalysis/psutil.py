# coding=utf-8
'''
created on 2019-06-14 15:16

@author: chadyang
'''
import sys
import psutil
import numpy as np
import os

if __name__ == '__main__':
    pid = os.getpid()
    process = psutil.Process(pid)
    sm = process.memory_full_info().rss/1024.0/1024.0
    array = np.random.uniform(-1,-1, (100,100)).astype(np.float32)
    em = process.memory_full_info().rss/1024.0/1024.0
    print('memory costing:{}'.format(em-sm))
    
    bytes_occpy = sys.getsizeof(array)
    print('bytes occupation:{}'.format(bytes_occpy))
