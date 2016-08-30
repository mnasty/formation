import webapp2
import cgi
import re

def escape_html(s):
    return cgi.escape(s, quote=True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASSWORD_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)


signup_form='''
<html>
  <head>
    <title>User Signup!</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup Here!</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">
            %(username_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="%(password)s">
          </td>
          <td class="error">
            %(password_error)s
          </td>

          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="%(verify)s">
          </td>
          <td class="error">
            %(verify_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email Address
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(email_error)s
          </td>
        </tr>
      </table>
      <br></br>
      <input type="submit">
    </form>
  </body>

</html>
'''

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("")

class SignupHandler(webapp2.RequestHandler):

    def write_form(self, username="", password="", verify="", email="", username_error="", password_error="", verify_error="", email_error=""):
        self.response.out.write(signup_form % {"username" : username,
                                                "password" : password,
                                                "verify" : verify,
                                                "email" : email,
                                                "username_error" : username_error,
                                                "password_error" : password_error,
                                                "verify_error" : verify_error,
                                                "email_error" : email_error})

    def get(self):
        self.write_form()

    def post(self):
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')

        sani_username = escape_html(user_username)
        sani_password = escape_html(user_password)
        sani_verify = escape_html(user_verify)
        sani_email = escape_html(user_email)

        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""

        error = False

        if not valid_username(user_username):
            username_error = "Invalid Username!"
            error = True

        if not valid_password(user_password):
            password_error = "Invalid Password!"
            error = True

        if not user_verify or not user_password == user_verify:
            verify_error = "Passwords Do Not Match!"
            error = True

        if not valid_email(user_email):
            email_error = "Invalid E-mail Address!"
            error = True

        if error:
            self.write_form(sani_username, sani_password, sani_verify, sani_email, username_error, password_error, verify_error, email_error)
        else:
            self.redirect("/welcome?username=%s" % user_username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.out.write("Welcome %s!" % username)

app = webapp2.WSGIApplication([('/main', MainHandler),
                                ('/welcome', WelcomeHandler),
                                ('/', SignupHandler)], debug=True)
