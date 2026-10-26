#!/usr/bin/env python3
"""Verify declared public bundle files; does not execute or import any asset.

Two checks only:
1. every file listed in manifest.json exists and matches its sha256;
2. every regular file on disk (except ignored ones) is listed in manifest.json.

Exit code 1 only for check 1. Unlisted files are a WARN, not a failure,
because .gitignore-ignored and build outputs are legitimately absent.
This is file integrity, not runtime acceptance.
"""
from pathlib import Path
import hashlib, json, sys

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))

IGNORE_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", ".vite"}
IGNORE_FILES = {".DS_Store"}

errors = []
listed = set()
for entry in manifest["files"]:
    rel = entry["path"]
    listed.add(rel)
    path = (root / rel).resolve()
    if root not in path.parents or not path.is_file():
        errors.append(rel + ": missing or invalid")
        continue
    if hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
        errors.append(rel + ": hash mismatch")

unlisted = []
for path in sorted(root.rglob("*")):
    if not path.is_file():
        continue
    rel = path.relative_to(root).as_posix()
    if rel in listed or rel == "manifest.json" or path.name in IGNORE_FILES:
        continue
    if any(part in IGNORE_DIRS for part in path.relative_to(root).parts):
        continue
    unlisted.append(rel)

if errors:
    print("\n".join(errors))
    sys.exit(1)

if unlisted:
    print("WARN: " + str(len(unlisted)) + " file(s) on disk not listed in manifest:")
    for rel in unlisted:
        print("  " + rel)

print(
    "PASS:",
    len(manifest["files"]),
    "files match manifest. This is file integrity, not runtime acceptance.",
)
