import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc

from sqlalchemy.orm.exc import NoResultFound

engine = create_engine('sqlite:///spinbin.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Playlist(Base):
    __tablename__ = "playlist"
    id = Column(Integer, primary_key=True)
    slug = Column(String, index=True)
    name = Column(String)
    description = Column(String)
    url = Column(String)
    endpoint = Column(String)
    date_updated = Column(DateTime)
    date_added = Column(DateTime)
    filename = Column(String)

    def __repr__(self):
        return "<Playlist %s from %s>" % (self.name, self.url)

    def format_date_updated(self):
        return self.format_date(self.date_updated)

    def format_date_added(self):
        return self.format_date(self.date_added)

    def format_date(self, thedate):
        if not thedate:
            return "(unknown)"
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
        return dstr

def create_playlist(slug):
    pl = Playlist(slug=slug)
    pl.date_added = datetime.datetime.now()
    return pl

def get_playlist(slug):
    try:
        u = session.query(Playlist).filter(Playlist.slug==slug).one()
        return u
    except NoResultFound:
        return None

def update_playlist(playlist):
    session.add(playlist)
    session.commit()

def playlists_by_added():
    return session.query(Playlist).order_by(desc(Playlist.date_added)).limit(5)

def playlists_by_updated():
    return session.query(Playlist).order_by(desc(Playlist.date_updated))
