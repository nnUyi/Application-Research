# Intern
  Summary in the period of Intern in Tencent

## Week 1
  Nothing but ...

## Week 2 
  - memory analysis
  - multiple threads
  - shared memory read/write

## Week 3
  - git merge
  - multi-processes for data preprocessing
  - logging usage

# 离线cache生成
## 1. 代码框架
  - offline_cache_generator/offline_cache_gen.py
  
      ***用于分离热点数据，使用多进程生成热点 `（120个方向）` 到障碍物的距离，合并生成的文件保存为npz格式***

  - offline_cache_generator/gen_vision_feature.py
 
      ***计算热点`（120个方向）`到障碍物的距离***
      
  - offline_cache_generator/logging_config.py
  
      ***logger的相关配置，用于记录日志， 日志默认记录在`offline_cache_log.txt`中***

  - offline_cache_generator/setting.py
  
      ***程序的基本配置信息***

## 2. 使用流程
### (1) 流程控制:
  代码分为三个过程：分离热点数据，使用多进程生成热点`（120个方向）`到障碍物的距离，合并生成的文件保存为npz格式
  
  - is_datasplit_enable = True [[setting.py line39]()]
  - is_mp_enable = True [[setting.py line41]()]
  - is_datamerge_enable = [True [setting.py line43]()]
      
### (2) 程序配置
- num_hot_points = 560000 [[热点数量：setting.py line45]()]
- num_threads = 12 [[进程数量: setting.py line51]()]
- input_obj_path = '../PVP_CF_Ship.obj' [[运输船地图路径: setting.py line49]()]
- save_dir = './data_test' [[文件保存文件夹: setting.py line53]()]
      
### (3) logging配置
- logger.setLevel [[设置日志记录级别：logging_config.py line6]()]
- logging.FileHandler [[设置日志输出目标文件：logging_config.py line8]()]
- logging.Formatter [[设置日志输出条目格式：logging_config.py line11]()]

### (4) 程序运行
  ```bash
      $ python offline_cache_gen.py
  ```
