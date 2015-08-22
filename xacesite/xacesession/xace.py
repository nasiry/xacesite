__author__ = 'jcteng'
import xacesession
import tornado.web
from tornado import gen

@gen.coroutine
def prepare(klass):
    #super.get_current_user()

    #incase of login/out route skip session update ,we will do it later
    try:
        if klass.SessionUpdateHandler != None:
            return
    except:
        c=1 #fake code ,do nothing here

    session_id = klass.get_secure_cookie("sessionId")
    ip = klass.request.remote_ip
    db = klass.settings['db']
    xaceses = xacesession.XaceSession(klass.request,db)
    session_id = yield  xaceses.UpdateSession(session_id=session_id,ip=ip)
    #print xaceses.sessionMade, usr ,ip
    if None==xaceses.sessionUser:
        klass.clear_cookie(xacesession.XaceSession_User_Cookie)
    else:
        klass.set_secure_cookie(xacesession.XaceSession_User_Cookie, xaceses.sessionUser)
    if xaceses.sessionExpired:
        klass.set_secure_cookie("sessionId", xaceses.sessionMade)
        klass.clear_cookie(xacesession.XaceSession_User_Cookie)
     #self.set_secure_cookie("user", str(user_check["usr"][0]))
@gen.coroutine
def LogInOutUpdate(klass,user):
    #super.get_current_user()
    print "LogInOutUpdate",user
    session_id = klass.get_secure_cookie("sessionId")
    ip = klass.request.remote_ip
    db = klass.settings['db']
    xaceses = xacesession.XaceSession(klass.request,db)
    session_id = yield  xaceses.UpdateLogInOutSession(session_id=session_id,user_id=user,ip=ip)
    klass.session_usr = user
    if xaceses.sessionExpired:
            klass.set_secure_cookie("sessionId", xaceses.sessionMade)




def get_current_user(klass):
    #super.get_current_user()

    return klass.get_secure_cookie("xaceuser")





def register(RequestHandler):
    #register current user method

    RequestHandler.prepare = prepare
    RequestHandler.get_current_user = get_current_user
    #try:
    import xaceauth.login
    xaceauth.login.XaceAuthLoginHandler.SessionUpdateHandler = LogInOutUpdate
    xaceauth.login.XaceAuthLogoutHandler.SessionUpdateHandler = LogInOutUpdate

    #except:
    #    c =1 #fake code ,do nothing here
    #register URL also


