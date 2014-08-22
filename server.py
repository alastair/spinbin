#!/usr/bin/python

import os
import sys
import json

import tornado.httpserver
import tornado.ioloop
import tornado.web

import kimono

FILE_PATH = "files"

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            d = json.load(open("kimono.json"))
        except IOError:
            d = {}
        except ValueError:
            d = {}
        return self.render("index.html", data=d)

class AddHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        print "adding data"
        print data
        kimono.add(data)
        self.write(":)")

class PipeHandler(tornado.web.RequestHandler):
    def post(self):
        d = self.get_argument("Data")
        print "Got data from pipe input"
        print d

        self.write({"status": "thanks!"})

class FileHandler(tornado.web.RequestHandler):
    def get(self, file):
        fname = os.path.join(FILE_PATH, "%s.xspf" % file)
        if os.path.exists(fname):
            d = open(fname).read()
            self.add_header("Content-type", "application/xml")
            self.write(d)
        else:
            self.write("no file?")

settings = {"static_path": os.path.join(os.path.dirname(__file__), "static"),
        "debug": True}
application = tornado.web.Application([(r"/", RootHandler),
    (r"/(.*).xspf", FileHandler),
    (r"/add", AddHandler),
    (r"/pipein", PipeHandler),
    ], **settings)

def main():
    server = tornado.httpserver.HTTPServer(application)
    server.listen(8999)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
