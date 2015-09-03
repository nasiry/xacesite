#!/usr/bin/python
# -*- coding:utf-8 -*-
#

__author__ = 'jcteng'


XaceSession_collection="XaceSession"
XaceSession_Realm="xace.in"
XaceSession_Prefix = "_XaceSession:"
XaceSession_Expired = 600
XaceSession_User_Cookie = "xaceuser"



from  datetime import datetime
import os

from bson.objectid import ObjectId

import xace
import tornado.web
xace.register(tornado.web.RequestHandler)
print "XaceSession registed"
#print tornado



from tornado import gen
class XaceSession(object):



    def __init__(self,request,db):
        #print "xaceSession Init"
        self._request = request
        self._db = db
        self.sessionMade = ""
        self.sessionExpired = False
        #init session id

    # this route should called  onetime only after server installed
    @gen.coroutine
    def set_ttl(self):
        yield self._db[XaceSession_collection].create_index("ActiveDate",expireAfterSeconds=XaceSession_Expired)

    @gen.coroutine
    def makeSession(self,user_id):
       # print "makeSession "
        ip = self._request.remote_ip
        activeDate= datetime.utcnow()

        record =  yield self._db[XaceSession_collection].insert({"ip":ip,"ActiveDate":activeDate,"user_id":user_id})
        #use ObjectID as sessionID
        raise gen.Return(record)

    @gen.coroutine
    def UpdateLogInOutSession(self,session_id,user_id,ip):
        print "UpdateLogInOutSession ",session_id
        csession =None
        self.sessionUser=user_id
        print session_id
        try:
            sid = ObjectId(session_id)
            csession = yield  self._db[XaceSession_collection].find_one({"ip":ip,'_id':sid,})
        except:
            pass

        if csession == None:
            self.sessionExpired = True
            #changed ip / user /expired alloc a new session id
            cur =  yield self.makeSession(user_id)
            raise gen.Return(str(cur))
        else:
            update =    yield self._db[XaceSession_collection].update({'_id': sid},{"$set":{"ActiveDate":datetime.utcnow(),"user_id":user_id }})
            raise gen.Return(str(csession['_id']))
    @gen.coroutine
    def getSessionUsr(self,session_id,ip):
        csession =None
        try:
            sid = ObjectId(session_id)
            csession = yield  self._db[XaceSession_collection].find_one({"ip":ip,'_id':sid,})
        except:
            raise gen.Return(None)

        if csession!=None :
            if csession['user_id']!=None and csession['user_id']!="":
                raise gen.Return(csession['user_id'])
                return

        raise gen.Return(None)

    @gen.coroutine
    def UpdateSession(self,session_id,ip):
        #print "UpdateSession ",session_id
        csession =None
        try:
            sid = ObjectId(session_id)
            csession = yield  self._db[XaceSession_collection].find_one({"ip":ip,'_id':sid,})
        except:
            pass



        if csession == None:
            #changed ip / user /expired alloc a new session id
            #or invalided session id
            cur =  yield self.makeSession(None)
            raise gen.Return(cur)
        else:
            update =    yield self._db[XaceSession_collection].update({'_id': sid},{"$set":{"ActiveDate":datetime.utcnow()  }})
            raise gen.Return(str(csession['_id']))
        #print "UpdateSession--",self.sessionMade
