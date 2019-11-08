#!/usr/bin/python2
# -*- coding:utf-8 -*-
import re
from fix_message import FIXMessage
import config


class FIXParser(object):
    """
    FIX消息文本解析器
    """
    def __init__(self, dict_path, fix_dict_name):
        """
        FIXParser构造函数
        :param dict_path: FIX字典目录
        :param fix_dict_name: FIX协议名称
        """
        # FIX消息匹配的正则表达式对象
        self.pattern = re.compile(config.MESSAGE_PATTERN)
        self.dict_path = dict_path
        self.fix_dict_name = fix_dict_name

    def parse_fix_message(self, fix_text):
        """
        FIX消息文本解析方法
        :param fix_text: FIX消息文本字符串
        :return: 返回解析后的FIX消息链表
        """
        messages = self._split_fix_text(fix_text)
        lines = list()
        for raw_message in messages:
            fix_message = FIXMessage(raw_message, self.dict_path, self.fix_dict_name).parse()
            lines.append(fix_message)

        return lines

    @staticmethod
    def time_lines(lines):
        """
        提取生成Time Line表格数据
        :param lines:
        :return:
        """
        result = list()
        for line in lines:
            line_dict = dict()
            line_dict['fields'] = line['fields']
            line_dict['raw'] = line['raw']
            fields = line['fields']
            details = ""
            msg_type = ""
            side = ""
            order_qty = ""
            symbol = ""
            text = ""
            line_dict['client_order_id'] = ""
            for field in fields:
                # client_order_id
                if field['tag'] == '11':
                    line_dict['client_order_id'] = field['value']
                if field['tag'] == '35':
                    msg_type = field['value']
                    # message
                    line_dict['message'] = line['message']
                    # msgcat为admin或app，用于Admin条件过滤
                    line_dict['msgcat'] = line['msgcat']
                if field['tag'] == '38':
                    order_qty = field['value']
                # sender
                if field['tag'] == '49':
                    line_dict['sender'] = field['value']
                # time
                if field['tag'] == '52':
                    line_dict['time'] = field['value']
                if field['tag'] == '54':
                    side = field['value_description']
                if field['tag'] == '55':
                    symbol = field['value']
                # target
                if field['tag'] == '56':
                    line_dict['target'] = field['value']
                if field['tag'] == '58':
                    text = field['value']
            # details生成
            if msg_type == 'D':
                details = side + " " + order_qty + " " + symbol
            elif msg_type == 'F':
                details = side + " " + order_qty + " " + symbol
            elif msg_type == "3":
                details = text
            line_dict['details'] = details
            result.append(line_dict)
        return result

    def _split_fix_text(self, fix_text):
        """
        FIX消息文本分割方法
        :param fix_text:
        :return:返回分割后的FIX消息链表
        """
        lines = list()
        text = fix_text
        if text is None:
            return lines
        while True:
            # 匹配第一条FIX消息
            match = self.pattern.search(text)
            # 没有匹配，退出
            if match is None:
                break
            # 匹配对象的结束索引
            index = match.span()[1]
            lines.append(str(text[0:index]).strip(" ") + '\n')
            # 更新FIX消息文本，进行下一次匹配
            text = text[index:]
        return lines


if __name__ == '__main__':
    pass

