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
import webapp2
import logging
import os
import jinja2
from models.greetings import Greetings


class MainHandler(webapp2.RequestHandler):
    def get(self):

        # Get all past Greetings from the datastore
        results = Greetings.query().fetch()  # Can put an integer argument in fetch() to limit to N number of results
        results_dict = {'greetings': results}


        # HTML Template
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')

        jinja_environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir)
        )

        template = jinja_environment.get_template('home.html')
        rendered_template = template.render(results_dict)

        self.response.write(rendered_template)


class GreetHandler(webapp2.RequestHandler):
    def post(self):
        logging.debug(self.request)
        user_name = self.request.get("user_name")
        message = self.request.get("message")

        logging.debug("Message: \n\tUser Name: {}\n\tMessage: {}\n".format(user_name, message))
        Greetings(name=user_name, message=message).put()
        logging.debug("POST Successful")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/greet', GreetHandler)
], debug=True)
