# coding=utf8
'''
created on 2019-06-14 15:16
@author: chadyang

c++中访问linux共享内存，共享内存函数由shmget、shmat、shmdt、shmctl四个函数组成， 在python中可以导入ctypes库，然后将c++中的libc_so链接到程序中,使用这四个函数：
    shmget:
    	int shmget(key_t key, size_t size, int shmflg)
	    Params:
		key: 0(IPC_PRIVATE)：会建立新共享内存对象
		     大于0的32位整数：视参数shmflg来确定操作。通常要求此值来源于ftok返回的IPC键值
		size: 大于0的整数：新建的共享内存大小，以字节为单位
		      0：只获取共享内存时指定为0
		shmflg: 0：取共享内存标识符，若不存在则函数会报错
			IPC_CREAT：当shmflg&IPC_CREAT为真时，如果内核中不存在键值与key相等的共享内存，则新建一个共享内存；\\
									如果存在这样的共享内存，返回此共享内存的标识符
			IPC_CREAT|IPC_EXCL：如果内核中不存在键值与key相等的共享内存，则新建一个消息队列；如果存在这样的共享内存则报错
	    Return:
	    	成功：返回共享内存的标识符
		出错：-1，错误原因存于error中

    shmat:
    	void *shmat(int shmid, const void *shmaddr, int shmflg)
	    Params:
		msqid: 共享内存标识符
		shmaddr: 指定共享内存出现在进程内存地址的什么位置，直接指定为NULL让内核自己决定一个合适的地址位置
		shmflg: SHM_RDONLY：为只读模式，其他为读写模式
	    Return:
	    	成功：附加好的共享内存地址
		出错：-1，错误原因存于error中

    shmdt断开共享内存连接):
    	int shmdt(const void *shmaddr)
	    Params:
	    	shmaddr：连接的共享内存的起始地址
	    Return:
	    	成功：0
		出错：-1，错误原因存于error中

    shmctl:
    	int shmctl(int shmid, int cmd, struct shmid_ds *buf)
	    Params:
		shmid: 共享内存标识符
		cmd: IPC_STAT：得到共享内存的状态，把共享内存的shmid_ds结构复制到buf中
		     IPC_SET：改变共享内存的状态，把buf所指的shmid_ds结构中的uid、gid、mode复制到共享内存的shmid_ds结构内
		     IPC_RMID：删除这片共享内存
		buf:
		     共享内存管理结构体。具体说明参见共享内存内核结构定义部分
	    Return:
	        成功：0
		出错：-1，错误原因存于error中
'''

import sys
import ctypes
import numpy

try:
    import cPpickle as pickle
except ImportError:
    import pickle

libc_so = {"darwin": "libc.dylib", "linux2": ""}[sys.platform]
libc = ctypes.CDLL(libc_so, use_errno=True, use_last_error=True)

get_errno_loc = libc.__errno_location
get_errno_loc.restype = ctypes.POINTER(ctypes.c_int)

shm_key_t = ctypes.c_int
IPC_PRIVATE = 0
IPC_RMID = 0
IPC_CREATE = 01000  # Create key if key does not exist.
IPC_EXCL = 02000   # Fail if key exists.

# int shmget(key_t key, size_t size, int shmflg);
shmget = libc.shmget
shmget.restype = ctypes.c_int
shmget.argtypes = (shm_key_t, ctypes.c_size_t, ctypes.c_int)
# void* shmat(int shmid, const void *shmaddr, int shmflg);
shmat = libc.shmat
shmat.restype = ctypes.c_void_p
shmat.argtypes = (ctypes.c_int, ctypes.c_void_p, ctypes.c_int)
# int shmdt(const void *shmaddr);
shmdt = libc.shmdt
shmdt.restype = ctypes.c_int
shmdt.argtypes = (ctypes.c_void_p,)
# int shmctl(int shmid, int cmd, struct shmid_ds *buf);
shmctl = libc.shmctl
shmctl.restype = ctypes.c_int
shmctl.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_void_p)
# void* memcpy( void *dest, const void *src, size_t count );
memcpy = libc.memcpy
memcpy.restype = ctypes.c_void_p
memcpy.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)

