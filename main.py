from linecache import checkcache

import modul_vmf_editing as vmf_func
import random
import configparser
import math
import json
from PIL import Image
# Formula - 32768 / 1024 = 32
# 1 = 1024
# -16384 16384 = 0, 0
# 16384 -16384 = 32768, 32768
# -15872 15872 = 1 chunk
def new_to_old_coord_system(a, b, c, d, e):
    return c + a, d - b, e
def chunk_pos(a, b, c, d):
    return (c/2) + (c * a), (c/2) + (c * b), d
def min_max_chunk(a, b):
    return 0, (b/a)
def map_creation(*args):
    map_result = []
    for i in args:
        with open(i[0], "r") as map_read:
            map_readed = map_read.read()
            map_solid = vmf_func.vmf_map_solid(map_readed)
            map_entity = vmf_func.vmf_map_entity(map_readed)
            map_solid = vmf_func.vmf_coordinates_set(map_solid, i[1])
            map_entity = vmf_func.vmf_coordinates_set_point(map_entity, i[1])
            map_result.append(map_solid)
            map_result.append(map_entity)
    return map_result
def map_creation_result(a, b):
    map_base = open(a, 'r')
    map_base_result = map_base.read()
    map_base.close()
    return " ".join(vmf_func.vmf_map_merge(map_base_result.split(), b))
def near_chunk(a):
    return (a[0] - 1, a[1]), (a[0], a[1] - 1), (a[0] + 1, a[1]), (a[0], a[1] + 1)
def num_equal(a, b):
    check = []
    for i in a:
        for v in b:
            if v == i:
                check.append(True)
                break
    return len(check) == len(a)
cfg = configparser.ConfigParser()
cfg.read("config_vmfg.cfg")
map_rooms_start = []
map_rooms_num = []
map_rooms = []
map_result_write = []
room_pattern = []
img = Image.open("image/map_example.png")

size1 = img.size[0]
size2 = img.size[1]
for i in range(0, size1):
    for v in range(0, size2):
        if img.getpixel((i, v)) == (0, 0, 0, 255):
            map_rooms_start.append((i, v))

img.close()

print(cfg.items("MAPS"))

for i in cfg.items("MAPS"):
    list_1 = []
    for v in i[1].split()[1:]:
        list_1.append(int(v))
    room_pattern.append((i[1].split()[0], list_1))
for i in map_rooms_start:
    num_list = []
    for v in map_rooms_start:
        chunk_num = near_chunk(i)
        if chunk_num[0] == v:
            num_list.append(1)
        elif chunk_num[1] == v:
            num_list.append(2)
        elif chunk_num[2] == v:
            num_list.append(3)
        elif chunk_num[3] == v:
            num_list.append(4)
    map_rooms_num.append(num_list)
for i, v in enumerate(map_rooms_num):
    room = []
    for val in room_pattern:
        if len(v) == len(val[1]):
            check = num_equal(v, val[1])
            if check:
                room.append(val[0])
    chunk_pos_new = chunk_pos(map_rooms_start[i][0], map_rooms_start[i][1], float(cfg["CONFIG_VAR"]['chunk_max']), float(cfg["CONFIG_VAR"]['chunk_max']))
    map_rooms.append((random.choice(room), new_to_old_coord_system(chunk_pos_new[0], chunk_pos_new[1], float(-16384), float(16384), int(cfg["CONFIG_VAR"]['height']))))
    # for i in range(len(map_rooms_start)):
    #     for val in v[1]:
    #         if map_rooms_start
    # for num in map_rooms_num[i]:
    #     print(next(num_1))
    # chunk_pos_new = chunk_pos(v[0], v[1], 1024, 1024)
    # map_rooms.append(("maps/vmfg_chunk.vmf", new_to_old_coord_system(chunk_pos_new[0], chunk_pos_new[1], -16384, 16384, 0)))
for i in map_rooms:
    map_result_write.extend(map_creation(i))
with open("map_result/vmfg_map_result_1.vmf", "w") as map_write:
    map_write.write(map_creation_result("maps/vmfg_base.vmf", map_result_write))


# test = False
