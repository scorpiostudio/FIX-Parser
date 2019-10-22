import fix_dict
import re


class FIXMessage(object):
    """

    """
    def __init__(self, raw):
        self.raw = raw
        # FIX protocol version
        pattern = re.compile(r'8=FIX.(\d).(\d)')
        match = pattern.search(self.raw)
        fix_dict_name = "FIX" + match.groups()[0] + match.groups()[1]
        self.fix_dict = fix_dict.get_fix_dict(fix_dict_name)

    def parse(self):
        message_dict = dict()
        tag_value_list = self._split_fix_message()
        fields = list()
        message = ""
        msgcat = ""
        for tag_value in tag_value_list:
            tag_value_dict = self._translate(tag_value)
            fields.append(tag_value_dict)
            if tag_value_dict['tag'] == "35":
                message = self.fix_dict['messages'][tag_value_dict['value']]['name']
                msgcat = self.fix_dict['messages'][tag_value_dict['value']]['msgcat']

        message_dict["fields"] = fields
        message_dict["raw"] = self.raw
        message_dict["messages"] = self.fix_dict['messages']
        message_dict["message"] = message
        message_dict["msgcat"] = msgcat
        message_dict["common_fields"] = self.fix_dict['common_fields']
        return message_dict

    def _split_fix_message(self):
        fields = list()
        pattern = re.compile(r'8=FIX.\d.\d[.|\^?,\x01]')
        tag_value_header = pattern.findall(self.raw)
        fields.extend(tag_value_header)
        pattern = re.compile(r'\d+=.+?[.|\^?,\x01]')
        tag_value_pairs = pattern.findall(self.raw[10:])
        fields.extend(tag_value_pairs[1:])
        return fields

    def _translate(self, tag_value_pair):
        result = dict()
        tag_value = tag_value_pair[0:-1]
        index = str(tag_value).index('=')
        tag = tag_value[0:index]
        value = tag_value[index+1:]
        result['tag'] = tag
        result['value'] = value
        result['tag_name'] = self.fix_dict['fields'][tag]['name']
        if 'values' in self.fix_dict['fields'][tag]:
            result['value_description'] = self.fix_dict['fields'][tag]['values'][value]['description']
        else:
            result['value_description'] = ""
        result['value_type'] = self.fix_dict['fields'][tag]['type']
        return result
