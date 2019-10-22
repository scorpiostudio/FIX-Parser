from flask import Flask, render_template, request
from model.fix_parser import FIXParser
import json


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


def header_lines(lines):
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


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['input']
    else:
        text = request.args.get('input')
    parser = FIXParser()
    messages = parser.parse_fix_message(text)
    lines = header_lines(messages)
    print messages
    result = ""
    for line in messages:
        for field in line['fields']:
            result += field['tag'] + field['tag_name'] + field['value'] + field['value_description']
        result += "\r\n\r\n"
    # return result
    return render_template('index.html', lines=lines, messages=messages)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
