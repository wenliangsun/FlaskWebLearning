#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'swl'
__mtime__ = '8/4/18'
在程序中集成发送电子邮件功能以及异步发送电子邮件
"""

import os

from flask import Flask, render_template, flash
from flask import url_for, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_moment import Moment
from flask_mail import Mail, Message
from flask_migrate import Migrate, MigrateCommand
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from threading import Thread

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'hard to guess string'

app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USERNAME'] = "wenlsun@163.com"
app.config['MAIL_PASSWORD'] = "swl786128891"
app.config['FLASKY_MIAL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FlASKY_MAIL_SENDER'] = 'Chapter7 Admin <wenlsun@163.com>'
app.config['FlASKY_ADMIN'] = 'wenlsun@163.com'

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)  # 程序使用的数据库
mail = Mail(app)
migrate = Migrate(app, db)


def send_email_sync(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MIAL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FlASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email_async(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MIAL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FlASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    th = Thread(target=send_async_email,args=[app,msg])
    th.start()
    return th


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')  # backref 参数向 User 模型中添加一个 role 属性,从而定义反向关系。

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['know'] = False
            if app.config['FlASKY_ADMIN']:
                send_email_async(app.config['FlASKY_ADMIN'], 'New User', 'mail/new_user', name=user.username)
        else:
            session['know'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form,
                           name=session.get('name'),
                           know=session.get('know', False))


if __name__ == '__main__':
    app.run(debug=True)
