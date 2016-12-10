import tornado.ioloop
import tornado.web
import os
import wordcloud
import webscrape
import worddb


class BaseHandler(tornado.web.RequestHandler):

    def get_login_url(self):
        return u"/auth/login/"

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            return None

class MainHandler(BaseHandler):
    """
    this is where the wordcloud is shown
    """
    @tornado.web.authenticated
    def get(self):
        username = tornado.escape.xhtml_escape(self.current_user)
        self.render("index.html", username = username)

    def post(self):
        #username = tornado.escape.xhtml_escape(self.current_user)
        weblink = self.get_argument("weblink", "")

        text = webscrape.content(weblink)
        if len(text) > 0:
            counts = wordcloud.processtext(text)
            worddb.trackwords(counts)
            wordcount = wordcloud.jsify(counts)
            self.render("wordcloud.html", weblink=weblink, wordcount=wordcount)
        else:
            self.redirect(self.get_argument("next", "/"))


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

class AuthLoginHandler(BaseHandler):
    def get(self):
        try:
            errormessage = self.get_argument("error")
        except:
            errormessage = ""
        self.render("login.html", errormessage = errormessage)

    def check_permission(self, password, username):
        if username == "admin" and password == "admin":
            return True
        if username == "user" and password == "user":
            return True
        return False

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        auth = self.check_permission(password, username)
        if auth:
            self.set_current_user(username)
            self.redirect(self.get_argument("next", u"/"))
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect")
            self.redirect(u"/auth/login/" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

class AdminHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        error_msg = ''
        username = tornado.escape.xhtml_escape(self.current_user)
        if username != 'admin':
            error_msg = 'admin authorization required'
            self.redirect(u"/auth/login/")  # + error_msg)
        else:
            counts = worddb.listwords()
            self.render("admin.html", words=counts, errormessage = error_msg)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/auth/login/", AuthLoginHandler),
            (r"/auth/logout/", AuthLogoutHandler),
            (r"/admin/", AdminHandler),
        ]
        settings = {
            "template_path": os.path.join(os.path.dirname(__file__), "template"),
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            #"debug":Settings.DEBUG,
            #"static_url_prefix": "/",
            "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            "login_url": "/auth/login/"
        }
        tornado.web.Application.__init__(self, handlers, **settings)



if __name__ == "__main__":
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


