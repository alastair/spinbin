import xspf
import json

# {"name": {"url": xxx, "last_updated": yyyymmddhhiiss, "filename": name.xspf}, ... }

def add(data):
    x = xspf.Xspf()
    x.title = data["name"]
    name = data["name"]
    last_updated = data["thisversionrun"]
    x.date = last_updated
    results = data["results"]
    keys = results.keys()
    if not keys:
        return

    for t in results[keys[0]]:
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

    open("files/%s.xspf" % name, "w").write(x.toXml())

    try:
        data = json.load(open("kimono.json"))
    except IOError:
        data = {}
    except ValueError:
        data = {}
    if name not in data:
        data[name] = {}
    data[name]["last_updated"] = last_updated
    data[name]["filename"] = "%s.xspf" % name
    json.dump(data, open("kimono.json", "w"))
