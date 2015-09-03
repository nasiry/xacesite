__author__ = 'jcteng'
import xacesession
import tornado.web
from tornado import gen

@gen.coroutine
def prepare(klass):
    #super.get_current_user()

    #incase of login/out route skip session update ,we will do it later

    session_id_save = klass.get_secure_cookie("sessionId")
    ip = klass.request.remote_ip
    db = klass.settings['db']
    xaceses = xacesession.XaceSession(klass.request,db)
    session_id = yield  xaceses.UpdateSession(session_id=session_id_save,ip=ip)

    if session_id_save!=str(session_id):
        klass.clear_cookie(xacesession.XaceSession_User_Cookie)
        klass.set_secure_cookie("sessionId",str(session_id))

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
    if xaceses.sessionExpired:
            klass.set_secure_cookie("sessionId", xaceses.sessionMade)



@gen.coroutine
def get_current_user(klass):
    #super.get_current_user()
    #print "get current"
    session_id = klass.get_secure_cookie("sessionId")
    ip = klass.request.remote_ip
    db = klass.settings['db']
    xaceses = xacesession.XaceSession(klass.request,db)
    user = yield  xaceses.getSessionUsr(session_id=session_id,ip=ip)
    #print user
    raise gen.Return(user)





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


