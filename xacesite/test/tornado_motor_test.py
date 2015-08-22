__author__ = 'jcteng'


import motor
import tornado
import tornado.web
from bson import SON

db_uri = "mongodb://192.168.1.21:27017"
db_name = "xacesite"
db_auth_collection="auth"
db_map_collection="map"
db_nav_collection="navi"


def my_callback(result, error):
    print 'result', repr(result)



class IndexHandler(tornado.web.RequestHandler):
    def get(self):

        #cursor =  db[db_auth_collection].find_one({"key":"value"})
        #for document in  cursor :
        #    print document
        for doc in (yield  db[db_auth_collection].each()):
            print doc
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

def insert():
    document = {'key': 'value'}
    db[db_auth_collection].insert(document, callback=my_callback)

client = motor.MotorClient(db_uri)
db= client[db_name]

application = tornado.web.Application([
    (r'/', IndexHandler)
], db=db)


application.listen(8888)
tornado.ioloop.IOLoop.instance().start()