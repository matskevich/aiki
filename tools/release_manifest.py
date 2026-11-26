#!/usr/bin/env python3
"""Seal and verify exact distribution files; no private source provenance."""
import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath

NAME = "RELEASE.json"


def inventory(root):
    root = Path(root).resolve()
    rows = []
    for directory, dirs, files in os.walk(root):
        for name in dirs:
            if (Path(directory) / name).is_symlink():
                raise ValueError("candidate_symlink_directory")
        dirs[:] = [name for name in dirs if name not in {".git", "__pycache__"}]
        for name in files:
            path = Path(directory) / name
            relative = path.relative_to(root).as_posix()
            if relative == NAME or name.endswith(".pyc"):
                continue
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                raise ValueError("candidate_symlink_or_escape")
            data = path.read_bytes()
            rows.append({"path": relative, "sha256": hashlib.sha256(data).hexdigest(),
                         "executable": bool(path.stat().st_mode & 0o111)})
    return sorted(rows, key=lambda row: row["path"])


def digest(rows):
    return hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def seal(root, channel, version):
    if channel not in {"preview", "public"} or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9.\-]{0,79}", version):
        raise ValueError("invalid_release_identity")
    if (Path(root) / NAME).is_symlink():
        raise ValueError("manifest_symlink")
    rows = inventory(root)
    value = {"schema_version": 1, "product": "aiki", "channel": channel,
             "version": version, "content_sha256": digest(rows), "files": rows,
             "scope": "product context, catalog, portable skills and synthetic examples"}
    (Path(root) / NAME).write_text(json.dumps(value, indent=2) + "\n")
    return value


def verify(root):
    if (Path(root) / NAME).is_symlink():
        raise ValueError("manifest_symlink")
    value = json.loads((Path(root) / NAME).read_text())
    if value.get("schema_version") != 1 or value.get("product") != "aiki" or value.get("channel") not in {"preview", "public"}:
        raise ValueError("invalid_release_manifest")
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9.\-]{0,79}", value.get("version", "")):
        raise ValueError("invalid_release_version")
    for row in value["files"]:
        path = PurePosixPath(row["path"])
        if path.is_absolute() or ".." in path.parts or row["path"] == NAME:
            raise ValueError("invalid_release_path")
    rows = inventory(root)
    if rows != value["files"] or digest(rows) != value["content_sha256"]:
        raise ValueError("candidate_content_changed")
    return value


if __name__ == "__main__":
    result = verify(Path(__file__).resolve().parents[1])
    print(json.dumps({"ok": True, "channel": result["channel"], "version": result["version"],
                      "content_sha256": result["content_sha256"]}))
