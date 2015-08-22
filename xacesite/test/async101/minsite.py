#!/usr/bin/python
# -*- coding:utf-8 -*-
#

#
__author__ = 'jcteng'


import tornado
import tornado.web
import motor






db_test_collection="test"

def db_callback(result, error):
    print 'result', repr(result)


def setDB():

    db_uri = "mongodb://192.168.1.21:27017"
    db_name = "xacesite"

    client = motor.MotorClient(db_uri)
    return client[db_name]

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')




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

from tornado import gen
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

if __name__ == '__main__':
    import tornado.options
    import tornado.httpserver
    tornado.options.parse_command_line()
    application = tornado.web.Application([(r'/', IndexHandler),
                                      (r'/query', QueryHandler),
                                      (r'/insert', InsertHandler),
                                      (r'/insert2', InsertHandler2),],
                                      db=setDB(),template_path="templates")
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()