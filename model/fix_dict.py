#!/usr/bin/python2
# -*- coding:utf-8 -*-
import json
import os


def get_fix_dict(dict_path, fix_name):
    """
    获取FIX字典
    :param dict_path: FIX字典目录
    :param fix_name: FIX字典名称
    :return: 返回FIX字典
    """
    if fix_name == "FIX40":
        return json.load(open(os.path.join(dict_path, "FIX40.json"), "r"))
    elif fix_name == "FIX41":
        return json.load(open(os.path.join(dict_path, "FIX41.json"), "r"))
    elif fix_name == "FIX42":
        return json.load(open(os.path.join(dict_path, "FIX42.json"), "r"))
    elif fix_name == "FIX43":
        return json.load(open(os.path.join(dict_path, "FIX43.json"), "r"))
    elif fix_name == "FIX44":
        return json.load(open(os.path.join(dict_path, "FIX44.json"), "r"))
    elif fix_name == "FIX50":
        return json.load(open(os.path.join(dict_path, "FIX50.json"), "r"))
    elif fix_name == "FIXT11":
        return json.load(open(os.path.join(dict_path, "FIXT11.json"), "r"))
    else:
        return json.load(open(os.path.join(dict_path, fix_name + ".json"), "r"))


if __name__ == '__main__':
    print get_fix_dict('../FIX_DICT', 'FIX40')
    print get_fix_dict('../FIX_DICT', 'FIX41')
    print get_fix_dict('../FIX_DICT', 'FIX42')
    print get_fix_dict('../FIX_DICT', 'FIX43')
    print get_fix_dict('../FIX_DICT', 'FIX44')
    print get_fix_dict('../FIX_DICT', 'FIX50')
    print get_fix_dict('../FIX_DICT', 'FIXT11')
