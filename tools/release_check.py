#!/usr/bin/env python3
"""Check the public hub's tracked file boundary; not a complete privacy audit."""
import fnmatch
import json
import subprocess
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
PRIVATE_PARTS = {".private", "sessions", "state", "private-evidence", "personal-profiles"}
PRIVATE_SUFFIXES = {".session", ".sqlite", ".sqlite3", ".db", ".pem", ".key"}


def violations(root, paths, allowed):
    errors = []
    for value in paths:
        path = PurePosixPath(value)
        file = root / value
        if path.is_absolute() or ".." in path.parts:
            errors.append(f"invalid public path: {value}")
        elif set(path.parts) & PRIVATE_PARTS or path.name.startswith(".env") or path.suffix in PRIVATE_SUFFIXES:
            errors.append(f"private state/configuration path: {value}")
        elif not any(fnmatch.fnmatchcase(value, pattern) for pattern in allowed):
            errors.append(f"outside reviewed public file policy: {value}")
        elif file.is_symlink():
            errors.append(f"public symlink requires separate review: {value}")
        elif not file.resolve().is_relative_to(root.resolve()):
            errors.append(f"public file resolves outside the candidate: {value}")
        elif not file.is_file():
            errors.append(f"tracked public file missing: {value}")
    return errors


def main():
    policy = json.loads((ROOT / "registry/public-files.json").read_text())
    result = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True)
    paths = list(filter(None, result.stdout.decode().split("\0")))
    errors = violations(ROOT, paths, policy["allowed"])
    for path in (ROOT / "examples").glob("*.json"):
        if json.loads(path.read_text()).get("example_only") is not True:
            errors.append(f"public example is not explicitly synthetic: {path.name}")
    print(json.dumps({"ok": not errors, "tracked_files": len(paths), "errors": errors,
                      "scope": policy["scope"], "secret_scan": "separate_required_check",
                      "complete_privacy_or_security_audit": False}, indent=2))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
