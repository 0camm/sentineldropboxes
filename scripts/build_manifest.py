#!/usr/bin/env python3
"""Rebuild files.json from every .exe (and .zip) in files/ plus anything in external.json.

Usage:  python3 scripts/build_manifest.py
"""
import hashlib, json, os
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES_DIR = os.path.join(ROOT, "files")


def load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


descriptions = load(os.path.join(FILES_DIR, "descriptions.json"), {})
entries = list(load(os.path.join(ROOT, "external.json"), []))
external_names = {e["name"] for e in entries}

for name in sorted(os.listdir(FILES_DIR), key=str.casefold):
    path = os.path.join(FILES_DIR, name)
    if not (os.path.isfile(path) and name.lower().endswith((".exe", ".zip"))) or name in external_names:
        continue
    entries.append({
        "name": name,
        "description": descriptions.get(name, "Windows download."),
        "size": os.path.getsize(path),
        "sha256": sha256(path),
        "url": "files/" + quote(name),
    })

with open(os.path.join(ROOT, "files.json"), "w", encoding="utf-8") as f:
    json.dump(entries, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"files.json: {len(entries)} file(s)")
