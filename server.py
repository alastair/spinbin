#!/usr/bin/python

import os
import sys
import json

import tornado.httpserver
import tornado.ioloop
import tornado.web

import kimono
from dateutil import parser
import datetime

FILE_PATH = "files"

try:
    datamap = json.load(open("kimono.json"))
except IOError:
    datamap = {}
except ValueError:
    datamap = {}

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        d = []
        for k, v in datamap.items():
            if v["last_updated"]:
                out = v
                thedate = parser.parse(v["last_updated"])
                out["date"] = thedate
                now = datetime.datetime.now(thedate.tzinfo)
                delta = now - thedate
                if delta.days:
                    dstr = "%s day%s ago" % (delta.days, "" if delta.days == 1 else "s")
                elif delta.seconds > 3600:
                    hr = delta.seconds / 3600
                    dstr = "%s hour%s ago" % (hr, "" if hr == 1 else "s")
                elif delta.seconds <= 600:
                    dstr = "recently"
                else:
                    m = delta.seconds / 600 * 10
                    dstr = "%s minutes ago" % m

                v["updatedstr"] = dstr
                d.append((k, out))
            else:
                pass
        d = sorted(d, key=lambda k: k[1]["date"], reverse=True)
        print d
        return self.render("index.html", data=d)

class AddHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        print "adding data"
        print data
        r = kimono.add(data)
        if r:
            key, data = r
            print "added key", key
            datamap[key] = data
            json.dump(datamap, open("kimono.json", "w"))
        self.write(":)")

class FileHandler(tornado.web.RequestHandler):
    def get(self, file):
        fname = os.path.join(FILE_PATH, "%s.xspf" % file)
        if os.path.exists(fname):
            d = open(fname).read()
            self.set_header("Content-Type", "text/xml")
            self.write(d)
        else:
            self.write("no file?")

settings = {"static_path": os.path.join(os.path.dirname(__file__), "static"),
        "debug": True}
application = tornado.web.Application([(r"/", RootHandler),
    (r"/(.*).xspf", FileHandler),
    (r"/add", AddHandler),
    ], **settings)

def main():
    server = tornado.httpserver.HTTPServer(application)
    server.listen(8999)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
