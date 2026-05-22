from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        expected = {"key", "source", "target"}
        if not reader.fieldnames or not expected.issubset(reader.fieldnames):
            raise ValueError(f"CSV must contain columns {sorted(expected)}: {path}")
        return [
            {
                "key": row.get("key", "") or "",
                "source": row.get("source", "") or "",
                "target": row.get("target", "") or "",
            }
            for row in reader
        ]


def load_json_rows(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"JSON must contain a list of rows: {path}")

    rows: list[dict[str, str]] = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"JSON row {index} is not an object: {path}")
        try:
            key = str(item["key"])
            source = str(item["source"])
            target = str(item["target"])
        except KeyError as exc:
            raise ValueError(f"JSON row {index} is missing field {exc.args[0]!r}: {path}") from exc
        rows.append({"key": key, "source": source, "target": target})
    return rows


def write_csv_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["key", "source", "target"])
        writer.writeheader()
        writer.writerows(rows)


def write_json_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def command_json_to_csv(args: argparse.Namespace) -> int:
    write_csv_rows(Path(args.output), load_json_rows(Path(args.input)))
    return 0


def command_csv_to_json(args: argparse.Namespace) -> int:
    write_json_rows(Path(args.output), load_csv_rows(Path(args.input)))
    return 0


def command_stats(args: argparse.Namespace) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    path = Path(args.input)
    rows = load_json_rows(path) if path.suffix.lower() == ".json" else load_csv_rows(path)

    filled = 0
    empty = 0
    same = 0
    likely_untranslated = 0
    for row in rows:
        source = row["source"].strip()
        target = row["target"].strip()
        if not target:
            empty += 1
        else:
            filled += 1
            if target == source:
                same += 1
                if is_probably_real_untranslated(row["key"], source):
                    likely_untranslated += 1

    print(f"Попълнени: {filled}")
    print(f"Празни: {empty}")
    print(f"Съвпадат с оригинала: {same}")
    print(f"Вероятно непреведени: {likely_untranslated}")
    return 0


def is_probably_real_untranslated(key: str, source: str) -> bool:
    text = source.strip()
    if not text:
        return False

    lowered = text.lower()
    key_lower = key.lower()

    # Intentional placeholders / work-in-progress strings.
    if "placeholder" in lowered or "coming soon" in lowered or text == "tk":
        return False

    # Known harmless source==target values.
    if text in {"???", "-", "PDA", "Twitch", "DLAA", "DLSS", "FSR 3.1", "TSR", "ROG Ally"}:
        return False

    # Known non-localized or developer-only buckets.
    ignored_key_fragments = (
        "st_old_",
        "donotloc",
        "unlocalizeduiplaceholders",
        "debug/",
        "characterselectui/character",
        "joinlangamescreen/",
        "hardcodedstringreplacementpass_m31/",
        "settingsgraphics/",
        "reasons/scantrait.generic",
        "friendsui/removebutton",
    )
    if any(fragment in key_lower for fragment in ignored_key_fragments):
        return False

    # IDs, codes, formatting templates, button glyphs, etc.
    if re.fullmatch(r"[A-Z0-9_./:#\\-]+", text):
        return False
    if re.fullmatch(r"[-0-9xX/ .:%{}?()\\[\\]_]+", text):
        return False
    if text.startswith("id ") or text.startswith("open ") or text.startswith("mount "):
        return False
    if text.startswith("cpimg ") or text.startswith("mount "):
        return False
    if "LOGIN " in text or "ACCESS GRANTED" in text or "Secure Terminal" in text:
        return False

    # File names, device paths, VIN/codes, and other technical literals.
    if ".txt" in lowered or "/dev/" in text or "noa_3.4.img" in text:
        return False
    if " isv " in f" {lowered} " or " frame " in lowered:
        return False

    # Very short strings are too noisy to classify here.
    if len(text) <= 25:
        return False

    # Likely real untranslated English prose/title.
    return bool(re.search(r"[A-Za-z]{4}", text))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Utilities for JSON/CSV Unreal localization working files."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    json_to_csv = subparsers.add_parser("json-to-csv", help="Convert working JSON to UnrealLocres CSV")
    json_to_csv.add_argument("--input", required=True)
    json_to_csv.add_argument("--output", required=True)
    json_to_csv.set_defaults(func=command_json_to_csv)

    csv_to_json = subparsers.add_parser("csv-to-json", help="Convert working CSV to JSON")
    csv_to_json.add_argument("--input", required=True)
    csv_to_json.add_argument("--output", required=True)
    csv_to_json.set_defaults(func=command_csv_to_json)

    stats = subparsers.add_parser("stats", help="Show translation fill stats for CSV or JSON")
    stats.add_argument("--input", required=True)
    stats.set_defaults(func=command_stats)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
