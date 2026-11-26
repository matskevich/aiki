#!/usr/bin/env python3
"""Run a redacted pinned scanner, with an explicit opt-in for binary download."""
import argparse
import hashlib
import os
import platform
import subprocess
import tarfile
import tempfile
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "8.30.1"
ARCHIVE_SHA256 = "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb"
URL = f"https://github.com/gitleaks/gitleaks/releases/download/v{VERSION}/gitleaks_{VERSION}_linux_x64.tar.gz"


def scan(binary, history):
    subprocess.run([str(binary), "dir", str(ROOT), "--redact", "--no-banner"], check=True)
    if history:
        subprocess.run([str(binary), "git", str(ROOT), "--redact", "--no-banner", "--log-opts=--all"], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--binary", type=Path)
    source.add_argument("--download", action="store_true")
    parser.add_argument("--history", action="store_true")
    args = parser.parse_args()
    if args.binary:
        scan(args.binary.resolve(), args.history)
        return
    if platform.system() != "Linux" or platform.machine() not in {"x86_64", "amd64"}:
        parser.error("pinned download supports linux x64; supply your own reviewed --binary")
    with tempfile.TemporaryDirectory(prefix="aiki-secret-scan-") as directory:
        root = Path(directory)
        archive = root / "gitleaks.tar.gz"
        with urllib.request.urlopen(URL, timeout=60) as response:
            data = response.read(30_000_001)
        if len(data) > 30_000_000 or hashlib.sha256(data).hexdigest() != ARCHIVE_SHA256:
            raise SystemExit("scanner archive integrity check failed")
        archive.write_bytes(data)
        with tarfile.open(archive) as package:
            member = package.getmember("gitleaks")
            if not member.isfile():
                raise SystemExit("scanner archive lacks a regular binary")
            binary = root / "gitleaks"
            with package.extractfile(member) as stream:
                binary.write_bytes(stream.read())
        os.chmod(binary, 0o700)
        scan(binary, args.history)


if __name__ == "__main__":
    main()