# shm key
index_shm_key = 123456
value_shm_key = 123457

class SharedMem:
    def __init__(self, size, shm_key=0):
        self.size = size
        self.shmid = shmget(shm_key, self.size, 0o666 | IPC_CREATE | IPC_EXCL)
        assert self.shmid > 0
        self.ptr = shmat(self.shmid, 0, 0)
        assert self.ptr

    def remove(self):
        shmdt(self.ptr)
        self.ptr = None
        #shmctl(self.shmid, IPC_RMID, 0)
        #self.shmid = None

    def __del__(self):
        self.remove()

class A:
    pass

def SetShmMemory():
    index_np, value_np = LoadNumpyByPkl("./index_560000_np",
                                        "./value_560000_np")
    SetShmMemoryByNp(index_np, index_shm_key)
    SetShmMemoryByNp(value_np, value_shm_key)

def LoadNumpyByPkl(index_path, value_path):
    with open(index_path, 'rb') as r_index:
        index = pickle.load(r_index)
    with open(value_path, 'rb') as r_value:
        value = pickle.load(r_value)
    return index, value

def SetShmMemoryByNp(np_data, shm_key):
    mem = SharedMem(np_data.nbytes, shm_key)
    memcpy(mem.ptr, np_data.ctypes.data, np_data.nbytes)

def GetIndexShmMemoryToNp(index_shm_key):
    shmid = shmget(index_shm_key, 0, 0)
    assert shmid > 0
    ptr = shmat(shmid, 0, 0)

    array_int = {
        "shape": (560000, 3),
        'typestr': '<i4',  # int32
        "version": 3  # static
    }
    array_int["data"] = (ptr, False)

    a = A()
    a.__array_interface__ = array_int
    cache_index = numpy.array(a, copy=False)
    # release the pointer
    shmdt(ptr)

    return cache_index

def GetValueShmMemoryToNpFloat(value_shm_key):
    shmid = shmget(value_shm_key, 0, 0)
    assert shmid > 0
    ptr = shmat(shmid, 0, 0)
    assert ptr

    array_float = {
        "shape": (560000, 2, 240),
        'typestr': '<f4',  # float32
        "version": 3  # static
    }
    array_float["data"] = (ptr, False)

    a = A()
    a.__array_interface__ = array_float
    cache_value = numpy.array(a, copy=False)
    # release the pointer
    shmdt(ptr)

    return cache_value

def GetCacheNumpy():
    global index_shm_key, value_shm_key
    index_shmid = shmget(index_shm_key, 0, 0)
    value_shmid = shmget(value_shm_key, 0, 0)
    if index_shmid <=0 or value_shmid <=0:
	SetShmMemory()
    cache_value = GetValueShmMemoryToNpFloat(value_shm_key)
    cache_index = GetIndexShmMemoryToNp(index_shm_key)
    return cache_index, cache_value

def FreeCacheNumpy():
    global index_shm_key, value_shm_key
    index_shmid = shmget(index_shm_key, 0, 0)
    value_shmid = shmget(value_shm_key, 0, 0)

    shmctl(index_shmid, IPC_RMID, 0)
    shmctl(value_shmid, IPC_RMID, 0)

def Client():
    cache_index, cache_value = GetCacheNumpy()
    print('This is a test client')
    print(cache_index.shape, cache_value.shape)

if __name__ == "__main__":
    import psutil
    import os
    import multiprocessing as mp
    pid = os.getpid()
    process = psutil.Process(pid)
    sm = process.memory_full_info().rss/1024.0/1024.0
    cache_index, cache_value = GetCacheNumpy()
    em = process.memory_full_info().rss/1024.0/1024.0
    print('memory costing:{}'.format(em-sm))
    print(cache_index.shape, cache_value.shape)
    #FreeCacheNumpy()
    client = mp.Process(target=Client, args=())
    client.start()
    em = process.memory_full_info().rss/1024.0/1024.0
    print('memory costing:{}'.format(em-sm))
    client.join()
