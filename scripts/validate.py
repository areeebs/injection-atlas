#!/usr/bin/env python3
"""
Validate the injection-atlas: every technique file is well-formed and index.json
matches the files on disk. Run by CI and locally:

  python3 scripts/validate.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TECH = ROOT / "techniques"
INDEX = ROOT / "index.json"

REQUIRED_FM = ("id", "title", "category", "severity")
REQUIRED_SECTIONS = ("## Summary", "## How it works", "## Minimal example",
                     "## Detection", "## Mitigation")
VALID_SEVERITY = {"critical", "high", "medium", "low"}
ID_RE = re.compile(r"^T\d{3}$")


def parse_front_matter(text: str) -> dict:
    m = re.match(r"\s*---\s*\n(.*?)\n---\s*\n", text, re.S)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip()
    return meta


def main() -> int:
    problems: list[str] = []

    files = sorted(TECH.glob("T*.md"))
    if not files:
        problems.append("no technique files found under techniques/")

    file_ids = {}
    for f in files:
        text = f.read_text()
        meta = parse_front_matter(text)
        for key in REQUIRED_FM:
            if not meta.get(key):
                problems.append(f"{f.name}: missing front-matter '{key}'")
        tid = meta.get("id", "")
        if tid and not ID_RE.match(tid):
            problems.append(f"{f.name}: id '{tid}' must look like T001")
        if meta.get("severity") and meta["severity"] not in VALID_SEVERITY:
            problems.append(f"{f.name}: invalid severity '{meta['severity']}'")
        if tid in file_ids:
            problems.append(f"{f.name}: duplicate id '{tid}' (also {file_ids[tid]})")
        else:
            file_ids[tid] = f.name
        for section in REQUIRED_SECTIONS:
            if section not in text:
                problems.append(f"{f.name}: missing section '{section}'")

    # cross-check index.json
    try:
        index = json.loads(INDEX.read_text())["techniques"]
    except (OSError, json.JSONDecodeError, KeyError) as e:
        problems.append(f"index.json unreadable: {e}")
        index = []

    index_ids = set()
    for entry in index:
        index_ids.add(entry.get("id"))
        fp = ROOT / entry.get("file", "")
        if not fp.is_file():
            problems.append(f"index.json: file for {entry.get('id')} not found: {entry.get('file')}")

    missing_from_index = set(file_ids) - index_ids
    missing_files = index_ids - set(file_ids)
    for i in sorted(x for x in missing_from_index if x):
        problems.append(f"{i} exists on disk but is not in index.json")
    for i in sorted(x for x in missing_files if x):
        problems.append(f"{i} is in index.json but has no technique file")

    if problems:
        print("atlas validation FAILED:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"atlas OK: {len(files)} techniques, index consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
