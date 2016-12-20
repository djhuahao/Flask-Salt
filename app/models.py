#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: Yxn
# date: 2016/10/18

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    '''用户表'''
    __tablename__ = "salt_user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.VARCHAR(6), nullable=False, unique=True)
    user_pass = db.Column(db.String(66), nullable=False, unique=True)
    user_email = db.Column(db.VARCHAR(30), nullable=False, unique=True)
    user_role = db.Column(db.VARCHAR(8), nullable=False)
    user_regtime = db.Column(db.DATETIME, nullable=False)

    def __init__(self, username, password, email, role, regtime):
        self.user_name = username
        self.password = password
        self.user_email = email
        self.user_role = role
        self.user_regtime = regtime

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, password):
        self.user_pass = generate_password_hash(password, salt_length=8)

    def verify_password(self, password):
        return check_password_hash(self.user_pass, password)

    def __repr__(self):
        return "<User> %s".format(self.user_name)

    def get_id(self):
        return str(self.user_id)


class Group(db.Model):
    '''主机组表'''
    __tablename__ = "salt_group"
    group_id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    group_name = db.Column(db.VARCHAR(10), unique=True, nullable=False)
    host_name = db.relationship("Host", backref="salt_host", lazy="dynamic")

    def __init__(self, groupname):
        self.group_name = groupname


class Host(db.Model):
    '''主机表'''
    __tablename__ = 'salt_host'
    host_id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    host_name = db.Column(db.VARCHAR(36), unique=True, nullable=False)
    host_group = db.Column(db.VARCHAR(10), db.ForeignKey('salt_group.group_name'), nullable=False)

    # host_status = db.Column(db.VARCHAR(6), nullable=False)
    # last_time = db.Column(db.TIMESTAMP(), nullable=False)

    def __init__(self, hostname, groupname):
        self.host_name = hostname
        self.host_group = groupname


class PublishLog(db.Model):
    __tablename__ = 'salt_publish_log'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    operator_time = db.Column(db.TIMESTAMP(), nullable=False)
    project_name = db.Column(db.NVARCHAR(30), nullable=False)
    project_version = db.Column(db.INTEGER, nullable=False)
    operator_user = db.Column(db.NVARCHAR(20), nullable=False)
    operator_message = db.Column(db.NVARCHAR(500), nullable=False)
    operator_path = db.Column(db.NVARCHAR(1000), nullable=False)

    def __init__(self, time, project, version, user, message, path):
        self.operator_time = time
        self.project_name = project
        self.project_version = version
        self.operator_user = user
        self.operator_path = path
        self.operator_message = message


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
