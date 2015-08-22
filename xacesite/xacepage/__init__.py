#!/usr/bin/python
# -*- coding:utf-8 -*-
#

__author__ = 'jcteng'

import tornado.web
from tornado import  gen


from wtforms.fields import IntegerField ,StringField,PasswordField,BooleanField
from wtforms.validators import Required
from wtforms import validators
from wtforms_tornado import Form

XacePages_collection="XacePages"
XacePages_Realm="xace.in"



class LoginForm(Form):

    email = StringField('url', [validators.Length(min=4, max=35)])


class XaceBasePage(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self,pageid):
        print "get"


    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        print "post"