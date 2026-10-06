# Sentinel

A GoFile-style download hub for `.exe` files.

## Add a file

1. Drop the `.exe` (or `.zip`) into `files/` (upload via GitHub's **Add file** works).
2. Commit. The `Update file list` action recomputes the size and SHA-256 and updates `files.json`. To do it locally instead, run `python3 scripts/build_manifest.py`.
3. Optional: add a description in `files/descriptions.json`, e.g. `{"Tool.exe": "What it does."}`.

## Files over 100 MB

GitHub rejects larger files in the repo. Attach them to a Release and add an entry to `external.json` with `name`, `description`, `size`, `sha256` and `url` (the release asset link).

## Hosting

Enable **Settings → Pages → Deploy from branch → main / root**. The site needs to be served over HTTP(S), since it loads `files.json`.
