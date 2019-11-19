from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__, static_url_path='')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT '] = timedelta(seconds=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAX_CONTENT_LENGTH'] = 1024 << 20  # max upload size < 1024M


db = SQLAlchemy(app)

