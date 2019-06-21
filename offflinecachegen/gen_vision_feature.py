# encoding=utf8
'''
Created on 2019年3月11日
@author: jankinxu
'''

import math
import os

import cPickle as pickle
import numpy as np
import setting as debug_setting


def Dot(v0, v1):
    return v0[0] * v1[0] + v0[1] * v1[1] + v0[2] * v1[2]


def Cross(v0, v1):
    x = v0[1] * v1[2] - v0[2] * v1[1]
    y = v0[2] * v1[0] - v0[0] * v1[2]
    z = v0[0] * v1[1] - v0[1] * v1[0]
    return [x, y, z]


def Minus(v0, v1):
    return [v0[0] - v1[0], v0[1] - v1[1], v0[2] - v1[2]]


def getMaxMin(a, b, c):
    return max(a, b, c), min(a, b, c)


def IntersectTriangle(agent, enemy, v0, v1, v2):
    E1 = Minus(v1, v0)  # v1.minus(v0)
    E2 = Minus(v2, v0)  # v2.minus(v0)
    directory = Minus(enemy, agent)  # enemy.minus(agent)
    P = Cross(directory, E2)  # directory.Cross(E2)
    det = Dot(E1, P)  # float(E1.Dot(P))
    T = [0, 0, 0]
    if det > 0:
        T = Minus(agent, v0)  # agent.minus(v0)
    else:
        T = Minus(v0, agent)  # v0.minus(agent)
        det = -det
    e = float(0.0001)
    if det < e:
        return False
    um = 0
    um = Dot(T, P)  # T.Dot(P)
    if um < 0.0 or um > det:
        return False
    Q = Cross(T, E1)  # T.Cross(E1)
    v = Dot(directory, Q)  # directory.Dot(Q)
    if v < 0.0 or (um + v) > det:
        return False
    return True


