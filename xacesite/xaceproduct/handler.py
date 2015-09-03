#!/usr/bin/python
# -*- coding:utf-8 -*-
#
import tornado

import xacedoc


from tornado import  gen

from xacedoc import  XaceBlog,XaceBlogContainer



class xProductHandler(tornado.web.RequestHandler):
    def  get(self,oid):
        currentUser = "123"
        self.render("Xproduct.html",isLogin=(currentUser!=None),currentUser=currentUser)