from flask import render_template
from flask.views import MethodView
from model.message_model import Message


class MessageView(MethodView):
    def dispatch_request(self, page=1):
        messages = Message.query.paginate(page, per_page=20)
        print messages
        return render_template('test.html', messages=messages)

    def get(self, page=1):
        messages = Message.query.paginate(page, per_page=20)
        print messages
        return render_template('test.html', messages=messages)