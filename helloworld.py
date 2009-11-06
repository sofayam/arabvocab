import cgi
import os
from google.appengine.ext.webapp import template

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Word(db.Model):
    arabtext = db.StringProperty()
    meaning = db.StringProperty()
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    usageexample = db.StringProperty(multiline=True)

# class Greeting(db.Model):
#     author = db.UserProperty()
#     content = db.StringProperty(multiline=True)
#     date = db.DateTimeProperty(auto_now_add=True)


class MainPage(webapp.RequestHandler):
    def get(self):
        words_query = Word.all().order('-date')
        words = words_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'words': words,
            'url': url,
            'url_linktext': url_linktext,
            }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class Definer(webapp.RequestHandler):
    def post(self):
        newword = Word()

        if users.get_current_user():
            newword.author = users.get_current_user()

        newword.meaning = self.request.get('meaning')
        newword.arabtext = self.request.get('arabtext')
        newword.usageexample = self.request.get('usageexample')
        newword.put()
        self.redirect('/')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Definer)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
