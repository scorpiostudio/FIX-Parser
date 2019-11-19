#!/usr/bin/python2
# -*- coding:utf-8 -*-
import json
import os
import config


FIX40_DICT = json.load(open(os.path.join(config.FIX_DICT_PATH, "FIX40.json"), "r"))
FIX41_DICT = json.load(open(os.path.join(config.FIX_DICT_PATH, "FIX41.json"), "r"))
FIX42_DICT = json.load(open(os.path.join(config.FIX_DICT_PATH, "FIX42.json"), "r"))
FIX43_DICT = json.load(open(os.path.join(config.FIX_DICT_PATH, "FIX43.json"), "r"))
FIX44_DICT = json.load(open(os.path.join(config.FIX_DICT_PATH, "FIX44.json"), "r"))
FIX50_DICT = json.load(open(os.path.join(config.FIX_DICT_PATH, "FIX50.json"), "r"))
FIXT11_DICT = json.load(open(os.path.join(config.FIX_DICT_PATH, "FIXT11.json"), "r"))
CICC_FIX42_DICT = json.load(open(os.path.join(config.FIX_DICT_PATH, "CICC_FIX42.json"), "r"))
UBS_FIX42_DICT = json.load(open(os.path.join(config.FIX_DICT_PATH, "UBS_FIX42.json"), "r"))


def get_fix_dict(fix_name):
    """
    获取FIX字典
    :param fix_name: FIX字典名称
    :return: 返回FIX字典
    """
    if fix_name == "FIX40":
        return FIX40_DICT
    elif fix_name == "FIX41":
        return FIX41_DICT
    elif fix_name == "FIX42":
        return FIX42_DICT
    elif fix_name == "FIX43":
        return FIX43_DICT
    elif fix_name == "FIX44":
        return FIX44_DICT
    elif fix_name == "FIX50":
        return FIX50_DICT
    elif fix_name == "FIXT11":
        return FIXT11_DICT
    elif fix_name == "CICC_FIX42":
        return CICC_FIX42_DICT
    elif fix_name == "UBS_FIX42":
        return UBS_FIX42_DICT


if __name__ == '__main__':
    print get_fix_dict('FIX40')
    print get_fix_dict('FIX41')
    print get_fix_dict('FIX42')
    print get_fix_dict('FIX43')
    print get_fix_dict('FIX44')
    print get_fix_dict('FIX50')
    print get_fix_dict('FIXT11')
    print get_fix_dict('CICC_FIX42')
    print get_fix_dict('UBS_FIX42')