class GridMapGener(object):
    def __init__(self, obj_path="./PVP_CF_Ship.obj"):

        self.obj_path = obj_path

        self.LoadNewMap(self.obj_path)
        self.memory = False
        self.body_high = 0.89
        if not debug_setting.is_offline:
            pkl_file = "pvp_cf_ship.pkl"
            if os.path.exists(pkl_file):
                self._loads(pkl_file)
            else:
                self.faces_merge(pkl_file)
        else:
            self.faces_merge()

    def get_face_direction(self, rotate_vec):

        x, y, z = 0, 0, 1
        rx = rotate_vec[0]
        ry = rotate_vec[1]  # 96
        # math.cos和math.sin输入为弧度
        rx_pi = math.pi * (rx / 180.0)
        ry_pi = math.pi * (ry / 180.0)
        cos_rx = math.cos(rx_pi)
        sin_rx = math.sin(rx_pi)
        cos_ry = math.cos(ry_pi)
        sin_ry = math.sin(ry_pi)
        new_x = cos_rx * sin_ry
        new_z = cos_rx * cos_ry
        new_y = -1 * sin_rx

        return [new_x, new_y, new_z]

    # 根据自身的位置以及相机的方向构成一个面，判断敌人的位置是否在面的正上方
    def length(self, vs):
        return math.sqrt(vs[0] * vs[0] + vs[1] * vs[1] + vs[2] * vs[2])

    def get_str(self, vec):
        return str(vec[0]) + " " + str(vec[1]) + " " + str(vec[2])

    def get_key(self, agent, enemy):
        key = ""
        if agent[0] < enemy[0] or (agent[0] == enemy[0] and agent[1] < enemy[1]) or \
                (agent[0] == enemy[0] and agent[1] == enemy[1] and agent[2] <= enemy[2]):

            key = self.get_str(agent) + " " + self.get_str(enemy)
        elif agent[0] > enemy[0] or (agent[0] == enemy[0] and agent[1] > enemy[1]) or \
                (agent[0] == enemy[0] and agent[1] == enemy[1] and agent[2] > enemy[2]):
            key = self.get_str(enemy) + " " + self.get_str(agent)
        return key

    def equal_last(self, agent, rotate_vector):
        if not self.memory:
            return False
        if agent[0] != self.last_agent[0] or agent[1] != self.last_agent[1] \
                or agent[2] != self.last_agent[2]:
            return False
        if rotate_vector[1] != self.last_rotate_vector[1]:
            return False
        return True

    def get_agent2enemy_distance(self, agent, enemys, rotate_vector, multi_dir=None):
        rotate_vector = rotate_vector[:]

        if multi_dir == None:
            multi_dir = debug_setting.direction_num_to_enemy
        agent = [agent[0] / 100.0, agent[1] / 100.0, agent[2] / 100.0]
        angle_range = 360.0 / multi_dir / 2
        left_angle = -1 * angle_range
        right_angle = angle_range
        rotate_vector[0] = rotate_vector[0] * 360.0 / 255
        rotate_vector[1] = rotate_vector[1] * 360.0 / 255
        if rotate_vector[0] > 90 and rotate_vector[0] < 270:
            rotate_vector[1] += 180
            if rotate_vector[1] > 360:
                rotate_vector[1] -= 360
        face_yaw = rotate_vector[1]

        if len(enemys) == 0:
            return [-1] * multi_dir
        a2e_yaws = []
        for enemy in enemys:
            enemy = [enemy[0] / 100.0, enemy[1] / 100.0, enemy[2] / 100.0]
            a2e_tan = math.atan2(enemy[2] - agent[2], enemy[0] - agent[0])
            a2e_yaw = ((-a2e_tan + 2.5 * math.pi) %
                       (2 * math.pi)) * 180 / math.pi
            a2e_yaws.append(a2e_yaw)

        multi_cross = []
        degree = 360.0 / multi_dir
        for i in range(multi_dir):
            rotate_y = (face_yaw + degree * i) % 360  # * math.pi / 180
            dis = -1
            for j in range(len(a2e_yaws)):
                if left_angle < (rotate_y - a2e_yaws[j]) <= right_angle:
                    # pdb.set_trace()
                    enemy = enemys[j]
                    enemy = [enemy[0] / 100.0, enemy[1] /
                             100.0, enemy[2] / 100.0]
                    new_dis = self.length(Minus(enemy, agent))
                    if dis < 0 or (dis > 0 and new_dis < dis):
                        dis = new_dis

            multi_cross.append(dis)

        return multi_cross

    def get_all_feature(self, agent, enemy, rotate_vector, enemy_rotate):

        rotate_vector = rotate_vector[:]
        enemy_rotate = enemy_rotate[:]
        rotate_vector[0] = rotate_vector[0] * 360.0 / 255
        rotate_vector[1] = rotate_vector[1] * 360.0 / 255

        agent = [agent[i] / 100.0 for i in range(len(agent))]
        agent[1] += self.body_high
        enemy = [enemy[i] / 100.0 for i in range(len(enemy))]
        enemy[1] += self.body_high
        # 相机的位置是自身的position的Z加100cm
        camera2enemy_ray = [enemy[0] - agent[0],
                            enemy[1] - agent[1], enemy[2] - agent[2]]

        visible = self.VisibleInField(agent, enemy)
        distance = self.distance(camera2enemy_ray)  # 计算相机到敌人的距离

        face_direction = self.get_face_direction(rotate_vector)

        # 计算face direction射线与相机到敌人射线的水平夹角弧度和竖直夹角弧度,同时偏移的方向用正负表示
        horizontal_angle, vertical_angle = self.Cos_Angle_of_Aimat_with_Face_direction(
            camera2enemy_ray, face_direction)

        # 计算敌人在以自身相机为原点,以face direction法方向的平面中的映射二维坐标
        screen_offset = self.getOffsetInScreen(
            camera2enemy_ray, face_direction)
        # 计算主玩家在敌人枪口方向夹角
        enemy_rotate[0] = enemy_rotate[0] * 360.0 / 255
        enemy_rotate[1] = enemy_rotate[1] * 360.0 / 255
        enemy_to_agent = [agent[0] - enemy[0],
                          agent[1] - enemy[1], agent[2] - enemy[2]]
        enemy_face_direction = self.get_face_direction(enemy_rotate)
        enemy_horizontal_angle, enemy_vertical_angle = self.Cos_Angle_of_Aimat_with_Face_direction(
            enemy_to_agent, enemy_face_direction)

        # distance是敌人位置到相机的距离，screen_offset是计算敌人在以自身相机为原点,以face direction法方向的平面中的映射二维坐标
        # visible是判断敌人和anget的相机连线之间是否有遮蔽物，（如何敌人在agent朝向后面，那么只要连线之间没有遮蔽物也是true）,不是视野中敌人是否可见，因为这个不是很好算
        # horizontal_angle，vertical_angle分别是face_direction和camera2enemy的水平夹角弧度和竖直夹角弧度，camera2enemy是enemy的位置向量减去相机的位置向量，可以表达敌人在相机的哪个方位的方向向量
        return [distance, screen_offset[0], screen_offset[1], visible, horizontal_angle, vertical_angle, camera2enemy_ray[0], camera2enemy_ray[1], camera2enemy_ray[2], enemy_horizontal_angle, enemy_vertical_angle]
    # 根据朝向了,相机的位置计算以及敌人的位置计算
    # if face direction is (x,y,z), then the screen axis is X: (z,0,-x), Y:(-xy,  x^2+z^2, -yz))
    # 输出敌人在屏幕里面的位置

    def getOffsetInScreen(self, camera2enemy_ray, face_direction):
        # map_x-->(-0.48,0.48)
        # map_y-->(-0.27,0.27)
        if face_direction[0] * camera2enemy_ray[0] + face_direction[1] * camera2enemy_ray[1] + \
                face_direction[2] * camera2enemy_ray[2] < 0:
            return [0, 0]
        screen_x = 0.48
        scrren_y = 0.27
        X = [face_direction[2], 0, -1 * face_direction[0]]
        Y = [-1 * face_direction[0] * face_direction[1], face_direction[0] **
             2 + face_direction[2]**2, -1 * face_direction[1] * face_direction[2]]
        ray_distance = self.length(camera2enemy_ray)
        len_x = self.length(X)
        len_y = self.length(Y)
        len_face = 1

        x = (camera2enemy_ray[0] * X[0] + camera2enemy_ray[1] * X[1] +
             camera2enemy_ray[2] * X[2]) / (len_x)
        y = (camera2enemy_ray[0] * Y[0] + camera2enemy_ray[1] * Y[1] +
             camera2enemy_ray[2] * Y[2]) / (len_y)

        z = (camera2enemy_ray[0] * face_direction[0] + camera2enemy_ray[1] * face_direction[1] +
             camera2enemy_ray[2] * face_direction[2])

        add_x = math.sqrt(3) * z * 16 / math.sqrt(337)  # 16**2+9**2=337
        add_y = math.sqrt(3) * z * 9 / math.sqrt(337)  # 16**2+9**2=337
        # 将射线在z距离外的大屏幕等比例缩放，首先找到大屏幕的长宽，然后判断点是否在屏幕内
        max_x = add_x + 0.48
        max_y = add_y + 0.27
        if math.fabs(x) > max_x or math.fabs(y) > max_y:
            return [0, 0]

        map_x = 0.48 * x / max_x + 0.48
        map_y = 0.27 * y / max_y + 0.27

        return [map_x, map_y]

    def angle_from_agent_to_enemy(self, enemy, agent, enemy_rotate):
        rotate_vector = enemy_rotate[:]
        rotate_vector[0] = rotate_vector[0] * 360.0 / 255
        rotate_vector[1] = rotate_vector[1] * 360.0 / 255
        agent = [agent[i] / 100.0 for i in range(len(agent))]
        enemy = [enemy[i] / 100.0 for i in range(len(enemy))]
        enemy_to_agent = [agent[0] - enemy[0],
                          agent[1] - enemy[1], agent[2] - enemy[2]]
        face_direction = self.get_face_direction(rotate_vector)
        horizontal_angle, vertical_angle = self.Cos_Angle_of_Aimat_with_Face_direction(
            enemy_to_agent, face_direction)
        return [horizontal_angle, vertical_angle]

    def Cos_Angle_of_Aimat_with_Face_direction(self, camera2enemy_ray, face_direction):
        horizontal_angle = 0
        if camera2enemy_ray[2] != 0 or camera2enemy_ray[0] != 0:

            horizontal_angle1 = - \
                math.atan2(camera2enemy_ray[2], camera2enemy_ray[0]) / math.pi
            horizontal_angle2 = - \
                math.atan2(face_direction[2], face_direction[0]) / math.pi
            horizontal_angle = (horizontal_angle1 + 2 - horizontal_angle2) % 2
            if horizontal_angle > 1:
                horizontal_angle -= 2
        vertical_angle = 0
        if self.length(camera2enemy_ray) != 0:
            vertical_cos1 = camera2enemy_ray[1] / self.length(camera2enemy_ray)
            vertical_cos2 = face_direction[1]
            vertical_angle1 = math.acos(vertical_cos1) / math.pi
            vertical_angle2 = math.acos(vertical_cos2) / math.pi
            vertical_angle = vertical_angle1 - vertical_angle2

        return horizontal_angle, vertical_angle

    def get_angle(self, agent, enemy, rotate_vector):
        rotate_vector = rotate_vector[:]
        rotate_vector[0] = rotate_vector[0] * 360.0 / 255
        rotate_vector[1] = rotate_vector[1] * 360.0 / 255
        agent = [agent[i] / 100.0 for i in range(len(agent))]
        enemy = [enemy[i] / 100.0 for i in range(len(enemy))]
        enemy[1] += self.body_high
        camera_pos = list(agent)
        camera_pos[1] += self.body_high
        # 相机的位置是自身的position的Z加100cm
        camera2enemy_ray = [enemy[0] - camera_pos[0],
                            enemy[1] - camera_pos[1], enemy[2] - camera_pos[2]]
        face_direction = self.get_face_direction(rotate_vector)

        # 计算face direction射线与相机到敌人射线的水平夹角弧度和竖直夹角弧度,同时偏移的方向用正负表示
        horizontal_angle, vertical_angle = self.Cos_Angle_of_Aimat_with_Face_direction(
            camera2enemy_ray, face_direction)
        return horizontal_angle, vertical_angle
    # 输入agent和enemy和face_direction，任务的坐标中心点，enemy是敌人的坐标中心点PosX ,face_direction是face_pitch
    # 抽取敌人是否视野可见，枪是否指向敌人

    def VisibleInField(self, camera_pos, enemy):
        # 判断自己与敌人之间是否有遮蔽物
        visible = self.CheckRayTriangle(camera_pos, enemy)
        return visible

    # 判断自己和敌人位置的距离
    def distance(self, ray):
        dis = 0
        for i in range(len(ray)):
            dis += ray[i]**2
        return math.sqrt(dis)

    def CheckRayTriangle(self, agent, enemy):
        visible = True
        ray_max_x, ray_min_x = max(agent[0], enemy[0]), min(agent[0], enemy[0])
        ray_max_y, ray_min_y = max(agent[1], enemy[1]), min(agent[1], enemy[1])
        ray_max_z, ray_min_z = max(agent[2], enemy[2]), min(agent[2], enemy[2])
        ray_max_min = (ray_max_x, ray_min_x, ray_max_y,
                       ray_min_y, ray_max_z, ray_min_z)

        E = Minus(enemy, agent)
        xyE = [E[0], E[1]]
        xzE = [E[0], E[2]]
        yzE = [E[1], E[2]]
        for (verts, multi_triangles, max_min, face_type) in zip(self.combine_faces, self.multi_triangles, self.max_mins, self.face_types):
            if self.ImpossibleInter(ray_max_min, max_min) or self.isSameSide(xzE, verts, agent, 0, 2) \
                    or self.isSameSide(xyE, verts, agent, 0, 1) \
                    or self.isSameSide(yzE, verts, agent, 1, 2):
                continue
            if face_type == 1 and self.side_on_line(verts[0], verts[-1], agent, enemy):
                continue
            for face_index in multi_triangles:
                face = self.faces[face_index]
                cross_check = IntersectTriangle(
                    agent, enemy, self.verts[face[0]], self.verts[face[1]], self.verts[face[2]])
                if cross_check:
                    visible = False
                    break
        return visible

    def ImpossibleInter(self, ray_max_min, max_min):
        max_x, min_x = max_min[0]
        max_y, min_y = max_min[1]
        max_z, min_z = max_min[2]
        ray_max_x, ray_min_x, ray_max_y, ray_min_y, ray_max_z, ray_min_z = ray_max_min
        if ray_max_x < min_x or ray_min_x > max_x or \
                ray_max_y < min_y or ray_min_y > max_y or \
                ray_max_z < min_z or ray_min_z > max_z:
            return True
        return False

    def side_on_line(self, start_vert, end_vert, agent, enemy):
        E = [end_vert[0] - start_vert[0], end_vert[2] - start_vert[2]]
        test1 = E[1] * (agent[0] - start_vert[0]) - \
            E[0] * (agent[2] - start_vert[2])
        test2 = E[1] * (enemy[0] - start_vert[0]) - \
            E[0] * (enemy[2] - start_vert[2])
        if test1 * test2 >= 0:
            return True

    def isSameSide(self, E, verts, agent, first, second):

        judge = None
        if E[0] == 0 and E[1] == 0:
            return False
        for vert in verts:
            test = E[1] * (vert[first] - agent[first]) - \
                E[0] * (vert[second] - agent[second])
            test = self.get_pos_neg(test)
            if judge == None or judge == 0:
                judge = test
                continue
            if judge * test < 0:
                return False
            continue
        return True

    def get_pos_neg(self, test):
        if test > 0:
            return 1
        if test < 0:
            return -1
        return 0

    def get_two_direction(self, verts, sides, height):
        low = []
        high = []
        same = []

        for i in range(len(verts)):
            y = verts[i][1]
            if y > height:
                high.append(i)
            if y < height:
                low.append(i)
            if y == height:
                same.append(i)
        cross_vert = []
        for i in same:
            cross_vert.append([verts[i][0], verts[i][2]])
        for start in low:
            for end in high:
                if start < end:
                    t = (start, end)
                else:
                    t = (end, start)
                if t not in sides:
                    continue
                direc = Minus(verts[end], verts[start])
                k = (height - verts[start][1]) / direc[1]
                x = k * direc[0] + verts[start][0]
                z = k * direc[2] + verts[start][2]
                cross_vert.append([x, z])
        new_verts = sorted(cross_vert, key=lambda x: x[0])
        new_verts = sorted(new_verts, key=lambda x: x[1])

        vert = [new_verts[0], new_verts[-1]]
        return vert

    def get_eight_direction(self, agent, rotate_vector, high):

        rotate_vector = rotate_vector[:]
        multi_dir = debug_setting.direction_num_to_obstacle
        max_stage = debug_setting.cross_obstacle_num
        max_distance = 50.0
        x, height, z = agent[0] / 100.0, agent[1] / \
            100.0 + high, agent[2] / 100.0

        rotate_vector[0] = rotate_vector[0] * 360.0 / 255
        rotate_vector[1] = rotate_vector[1] * 360.0 / 255
        if rotate_vector[0] > 90 and rotate_vector[0] < 270:
            rotate_vector[1] += 180
            if rotate_vector[1] > 360:
                rotate_vector[1] -= 360
        if self.equal_last(agent, rotate_vector):
            return self.last_multi_dis
        self.last_agent = agent
        self.last_rotate_vector = rotate_vector
        multi_radian = []
        multi_tan = []
        multi_dis = np.arange(multi_dir)
        for i in range(len(multi_dis)):
            multi_dis[i] = max_distance
        multi_dis = multi_dis.reshape(multi_dir, 1).tolist()

        degree = 360.0 / multi_dir
        for i in range(multi_dir):
            rotate_y = rotate_vector[1] + degree * i
            rotate_y = ((450 - rotate_y) % 360) * math.pi / 180
            multi_radian.append(rotate_y)
            multi_tan.append(math.tan(rotate_y))
        for verts, sides, max_min in zip(self.combine_faces, self.combine_sides, self.max_mins):
            max_y, min_y = max_min[1]
            if height < min_y or height > max_y or max_y == min_y:
                continue

            vert = self.get_two_direction(verts, sides, height)
            x1, z1 = vert[0][0] - x, vert[0][1] - z
            x2, z2 = vert[1][0] - x, vert[1][1] - z

            radian1 = math.atan2(z1, x1)
            radian2 = math.atan2(z2, x2)
            if radian1 < 0:
                radian1 += math.pi * 2
            if radian2 < 0:
                radian2 += math.pi * 2
            min_radian, max_radian = min(
                radian1, radian2), max(radian1, radian2)
            start_radian = []
            end_radian = []
            if (max_radian - min_radian) > math.pi:
                start_radian.append(0)
                end_radian.append(min_radian)
                start_radian.append(max_radian)
                end_radian.append(math.pi * 2)
            else:
                start_radian.append(min_radian)
                end_radian.append(max_radian)
            for i in range(len(multi_radian)):
                for start, end in zip(start_radian, end_radian):

                    if multi_radian[i] >= (start - 0.0001) and multi_radian[i] <= (end + 0.0001):
                        # y = p*x, p为沿着x轴旋转的射线斜率
                        # x = (x2*z1-x1*z2)/(p)
                        dis = 50
                        p = multi_tan[i]
                        if x1 == x2 and z1 == z2:
                            dis = math.sqrt(x1 ** 2 + z1 ** 2)
                        elif p * (x2 - x1) == (z2 - z1):
                            dis = min(math.fabs(x1), math.fabs(x2)) * \
                                math.sqrt(p ** 2 + 1)
                        elif z1 == z2:
                            dis = math.sqrt(1 + 1 / (p ** 2)) * math.fabs(z1)
                        elif x1 == x2:
                            if x1 == 0:
                                dis = min(math.fabs(z1), math.fabs(z2))
                            else:
                                dis = math.sqrt(1 + p ** 2) * math.fabs(x1)
                        elif math.fabs(multi_tan[i] % math.pi - 0.5 * math.pi) < 0.001:
                            dis = math.fabs((x2 * z1 - x1 * z2) / (x2 - x1))
                        else:
                            dis = math.fabs(
                                (x2 * z1 - x1 * z2) / (p * (x2 - x1) - z2 + z1)) * math.sqrt(1 + p ** 2)
                        multi_stage = multi_dis[i]
                        if dis not in multi_stage:
                            multi_stage.append(dis)

        self.memory = True
        for i in range(len(multi_dis)):
            multi_stage = multi_dis[i]
            multi_stage.sort()
            lens = len(multi_stage)
            if lens > max_stage:
                multi_dis[i] = multi_stage[:max_stage]
            if lens < max_stage:
                multi_stage.extend([max_distance] * (max_stage - lens))
        multi_dis = np.array(multi_dis).reshape(-1).tolist()
        self.last_multi_dis = multi_dis
        return multi_dis

    def LoadNewMap(self, map_file_name):
        self.verts = []
        self.faces = []
        fo = open(map_file_name, "r")
        for line in fo:
            if line[0] == "v":
                line = line[2:]
                line.strip()
                templine = line.split(' ')
                vert = []

                for subline in templine:
                    vert.append(float(subline))
                    #vert.append( float(Decimal("%.3f"%float(subline))));
                vert[0] = -vert[0]
                self.verts.append(vert)  # Vector3(vert[0], vert[1], vert[2]))

            elif line[0] == "f":
                line = line[2:]
                line.strip()
                templine = line.split(' ')
                face = []
                for subline in templine:
                    subline = subline[0:subline.index("/")]
                    face.append(int(subline) - 1)
                self.faces.append(face)
        fo.close()

    def in_one_face(self, faces):

        if self.in_one_face_key(faces, 0):
            return True
        if self.in_one_face_key(faces, 1):
            return True
        if self.in_one_face_key(faces, 2):
            return True
        return False

    def in_one_face_key(self, faces, key):
        dis = None
        for index in faces:
            if dis == None:
                dis = self.verts[index][key]
            elif math.fabs(dis - self.verts[index][key]) > 1e-3:
                return False
        return True

    def get_face_type(self, face, key1, key2):
        values = set()
        for i in face:
            vert = self.verts[i]
            values.add((vert[key1], vert[key2]))
        if len(values) < 3:
            return True

    def same_face(self, faces, vert_indexs, debug=False):
        other = self.verts[list(faces)[0]]
        vector = []
        for i in vert_indexs:
            vert = self.verts[i]
            x = [vert[0] - other[0], vert[1] - other[1], vert[2] - other[2]]
            vector.append(x)
        # 判断三阶行列式视为0,0的话共面
        _1 = vector[0][0] * vector[1][1] * vector[2][2]  # x1,y2,z3
        _2 = vector[0][2] * vector[1][0] * vector[2][1]  # z1,x2,y3
        _3 = vector[0][1] * vector[1][2] * vector[2][0]  # y1,z2,x3
        _4 = vector[0][2] * vector[1][1] * vector[2][0]  # z1,y2,x3
        _5 = vector[0][0] * vector[1][2] * vector[2][1]  # x1,z2,y3
        _6 = vector[0][1] * vector[1][0] * vector[2][2]  # y1,x2,z3
        _is_same_face = _1 + _2 + _3 - _4 - _5 - _6
        if math.fabs(_is_same_face) <= 1e-4:
            return True
        return False

    def faces_merge(self, pkl_file=None):
        self.combine_faces = []
        self.combine_sides = []
        self.multi_triangles = []
        self.max_mins = []
        self.face_types = []
        pass_faces = set()

        for i in range(len(self.faces)):
            drop = True
            for index in self.faces[i]:
                if self.verts[index][1] < 5:
                    drop = False
            if self.in_one_face_key(self.faces[i], 1):
                y = self.verts[self.faces[i][0]][1]

                if y < -0.2 or y > 0.2:
                    drop = True
            if drop:
                pass_faces.add(i)
        find_faces = set()
        for i in range(len(self.faces)):
            if i in pass_faces or i in find_faces:
                continue
            face_type = 0

            if not self.in_one_face(self.faces[i]) and self.get_face_type(self.faces[i], 0, 2):
                face_type = 1

            faces_list = self.faces[i]
            faces = set(faces_list)
            sides = set()
            multi_triangle = [i]
            for m in range(len(faces_list)):
                for n in range(m + 1, len(faces_list)):
                    if faces_list[m] < faces_list[n]:
                        sides.add((faces_list[m], faces_list[n]))
                    else:
                        sides.add((faces_list[n], faces_list[m]))
            find = True
            not_same_face = set()
            while find:
                find = False
                for j in range(i + 1, len(self.faces)):

                    if j in pass_faces or j in find_faces or j in not_same_face:
                        continue
                    b = set(self.faces[j])
                    inter = faces.intersection(b)
                    if len(inter) > 2:
                        find_faces.add(j)
                        continue
                    if len(inter) == 2:
                        if self.same_face(faces - inter, b):
                            multi_triangle.append(j)
                            faces = faces | b
                            find_faces.add(j)
                            find = True
                            # 把新的边加进去
                            new_verts = b - inter
                            for new_vert in new_verts:
                                for v in inter:
                                    if new_vert < v:
                                        sides.add((new_vert, v))
                                    else:
                                        sides.add((v, new_vert))
                            inter = list(inter)
                            if inter[0] < inter[1]:
                                sides.remove((inter[0], inter[1]))
                            else:
                                sides.remove((inter[1], inter[0]))
                        else:
                            not_same_face.add(j)

            face2verts = []
            max_x = min_x = max_y = min_y = max_z = min_z = None
            vert2idx = {}

            faces = list(faces)
            if face_type == 1:
                faces = sorted(faces, key=lambda x: self.verts[x][0])

            for index in faces:
                vert2idx[index] = len(face2verts)
                vert = self.verts[index]
                face2verts.append(vert)
                if max_x == None:
                    max_x = min_x = vert[0]
                    max_y = min_y = vert[1]
                    max_z = min_z = vert[2]
                else:
                    max_x = max(max_x, vert[0])
                    min_x = min(min_x, vert[0])
                    max_y = max(max_y, vert[1])
                    min_y = min(min_y, vert[1])
                    max_z = max(max_z, vert[2])
                    min_z = min(min_z, vert[2])

            new_sides = []
            for pair in sides:
                start, end = pair
                if vert2idx[start] < vert2idx[end]:
                    new_sides.append((vert2idx[start], vert2idx[end]))
                else:
                    new_sides.append((vert2idx[end], vert2idx[start]))
            self.max_mins.append(
                [(max_x, min_x), (max_y, min_y), (max_z, min_z)])
            self.combine_faces.append(face2verts)
            self.multi_triangles.append(multi_triangle)
            self.combine_sides.append(new_sides)
            self.face_types.append(face_type)

        if pkl_file != None:
            f = open(pkl_file, 'w')
            pickle.dump(self.combine_faces, f)
            pickle.dump(self.max_mins, f)
            pickle.dump(self.multi_triangles, f)
            pickle.dump(self.combine_sides, f)
            pickle.dump(self.face_types, f)
            f.close()

    def _loads(self, pkl_file):
        f = open(pkl_file, 'r')
        self.combine_faces = pickle.load(f)
        self.max_mins = pickle.load(f)
        self.multi_triangles = pickle.load(f)
        self.combine_sides = pickle.load(f)
        self.face_types = pickle.load(f)
        f.close()


