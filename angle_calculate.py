#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import math
import tools
import re


class Degree(object):
    def __init__(self):
        None

    @staticmethod
    def dd_to_dms(dd):
        """
        十进制度转为度分秒
        Paramaters:
            dd : 十进制度
        Return:
            dms : 度分秒
        """
        degree = (int)(float(dd))
        minute = (int)((float(dd)-degree)*60)
        second = (int)((float(dd)-degree-float(minute)/60)*3600)
        if second < 0:
            dms = '-' + str(degree) + '°' + str(minute) + '′' + str(second) + '″'
        else:
            dms = str(degree) + '°' + str(minute) + '′' + str(second)[1:] + '″'
        return dms

    @staticmethod
    def dms_to_dd(dms):
        """
        度分秒转为十进制度
        Paramater:
            degree : 度
            minute : 分
            second : 秒
        Return:
            dd : 十进制度
        """
        degree,minute,second = dms[0], dms[1], dms[2]
        dd = degree+minute/60+second/60/60
        return dd

    @staticmethod
    def parse_dms(dms, type):
        """
        解析度分秒字符串
        Paramater:
            dms : 度分秒字符串
        Returns:
            degree : 度
            minute : 分
            second : 秒
        """
        if type == "input":
            parts = dms.split('.')
            degree = float(parts[0])
            minute = float(parts[1][:2])
            second = float(parts[1][2:])
        elif type == "output":
            parts = re.split('°|′|″', dms)
            degree = float(parts[0])
            minute = float(parts[1])
            second = float(parts[2])
        return degree, minute, second


def angle_match(station, back, front, t_ang):
    ang_record = {}
    for ks, vs in station.items():
        for kb, vb in back.items():
            for kf, vf in front.items():
                pairs_key, angle1, angle2 = ang_reverse_calculate(ks, kb, kf, vs, vb, vf)
                if abs(t_ang - angle1) <= abs(t_ang - angle2):
                    ang_record[",".join(pairs_key)] = Degree.dd_to_dms(angle1-t_ang)
                else:
                    ang_record[",".join(pairs_key)] = Degree.dd_to_dms(angle2-t_ang)
    return ang_record


def ang_reverse_calculate(s_name, b_name, f_name, s_pos, b_pos, f_pos):
    angle_pair = [s_name, b_name, f_name]
    dx_back = b_pos[0] - s_pos[0]
    dy_back = b_pos[1] - s_pos[1]
    dx_front = f_pos[0] - s_pos[0]
    dy_front = f_pos[1] - s_pos[1]

    ang_back = math.atan(dy_back / dx_back)
    ang_front = math.atan(dy_front / dx_front)

    ang_back = math.degrees(ang_back)
    ang_front = math.degrees(ang_front)

    if ang_back * ang_front >= 0:
        ang = abs(ang_back - ang_front)
    else:
        ang = abs(ang_back) + abs(ang_front)

    return angle_pair, ang, 360-ang


def angle_compare(rtk_path, ts_path, level=2):
    pairs_angle = {}

    ts_records = tools.tt_pre_process(ts_path)
    for rec in ts_records:
        if len(rec) <= 2 and 'V' in rec[0]:
            base = rec
            back = ts_records[ts_records.index(rec) + 1]
            front = ts_records[ts_records.index(rec) + 2]

            if len(front) > 2:
                t_ang = calcu_ang(back, front)
                base_pos, back_pos, front_pos = tools.search_rtk(rtk_path, base, back[:2], front[:2])
                cal_angle = angle_match(base_pos, back_pos, front_pos, t_ang)
                pairs_angle.update(cal_angle)

    chosen_record = angle_vote(pairs_angle, level*2)
    if not pairs_angle:
        chosen_record = '提示: 未找到观测夹角！'
    return chosen_record, pairs_angle


def calcu_ang(b, f):
    b_ang = Degree.dms_to_dd(Degree.parse_dms(b[2], "input"))
    f_ang = Degree.dms_to_dd(Degree.parse_dms(f[2], "input"))
    if b_ang > 180:
        b_ang = 360 - 180
    t_ang = f_ang - b_ang
    return t_ang


def angle_vote(pairs, level=2):
    # pairs 所有站点所有观测组合

    score, group, result = {}, {}, {}
    for k, v in pairs.items():
        points = k.split(',')
        # ang1 = Degree.dms_to_dd(Degree.parse_dms(v[0]))
        # ang2 = Degree.dms_to_dd(Degree.parse_dms(v[1]))
        dist = abs(Degree.dms_to_dd(Degree.parse_dms(v, "output")))
        for p in points:
            if p in score.keys():
                score[p] += dist
            else:
                score[p] = dist

            for k, v in score.items():
                s = k.split('-')[0]
                if s in group.keys():
                    group[s].update({k: v})
                else:
                    group[s] = {k: v}

    for k, v in group.items():
        rank = sorted(v.items(), key=lambda x: x[1])
        rank = [i[0] for i in rank]
        result[k] = rank[:level]
    return result