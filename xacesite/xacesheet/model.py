__author__ = 'jcteng'

import motorengine.fields

from motorengine.fields import StringField, DateTimeField,ListField,EmbeddedDocumentField,BaseField,ReferenceField,IntField,BooleanField
from xacedoc.ObjectIdField import ObjectIdField

from tornado import  gen
from tornado.concurrent import return_future


class XaceSheetItem(motorengine.Document):
    default =ListField()
    type = ObjectIdField()


class XaceSheetType(motorengine.Document):
    sheettype = StringField()
    item = ListField()