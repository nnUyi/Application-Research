# encoding=utf8
'''
created on 2019-06-21
@author chadyang
'''
import logging

logger = logging.getLogger(__name__)
# 设置log显示的级别
logger.setLevel(logging.DEBUG)
# 设置log输出目的地, 并设置写入模式：r,w,a
fh = logging.FileHandler('offline_cache_log.txt', 'w')
# 设置过滤器,是的logger名字为'my_logger'才会出现在log中
# 设置log输出格式
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
# 添加格式到文件句柄中
fh.setFormatter(formatter)
# 将文件句柄添加到logger中
logger.addHandler(fh)
