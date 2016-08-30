import webapp2
import cgi
from caesar import encrypt

form="""<head>
<title>Formation</title>
<!---link rel="stylesheet" href="style.css"--->
</head>
<body>
<form method="post" action="/">
  <label for="formation">Rotate around:</label>
  <input type="text" name="rotationValu" value="%(rotationValu)s"></input>
  <br></br>
  <label>This text:</label>
  <br></br>
  <textarea type="text" name="text">{0}</textarea>
  <br></br>
  <input type="submit"></input>
</form>
</body>
"""

rotationValu = "13"

def escape_html(s):
    return cgi.escape(s, quote=True)

class MainHandler(webapp2.RequestHandler):
    def get(self, rotationValu=""):
        rotationValu = self.request.get("rotationValu")
        self.response.write(form % {"rotationValu" : rotationValu})


    def post(self):
        a = self.request.get("text")
        b = int(self.request.get("rotationValu"))

        escape_html("a")
        escape_html("b")

        ans = encrypt(a, b)

        self.response.write(form.format(ans) % {"rotationValu" : rotationValu})


app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
