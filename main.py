import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class BlogPost(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(webapp2.RequestHandler):
    def render_front(self, title="", body="", error=""):
        posts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC LIMIT 5")
        #store the results from the query (cursor = pointer to the results)

        t = jinja_env.get_template("frontpage.html")
        content = t.render(title=title, body=body, error=error, posts = posts)
        self.response.write(content)

    def get(self):
        self.render_front()


class NewPost(webapp2.RequestHandler):
    def render_newpost(self, title="", body="", error=""):
        t = jinja_env.get_template("newpost.html")
        content = t.render(title=title, body=body, error=error)
        self.response.write(content)

    def get(self):
        self.render_newpost()

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")

        if title and body:
            a = BlogPost(title = title, body = body)
            a.put()

            self.redirect("/")
        else:
            error = "we need both a title and some text!"
            self.render_newpost(title, body, error)

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):

        title = ""
        body = ""

        post = BlogPost.get_by_id( int(id) )
        if post:
            t = jinja_env.get_template("post.html")
            content = t.render(title = title, body=body, post = post)
            self.response.write(content)

        else:
            error = "this ID does not exist!"
            error2 = "please try again :)"
            t = jinja_env.get_template("post.html")
            content = t.render(title = title, body=body, post = post, error = error, tinyerror = error2)
            self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPost),
    (webapp2.Route('/blog/<id:\d+>', ViewPostHandler))
], debug=True)
