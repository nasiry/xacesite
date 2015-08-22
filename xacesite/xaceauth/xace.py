__author__ = 'jcteng'


def get_current_user(klass):
    #super.get_current_user()
    return klass.get_secure_cookie("xaceuser")


def register(RequestHandler):
    #register current user method

    RequestHandler.get_current_user = get_current_user
    #register URL also