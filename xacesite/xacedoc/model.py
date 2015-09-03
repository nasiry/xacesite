#!/usr/bin/python
# -*- coding:utf-8 -*-
#

__author__ = 'jcteng'


import motorengine.fields

from motorengine.fields import StringField, DateTimeField,ListField,EmbeddedDocumentField,BaseField,ReferenceField,IntField,BooleanField
from xacedoc.ObjectIdField import ObjectIdField

from tornado import  gen
from tornado.concurrent import return_future

class XaceSideNotes(motorengine.Document):

    achieved = BooleanField(default=False)
    note = StringField(default="Task to do there!")
    creator =  StringField(default="")
    closeby =  StringField(default="")
    index = IntField(default=0)





class XaceSideNotesList(motorengine.Document):
    default = ListField( EmbeddedDocumentField(embedded_document_type=XaceSideNotes))
    indexCount = IntField(default=0)
    @gen.coroutine
    def addNote(self,noteTxt,creator):
        self.default.append(XaceSideNotes(index=self.indexCount,note=noteTxt,creator=creator))
        self.indexCount+=1
        saved = yield self.save()
        raise gen.Return(saved)

    @gen.coroutine
    def updateNote(self,index,noteTxt=None,toclose=False,user=""):
        #while close

        for note in self.default:
            if note.index == int(index):
                #while update text
                if None!=noteTxt:
                    note.note = noteTxt

                #while close note
                if toclose:
                    note.achieved = True
                    note.closeby = user
                saved = yield self.save()
                raise gen.Return(saved)






    @gen.coroutine
    def delNote(self,index):

        for note in self.default:
            if note.index == int(index):
                self.default.remove(note)

        saved = yield self.save()
        raise gen.Return(saved)

class XaceSideReferList(motorengine.Document):
    default = ListField( StringField(default="save your reference here"))

class XaceBlog(motorengine.Document):
    title = StringField(default="Please input article title here")
    keywords=  ListField(StringField(default=""),default=["tag to add"])
    content =  StringField(default="Input content here")
    status =   StringField(default="status")
    subTitle = StringField(default="Sub Title")
    authors = ListField(StringField())

    @gen.coroutine
    def updateXBlog(self,title=None,subTitle=None,content=None,user="",keywords=None,isSave=True):
        print title,subTitle
        if title!=None:
            self.title = title
        if subTitle!=None:
            self.subTitle = subTitle
        if content!=None:
            self.content = content
        if keywords!=None:
            keys = set()
            for key in keywords.split(','):
                keys.add(key)

            print keywords
            self.keywords =list(keys)
        if isSave:
            saved = yield self.save()
            raise gen.Return(saved)


class XaceChange(motorengine.Document):

    lastChange =DateTimeField()
    operator =StringField()
    tag = StringField(default="default")
    refernceXele =ObjectIdField()

class XaceChangeList(motorengine.Document):
    default = ListField( EmbeddedDocumentField(embedded_document_type=XaceChange))

class XaceComments(motorengine.Document):

    lastChange =DateTimeField()
    operator =StringField()
    tag = StringField(default="default")


class XaceCommentsList(motorengine.Document):
    default = ListField( EmbeddedDocumentField(embedded_document_type=XaceComments))

import  datetime

class XaceBlogContainer(motorengine.Document):


    #oid = StringField(default="")
    elements = ReferenceField(reference_document_type=XaceBlog) #{} #type is element
    changelog= ReferenceField(reference_document_type=XaceChangeList)#{}  #type is change log
    comments= ReferenceField(reference_document_type=XaceCommentsList)#{}  #type is change log
    notes= ReferenceField(reference_document_type=XaceSideNotesList)#{}  #type is change log
    refers=ReferenceField(reference_document_type=XaceSideReferList) # reference for editor mode
    createTime =DateTimeField()
    lastTouched =DateTimeField(auto_now_on_update=True)
    #elementsType = StringField(default="")
    title = StringField(default="default Element")
    createby =  StringField(default="")
    readCount = IntField(default=0)
    keywords=  ListField(StringField())
    allowUser = ListField(StringField())



    @gen.coroutine
    def coCreate(self,user,alias=None,):




        self.elements =xl = yield XaceBlog().objects.create(authors=[user])

        lgl = XaceChangeList()

        curch = XaceChange(operator=user,lastChange=datetime.datetime.utcnow(),tag=("create by "+user),refernceXele=xl._id)
        lgl.default.append(curch)
        self.changelog =  yield lgl.save()
        self.createby = user
        self.comments = cmt = yield XaceCommentsList.objects.create()
        self.refers =yield XaceSideReferList.objects.create()
        self.notes =yield XaceSideNotesList.objects.create()

        self.createTime = datetime.datetime.now()
        created = yield self.save()
        print created
        raise gen.Return(created)




    #new document have been filled out side
    @gen.coroutine
    def coSave(self,user,element,changetag,alias=None):
        yield  self.load_references(fields=["changelog"])
        userlist =set()
        userlist.add(user)
        for change in self.changelog.default:
            userlist.add(change.operator)
        print userlist
        element.authors = list(userlist)
        print userlist
        self.elements = xl = yield element.save()

        curch = XaceChange(operator=user,lastChange=datetime.datetime.utcnow(),tag=changetag,refernceXele=xl._id)
        self.changelog.default.append(curch)
        self.title = element.title
        yield self.changelog.save()
        ret = yield self.save()
        raise gen.Return(ret)

