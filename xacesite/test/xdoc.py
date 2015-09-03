__author__ = 'jcteng'

import motor
import tornado

from tornado import  gen

import tornado.ioloop

from tornado.ioloop import IOLoop
import motorengine
from motorengine import Document
import motorengine.fields
from motorengine.fields.dynamic_field import DynamicField
from motorengine.fields import StringField, DateTimeField,ListField,EmbeddedDocumentField,BaseField,ReferenceField
from bson.objectid import  ObjectId

from motorengine.connection import connect

def setDB():

    db_uri = "mongodb://192.168.1.21:27017"
    db_name = "xacesite"

    client = motor.MotorClient(db_uri)
    return client[db_name]


def setMotorEngine():
    io_loop = tornado.ioloop.IOLoop.instance()
    motorengine.connect("xacesite", host="192.168.1.21", port=27017, io_loop=io_loop)






import xacedoc
from xacedoc import XaceBlogContainer,XaceBlog,XaceChangeList,XaceChange,XaceSideNotesList,XaceSideNotes

import  datetime




@gen.coroutine
def createnew(index):

    #print index

    ret = []
    xacedoc = XaceBlogContainer()
    xacedoc = yield xacedoc.coCreate(user="coCreateUser",retcontain=ret)
    results = yield XaceBlogContainer.objects.filter().find_all()
    for item in results:
        print item.to_son()
        ret.append(item)

    #print ret[0]._id
    #return
    oid = xacedoc._id
    print oid



    xblog = XaceBlog()
    xacedoc = yield XaceBlogContainer.objects.get(id=oid)
    yield xacedoc.load_references(fields=["notes"])
    xacedoc.notes.default.append(XaceSideNotes())
    xacedoc.notes.default.append(XaceSideNotes())
    xacedoc.notes.default.append(XaceSideNotes())
    xacedoc.notes.default.append(XaceSideNotes())
    xacedoc.notes.default.append(XaceSideNotes())
    xacedoc.notes.default.append(XaceSideNotes())
    xacedoc.notes.save()
    yield xacedoc.coSave(element=xblog,changetag="change 1",user="user1")


    xblog = XaceBlog()
    xacedoc = yield XaceBlogContainer.objects.get(id=oid)
    xacedoc= yield xacedoc.coSave(element=xblog,changetag="change 2",user="user2")
    xblog = XaceBlog()
    xacedoc = yield XaceBlogContainer.objects.get(id=oid)
    xacedoc= yield xacedoc.coSave(element=xblog,changetag="change 3",user="user3")
    #print "done"

    return





def createMass():
    start = datetime.datetime.now()
    for i in range(1,2,1):
        createnew(i)

    print (datetime.datetime.now()-start)

    #io_loop.stop()

setMotorEngine()
io_loop = tornado.ioloop.IOLoop.instance()



#XaceDocs.objects.filter().find_all(callback = pcallback)


io_loop.add_timeout(300, createMass)
io_loop.start()