#!/usr/bin/env python3
"""Read a bounded local product context without contacting accounts or services."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    release = ROOT / "RELEASE.json"
    value = {"schema": "aiki-product-context/v1", "product": "aiki",
             "channel": json.loads(release.read_text())["channel"] if release.is_file() else "source",
             "authority": "context only; no access or action grant",
             "entry": "AGENTS.md", "components": "registry/components.json",
             "views": "docs/views/", "shared_skills": "skills/",
             "context": {name: (ROOT / name).read_text() for name in
                         ["PRODUCT.md", "CURRENT.md", "ROADMAP.md"]}}
    print(json.dumps(value, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
