# encoding=utf8
'''
created on 2019-06-18 12:08
@author chadyang
'''

import gen_vision_feature as position_calcer
import setting
from logging_config import logger

import os
import numpy as np
import multiprocessing as mp

#================================  cache生成  =======================================
class DataProcess(mp.Process):
    #==============================================================================
                                    # 数据处理进程器
    #==============================================================================
    def __init__(self, head_list, feature_calcer, config):
        mp.Process.__init__(self)
        self.head_list = head_list

        keys = config.keys()
        self.index_path = config[keys[1]]
        self.value_path = config[keys[0]]

        self.precal_index = []
        self.precal_value = []

        self.feature_calcer = feature_calcer

    def run(self):
        logger.info('{} start'.format(self.name))
        # 计算120个方向的障碍物
        self.CalcDirection()
        # pickle将数据保存
        self.SaveNumpyByNpy()
        logger.info('{} end'.format(self.name))

    def CalcDirection(self):
        # =========================================================================
        # 根据出入obj文件和热点位置xyz坐标，计算热点位置的120个方向到障碍物距离结果，
        # 存放在precalc_array中(cache)
        # =========================================================================
        for line in self.head_list:
            x, y, z = line
            cache_direction_low = self.feature_calcer.get_eight_direction(
                [x, y, z], [0, 0, 0], 0.3)
            cache_direction_high = self.feature_calcer.get_eight_direction(
                [x, y, z], [0, 0, 0], 0.9)

            self.precal_index.append(line)
            self.precal_value.append([cache_direction_low, cache_direction_high])

    def SaveNumpyByNpy(self):
        #=========================================================================
        # 把cache save到npy文件
        #=========================================================================
        if len(self.precal_index) != 0 and len(self.precal_value) != 0:
            np.save(self.index_path, np.array(self.precal_index).astype(np.int32))
            np.save(self.value_path, np.array(self.precal_value).astype(np.float32))
        else:
            logger.error('DataProcess: data flow is empty!!!')
            raise Exception('DataProcess: data flow is empty!!!')

def _DataSplit():
    # =========================================================================
    # 从thin_all_sort分离出所需要的数据，并保存为tuple形式(x,y,z)
    # =========================================================================
    count = 0
    head_list = []
    try:
        with open(setting.sorted_coord_path, 'rb') as reader:
            for line in reader:
                x,y,z = map(int, line.split("\t")[0].split("_"))
                head_list.append((x,y,z))
                count += 1
                if count >= setting.num_hot_points:
                    break
    except IOError:
        logger.error('_DataSplit: file {} not exists'.format(setting.sorted_coord_path))
        raise Exception('_DataSplit: fail to open {}'.format(setting.sorted_coord_path))
    # 对(x,y,z)按照坐标元组排序(升序)
    head_list.sort()
    return  head_list

def _DataMerge(index_list, value_list, save_list):
    # =========================================================================
    # 归并各个进程处理得到的数据块,保存为npz压缩格式
    # =========================================================================
    index, value = [],[]
    try:
        for index_path, value_path in zip(index_list, value_list):
            with open(index_path, 'rb') as r_index:
                index.append(np.load(r_index))
            with open(value_path, 'rb') as r_value:
                value.append(np.load(r_value))

            # 获取文件数据之后自动删除文件
            os.system('rm {}'.format(index_path))
            os.system('rm {}'.format(value_path))
        index = np.concatenate(index, 0)
        value = np.concatenate(value, 0)
        np.savez_compressed(save_list[0], index=index)
        np.savez_compressed(save_list[1], value=value)
    except IOError:
        logger.error('_DataMerge: file path not exists!!!')
        raise Exception('_DataMerge: fail to open file for merging!!!')

if __name__ == '__main__':
    head_list = []
    if not os.path.exists(setting.save_dir):
        os.mkdir(setting.save_dir)
    # 数据分离
    if setting.is_datasplit_enable:
        head_list = _DataSplit()

    # 数据处理
    if setting.is_mp_enable:
        assert head_list
        threads = []
        gap = setting.num_hot_points/setting.num_threads
        config = dict()
        feature_calcer = position_calcer.GridMapGener(setting.input_obj_path)
        # 启动多进程
        for i in range(setting.num_threads):
            config['index_path'] = setting.index_list[i]
            config['value_path'] = setting.value_list[i]
            if i==setting.num_threads-1:
                thread = DataProcess(head_list[i*gap:], feature_calcer, config)
            else:
                thread = DataProcess(head_list[i*gap: (i+1)*gap], feature_calcer, config)
            threads.append(thread)
            thread.start()
        # 阻塞进程
        for thread in threads:
            thread.join()

    # 数据合并
    if setting.is_datamerge_enable:
        # 合并数据
        _DataMerge(setting.index_list, setting.value_list, setting.save_list)
