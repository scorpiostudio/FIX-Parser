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
from werkzeug.utils import secure_filename


def paginate_query(page, per_page):
    pagination = Message.query.paginate(page=page, per_page=per_page)
    messages = list()
    for item in pagination.items:
        line_dict = dict()
        line_dict['id'] = item.id
        line_dict['time'] = item.time
        line_dict['sender'] = item.sender
        line_dict['target'] = item.target
        line_dict['message'] = item.message
        line_dict['client_order_id'] = item.client_order_id
        line_dict['details'] = item.details
        line_dict['msgcat'] = item.msgcat
        line_dict['raw'] = item.raw
        line_dict['fields'] = json.loads(item.fields)
        messages.append(line_dict)
    return pagination, messages


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    config.log.logger.info('an new connection from {}'.format(request.remote_addr))
    text_list = list()
    if request.method == 'POST':
        # FIX协议版本
        fix_version = request.form['fix_version_select']
        # 上传文件
        f = request.files['file']
        filename = secure_filename(f.filename)
        config.log.logger.info('upload filename: {}'.format(filename))
        while True:
            text = f.read(1024)
            if len(text) > 0:
                text_list.append(text)
            else:
                break
        # 如果没有上传文件
        if len(text_list) < 1:
            # 文本编辑框内容
            text = request.form['input']
            text_list.append(text)
    else:
        text = request.args.get('input')
        fix_version = request.args.get('fix_version_select')
        if text is not None:
            text_list.append(text)

    if fix_version is None:
        fix_version = "auto"
    config.log.logger.info('fix version: {}'.format(fix_version))
    before = datetime.datetime.now()
    parser = FIXParser(fix_version)
    lines = parser.parse_fix_message(text_list)
    after = datetime.datetime.now()
    config.log.logger.info('parse elapsed time: {}'.format(after - before))
    try:
        before = datetime.datetime.now()
        # 删除表messages的所有记录
        sql = "DELETE FROM messages;"
        # sql = "DROP TABLE IF EXISTS messages;"
        db.session.execute(sql)
        db.session.commit()
        n = 0
        for line in lines:
            n = n + 1
            msg = Message(line['time'], line['sender'], line['target'], line['message'], line['client_order_id'],
                          line['details'], line['msgcat'], line['raw'], json.dumps(line['fields']))
            # 将用户添加到数据库会话中
            db.session.add(msg)
            if n % 1000 == 0:
                # 将数据库会话中的变动提交到数据库中,如果不Commit,数据库中是没有改动的
                db.session.commit()
        db.session.commit()
        after = datetime.datetime.now()
        config.log.logger.info('sqlite save elapsed time: {}'.format(after - before))
    except Exception as err:
        config.log.logger.error(err)
        db.session.rollback()
    pagination, messages = paginate_query(1, config.NUMBER_PER_PAGE)
    return render_template('index.html', standard_fix_list=config.STANDARD_FIX_LIST, pagination=pagination,
                           custom_fix_list=config.CUSTOM_FIX_LIST, fix_version=fix_version, messages=messages)


@app.route('/page', methods=['GET', 'POST'])
def query():
    pagination, messages = paginate_query(1, config.NUMBER_PER_PAGE)
    return render_template('query.html', messages=messages, pagination=pagination)


@app.route('/page/<int:page>', methods=['GET', 'POST'])
def query_page(page):
    pagination, messages = paginate_query(page, config.NUMBER_PER_PAGE)
    return render_template('query.html', messages=messages, pagination=pagination)


if __name__ == '__main__':
    # 生成JSON格式的FIX字典
    # fix_xml_to_json(config.FIX_DICT_PATH)
    # 创建数据库及表messages
    db.create_all()
    # 启动Server
    app.run(host=config.HOST, port=config.PORT, debug=False)
