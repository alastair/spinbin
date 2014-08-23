import xspf
import json
from dateutil import parser

# {"name": {"url": xxx, "last_updated": yyyymmddhhiiss, "filename": name.xspf}, ... }

def add(data):
    x = xspf.Xspf()
    x.title = data["name"]
    name = data["name"]
    last_updated = data["thisversionrun"]
    if not last_updated:
        last_updated = data["lastsuccess"]
    pdate = parser.parse(last_updated)
    version = data["version"]
    new = data["newdata"]
    #if not new:
    #    return

    x.date = pdate.strftime("%Y-%m-%dT%H:%M:%S%z")
    results = data["results"]
    keys = results.keys()
    if not keys:
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

    filename = name.replace(" ", "-").lower()

    open("files/%s.xspf" % filename, "w").write(x.toXml())

    resp = {}
    resp["last_updated"] = pdate.strftime("%Y-%m-%dT%H:%M:%S%z")
    resp["filename"] = "%s.xspf" % filename
    resp["url"] = url
    resp["endpoint"] = data["endpoint"]
    resp["name"] = name
    return filename, resp
