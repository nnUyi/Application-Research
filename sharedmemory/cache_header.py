import ctypes
import os
import struct

import numpy as np

class CacheHeader:
    #=========================================================================
    # Cache Header
    #=========================================================================
    s_cache_magic_id = 190701115

    def __init__(self):
        self.magic_id = 0
        self.cross_obstacle_num = 0
        self.dtype_str = ""  # 固定三个
        self.shape = ()
        self.high_level = ()

    def DebugInit(self):
        self.magic_id = CacheHeader.s_cache_magic_id
        self.cross_obstacle_num = 2
        self.dtype_str = ">i4"  # 固定三个
        self.shape = (3360000, 2, 240)
        self.high_level_list = (0.3, 0.9)

    def _PackIntList(self, int_list, is_float=False):
        in_len = len(int_list)
        if is_float:
            rel = struct.pack("@I" + str(in_len) + "f", in_len, *int_list)
        else:
            rel = struct.pack("@I" + str(in_len) + "I", in_len, *int_list)
        return rel

    def _UnpackIntList(self, in_str_all, is_float=False):
        arr_len, = struct.unpack("@I", in_str_all[:4])
        off_set = 4
        unpack_tuple = ()  # 空tuple

        if arr_len > 0:
            if is_float:
                fmt = "@" + str(arr_len) + "f"
            else:
                fmt = "@" + str(arr_len) + "i"
            calc_size = struct.calcsize(fmt)
            off_set += calc_size
            unpack_tuple = struct.unpack(fmt, in_str_all[4:off_set])
        return True, unpack_tuple, off_set

    def ToString(self):
        return "magic_id {} cross_obstacle_num {} dtype {} shape {} high_level {}".format(
            self.magic_id,
            self.cross_obstacle_num,
            self.dtype_str,
            self.shape,
            self.high_level)

    def Pack(self):

        dtype_len = len(self.dtype_str)
        first_pack = struct.pack(
            "@II" + str(dtype_len) + "s",
            self.cross_obstacle_num, dtype_len, self.dtype_str)
        shape_pack = self._PackIntList(self.shape)
        high_level_pack = self._PackIntList(
            self.high_level, is_float=True)

        content = first_pack + shape_pack + high_level_pack
        content_len = len(content)

        rel = struct.pack("@II" + str(content_len) + "s",
                          self.magic_id, content_len, content)
        return rel

    def UnPackFromCPtr(self, in_c_int_ptr):
        self.magic_id, = struct.unpack("@I", ctypes.string_at(in_c_int_ptr, 4))
        if self.magic_id != CacheHeader.s_cache_magic_id:
            return False
        str_len, = struct.unpack("@I", ctypes.string_at(in_c_int_ptr + 4, 4))
        str_len += 4 + 4  # 加上前面的magic和总长度，所有有两个4
        total_header_str = ctypes.string_at(in_c_int_ptr, str_len)
        return self.UnPackFromPyStr(total_header_str), str_len

    def UnPackFromPyStr(self, total_header_str):
        # 这个函数还是需要检查一下magicid
        ptr_index = 0
        self.magic_id, total_len = struct.unpack(
            "@II", total_header_str[ptr_index: ptr_index + 8])
        if self.magic_id != CacheHeader.s_cache_magic_id:
            return False
        ptr_index += 8

        self.cross_obstacle_num, = struct.unpack(
            "@I", total_header_str[ptr_index: ptr_index + 4])
        ptr_index += 4

        dtype_len, = struct.unpack(
            "@I", total_header_str[ptr_index: ptr_index + 4])
        ptr_index += 4

        if dtype_len > 0:
            self.dtype_str, = struct.unpack(
                "@" + str(dtype_len) + "s", total_header_str[ptr_index: ptr_index + dtype_len])
            ptr_index += dtype_len

        _, self.shape, off_set = self._UnpackIntList(
            total_header_str[ptr_index:])
        ptr_index += off_set
        _, self.high_level_list, off_set = self._UnpackIntList(
            total_header_str[ptr_index:], is_float=True)
        return True

def TestCacheHeaderHead():
    head = CacheHeader()
    head.DebugInit()
    print head.ToString()
    ss = head.Pack()
    print len(ss)
    head2 = CacheHeader()
    head2.UnPackFromPyStr(ss)
    print head2.ToString()

if __name__ == '__main__':
    TestCacheHeaderHead()
