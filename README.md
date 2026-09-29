# Andris73 Apps — AltStore source

Combined [AltStore](https://altstore.io) / SideStore source for all my apps.

**Source URL:** `https://raw.githubusercontent.com/Andris73/altstore/master/apps.json`

**SideStore Fork** `https://raw.githubusercontent.com/Andris73/altstore/refs/heads/master/sidestore-dev.json`

Each app's CI builds its IPA and publishes here via `tools/update_app.py`
(deduped on build number, newest first). `tools/apps/<app>.json` holds each
app's static metadata.
