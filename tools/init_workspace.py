from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def resolve_tool(explicit: str | None, env_name: str, local_candidate: Path | None) -> str:
    if explicit:
        return explicit
    if os.environ.get(env_name):
        return os.environ[env_name]
    if local_candidate and local_candidate.exists():
        return str(local_candidate)
    raise FileNotFoundError(f"Could not locate tool. Pass an explicit path or set {env_name}.")


def run_command(command: list[str]) -> None:
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {completed.returncode}: {' '.join(command)}")


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        expected = {"key", "source"}
        if not reader.fieldnames or not expected.issubset(reader.fieldnames):
            raise ValueError(f"CSV must contain at least {sorted(expected)} columns: {path}")
        rows: list[dict[str, str]] = []
        for row in reader:
            rows.append(
                {
                    "key": row.get("key", "") or "",
                    "source": row.get("source", "") or "",
                    "target": row.get("target", "") or "",
                }
            )
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Initialize a UELocKit translation workspace from a source .locres")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--source-locres", required=True)
    parser.add_argument("--localization-target", default="Game")
    parser.add_argument("--culture-tag", default="bg")
    parser.add_argument("--unreal-locres")
    parser.add_argument("--force", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    workspace_root = Path(args.workspace_root).resolve()
    source_locres = Path(args.source_locres).resolve()
    unreal_locres = resolve_tool(
        args.unreal_locres,
        "UNREALLOCRES_EXE",
        workspace_root / "tools" / "UnrealLocres.exe",
    )

    source_dir = workspace_root / "source"
    working_dir = workspace_root / "working"
    output_dir = workspace_root / "output"
    pak_output_dir = workspace_root / "pak-output"
    pak_staging_dir = workspace_root / "pak-staging"

    english_csv = working_dir / f"{args.localization_target}.en.csv"
    translation_csv = working_dir / f"{args.localization_target}.{args.culture_tag}.csv"
    translation_json = working_dir / f"{args.localization_target}.{args.culture_tag}.json"
    stored_source_locres = source_dir / f"{args.localization_target}.en.locres"

    for directory in (source_dir, working_dir, output_dir, pak_output_dir, pak_staging_dir):
        directory.mkdir(parents=True, exist_ok=True)

    if not stored_source_locres.exists() or args.force:
        shutil.copy2(source_locres, stored_source_locres)

    if (english_csv.exists() or translation_csv.exists() or translation_json.exists()) and not args.force:
        raise FileExistsError(
            "Working files already exist. Use --force to overwrite them."
        )

    with tempfile.TemporaryDirectory(dir=working_dir) as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        exported_csv = temp_dir / f"{args.localization_target}.en.csv"
        run_command([unreal_locres, "export", str(stored_source_locres), "-f", "csv", "-o", str(exported_csv)])
        rows = load_csv_rows(exported_csv)

    english_rows = [{"key": row["key"], "source": row["source"], "target": row["target"]} for row in rows]
    translation_rows = [{"key": row["key"], "source": row["source"], "target": ""} for row in rows]

    write_csv_rows(english_csv, english_rows)
    write_csv_rows(translation_csv, translation_rows)
    write_json_rows(translation_json, translation_rows)

    print(f"Initialized workspace from: {stored_source_locres}")
    print(f"Generated: {english_csv}")
    print(f"Generated: {translation_csv}")
    print(f"Generated: {translation_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
