def self_choose(level, records):
    dist = {}
    i = 0
    j = 1
    while i < len(records) - 1:
        a = records[i][1:]
        b = records[j][1:]
        a = np.float32(a)
        b = np.float32(b)
        d = np.sqrt(np.sum((a - b) ** 2))
        pair = records[i][0] + " " + records[j][0]
        dist[pair] = d
        j += 1
        if j == len(records):
            i += 1
            j = i + 1

    dist = sorted(dist.items(), key=lambda x: x[1])
    candidates = []
    result = []

    for i, d in enumerate(dist):
        p1, p2 = d[0].split(" ")
        candidates.extend([p1, p2])

    for c in candidates:
        if c not in result and len(result) < level:
            result.append(c)
    return result


def self_compare(rtk_path, level=2):
    records = np.loadtxt(rtk_path, dtype=str, encoding='utf-8-sig')
    point_records = {}
    self_filted = []

    for idx, line in enumerate(records):
        point_name = line[0]
        point_number = point_name[:4]
        if "HD" in point_name:
            np.delete(records, idx)
        else:
            point_records.setdefault(point_number, []).append(line)

    for k, v in point_records.items():
        if len(v) > level * 2:
            new_v = self_choose(level*2, v)
        elif len(v) == level * 2:
            new_v = [i[0] for i in v]
        else:
            new_v = [i[0] for i in v]
        self_filted.extend(new_v)
    return self_filted
