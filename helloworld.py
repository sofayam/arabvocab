import cgi
import os
from google.appengine.ext.webapp import template

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import arabise

class Word(db.Model):
    arabtext = db.StringProperty()
    romantext = db.StringProperty()
    meaning = db.StringProperty()
    root = db.StringProperty()
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

class Lister(webapp.RequestHandler):
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

        path = os.path.join(os.path.dirname(__file__), 'list.html')
        self.response.out.write(template.render(path, template_values))

class Definer(webapp.RequestHandler):
    def post(self):
        newword = Word()

        if users.get_current_user():
            newword.author = users.get_current_user()
        newword.meaning = self.request.get('meaning')
        newword.arabtext = self.request.get('arabtext')
        newword.romantext = self.request.get('romantext')
        newword.root = self.request.get('root')
        newword.usageexample = self.request.get('usageexample')
        if newword.romantext and (newword.arabtext == ""):
            newword.arabtext = arabise.arabise(newword.romantext)
        newword.put()
        self.redirect('/')


class Editor(webapp.RequestHandler):
    def get(self):
        k = self.request.get('key')
        word = Word.get(k)
#        self.response.out.write(word.meaning)
#        self.response.out.write("thats it %s \n" % k)        
        path = os.path.join(os.path.dirname(__file__), 'edit.html')
        template_values = {
            'word': word
            }
        self.response.out.write(template.render(path, template_values))

class Deleter(webapp.RequestHandler):
    def get(self):
        k = self.request.get('key')
        word = Word.get(k)
#        self.response.out.write(word.meaning)
#        self.response.out.write("thats it %s \n" % k)        
        path = os.path.join(os.path.dirname(__file__), 'edit.html')
        template_values = {
            'word': word
            }
        self.response.out.write(template.render(path, template_values))
        self.redirect('/')


class Saver(webapp.RequestHandler):
    def post(self):

        word = Word.get(self.request.get('key'))


        word.meaning = self.request.get('meaning')
        word.arabtext = self.request.get('arabtext')
        word.romantext = self.request.get('romantext')
        word.root = self.request.get('root')
        word.usageexample = self.request.get('usageexample')
        if word.romantext and (word.arabtext == ""):
            word.arabtext = arabise.arabise(word.romantext)
        word.put()
        self.redirect('/')


class RomTab(webapp.RequestHandler):
    def get(self):
        tabwidth = 5
        ctr = 0
        buff = []
        w = buff.append
        w('<table border="0">')
        for key,val in arabise.codelist:
            if (ctr % tabwidth) == 0:
                w("<tr>")
            w("<td>%s</td><td>:</td><td>%s</td><td>  </td>" % (key, arabise.ar(val)))
            if (ctr % tabwidth) == (tabwidth - 1):
                w("</tr>")
            ctr += 1
        w("</table>")
        template_values = {
            'tabledata': u"".join(buff),
            }

        path = os.path.join(os.path.dirname(__file__), 'romtab.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/list', Lister),
                                      ('/sign', Definer),
                                      ('/edit', Editor),
                                      ('/delete', Deleter),
                                      ('/alter', Saver),
                                      #('/test', Tester),
                                      ('/romtab', RomTab)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
