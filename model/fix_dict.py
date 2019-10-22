#!/usr/bin/python2
# -*- coding: UTF-8 -*-
import json
import os

"""
FIX数据字典定义
"""

FIX_DICT_PATH = "model/FIX_Dict"
FIX40_DICT = json.load(open(os.path.join(FIX_DICT_PATH, "FIX40.json"), "r"))
FIX41_DICT = json.load(open(os.path.join(FIX_DICT_PATH, "FIX41.json"), "r"))
FIX42_DICT = json.load(open(os.path.join(FIX_DICT_PATH, "FIX42.json"), "r"))
FIX43_DICT = json.load(open(os.path.join(FIX_DICT_PATH, "FIX43.json"), "r"))
FIX44_DICT = json.load(open(os.path.join(FIX_DICT_PATH, "FIX44.json"), "r"))
FIX50_DICT = json.load(open(os.path.join(FIX_DICT_PATH, "FIX50.json"), "r"))
FIXT11_DICT = json.load(open(os.path.join(FIX_DICT_PATH, "FIXT11.json"), "r"))


def get_fix_dict(fix_name):
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
    else:
        return dict()


if __name__ == '__main__':
    print FIX40_DICT
    print FIX41_DICT
    print FIX42_DICT
    print FIX43_DICT
    print FIX44_DICT
    print FIX50_DICT
    print FIXT11_DICT
