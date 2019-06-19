# encoding=utf8
'''
created on 2019-06-19 16:44
@author chadyang
'''

import logging
#====================================================
                # 直接使用logging
#====================================================
'''
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='test.log',
                    filemode='w')
'''
#====================================================
                # 使用logger模块
#====================================================
# 创建一个logger
logger = logging.getLogger('my_logger')
# 设置log显示的级别
logger.setLevel(logging.DEBUG)
# 设置log输出目的地, 并设置写入模式：r,w,a
fh = logging.FileHandler('my_log.txt', 'a')
# 设置过滤器,是的logger名字为'my_logger'才会出现在log中
filter = logging.Filter('my_logger')
# 添加过滤器到文件句柄中
fh.addFilter(filter)
# 设置log输出格式
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
# 添加格式到文件句柄中
fh.setFormatter(formatter)
# 将文件句柄添加到logger中
logger.addHandler(fh)

if __name__ == '__main__':
    '''
    logging.debug('debug message')
    logging.info('info message')
    logging.warning('warning message')
    logging.error('error message')
    logging.critical('critical message')
    '''
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')
