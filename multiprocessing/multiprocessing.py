# coding = utf-8
'''
created on 2019-06-14 15:16
@author: chadyang

threading和multiprocessing的区别：
    threading：只能利用一个cpu核，然后空闲时分段计算
    multiprocessing：可以利用多个CPU核，并行计算
'''

import threading
import multiprocessing as mp
import time

def thread1(thread_id):
    print('This is thread{}!!!'.format(thread_id))
    time.sleep(5)
    print('sleeping 5 seconds in thread {}!!!'.format(thread_id))

def test_threading():
    '''
      1 python 默认参数创建线程后，不管主线程是否执行完毕，都会等待子线程执行完毕才一起退出，有无join结果一样
      
      2 如果创建线程，并且设置了daemon为true，即thread.setDaemon(True), 则主线程执行完毕后自动退出，不会等待子线程的执行结果。
        而且随着主线程退出，子线程也消亡。

      3 join方法的作用是阻塞，等待子线程结束，join方法有一个参数是timeout，即如果主线程等待timeout，子线程还没有结束，则主线程强制结束子线程。

      4 如果线程daemon属性为False， 则join里的timeout参数无效。主线程会一直等待子线程结束。

      5 如果线程daemon属性为True， 则join里的timeout参数是有效的， 主线程会等待timeout时间后，结束子线程。此处有一个坑，
        即如果同时有N个子线程join(timeout），那么实际上主线程会等待的超时时间最长为 N ＊ timeout，
        因为每个子线程的超时开始时刻是上一个子线程超时结束的时刻。
    '''
    threads = []
    for i in range(3):
        thread = threading.Thread(target=thread1, args=(i,))
        threads.append(thread)
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()

def test_multiprocessing():
    threads_mp = []
    for i in range(3):
        thread = mp.Process(target=thread1, args=(i,))
        threads_mp.append(thread)
    for t in threads_mp:
        t.daemon = True
        t.start()
    for t in threads_mp:
        t.join()


if __name__ == '__main__':
    test_threading()
    test_multiprocessing()
