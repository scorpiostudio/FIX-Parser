#!/usr/bin/python2
# -*- coding:utf-8 -*-
import fix_dict
import re
import config


class FIXMessage(object):
    """
    FIX消息类
    """
    def __init__(self, raw, dict_path, fix_dict_name):
        """
        FIXMessage构造函数
        :param raw: FIX消息原始数据
        :param dict_path: FIX字典目录
        :param fix_dict_name: FIX字典名称
        """
        self.raw = raw
        # 选择AutoDetect时，根据FIX消息选择FIX协议字典
        if fix_dict_name == "auto":
            # FIX protocol version
            pattern = re.compile(r'8=FIX.(\d).(\d)')
            match = pattern.search(self.raw)
            dict_name = "FIX" + match.groups()[0] + match.groups()[1]
            self.fix_dict = fix_dict.get_fix_dict(dict_path, dict_name)
        else:
            self.fix_dict = fix_dict.get_fix_dict(dict_path, fix_dict_name)

    def parse(self):
        """
        FIX消息解析方法
        :return:
        """
        message_dict = dict()
        tag_value_list = self._split_fix_message()
        fields = list()
        message = ""
        msgcat = ""
        for tag_value in tag_value_list:
            # 解析tag-value对
            tag_value_dict = self._translate(tag_value)
            fields.append(tag_value_dict)
            # tag=35时增加message和msgcat属性
            if tag_value_dict['tag'] == "35":
                tag35_value = tag_value_dict['value']
                # 获取FIX消息的message和msgcat
                if tag35_value in self.fix_dict['messages']:
                    message = self.fix_dict['messages'][tag35_value]['name']
                    msgcat = self.fix_dict['messages'][tag35_value]['msgcat']
                else:
                    message = 'undefined'
                    msgcat = 'undefined'
        # tag-value对解析字典链表
        message_dict["fields"] = fields
        # FIX消息原始数据
        message_dict["raw"] = self.raw
        # message_dict["messages"] = self.fix_dict['messages']
        # 消息类型对应的message信息
        message_dict["message"] = message
        # 消息类型对应的msgcat
        message_dict["msgcat"] = msgcat
        # FIX消息对应的FIX字典的common_fields
        # message_dict["common_fields"] = self.fix_dict['common_fields']
        return message_dict

    def _split_fix_message(self):
        """
        将FIX消息原始数据分割为tag-value对的链表
        :return:
        """
        fields = list()
        pattern = re.compile(config.FIELD_PATTERN)
        # 匹配所有的tag-value对，并返回
        tag_value_pairs = pattern.findall(self.raw)
        fields.extend(tag_value_pairs)
        return fields

    def _translate(self, tag_value_pair):
        result = dict()
        # 将tag-value对的分隔符删除
        tag_value = re.sub(r'{}|\^A$'.format(config.DELIMITER_PATTERN), "", tag_value_pair)
        # 找到=的索引
        index = str(tag_value).index('=')
        # 提取tag
        tag = tag_value[0:index]
        # 提取value
        value = tag_value[index+1:]
        result['tag'] = tag
        result['value'] = value
        # 解析tag和value对应的信息
        if tag in self.fix_dict['fields']:
            # 获取tag_name
            result['tag_name'] = self.fix_dict['fields'][tag]['name']
            if result['tag_name'] in self.fix_dict['common_fields']:
                result['is_common_field'] = 'True'
            else:
                result['is_common_field'] = 'False'
            # 如果存在values
            if 'values' in self.fix_dict['fields'][tag]:
                if value in self.fix_dict['fields'][tag]['values']:
                    # 获取value_description
                    result['value_description'] = self.fix_dict['fields'][tag]['values'][value]['description']
                else:
                    # 如果value不再values内
                    result['value_description'] = 'undefined'
            else:
                result['value_description'] = ""
            result['value_type'] = self.fix_dict['fields'][tag]['type']
        else:
            # tag未在FIX字典定义
            result['tag_name'] = 'undefined'
            result['value_description'] = 'undefined'
            result['value_type'] = 'undefined'
        return result
