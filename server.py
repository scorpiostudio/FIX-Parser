#!/usr/bin/python2
# -*- coding:utf-8 -*-
from flask import render_template, request
from model.fix_parser import FIXParser
from model.fix_xml_to_json import fix_xml_to_json
import json
import config
from app import app, db
from model.message_model import Message
import datetime


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
    parser = FIXParser(fix_version)
    text_list = list()
    if text is not None:
        text_list.append(text)
    lines = parser.parse_fix_message(text_list)
    # 删除表messages的所有记录
    # sql = "DELETE FROM messages;"
    # db.session.execute(sql)
    # for line in lines:
    #     print line
    #     msg = Message(line['time'], line['sender'], line['target'], line['message'], line['client_order_id'],
    #                   line['details'], line['msgcat'], line['raw'], json.dumps(line['fields']))
    #
    #     # 将用户添加到数据库会话中
    #     db.session.add(msg)
    #     # 将数据库会话中的变动提交到数据库中,如果不Commit,数据库中是没有改动的
    #     db.session.commit()
    return render_template('index.html', standard_fix_list=config.STANDARD_FIX_LIST,
                           custom_fix_list=config.CUSTOM_FIX_LIST, fix_version=fix_version, messages=lines)


@app.route('/page/<int:page>', methods=['GET', 'POST'])
def query(page):
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.paginate(page, 100, False)
    return render_template('test.html', pagination=pagination)


@app.route('/upload', methods=['POST'])
def upload_file():
    before = datetime.datetime.now()
    f = request.files.get('file')  # 获取文件对象
    text_list = list()
    while True:
        text = f.read(1024)
        if len(text) > 0:
            text_list.append(text)
        else:
            break
    fix_version = "auto"
    parser = FIXParser(fix_version)
    lines = parser.parse_fix_message(text_list)
    after = datetime.datetime.now()
    print 'parse: ', (after - before)
    before = datetime.datetime.now()
    # 删除表messages的所有记录
    sql = "DELETE FROM messages;"
    db.session.execute(sql)
    n = 0
    for line in lines:
        n = n + 1
        msg = Message(line['time'], line['sender'], line['target'], line['message'], line['client_order_id'],
                      line['details'], line['msgcat'], line['raw'], json.dumps(line['fields']))
        # if len(line['raw']) > 512:
        #     print len(line['raw'])
        # if len(json.dumps(line['fields'])) > 4096:
        #     print len(json.dumps(line['fields']))
        if n < 5:
            print line
        # 将用户添加到数据库会话中
        db.session.add(msg)
        if n % 1000 == 0:
            # 将数据库会话中的变动提交到数据库中,如果不Commit,数据库中是没有改动的
            db.session.commit()
    db.session.commit()
    after = datetime.datetime.now()
    print 'sqlite: ', (after - before)
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.paginate(page, 100, False)
    return render_template('test.html', pagination=pagination)


if __name__ == '__main__':
    # 生成JSON格式的FIX字典
    fix_xml_to_json(config.FIX_DICT_PATH)
    # 创建数据库及表messages
    db.create_all()
    # 启动Server
    app.run(host=config.HOST, port=config.PORT, debug=True, threaded=True)
