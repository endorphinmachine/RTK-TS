#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import math
import tools
import re


def pairs_match(base: dict, target: dict):
    dist_record = {}
    for kb, vb in base.items():
        for kt, vt in target.items():
            pairs_key, pairs_dist = dist_reverse_calculate(kb, kt, vb, vt)
            dist_record[",".join(pairs_key)] = round(pairs_dist, 3)
    return dist_record


def dist_reverse_calculate(base_name: str, target_name: str, base_pos: dict,  target_pos: dict):
    pair = [base_name, target_name]
    temp = [(base_pos[0]-target_pos[0])**2,
            (base_pos[1]-target_pos[1])**2,
            (base_pos[2]-target_pos[2] + base_pos[3]-target_pos[3])**2]
    dist = math.sqrt(sum(temp))
    return pair, dist


def dist_vote(pairs, level=2):
    # pairs 所有站点所有观测组合

    score, group, result = {}, {}, {}
    for k, v in pairs.items():
        points = k.split(',')
        for p in points:
            dist = abs(v[0] - v[1])
            if p in score.keys():
                score[p] += dist
            else:
                score[p] = dist

        for k, v in score.items():
            s = k.split('-')[0]
            s = s[:4]
            if s in group.keys():
                group[s].update({k: v})
            else:
                group[s] = {k: v}

    for k, v in group.items():
        rank = sorted(v.items(), key=lambda x: x[1])
        rank = [i[0] for i in rank]
        result[k] = rank[:level]
    return result


def dist_compare(rtk_path, ts_path, level=2):
    pairs_dist = {}
    ts_records = tools.tt_pre_process(ts_path)
    for rec in ts_records:
        if len(rec) <= 2 and 'V' in rec[0]:
            base = rec
            back = ts_records[ts_records.index(rec) + 1]
            front = ts_records[ts_records.index(rec) + 2]
            # 根据全站仪观测点名搜索RTK观测记录
            base_pos, back_pos, front_pos = tools.search_rtk(rtk_path, base, back[:2], front[:2])

            if 'V' in base[0] and 'V' in back[0]:
                back_ts_dist = float(back[-1])
                back_cal_dist = pairs_match(base_pos, back_pos)
                back_dist = {k: [v, back_ts_dist] for k, v in back_cal_dist.items()}
                pairs_dist.update(back_dist)

            if 'V' in base[0] and 'V' in front[0]:
                front_ts_dist = float(front[-1])
                front_cal_dist = pairs_match(base_pos, front_pos)
                front_dist = {k: [v, front_ts_dist] for k, v in front_cal_dist.items()}
                pairs_dist.update(front_dist)

    chosen_records = dist_vote(pairs_dist, level*2)
    return chosen_records, pairs_dist






