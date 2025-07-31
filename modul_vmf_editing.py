import re
from unittest import expectedFailure


def vmf_map_solid(a):
    try:
        split_a = a.split()
        start = split_a.index("solid")
        end = split_a.index("}", split_a.index("entity") - 1)
        return split_a[start:end]
    except:
        print(a)
        print("No found solid or entity")
        return "nil"
def vmf_map_entity(a):
    try:
        split_a = a.split()
        start = split_a.index("entity")
        end = split_a.index("cameras")
        return split_a[start:end]
    except:
        print(a)
        print("No found entity or cameras")
        return "nil"
def vmf_map_merge(a, b):
    result = a
    for i in b:
        if i[0] == "solid":
            try:
                result.insert(result.index('"detailmaterial"') + 2, " ".join(i))
            except:
                print(result)
                print("No found detailmaterial")
        elif i[0] == "entity":
            try:
                result.insert(result.index('cameras'), " ".join(i))
            except:
                print("No found cameras")
    return result
def vmf_coordinates_set(a, b):
    sub_result = []
    result = []
    joins = " ".join(a)
    solid = a
    for i in range(0, solid.count('"plane"')):
        # print(solid.index('"material"', ind))
        # print(solid.index('"plane"', ind))
        table = solid[solid.index('"plane"') + 1:solid.index('"material"')]
        sub_result.append(" ".join(table))
        table[0] = table[0].replace('"(', "")
        table[3] = table[3].replace('(', "")
        table[6] = table[6].replace('(', "")
        table[2] = table[2].replace(')', "")
        table[5] = table[5].replace(')', "")
        table[8] = table[8].replace(')"', "")
        table2 = [[float(table[0]), float(table[1]), float(table[2])], [float(table[3]), float(table[4]), float(table[5])], [float(table[6]), float(table[7]), float(table[8])]]
        table3 = []
        for index, x in enumerate(table2):
            for ind, v in enumerate(table2[index]):
                if ind == 0:
                    table3.append("(" + str(table2[index][ind] + b[ind]))
                elif ind == 2:
                    table3.append(str(table2[index][ind] + b[ind]) + ")")
                else:
                    table3.append(str(table2[index][ind] + b[ind]))
        table3 = " ".join(table3)
        table3 = table3.replace("), (", ") (")
        table3 = '"' + table3 + '"'
        result.append(table3)
        solid.remove('"plane"')
        solid.remove('"material"')
    for i, v in enumerate(sub_result):
        joins = joins.replace(v, result[i])
    return joins.split()
def vmf_coordinates_set_point(a, b):
    sub_result = []
    result = []
    joins = " ".join(a)
    point = a
    for i in range(point.count('"origin"')):
        cor_1 = '"' + str(float(point[point.index('"origin"') + 1][1:]) + b[0])
        cor_2 = str(float(point[point.index('"origin"') + 2]) + b[1])
        cor_3 = str(float(point[point.index('"origin"') + 3][0:-1]) + b[2]) + '"'
        sub_cor_1 = point[point.index('"origin"') + 1]
        sub_cor_2 = point[point.index('"origin"') + 2]
        sub_cor_3 = point[point.index('"origin"') + 3]
        result.append('"origin" ' + " ".join([cor_1, cor_2, cor_3]))
        sub_result.append('"origin" ' + " ".join([sub_cor_1, sub_cor_2, sub_cor_3]))
        point.remove('"origin"')
    for i, v in enumerate(sub_result):
        # joins = joins.replace(v, result[i])
        joins = joins.replace(v, result[i])
        print(joins)
    return joins.split()
def vmf_coordinates_get_pos(a, b):
    point = a
    cor_1 = point[point.index('"origin"', point.index('"info_vmfg_point_extnd_' + str(b) + '"')) + 1][1:]
    cor_2 = point[point.index('"origin"', point.index('"info_vmfg_point_extnd_' + str(b) + '"')) + 2]
    cor_3 = point[point.index('"origin"', point.index('"info_vmfg_point_extnd_' + str(b) + '"')) + 3][0:-1]
    return [float(cor_1), float(cor_2), float(cor_3)]
def vmf_coordinates_get_count(a):
    point = a
    cor_count = []
    try:
        point.index('"info_vmfg_point_extnd_1"')
        cor_count.append(1)
    except:
        cor_count_1 = []
    try:
        point.index('"info_vmfg_point_extnd_2"')
        cor_count.append(2)
    except:
        cor_count_2 = []
    try:
        point.index('"info_vmfg_point_extnd_3"')
        cor_count.append(3)
    except:
        cor_count_3 = []
    try:
        point.index('"info_vmfg_point_extnd_4"')
        cor_count.append(4)
    except:
        cor_count_4 = []

    return cor_count
def vmf_coordinates_del_ext(a, b):
    joins = " ".join(a)
    point = a
    for i in range(point.count('entity')):
        ent = point[point.index('entity'):point.index('}', point.index('entity')) + 2]
        try:
            ent.index('"info_vmfg_point_extnd_' + str(b) + '"')
        except:
            point.remove(point[point.index('entity')])
    delit = " ".join(point[point.index('entity'):point.index('}', point.index('entity')) + 2])
    joins = joins.replace(delit,"")
    return joins.split()
def vmf_collision_found(a):
    col_0_1_a = ""
    col_0_2_a = ""
    col_1_1_a = ""
    col_1_2_a = ""
    try:
        col_0_1_a = float(a[a.index('"origin"', a.index('"info_vmfg_point_col_0"')) + 1][1:])
        col_0_2_a = float(a[a.index('"origin"', a.index('"info_vmfg_point_col_0"')) + 2])
        col_1_1_a = float(a[a.index('"origin"', a.index('"info_vmfg_point_col_1"')) + 1][1:])
        col_1_2_a = float(a[a.index('"origin"', a.index('"info_vmfg_point_col_1"')) + 2])
    except:
        print("No index")
        return
    return [col_0_1_a, col_0_2_a, col_1_1_a, col_1_2_a]
def vmf_collision(a, b):
    try:
        def collision_check(c, d):
            is_col = 0
            for i in [d[0], d[2]]:
                if c[0] < i < c[2] or c[2] < i < c[0]:
                    is_col += 0.5
                    break
            for i in [d[1], d[3]]:
                if c[1] < i < c[3] or c[3] < i < c[1]:
                    is_col += 0.5
                    break
            if is_col == 1:
                return True
            else:
                return False
        col_box_1_a = []
        col_box_1_b = []
        return collision_check(a, b)
    except:
        print(a)
        print(b)
    # print("Lol")
    # print(col_box_1_a)
    # print(col_box_1_b)
