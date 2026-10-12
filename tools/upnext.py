#!/usr/bin/env python3
"""Build the dashboard's "Up next" file: every scheduled post that hasn't gone out yet.

Usage: python3 tools/upnext.py out.json
Reads state/schedule.json and the images it names. Each row carries small thumbnails
(data URIs) so the dashboard can show them without loading anything from another site.
"""
import base64, json, subprocess, sys, tempfile, os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

MT = ZoneInfo("America/Denver")
PLAT = {"twitter": "X", "instagram": "Instagram"}


def thumb(path, width=240):
    if not os.path.exists(path):
        return None
    with tempfile.NamedTemporaryFile(suffix=".jpg") as t:
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", path,
                        "-vf", f"scale={width}:-2", "-q:v", "5", t.name], check=True)
        return "data:image/jpeg;base64," + base64.b64encode(open(t.name, "rb").read()).decode()


def main(out):
    sched = json.load(open("state/schedule.json"))
    now = datetime.now(timezone.utc)
    rows = []
    for p in sched.get("posts", []):
        if p.get("status") not in ("scheduled", "fixed"):
            continue
        local = datetime.strptime(f"{p['date']} {p['time_mt']}", "%Y-%m-%d %H:%M").replace(tzinfo=MT)
        when = local.astimezone(timezone.utc)
        if when < now:
            continue
        imgs = p.get("images") or ([p["image"]] if p.get("image") else [])
        rows.append({
            "when": when.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "when_mt": local.strftime("%a %b %-d · %-I:%M%p").replace("AM", "am").replace("PM", "pm"),
            "caption": p.get("caption", ""),
            "where": PLAT.get(p.get("platform"), p.get("platform", "")),
            "kind": "carousel" if len(imgs) > 1 else "photo",
            "thumbs": [t for t in (thumb(i) for i in imgs) if t],
            "note": p.get("note", ""),
        })
    rows.sort(key=lambda r: r["when"])
    json.dump(rows, open(out, "w"))
    print(f"{len(rows)} upcoming posts -> {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "upnext.json")
