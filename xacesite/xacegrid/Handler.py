__author__ = 'jcteng'
import tornado

import xacedoc


from tornado import  gen



from layoutGen import  xaceGridNode

tmpstr = '''
it is line 1</p>
it is line 2</p>
it is line 3</p>

'''
from bson import ObjectId

class gridDesignerHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self,arg):



        try:
            act = self.get_argument("action")
        except:
            act = "query"
            pass


        if act == "create":
            rootGrid = xaceGridNode(templatePath="") #do not show any content in root
            rootGrid = yield  rootGrid.save()
            self.redirect(str(rootGrid._id))
            return

        try:
            oid =  ObjectId(arg)
        except:
            act = "list"

        if act!="list" :
            rootGrid = yield xaceGridNode.objects.get(id=oid)


        if act == "add":
            isGroupNode=self.get_argument("isGroupNode")
            if isGroupNode.lower()=="true":
                isGroupNode = True
            else:
                isGroupNode = False
            rootGrid.addNode2Id(tag=self.get_argument("tag"),width= self.get_argument("width"),isGroupNode=isGroupNode)
            rootGrid = yield  rootGrid.save()
            self.redirect(str(rootGrid._id))
            return

        if act == "del":
            rootGrid.delNode(tag=self.get_argument("tag"))
            rootGrid = yield  rootGrid.save()
            self.redirect(str(rootGrid._id))
            return

        if rootGrid!=None:
            self.render("pageDesigner.html",content=rootGrid.mergeTemplates())
        else:
            self.write("No such Item")
            self.finish()