from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import timedelta
from flask_dropzone import Dropzone

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT '] = timedelta(seconds=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/messages.db'
db = SQLAlchemy(app)

dropzone = Dropzone(app)
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'text'
