from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_working_rows(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"Working JSON must contain a list of rows: {path}")
    return data


def load_flat_source_rows(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Source Game.json must contain a namespace dictionary: {path}")

    flat: dict[str, str] = {}
    for namespace, payload in data.items():
        if not isinstance(payload, dict):
            continue
        for key, value in payload.items():
            flat[f"{namespace}/{key}"] = "" if value is None else str(value)
    return flat


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare an existing working translation file against a newly extracted source Game.json."
    )
    parser.add_argument("--working", required=True, type=Path)
    parser.add_argument("--source-json", required=True, type=Path)
    parser.add_argument("--limit", type=int, default=20)
    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    args = build_parser().parse_args()
    working_rows = load_working_rows(args.working)
    source_map = load_flat_source_rows(args.source_json)

    working_map = {row["key"]: row for row in working_rows}
    working_keys = set(working_map)
    source_keys = set(source_map)

    added = sorted(source_keys - working_keys)
    removed = sorted(working_keys - source_keys)
    changed = sorted(
        key for key in (working_keys & source_keys) if working_map[key].get("source", "") != source_map[key]
    )

    print(f"Working rows:          {len(working_rows)}")
    print(f"Source rows:           {len(source_map)}")
    print(f"Added keys:            {len(added)}")
    print(f"Removed keys:          {len(removed)}")
    print(f"Changed source values: {len(changed)}")

    if added:
        print("\nAdded keys:")
        for key in added[: args.limit]:
            print(f"  {key}")

    if removed:
        print("\nRemoved keys:")
        for key in removed[: args.limit]:
            print(f"  {key}")

    if changed:
        print("\nChanged source values:")
        for key in changed[: args.limit]:
            working_source = working_map[key].get("source", "").replace("\n", " / ")
            new_source = source_map[key].replace("\n", " / ")
            print(f"  {key}")
            print(f"    Working: {working_source[:180]}")
            print(f"    New:     {new_source[:180]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
