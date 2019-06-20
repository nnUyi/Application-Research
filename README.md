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
## 代码框架
  - offline_cache_generator
      - offline_cache_gen.py
      
          用于分离热点数据，使用多进程生成热点（120个方向）到障碍物的距离，合并生成的文件保存为npz格式
          
      - gen_vision_feature.py
      
          计算热点（120个方向）到障碍物的距离
          
      - logging_config.py
      
          logger的相关配置，用于记录日志
         
      - setting.py             
          程序的基本配置信息

## 使用流程
  (1) 流程控制:
      代码分为三个模块：分离热点数据，使用多进程生成热点（120个方向）到障碍物的距离，合并生成的文件保存为npz格式
      - is_datasplit_enable = True [setting.py line39]
      - is_mp_enable = True [setting.py line41]
      - is_datamerge_enable = True [setting.py line43]
