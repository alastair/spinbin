import xspf
import json
from dateutil import parser
import os

def add(data):
    x = xspf.Xspf()
    x.title = data["name"]
    name = data["name"]
    print "playlist", name
    last_updated = data["thisversionrun"]
    if not last_updated:
        print " - LAST UPDATED WAS NULL"
        last_updated = data["lastsuccess"]
    pdate = parser.parse(last_updated)
    new = data["newdata"]

    x.date = pdate.strftime("%Y-%m-%dT%H:%M:%S%z")
    results = data["results"]
    version = data["version"]
    keys = results.keys()
    if not keys:
        print " * no results, skipping"
        return

    url = None
    for t in results[keys[0]]:
        u = t.get("url")
        if u and not url:
            url = u
        tr = t.get("track")
        cr = t.get("artist")
        al = t.get("album")
        if tr and isinstance(tr, dict):
            if "text" in tr:
                trname = tr["text"]
            if "href" in tr:
                location = tr["href"]
            else:
                location = None
        else:
            trname = tr
            location = None
        if cr and isinstance(cr, dict):
            crname = cr.get("text")
        else:
            crname = cr
        if al and isinstance(al, dict):
            alname = al.get("text")
        else:
            alname = al
        x.add_track(title=trname, creator=crname, album=alname, location=location)

    if url:
        x.location = url

    slug = name.replace(" ", "-").lower()
    filename = "%s-%s.xspf" % (slug, version)

    if not os.path.exists(os.path.join("files", filename)):
        open("files/%s" % filename, "w").write(x.toXml())

    resp = {}
    resp["last_updated_str"] = pdate.strftime("%Y-%m-%dT%H:%M:%S%z")
    resp["last_updated_obj"] = pdate
    resp["filename"] = filename
    resp["slug"] = slug
    resp["url"] = url
    resp["endpoint"] = data["endpoint"]
    resp["name"] = name
    resp["version"] = version
    return resp
