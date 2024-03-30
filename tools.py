import os
import re
import random

def tt_pre_process(path):
    with open(path, 'r', encoding='utf-8-sig') as data:
        records = data.readlines()
    records = [r for r in records if r != '\n']
    records = [r.split(',')[1:] for r in records]
    # 删除碎部点
    records = [r for r in records if float(r[-1]) != 0]

    clean_records = []
    start = 0
    end = 1
    while start <= len(records) and end <= len(records):
        while 'V' in records[start][0] and len(records[start]) <= 2:
            if 'V' not in records[end][0] and len(records[end]) <= 2:
                clean_records += records[start: end]
                start = end
                end += 1
            else:
                end += 1
        start = end
        end += 1

    # 删除控制点观测支点
    clean_records = [r for r in clean_records if 'V' in r[0] or len(r) == 2]
    clean_records.append(['\n'])
    return clean_records


def search_rtk(rtk_path, base, back, front):
    with open(rtk_path, 'r', encoding='utf-8-sig') as rtk:
        rtk_records = rtk.readlines()
    rtk_base, rtk_back, rtk_front = {}, {}, {}

    for rtk in rtk_records:

        rtk = rtk.split(' ')
        coord = list(map(float, rtk[1:]))

        base_name = base[0]
        back_name = back[0]
        front_name = front[0]

        if base_name in rtk[0]:
            rtk_base[rtk[0]] = coord + [float(base[1])]
        elif back_name in rtk[0]:
            rtk_back[rtk[0]] = coord + [float(back[1])]
        elif front_name in rtk[0]:
            rtk_front[rtk[0]] = coord + [float(front[1])]

    return rtk_base, rtk_back, rtk_front


def rtk_rename(rtk_path, result, control_level):
    result = result.split('\n')[1:]
    result = [i.split(' ') for i in result if 'V' in i and ':' not in i]
    result = sum(result, [])
    obs_number = control_level * 2
    tail_list = []
    new_name = []
    new_record = []
    if obs_number == 4:
        tail_list = ["-1", "-2", "J-1", "J-2"]
    elif obs_number == 6:
        tail_list = ["-1", "-2", "-3", "J-1", "J-2", "J-3"]
    for f in result:
        idx = result.index(f)
        tail = tail_list[idx % obs_number]
        new_name.append(f[:4] + tail)
    with open(rtk_path, 'r') as rtk:
        rtk_records = rtk.readlines()
    for r in rtk_records:
        rec_line = re.split(",| ", r)
        rtk_no = rec_line[0]

        if rtk_no in result:
            idx = result.index(rtk_no)
            rec_line.insert(0, new_name[idx])
            del(rec_line[1])
            new_record.append(rec_line)
    new_record = sorted(new_record, key=lambda x: x[0])
    file_dir, old_name = os.path.split(rtk_path)
    new_name = os.path.splitext(old_name)[0] + "_new.txt"
    new_path = os.path.join(file_dir, new_name)
    with open(new_path, 'w+', encoding='utf-8-sig') as file:
        file.writelines('新点号 坐标\n')
        file.writelines(' '.join(i) for i in new_record)


def output_format(check_data):
    result = ''
    if isinstance(check_data, dict):
        for k, v in check_data.items():
            v = ' '.join(v)
            result += k + ':\n' + v + '\n'
    return result


def errors_format(check_data, type):
    result = ''
    if isinstance(check_data, dict):
        if type == 'dist':
            for k, v in check_data.items():
                error = round(v[0]-v[1], 2)
                result += k + ':  ' + str(error) + '\n'
        elif type == 'angel':
            for k, v in check_data.items():
                v = ' '.join(v)
                result += k + ':  ' + v + '\n'
    return result






