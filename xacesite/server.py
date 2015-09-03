#!/usr/bin/python
# -*- coding:utf-8 -*-
#

#
__author__ = 'jcteng'


import tornado
import tornado.web
import motor




from tornado import gen

db_test_collection="test"

def db_callback(result, error):
    print 'result', repr(result)

import motorengine
def setMotorEngine():
    io_loop = tornado.ioloop.IOLoop.instance()
    motorengine.connect("xacesite", host="192.168.1.21", port=27017, io_loop=io_loop)
    return io_loop

def setDB():

    db_uri = "mongodb://192.168.1.21:27017"
    db_name = "xacesite"

    client = motor.MotorClient(db_uri)
    return client[db_name]

class IndexHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        print self.request.remote_ip
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')
        usr = yield self.get_current_user()
        self.write(str(usr))
        self.finish()




class QueryHandler(tornado.web.RequestHandler):
    items=[]
    @tornado.web.asynchronous
    def get(self):
        db = self.settings['db']
        db[db_test_collection].find().each(self._got)
        self.items = []

    def _got(self, result, error):
        if result == None:
            self.render("QueryResults.html", title="Query Results", items=self.items)
        else:
            self.items.append(str(result))


class InsertHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("Insert.html")
    @tornado.web.asynchronous
    def post(self):

        usr = self.get_argument('username')
        pwd = self.get_argument('password')
        db = self.settings['db']
        db[db_test_collection].insert({"usr":usr,"pwd":pwd},callback=self.posted)

    def posted(self, result, error):

        print self.current_user
        self.write("Post done!")
        self.finish()
#sample with gen.coroutine
class InsertHandler2(tornado.web.RequestHandler):
    def get(self):
        self.render("Insert.html")

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        usr = self.get_argument('username')
        pwd = self.get_argument('password')
        db = self.settings['db']
        db[db_test_collection].insert({"usr":usr,"pwd":pwd})
        self.write("Post done!")
        self.finish()




import os
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "statics"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    #"xsrf_cookies": True,
    "template_path":"templates",
    "debug":True,
    "autoreload":True}

if __name__ == '__main__':
    import tornado.options
    import tornado.httpserver
    import xaceauth.register
    import xaceauth.login

    import os
    from xacedoc.simpleBlog import versionBlogHandler,XBlogSideNotesHandler,XblogElementsHandler
    from xaceproduct.handler import xProductHandler
    from xacegrid.Handler import gridDesignerHandler
    tornado.options.parse_command_line()
    application = tornado.web.Application([(r'/', IndexHandler),
                                      (r'/query', QueryHandler),
                                      (r'/insert', InsertHandler),
                                      (r'/insert2', InsertHandler2),
                                      (r'/register', xaceauth.register.XaceAuthRegisterHandler),
                                      (r'/login', xaceauth.login.XaceAuthLoginHandler),
                                      (r'/logout', xaceauth.login.XaceAuthLogoutHandler),
                                      (r"/xacesite/statics/(.*)",tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
                                      (r'/blog/xblog/(.*)',XblogElementsHandler),
                                      (r'/blog/sidenotes/(.*)',XBlogSideNotesHandler),
                                      (r'/blog/(.*)',versionBlogHandler),
                                       (r'/grid/(.*)',gridDesignerHandler),
                                      (r'/product/(.*)',xProductHandler),

                                      ],
                                      db=setDB(),**settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888,address="0.0.0.0")

    #print settings['static_path']
#register xace modules
    import xaceauth.xace
    import xacesession.xace
    #xaceauth.xace.register(tornado.web.RequestHandler)
    #xacesession.xace.register(tornado.web.RequestHandler)

    setMotorEngine().start()
    #print tornado
    #tornado.ioloop.IOLoop.instance().start()