#!/usr/bin/env python3
"""Verify declared public bundle files; does not execute or import any asset."""
from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
errors=[]
for entry in manifest['files']:
 path=(root/entry['path']).resolve()
 if root not in path.parents or not path.is_file():errors.append(entry['path']+': missing or invalid');continue
 if hashlib.sha256(path.read_bytes()).hexdigest()!=entry['sha256']:errors.append(entry['path']+': hash mismatch')
if errors:
 print('\n'.join(errors));sys.exit(1)
print('PASS:',len(manifest['files']),'files match manifest. This is file integrity, not runtime acceptance.')
