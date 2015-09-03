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


from tornado.web import RequestHandler


class LoginForm(Form):

    email = StringField('email', [validators.Length(min=4, max=35)])
    pwd = PasswordField('pwd', [
        validators.DataRequired(),
        validators.EqualTo('pwd', message='Passwords must match')
    ])



class XaceAuthLoginHandler(tornado.web.RequestHandler):
    SessionUpdateHandler=None

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        usr = yield  self.get_current_user()
        if usr!=None :
            print "login already"
            self.redirect("/")
            print self.current_user
            return
        self.render("login.html")


    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):

        form = LoginForm(self.request.arguments)
        userinfo = self.request.arguments
        if form.validate():
            print "form OK"
        else:
           print self.request.body
           self.write("validate error")
           self.finish()
           return

        userinfo['pwd'] = hashlib.sha1(userinfo['pwd'][0]+xaceauth.XaceAuth_Realm).hexdigest()

        db = self.settings['db']
        user_check  = yield  db[xaceauth.XaceAuth_collection].find_one({'usr':userinfo['email'],'pwd':userinfo['pwd']})
        if(user_check==None):
            user_check = yield  db[xaceauth.XaceAuth_collection].find_one({'email':userinfo['email'],'pwd':userinfo['pwd']})

        if(user_check==None):
           print self.request.body
           self.write("Login failed!")
           self.finish()
           return

        print user_check
        self.set_secure_cookie(xaceauth.XaceAuth_User_Cookie, str(user_check["usr"][0]))
        #if captcha and captcha == self.get_secure_cookie('captcha').replace(' ',''):
        #    self.flash('验证码输入正确', 'info')
        #else:
        #    self.flash('验证码输入错误', 'error')
        if self.SessionUpdateHandler:
            self.SessionUpdateHandler(str(user_check["usr"][0]))
        self.write("Login done!")
        self.redirect("/")
        #self.finish()

class XaceAuthLogoutHandler(tornado.web.RequestHandler):
        SessionUpdateHandler=None
        def get(self):

            if self.SessionUpdateHandler:
                self.SessionUpdateHandler(None)
            self.clear_cookie(xaceauth.XaceAuth_User_Cookie)
            self.redirect(self.get_argument("next", "/"))

