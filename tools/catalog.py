#!/usr/bin/env python3
"""Inspect local component metadata without executing installation or service calls."""
import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path):
    data = json.loads(path.read_text())
    if data.get("schema_version") != 1:
        raise ValueError("unsupported catalog schema")
    components = data.get("components", [])
    index = {}
    for component in components:
        key = component["id"]
        if key in index or not re.fullmatch(r"[a-z][a-z0-9-]*", key):
            raise ValueError(f"invalid or duplicate component id: {key}")
        if component["source"]["visibility"] not in {"public", "private"}:
            raise ValueError(f"invalid source visibility: {key}")
        if component["live_status"] != "not_checked":
            raise ValueError(f"local catalog cannot assert live readiness: {key}")
        if component["independent_acceptance"] not in {"not_verified", "verified"}:
            raise ValueError(f"invalid independent acceptance: {key}")
        if component["independent_acceptance"] == "verified" and not component.get("acceptance_receipt"):
            raise ValueError(f"verified acceptance requires a receipt: {key}")
        for field in ["title", "role", "requires", "optional", "packaging", "recipe"]:
            if field not in component:
                raise ValueError(f"missing {field}: {key}")
        index[key] = component
    for key, component in index.items():
        for dependency in component["requires"] + component["optional"]:
            if dependency not in index:
                raise ValueError(f"unknown dependency {dependency}: {key}")
        if set(component["requires"]) & set(component["optional"]):
            raise ValueError(f"required dependency also optional: {key}")
    plan(index, list(index))
    return data, index


def plan(index, requested):
    ordered, complete, active = [], set(), set()

    def visit(key):
        if key not in index:
            raise ValueError(f"unknown component: {key}")
        if key in active:
            raise ValueError(f"required dependency cycle: {key}")
        if key in complete:
            return
        active.add(key)
        for dependency in index[key]["requires"]:
            visit(dependency)
        active.remove(key)
        complete.add(key)
        ordered.append(index[key])

    for key in requested:
        visit(key)
    return ordered


def check_links():
    failures = []
    for path in ROOT.rglob("*.md"):
        if any(part in {".git", ".private", ".venv"} for part in path.relative_to(ROOT).parts):
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text()):
            if target.startswith(("http:", "https:", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if target and not (path.parent / target).is_file():
                failures.append(f"{path.relative_to(ROOT)}: {target}")
    if failures:
        raise ValueError("broken local links: " + ", ".join(failures))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=ROOT / "registry/components.json")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    show = sub.add_parser("show")
    show.add_argument("component")
    resolve = sub.add_parser("plan")
    resolve.add_argument("components", nargs="+")
    sub.add_parser("check")
    args = parser.parse_args()
    try:
        data, index = load(args.catalog)
        if args.command == "list":
            result = [{k: component[k] for k in ["id", "title", "role", "source"]}
                      for component in index.values()]
        elif args.command == "show":
            if args.component not in index:
                raise ValueError(f"unknown component: {args.component}")
            result = index[args.component]
        elif args.command == "plan":
            ordered = plan(index, args.components)
            result = {"requested": args.components, "execution": "none",
                      "dependency_semantics": data["dependency_semantics"],
                      "ordered_components": ordered,
                      "availability_gaps": [c["id"] for c in ordered if c["source"]["visibility"] == "private"],
                      "independent_acceptance": "not_established_by_plan"}
        else:
            check_links()
            for fixture in (ROOT / "examples").glob("*.json"):
                value = json.loads(fixture.read_text())
                if value.get("example_only") is not True:
                    raise ValueError(f"example must be explicitly synthetic: {fixture.name}")
            result = {"ok": True, "components": len(index), "local_links": "checked",
                      "examples": "synthetic", "live_services": "not_checked"}
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f"catalog error: {exc}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
