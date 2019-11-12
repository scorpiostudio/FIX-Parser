#!/usr/bin/python2
# -*- coding:utf-8 -*-
import re
from fix_message import FIXMessage
import config
import datetime, time

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
                if field['tag'] == '11':
                    line_dict['client_order_id'] = field['value']
                elif field['tag'] == '35':
                    msg_type = field['value']
                    # message
                    line_dict['message'] = line['message']
                    # msgcat为admin或app，用于Admin条件过滤
                    line_dict['msgcat'] = line['msgcat']
                elif field['tag'] == '38':
                    order_qty = field['value']
                # sender
                elif field['tag'] == '49':
                    line_dict['sender'] = field['value']
                # time
                elif field['tag'] == '52':
                    line_dict['time'] = field['value']
                elif field['tag'] == '54':
                    side = field['value_description']
                elif field['tag'] == '55':
                    symbol = field['value']
                # target
                elif field['tag'] == '56':
                    line_dict['target'] = field['value']
                elif field['tag'] == '58':
                    text = field['value']
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
        before = datetime.datetime.now()
        lines = list()
        if fix_text_list is None:
            return lines
        other_text = ''
        for text in fix_text_list:
            # print 'raw'
            # print text
            text = other_text + text
            # print 'concat '
            # print text
            n = 0
            while 1:
                # 匹配第一条FIX消息
                match = self.pattern.search(text)
                # 没有匹配，退出
                if match is None:
                    other_text = text
                    # print 'other_text'
                    # print other_text
                    break
                # 匹配对象的结束索引
                index = match.span()[1]
                n = index
                lines.append(str(text[0:index]).strip(" "))
                # 更新FIX消息文本，进行下一次匹配
                text = text[index:]

            # time.sleep(5)
        after = datetime.datetime.now()
        print 'split ', after - before
        return lines


if __name__ == '__main__':
    pass

