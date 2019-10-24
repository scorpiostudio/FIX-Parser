#!/usr/bin/python2
# -*- coding:utf-8 -*-
import fix_dict
import re
import config


class FIXMessage(object):
    """

    """
    def __init__(self, raw, dict_path, fix_dict_name):
        self.raw = raw
        if fix_dict_name == "auto":
            # FIX protocol version
            pattern = re.compile(r'8=FIX.(\d).(\d)')
            match = pattern.search(self.raw)
            dict_name = "FIX" + match.groups()[0] + match.groups()[1]
            self.fix_dict = fix_dict.get_fix_dict(dict_path, dict_name)
        else:
            self.fix_dict = fix_dict.get_fix_dict(dict_path, fix_dict_name)

    def parse(self):
        message_dict = dict()
        tag_value_list = self._split_fix_message()
        fields = list()
        message = ""
        msgcat = ""
        for tag_value in tag_value_list:
            tag_value_dict = self._translate(tag_value)
            fields.append(tag_value_dict)
            # tag=35时增加message和msgcat属性
            if tag_value_dict['tag'] == "35":
                tag35_value = tag_value_dict['value']
                if tag35_value in self.fix_dict['messages']:
                    message = self.fix_dict['messages'][tag35_value]['name']
                    msgcat = self.fix_dict['messages'][tag35_value]['msgcat']
                else:
                    message = 'undefined'
                    msgcat = 'undefined'

        message_dict["fields"] = fields
        message_dict["raw"] = self.raw
        # message_dict["messages"] = self.fix_dict['messages']
        message_dict["message"] = message
        message_dict["msgcat"] = msgcat
        message_dict["common_fields"] = self.fix_dict['common_fields']
        return message_dict

    def _split_fix_message(self):
        fields = list()
        pattern = re.compile(config.FIELD_PATTERN)
        tag_value_pairs = pattern.findall(self.raw)
        fields.extend(tag_value_pairs)
        return fields

    def _translate(self, tag_value_pair):
        result = dict()
        tag_value = re.sub(r'{}|\^A$'.format(config.DELIMITER_PATTERN), "", tag_value_pair)
        index = str(tag_value).index('=')
        tag = tag_value[0:index]
        value = tag_value[index+1:]
        result['tag'] = tag
        result['value'] = value
        if tag in self.fix_dict['fields']:
            result['tag_name'] = self.fix_dict['fields'][tag]['name']
            if 'values' in self.fix_dict['fields'][tag]:
                if value in self.fix_dict['fields'][tag]['values']:
                    result['value_description'] = self.fix_dict['fields'][tag]['values'][value]['description']
                else:
                    result['value_description'] = 'undefined'
            else:
                result['value_description'] = ""
            result['value_type'] = self.fix_dict['fields'][tag]['type']
        else:
            result['tag_name'] = 'undefined'
            result['value_description'] = 'undefined'
            result['value_type'] = 'undefined'
        return result
