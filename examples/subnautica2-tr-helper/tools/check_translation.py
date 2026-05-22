import argparse
import csv
import json
from collections import Counter
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "working" / "Game.bg.json"
CSV_PATH = ROOT / "working" / "Game.bg.csv"

EXPECTED_CSV_HEADER = ["key", "source", "target"]


def resolve_default_input(use_csv: bool) -> Path:
    if use_csv:
        return CSV_PATH

    if JSON_PATH.exists():
        return JSON_PATH

    return CSV_PATH


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Show translation stats for the current working localization file."
    )

    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=None,
        help="Optional input path. Same as --input.",
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Optional path to a .json or .csv working file.",
    )

    parser.add_argument(
        "--csv",
        action="store_true",
        help="Use working/Game.bg.csv instead of the default working/Game.bg.json.",
    )

    return parser

def check_json_untranslated(path: Path) -> int:
    print("\nJSON untranslated check")
    print("=======================")
    print(f"File: {path}")

    if not path.exists():
        print(f"ERROR: File does not exist: {path}")
        return 1

    with path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("ERROR: Expected JSON array with key/source/target objects.")
        return 1

    empty_keys = 0
    empty_sources = 0
    empty_targets = 0
    malformed_entries = 0
    first_empty_targets = []

    for index, entry in enumerate(data, start=1):
        if not isinstance(entry, dict):
            malformed_entries += 1
            continue

        key = str(entry.get("key", ""))
        source = str(entry.get("source", ""))
        target = str(entry.get("target", ""))

        if not key.strip():
            empty_keys += 1

        if not source.strip():
            empty_sources += 1

        if not target.strip():
            empty_targets += 1

            if len(first_empty_targets) < 10:
                first_empty_targets.append((index, key, source))

    total_entries = len(data)

    print("\nTranslation stats:")
    print(f"  Entries:           {total_entries}")
    print(f"  Empty keys:        {empty_keys}")
    print(f"  Empty source:      {empty_sources}")
    print(f"  Empty target:      {empty_targets}")
    print(f"  Filled target:     {total_entries - empty_targets}")
    print(f"  Malformed entries: {malformed_entries}")

    if first_empty_targets:
        print("\nFirst untranslated entries:")
        for index, key, source in first_empty_targets:
            print(f"  Entry {index}: {key}")
            print(f"    Source: {source[:120]}")

    return malformed_entries

def check_csv_integrity(path: Path) -> int:
    issues = 0

    print("\nCSV integrity check")
    print("===================")
    print(f"File: {path}")

    if not path.exists():
        print(f"ERROR: File does not exist: {path}")
        return 1

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        print("ERROR: CSV file is empty.")
        return 1

    header = rows[0]
    expected_cols = len(EXPECTED_CSV_HEADER)

    print(f"Expected header: {EXPECTED_CSV_HEADER}")
    print(f"Found header:    {header}")

    if header != EXPECTED_CSV_HEADER:
        issues += 1
        print("WARNING: CSV header does not match expected columns.")

    column_counts = Counter(len(row) for row in rows)

    print("\nColumn count distribution:")
    for count, amount in sorted(column_counts.items()):
        print(f"  {count} columns: {amount} rows")

    print("\nBroken rows:")
    broken_rows = 0

    for line_number, row in enumerate(rows[1:], start=2):
        if len(row) != expected_cols:
            issues += 1
            broken_rows += 1
            print(f"  Line {line_number}: expected {expected_cols}, got {len(row)}")
            print(f"    {row[:6]}")

    if broken_rows == 0:
        print("  None")

    empty_keys = 0
    empty_sources = 0
    empty_targets = 0
    first_empty_targets = []

    for line_number, row in enumerate(rows[1:], start=2):
        if len(row) < expected_cols:
            continue

        key, source, target = row[0], row[1], row[2]

        if not key.strip():
            empty_keys += 1
            print(f"  Empty key at line {line_number}")

        if not source.strip():
            empty_sources += 1

        if not target.strip():
            empty_targets += 1

            if len(first_empty_targets) < 10:
                first_empty_targets.append((line_number, key, source))

    total_entries = max(len(rows) - 1, 0)

    print("\nTranslation stats:")
    print(f"  Entries:        {total_entries}")
    print(f"  Empty keys:     {empty_keys}")
    print(f"  Empty source:   {empty_sources}")
    print(f"  Empty target:   {empty_targets}")
    print(f"  Filled target:  {total_entries - empty_targets}")

    if first_empty_targets:
        print("\nFirst untranslated entries:")
        for line_number, key, source in first_empty_targets:
            print(f"  Line {line_number}: {key}")
            print(f"    Source: {source[:120]}")

    if issues:
        print(f"\nWARNING: Found {issues} CSV structure issue(s).")
    else:
        print("\nCSV structure looks OK.")

    return issues


def run_translation_io_stats(input_path: Path) -> int:
    tool = Path(__file__).resolve().with_name("translation_io.py")

    if not tool.exists():
        print(f"ERROR: Missing tool: {tool}")
        return 1

    command = [
        sys.executable,
        str(tool),
        "stats",
        "--input",
        str(input_path),
    ]

    return subprocess.call(command)


def main() -> int:
    args = build_parser().parse_args()

    input_path = args.input or args.path or resolve_default_input(args.csv)
    suffix = input_path.suffix.lower()

    if suffix not in {".json", ".csv"}:
        print(f"ERROR: Unsupported file type: {input_path.suffix}")
        return 1

    if suffix == ".csv":
        csv_issues = check_csv_integrity(input_path)

        print("\nRunning normal translation stats")
        print("===============================")
        stats_result = run_translation_io_stats(input_path)

        return csv_issues or stats_result

    json_check_result = check_json_untranslated(input_path)

    print("\nRunning normal translation stats")
    print("===============================")
    stats_result = run_translation_io_stats(input_path)

    return json_check_result or stats_result


if __name__ == "__main__":
    raise SystemExit(main())