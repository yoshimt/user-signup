
import webapp2
import cgi
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Sign-up</title)
    <style type="text/css">
    .error {
        color: #ff0000;
    }
    </style>
</head>
"""
main_content = """
</body>
    <h1>User Sign-Up</h1>
    <form method="post">
        <label>
            Username:
            <input type="text" name="username" value="%(username)s">
            <span class="error">%(user_error)s</span>
        </label>
        <br>
        <label>
            Password:
            <input type="password" type="required" name="password" value="">
            <span class="error">%(pw_error)s</span>
        </label>
        <br>
        <label>
            Verify Password:
            <input type="password" type="required" name="vpassword" value="">
            <span class="error">%(verif_error)s</span>
        </label>
        <br>
        <label>
            E-mail (optional):
            <input type="email" name="email" value="%(email)s">
            <span class="error">%(email_error)s</span>
        </label>
        <br>
        <input type="submit">
    </form>
"""
class Signup(webapp2.RequestHandler):
    def write_form(self, username="", email="", user_error="", pw_error="", verif_error="", email_error=""):
        self.response.write(main_content % {"user_error": user_error,
            "verif_error": verif_error,
            "email_error": email_error,
            "pw_error": pw_error,
            "username": username,
            "email": email})

    def get(self):
        self.write_form()

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        vpassword = self.request.get("vpassword")
        email = self.request.get("email")

        pw_error = ''
        user_error = ''
        verif_error = ''
        email_error = ''
        if not valid_username(username):
            user_error = "Invalid username."
            have_error = True

        if not valid_password(password):
            pw_error = "Invalid password."
            have_error = True

        elif vpassword != password:
            verif_error = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            email_error = "That is an invalid e-mail."
            have_error = True

        if have_error:
            self.write_form(username, email, user_error, pw_error, verif_error, email_error)
        else:
            self.redirect('/welcome?username=' +username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        content = "YAY, " + username + ". You did a thing!"
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome)
], debug=True)
