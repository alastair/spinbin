#!/usr/bin/python

import os
import sys
import json

import tornado.httpserver
import tornado.ioloop
import tornado.web

from dateutil import parser
import datetime

import db
import kimono
import tw

FILE_PATH = "files"

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        by_added = db.playlists_by_added()
        by_updated = db.playlists_by_updated()
        return self.render("index.html", by_updated=by_updated, by_added=by_added)

class AddHandler(object):
    def process_data(self, data):
        print "adding data"
        print data
        r = kimono.add(data)
        if r:
            s = r["slug"]
            playlist = db.get_playlist(s)
            if not playlist:
                playlist = db.create_playlist(r["slug"])
            playlist.url = r["url"]
            playlist.filename = r["filename"]
            playlist.endpoint = r["endpoint"]
            playlist.name = r["name"]
            playlist.date_updated = r["last_updated_obj"]
            db.update_playlist(playlist)
            return playlist
        else:
            return None

    def send_tweet(self, playlist):
        tw.send_update(playlist.name)

    def post(self):
        data = json.loads(self.request.body)
        pl = self.process_data(self)
        if pl:
            send_tweet(pl)
        self.write(":)")

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
