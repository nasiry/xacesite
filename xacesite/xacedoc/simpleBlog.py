#!/usr/bin/python
# -*- coding:utf-8 -*-
#
import tornado

import xacedoc


from tornado import  gen

from xacedoc import  XaceBlog,XaceBlogContainer


XaceBlogBaseURL = "/blog"

def id2Url(id):
    print "id2Url()"

from bson import ObjectId
class versionBlogHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def listBlogs(self):

        bl = yield XaceBlogContainer.objects.find_all()
        self.render("versionBlog.html",items= bl)
        #self.finish()


    @tornado.web.asynchronous
    @gen.coroutine
    def get(self,args):

        try:
            act = self.get_argument("action")
        except:
            act = "query"

        if(act=='create'):
            xbc = XaceBlogContainer()
            usr=yield self.get_current_user()
            xbc = yield xbc.coCreate(usr)
            self.redirect(str(xbc._id))
            return
        try:
            oid =  ObjectId(args)
        except:
            act = "list"


        if act == "query":
            xblog = yield XaceBlogContainer.objects.get(id=oid)
            if xblog!=None:
                yield xblog.load_references(fields=["changelog","elements","notes"])
                currentUser = yield self.get_current_user()
                self.render("versionBlog.html",verionBlog= xblog,blog=xblog.elements,notelist =xblog.notes.default,notes_oid = str(xblog.notes._id),isLogin=(currentUser!=None),currentUser=currentUser)
            else:
                self.write("No such Blog")
                self.finish()

        try:
            pass
        except:
            print "do list"
            yield  self.listBlogs()

        #yield  XaceBlogContainer.object.






    @gen.coroutine
    @tornado.web.asynchronous
    def post(self,oid):
        try:
            act = self.get_argument("action")
        except:
            act = "query"

        try:
            xbc = yield  XaceBlogContainer.objects.get(id=ObjectId(oid))
        except:
            self.finish()
            return

        if(act=='edit'):
            xblog = XaceBlog()
            xblog.updateXBlog(title=self.get_argument("title"),subTitle=self.get_argument("subtitle"),content=self.get_argument("content"),user=(yield self.get_current_user()),keywords=self.get_argument("keywords"),isSave=False)

            xbc = yield xbc.coSave((yield self.get_current_user()),xblog,self.get_argument("tags"))
            self.write("保存成功")
            self.finish()
            return

        self.finish()

from  model import  XaceSideNotesList,XaceSideNotes
class XBlogSideNotesHandler(tornado.web.RequestHandler):


    @tornado.web.asynchronous
    @gen.coroutine
    def get(self,args):
        try:
            oid =  ObjectId(args)
            print "11"
        except:
            self.finish()
            raise gen.Return(None)
            return

        print oid
        xsnote = yield  XaceSideNotesList.objects.get(id=oid)



        if(xsnote != None):
            self.render("component/XblogNotes.html",notelist = xsnote.default,objectid=oid)
        else:
            self.finish()

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self,oid):
        #default is query
        try:
            act = self.get_argument("action")
        except:
            act = "query"

        try:
            xsnote = yield  XaceSideNotesList.objects.get(id=ObjectId(oid))
        except:
            self.finish()
            return


        # to co-work with auth system
        if(act=="add"):
            print self.get_argument("note")
            print self.get_argument("note")
            xsnote = yield xsnote.addNote(noteTxt=self.get_argument("note"),creator=(yield self.get_current_user()))

        if(act=="del"):
            xsnote = yield xsnote.delNote(index=self.get_argument("id"))

        if(act=='close'):
            xsnote = yield xsnote.updateNote(index=self.get_argument("id"),toclose=True,user=(yield self.get_current_user()))
        if(act=='edit'):
            xsnote = yield xsnote.updateNote(index=self.get_argument("id"),noteTxt=self.get_argument("note"))

        if(xsnote != None):

            print "6"
            self.render("component/XblogNotes.html",notelist = xsnote.default,notes_oid=str( xsnote._id))
        else:
            self.finish()


from model import XaceBlog
class XblogElementsHandler(tornado.web.RequestHandler)   :

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self,oid):


        try:
            act = self.get_argument("action")
            print act
            if(act=='create'):
                xblog = yield  XaceBlog().objects.create()
                self.redirect(str(xblog._id))
                return
        except:
            act = "query"

        try:
            xblog = yield  XaceBlog.objects.get(id=ObjectId(oid))
        except:
            self.finish()
            return
        #check access for user group
        self.render("baseBlog.html",blog = xblog,is_editable = True)
        return


    @tornado.web.asynchronous
    @gen.coroutine
    def post(self,oid):
        try:
            act = self.get_argument("action")
        except:
            act = "query"

        try:
            xblog = yield  XaceBlog.objects.get(id=ObjectId(oid))
        except:
            self.finish()
            return



        if(act=='edit'):
            xblog = yield xblog.updateXBlog(title=self.get_argument("title"),subTitle=self.get_argument("subtitle"),content=self.get_argument("content"),user=(yield self.get_current_user()),keywords=self.get_argument("keywords"))





        self.render("baseBlog.html",blog = xblog,is_editable = True)
        return