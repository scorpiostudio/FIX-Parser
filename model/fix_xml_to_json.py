#!/usr/bin/python2
# -*- coding:utf-8 -*-
import json
import xml.etree.cElementTree as ElementTree
import os


def xml_to_json(xml_filename):
    fix_dict = dict()
    xml_parser = ElementTree.parse(xml_filename)
    root = xml_parser.getroot()
    fields_dict = dict()
    messages_dict = dict()

    common_fields = list()
    headers = root.find("header")
    for header in headers.findall('field'):
        common_fields.append(header.get('name'))

    trailers = root.find("trailer")
    for trailer in trailers.findall('field'):
        common_fields.append(trailer.get('name'))

    fix_dict['common_fields'] = common_fields

    messages = root.find("messages")
    for message in messages.findall("message"):
        message_dict = dict()
        message_dict['name'] = message.get('name')
        message_dict['msgcat'] = message.get('msgcat')
        messages_dict[message.get('msgtype')] = message_dict

    fix_dict['messages'] = messages_dict

    fields = root.find("fields")
    for field in fields.findall("field"):
        # print field.get("number"), field.get("name"), field.get("type")
        field_dict = dict()
        field_dict["name"] = field.get("name")
        field_dict["type"] = field.get("type")
        values = dict()
        for value in field.findall("value"):
            # print "\t", value.get("enum"), value.get("description")
            enum_dict = dict()
            enum_dict["description"] = value.get("description")
            values[value.get("enum")] = enum_dict
        if len(values) > 0:
            field_dict["values"] = values
        fields_dict[int(field.get("number"))] = field_dict
    fix_dict['fields'] = fields_dict

    json_str = json.dumps(fix_dict, indent=4, sort_keys=True)
    return json_str


def fix_xml_to_json(xml_path):
    files = os.listdir(xml_path)
    for name in files:
        if name.endswith(".xml"):
            json_data = xml_to_json(os.path.join(xml_path, name))
            filename = name[:-4] + ".json"
            with open(os.path.join(xml_path, filename), "w+") as f:
                f.write(json_data)


if __name__ == '__main__':
    fix_xml_to_json(".")
