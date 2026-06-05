#!/usr/bin/env python3
"""Update the combined AltStore `apps.json` with one app's new build.

Driven by env vars (set by each app's CI):
  APP_ID     key matching tools/apps/<APP_ID>.json
  VERSION    marketing version (CFBundleShortVersionString)
  BUILD      build number (CFBundleVersion) — unique per commit
  SIZE       IPA size in bytes
  SHA_SHORT  short commit sha (optional)
  DATE       YYYY-MM-DD (optional)

Inserts a new version entry at the front of that app's `versions`, deduped on
buildVersion, creating the app entry from tools/apps/<APP_ID>.json if needed.
"""
import json
import os
import sys

APP_ID = os.environ["APP_ID"]
VERSION = os.environ["VERSION"]
BUILD = str(os.environ["BUILD"])
SIZE = int(os.environ["SIZE"])
SHA_SHORT = os.environ.get("SHA_SHORT", "")
DATE = os.environ.get("DATE", "")

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS_DIR)
APPS_JSON = os.path.join(REPO_ROOT, "apps.json")

with open(os.path.join(TOOLS_DIR, "apps", f"{APP_ID}.json")) as f:
    meta = json.load(f)

if os.path.exists(APPS_JSON):
    with open(APPS_JSON) as f:
        source = json.load(f)
else:
    source = {
        "name": "Andris73 Apps",
        "identifier": "com.andris73.altstore",
        "apps": [],
        "news": [],
    }

apps = source.setdefault("apps", [])
app = next((a for a in apps if a.get("bundleIdentifier") == meta["bundleIdentifier"]), None)
if app is None:
    app = {
        "name": meta["name"],
        "bundleIdentifier": meta["bundleIdentifier"],
        "developerName": meta.get("developerName", ""),
        "subtitle": meta.get("subtitle", ""),
        "localizedDescription": meta.get("localizedDescription", ""),
        "iconURL": meta["iconURL"],
        "versions": [],
    }
    apps.append(app)
else:
    for key in ("name", "developerName", "subtitle", "localizedDescription", "iconURL"):
        if key in meta:
            app[key] = meta[key]

versions = app.setdefault("versions", [])
if any(str(v.get("buildVersion")) == BUILD for v in versions):
    print(f"{APP_ID} build {BUILD} already present, skipping")
    sys.exit(0)

versions.insert(0, {
    "version": VERSION,
    "buildVersion": BUILD,
    "date": DATE,
    "localizedDescription": f"Build {SHA_SHORT}" if SHA_SHORT else "",
    "downloadURL": meta["downloadURL"],
    "size": SIZE,
    "minOSVersion": meta.get("minOSVersion", "26.0"),
})

with open(APPS_JSON, "w") as f:
    json.dump(source, f, indent=2)
print(f"Updated {APP_ID} -> {VERSION} ({BUILD}) [{len(apps)} app(s)]")
