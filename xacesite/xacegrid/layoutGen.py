#!/usr/bin/python
# -*- coding:utf-8 -*-
#

#
__author__ = 'jcteng'


import motorengine.fields

from motorengine.fields import StringField, DateTimeField,ListField,EmbeddedDocumentField,BaseField,ReferenceField,IntField,BooleanField
from xacedoc.ObjectIdField import ObjectIdField

from tornado import  gen
from tornado.concurrent import return_future


from motorengine.utils import get_class

import random

GRID_MAX=12

class xaceGridNode(motorengine.Document):

    nodeType = StringField(default="layoutNode") #grid or instance
    styleDiv = IntField(default=GRID_MAX)    #12 Grid in total
    layoutNode = ListField( EmbeddedDocumentField(embedded_document_type="xacegrid.layoutGen.xaceGridNode"))
    isGroupNode = BooleanField(default=True)
    autoTag =  IntField(default=0)
    #hardcode this for simplify implements
    mergeStrs = {"gStart":'<div class="am-g am-g-collapse node-g ">',"gItemStart":'<div class="am-u-md-%d node-i">',"endStr":'</div>'}
    #hardcode this for simplify implements
    panelStr = '''

            <div class="node-header ">
                NodeID:%s
                <a href="javascript:editComponent(%d)"><span
                        class="am-icon-plus-square"></span></a>

            </div>
    '''
    templatePath =StringField(default="<div><p>Put Your component there</p></div>")

    def addNode(self,layoutNode):
        layoutNode.autoTag = random.randint(1,100000)
        self.layoutNode.append(layoutNode)

    def addNode2Id(self,tag=0,width=GRID_MAX,isGroupNode=True):
       print "tag is",tag,width,isGroupNode,type(isGroupNode)

       newNode = xaceGridNode(isGroupNode=(isGroupNode),styleDiv=width)
       node  = self.findNode(tag)
       print node
       newNode.autoTag = random.randint(100000,900000) #lazy code :potential duplicate tags there
       node.layoutNode.append(newNode)

    def findNode(self,tag=0):
        if self.autoTag == int(tag):
            return self
        if self.layoutNode!=None:
            for node in self.layoutNode:
                #node.parent = self
                ret = node.findNode(tag)
                if ret !=None:
                    return ret
        return None



    def delNode(self,tag=0):

        i = 0
        ret = False
        for node in self.layoutNode:
           print node.autoTag
           if node.autoTag == int(tag):
               self.layoutNode.pop(i)
               return  True
           i+=1
           if(node.delNode(tag)):
               return True
        return False

        #for i in range(reverse(len(self.layoutNode))):
        #    node = self.layoutNode[i]
        #    node = node.delNode(tag)
        #    if self.autoTag == int(tag):
        #        self.layoutNode.remove(node)




    def rendering_start(self):
        pass

    def rendering_end(self):
        pass

    def mergeTemplates(self):


        merged = ""
        if self.isGroupNode:
            merged += self.mergeStrs['gStart']
        else:
            merged += self.mergeStrs['gItemStart']%self.styleDiv
        merged +=(self.panelStr%(self.autoTag,self.autoTag))

        if len(self.layoutNode)>0:
            for node in self.layoutNode:
                merged +=node.mergeTemplates()


        merged +=self.templatePath
        merged +=self.mergeStrs['endStr']

        return merged


