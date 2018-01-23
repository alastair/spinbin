#!/usr/bin/python

import os
import sys
import json

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

from dateutil import parser
import datetime

import db

FILE_PATH = "/files"

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        by_added = db.playlists_by_added()
        by_updated = db.playlists_by_updated()
        return self.render("index.html", by_updated=by_updated, by_added=by_added)

class FileHandler(tornado.web.RequestHandler):
    def get(self, file):
        playlist = db.get_playlist(file)
        if playlist:
            fname = os.path.join(FILE_PATH, playlist.filename)
            if os.path.exists(fname):
                d = open(fname).read()
                self.set_header("Content-Type", "text/xml")
                self.write(d)
            else:
                raise tornado.web.HTTPError(404, reason="Sorry, not a playlist")
        else:
            raise tornado.web.HTTPError(404, reason="Sorry, not a playlist")

settings = {"static_path": os.path.join(os.path.dirname(__file__), "static"),
        "debug": False}
application = tornado.web.Application([(r"/", RootHandler),
    (r"/(.*).xspf", FileHandler),
    ], **settings)

wapp = tornado.wsgi.WSGIAdapter(application)

def main():
    server = tornado.httpserver.HTTPServer(application)
    server.listen(8999)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
