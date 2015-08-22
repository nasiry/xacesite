XaceAuth_collection="XaceAuth"
XaceAuth_Realm="xace.in"
XaceAuth_User_Cookie = "xaceuser"



import tornado.web
import xace
xace.register(tornado.web.RequestHandler)
print "xaceAuth registed"
#print tornado


