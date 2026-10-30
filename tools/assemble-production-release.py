#!/usr/bin/env python3
"""Assemble one immutable, hash-bound production release set.

This helper does not publish anything. Publication is performed only by the
protected production workflow after this manifest has been reviewed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument("--version", required=True)
parser.add_argument("--commit", required=True)
parser.add_argument("--notes", type=Path, required=True)
parser.add_argument("--package", type=Path, required=True)
parser.add_argument("--installer", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()

if len(args.commit) != 40 or any(c not in "0123456789abcdef" for c in args.commit.lower()):
    raise SystemExit("--commit must be a full lowercase Git SHA")
if not args.notes.is_file():
    raise SystemExit("release notes file is missing")
if not args.installer.is_file():
    raise SystemExit("installer is missing")
if not args.package.is_dir():
    raise SystemExit("production package directory is missing")

root = Path(__file__).resolve().parents[1]
out = args.output.resolve()
if out.exists():
    raise SystemExit("refusing to overwrite an existing release directory")
out.mkdir(parents=True)

installer_name = f"SKAGER-{args.version}-Setup.exe"
recovery_candidates = sorted(args.package.glob("*Portable-Recovery.zip"))
if len(recovery_candidates) != 1:
    raise SystemExit("expected exactly one portable recovery ZIP")
recovery_name = f"SKAGER-{args.version}-Portable-Recovery.zip"
source_name = f"SKAGER-{args.version}-Source.zip"

installer = out / installer_name
recovery = out / recovery_name
source = out / source_name
shutil.copy2(args.installer, installer)
shutil.copy2(recovery_candidates[0], recovery)

subprocess.run(["git", "archive", "--format=zip", "--output", str(source), args.commit],
               cwd=root, check=True)
shutil.copy2(args.notes, out / "RELEASE_NOTES.md")

records = {}
for path in sorted(out.iterdir()):
    if path.is_file() and path.name not in {"RELEASE.json", "SHA256SUMS.txt"}:
        records[path.name] = {"bytes": path.stat().st_size, "sha256": digest(path)}

release = {
    "schema": 1,
    "product": "SKAGER",
    "version": args.version,
    "commit": args.commit,
    "openCpn": {"version": "5.12.4", "upstreamCommit": "37fd0cddb7334fe489e9f18aa163977a9c5c84f7", "abi": "Win32/x86"},
    "objects": records,
    "publication": "production-only",
}
(out / "RELEASE.json").write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")
(out / "SHA256SUMS.txt").write_text(
    "".join(f"{record['sha256']}  {name}\n" for name, record in records.items()), encoding="utf-8"
)

# The update signer consumes this unsigned payload inside the protected job.
(out / "update-manifest.json").write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"output": str(out), "objects": records}, indent=2))
