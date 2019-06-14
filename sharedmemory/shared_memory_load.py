# coding=utf8
'''
created on 2019-06-14 15:16

@author: chadyang
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