def test():

    #grid_map_drawer = GridMapGener("sample.obj")
    grid_map_drawer = GridMapGener()

    agent = [-690, -111, 1867]

    rotate_vector = [10, 132, 0]
   # multi_dis = grid_map_drawer.get_eight_direction(agent,rotate_vector)
    #print (multi_dis)
    face_direction = [0, 0, 1]
    camera2enemy_ray = [1, 0, 0]
    # getOffsetInScreen(self, camera2enemy_ray, face_direction):

    agent = [211, 52, 1266]
    enemy = [200, -30, 0]
    rotate = [0, 140, 0]
    #features = grid_map_drawer.get_all_feature(agent, enemy, rotate)
    #print (features)
    multi_dis = grid_map_drawer.get_eight_direction(agent, rotate, 0.3)
    print (multi_dis)
    #[distance, screen_offset[0], screen_offset[1], visible, horizontal_angle, vertical_angle, camera2enemy_ray[0], camera2enemy_ray[1], camera2enemy_ray[2]]


def CheckIntersectTriangle():
    orig = [0, 0, 1]
    enemy = [0.25, 0.25, -1.0]
    v0 = [0, 0, 0]
    v1 = [1, 0, 0]
    v2 = [0, 1, 0]
    # pdb.set_trace()
    result = IntersectTriangle(orig, enemy, v0, v1, v2)


def main_job(file_lists, thread_idx):
    grid_map_drawer = GridMapGener()
    grid_map_drawer.process(file_lists)


if __name__ == "__main__":
    # pdb.set_trace()
    test()
    # main_job()
