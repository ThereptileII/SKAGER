#!/usr/bin/env python3
"""Verify the update-server response against the local release hashes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


p = argparse.ArgumentParser()
p.add_argument("--release", type=Path, required=True)
p.add_argument("--server-response", type=Path, required=True)
a = p.parse_args()
release = json.loads((a.release / "RELEASE.json").read_text(encoding="utf-8"))
response = json.loads(a.server_response.read_text(encoding="utf-8"))
if response.get("status") not in {"published", "verified"}:
    raise SystemExit("server did not confirm publication")
server_objects = response.get("objects")
if not isinstance(server_objects, dict):
    raise SystemExit("server response has no object hash map")
for name, record in release["objects"].items():
    local = a.release / name
    if not local.is_file() or sha(local) != record["sha256"]:
        raise SystemExit(f"local release hash mismatch: {name}")
    remote = server_objects.get(name)
    if not isinstance(remote, dict) or remote.get("sha256") != record["sha256"]:
        raise SystemExit(f"server hash mismatch: {name}")
print("production publication verified", release["version"], release["commit"])
