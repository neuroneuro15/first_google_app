#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import ndb
import webapp2
import logging

class Greetings(ndb.Model):
    name = ndb.StringProperty(required=True)
    message = ndb.TextProperty(required=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("""
        <html>
        <head></head>
        <body>

        <h1>My Guest Book</h1>

        <form action="/greet" method="post">
            <p>
            Name: <input type="text" name="user_name" style="width: 300px">
            </p>
            <p>
            Message: <textarea name="message" style="width: 300px" rows="5"></textarea>
            </p>
            <p>
            <input type="submit" value="Send">
            </p>
        </form>

        </body>
        </html>
        """)


class GreetHandler(webapp2.RequestHandler):
    def post(self):
        logging.debug(self.request)
        user_name = self.request.get("user_name")
        message = self.request.get("message")

        logging.debug("Message: \n\tUser Name: {}\n\tMessage: {}\n".format(user_name, message))
        Greetings(name=user_name, message=message).put()


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/greet', GreetHandler)
], debug=True)
