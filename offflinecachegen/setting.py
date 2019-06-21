#coding=utf-8
# 是否计算feature
is_calc_feature=True
# 是否输出入中间的一些debug文件，默认不要输出
is_debug_print_file=False
# 是否采用本地debug模式，方便本地调试用而已
is_debug = False
# 是否不转换，直接使用武器id
is_output_org_weaponid = True

# 补帧的帧号是否取反
is_fillup_frame_index_neg = True

#日志文件
log_file = "./log.txt"

#hdf5
version = 20190506001

#需要grid图
need_grid = False
#是否是离线
is_offline = True

#是否为1v1模式
is_1v1_mode = True
#发射多少条射线寻找敌人
direction_num_to_enemy = 120
#发射多少条射线到障碍物
direction_num_to_obstacle = 120
#每条射线穿过几个障碍物
cross_obstacle_num = 2

min_max_x = (-710.0, 540.0)
min_max_z = (-1725.0, 2200.0)

# 离线cache生成配置
# 数据分离
is_datasplit_enable = True
# 多进程数据处理
is_mp_enable = True
# 数据合并
is_datamerge_enable = True
# 热点数量
num_hot_points = 560000
# this all sort 文件路径
sorted_coord_path = '/data/chadyang/data_dir/thin_all_sort'
# input_obj_path路径
input_obj_path = '/data/chadyang/data_dir/PVP_CF_Ship.obj'
# 进程数量
num_threads = 12
# 保存生成数据的文件夹
save_dir = './data'
# index 和 value 文件配置
index_list = [save_dir + '/index_{}_block_{}_np.npy'.format(num_hot_points, i) for i in range(num_threads)]
value_list = [save_dir + '/value_{}_block_{}_np.npy'.format(num_hot_points, i) for i in range(num_threads)]
save_list = [save_dir + '/index_{}_np'.format(num_hot_points), 
             save_dir + '/value_{}_np'.format(num_hot_points)]

