#!/usr/bin/python2
# -*- coding:utf-8 -*-
import re
from fix_message import FIXMessage
import config


class FIXParser(object):
    """
    """
    def __init__(self, dict_path, fix_dict_name):
        self.pattern = re.compile(config.MESSAGE_PATTERN)
        self.dict_path = dict_path
        self.fix_dict_name = fix_dict_name

    def parse_fix_message(self, fix_text):
        messages = self._split_fix_text(fix_text)
        lines = list()
        for raw_message in messages:
            fix_message = FIXMessage(raw_message, self.dict_path, self.fix_dict_name).parse()
            lines.append(fix_message)

        return lines

    @staticmethod
    def time_lines(lines):
        result = list()
        for line in lines:
            line_dict = dict()
            fields = line['fields']
            details = ""
            msg_type = ""
            side = ""
            order_qty = ""
            symbol = ""
            text = ""
            line_dict['client_order_id'] = ""
            for field in fields:
                if field['tag'] == '11':
                    line_dict['client_order_id'] = field['value']
                if field['tag'] == '35':
                    msg_type = field['value']
                    line_dict['message'] = line['message']
                    line_dict['msgcat'] = line['msgcat']
                if field['tag'] == '38':
                    order_qty = field['value']
                if field['tag'] == '49':
                    line_dict['sender'] = field['value']
                if field['tag'] == '52':
                    line_dict['time'] = field['value']
                if field['tag'] == '54':
                    side = field['value_description']
                if field['tag'] == '55':
                    symbol = field['value']
                if field['tag'] == '56':
                    line_dict['target'] = field['value']
                if field['tag'] == '58':
                    text = field['value']
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
        lines = list()
        text = fix_text
        if text is None:
            return lines
        while True:
            match = self.pattern.search(text)
            if match is None:
                break
            index = match.span()[1]
            lines.append(text[0:index])
            text = text[index:]
        return lines


if __name__ == '__main__':
    pass

