#!/usr/bin/python
# -*- coding:utf-8 -*-
#

__author__ = 'jcteng'


import tornado.web
import captcha


from tornado import gen


from wtforms.fields import IntegerField ,StringField,PasswordField,BooleanField
from wtforms.validators import Required
from wtforms import validators
from wtforms_tornado import Form

import hashlib


import xaceauth
class RegisterForm(Form):

    usr =  StringField('usr', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=6, max=35)])
    pwd = PasswordField('pwd', [
        validators.DataRequired(),
        validators.EqualTo('pwd2', message='Passwords must match')
    ])
    pwd2 = PasswordField('pwd2')
    tos = BooleanField('tos', [validators.DataRequired()])


class XaceAuthRegisterHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        self.render("register.html")


    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):

        form = RegisterForm(self.request.arguments)
        userinfo = self.request.arguments
        if form.validate():
            print "form OK"
        else:
           print self.request.body
           self.write("validate error")
           self.finish()
           return

        db = self.settings['db']
        user_check  = yield  db[xaceauth.XaceAuth_collection].find_one({'usr':userinfo['usr']})
        email_check = yield  db[xaceauth.XaceAuth_collection].find_one({'email':userinfo['email']})

        if (user_check!=None) or (email_check!=None):
           print self.request.body
           self.write("validate error:user & email registed")
           self.finish()
           return

        #simply remove items
        del userinfo['tos']
        del userinfo['pwd2']
        del userinfo['_xsrf']
        userinfo['pwd'] = hashlib.sha1(userinfo['pwd'][0]+xaceauth.XaceAuth_Realm).hexdigest()
        db[xaceauth.XaceAuth_collection].insert(userinfo)
        #if captcha and captcha == self.get_secure_cookie('captcha').replace(' ',''):
        #    self.flash('验证码输入正确', 'info')
        #else:
        #    self.flash('验证码输入错误', 'error')
        self.write("Register done!")
        print "register done"
        self.finish()