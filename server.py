#!/usr/bin/python2
# -*- coding:utf-8 -*-
from flask import Flask, render_template, request
from model.fix_parser import FIXParser
from model.fix_xml_to_json import fix_xml_to_json
import json
import config


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['input']
        fix_version = request.form['fix_version_select']
    else:
        text = request.args.get('input')
        fix_version = request.args.get('fix_version_select')
    if fix_version is None:
        fix_version = "auto"
    parser = FIXParser(config.FIX_DICT_PATH, fix_version)
    messages = parser.parse_fix_message(text)
    lines = parser.time_lines(messages)
    return render_template('index.html', standard_fix_list=config.STANDARD_FIX_LIST,
                           custom_fix_list=config.CUSTOM_FIX_LIST, fix_version=fix_version, lines=lines,
                           messages=messages, raw=text)


if __name__ == '__main__':
    # 生成JSON格式的FIX字典
    fix_xml_to_json(config.FIX_DICT_PATH)

    # 启动Server
    app.run(host=config.HOST, port=config.PORT, debug=True)
