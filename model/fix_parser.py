#!/usr/bin/python2
# -*- coding:utf-8 -*-
import re
from fix_message import FIXMessage
import config

FIX_PARSER_PATTERN = re.compile(config.MESSAGE_PATTERN)


class FIXParser(object):
    """
    FIX消息文本解析器
    """
    def __init__(self, fix_dict_name):
        """
        FIXParser构造函数
        :param fix_dict_name: FIX协议名称
        """
        # FIX消息匹配的正则表达式对象
        self.pattern = FIX_PARSER_PATTERN
        self.fix_dict_name = fix_dict_name

    def parse_fix_message(self, fix_text_list):
        """
        FIX消息文本解析方法
        :param fix_text_list: FIX消息文本字符串
        :return: 返回解析后的FIX消息链表
        """
        messages = self.split_fix_text(fix_text_list)
        lines = list()
        for raw_message in messages:
            line = FIXMessage(raw_message, self.fix_dict_name).parse()
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
                if field[0] == '11':
                    line_dict['client_order_id'] = field[1]
                elif field[0] == '35':
                    msg_type = field[1]
                    # message
                    line_dict['message'] = line['message']
                    # msgcat为admin或app，用于Admin条件过滤
                    line_dict['msgcat'] = line['msgcat']
                elif field[0] == '38':
                    order_qty = field[1]
                # sender
                elif field[0] == '49':
                    line_dict['sender'] = field[1]
                # time
                elif field[0] == '52':
                    line_dict['time'] = field[1]
                elif field[0] == '54':
                    side = field[4]
                elif field[0] == '55':
                    symbol = field[1]
                # target
                elif field[0] == '56':
                    line_dict['target'] = field[1]
                elif field[0] == '58':
                    text = field[1]
            # details生成
            if msg_type == 'D':
                details = side + " " + order_qty + " " + symbol
            elif msg_type == 'F':
                details = side + " " + order_qty + " " + symbol
            elif msg_type == "3":
                details = text
            line_dict['details'] = details
            lines.append(line_dict)

        return lines

    def split_fix_text(self, fix_text_list):
        """
        FIX消息文本分割方法
        :param fix_text_list:
        :return:返回分割后的FIX消息链表
        """
        lines = list()
        if fix_text_list is None:
            return lines
        other_text = ''
        for text in fix_text_list:
            text = other_text + text
            n = 0
            while 1:
                # 匹配第一条FIX消息
                match = self.pattern.search(text)
                # 没有匹配，退出
                if match is None:
                    other_text = text
                    break
                # 匹配对象的结束索引
                index = match.span()[1]
                lines.append(str(text[0:index]).strip(" "))
                # 更新FIX消息文本，进行下一次匹配
                text = text[index:]
        return lines


if __name__ == '__main__':
    pass

