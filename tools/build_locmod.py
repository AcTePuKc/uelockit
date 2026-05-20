from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import struct
import subprocess
import tempfile
import time
from pathlib import Path


def resolve_tool(explicit: str | None, env_name: str, local_candidate: Path | None) -> str:
    if explicit:
        return explicit
    if os.environ.get(env_name):
        return os.environ[env_name]
    if local_candidate and local_candidate.exists():
        return str(local_candidate)
    raise FileNotFoundError(f"Could not locate tool. Pass an explicit path or set {env_name}.")


def load_rows_from_json(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"JSON must contain a list: {path}")
    rows: list[dict[str, str]] = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"JSON row {index} is not an object: {path}")
        rows.append(
            {
                "key": str(item["key"]),
                "source": str(item["source"]),
                "target": str(item["target"]),
            }
        )
    return rows


def write_rows_to_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["key", "source", "target"])
        writer.writeheader()
        writer.writerows(rows)


def run_command(command: list[str]) -> None:
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {completed.returncode}: {' '.join(command)}")


def wait_file_ready(path: Path, timeout_seconds: float = 5.0) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with path.open("rb+"):
                return
        except OSError:
            time.sleep(0.2)
    raise TimeoutError(f"Timed out waiting for file lock to clear: {path}")


def write_ue_ascii_string(handle, value: str) -> None:
    encoded = (value + "\0").encode("ascii")
    handle.write(struct.pack("<i", len(encoded)))
    handle.write(encoded)


def build_locmeta(path: Path, culture_code: str) -> None:
    magic = bytes([0x4F, 0xEE, 0x4C, 0xA1, 0x68, 0x48, 0x55, 0x83, 0x6C, 0x4C, 0x46, 0xBD, 0x70, 0xDA, 0x50, 0x7C])
    cultures = [
        "de-DE",
        "en",
        "es-419",
        "fr-FR",
        "it",
        "ja-JP",
        "ko-KR",
        "pt-BR",
        "ru-RU",
        "uk-UA",
        "zh-Hans",
        culture_code,
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        handle.write(magic)
        handle.write(bytes([1]))
        write_ue_ascii_string(handle, "en")
        write_ue_ascii_string(handle, "en/Game.locres")
        handle.write(struct.pack("<I", len(cultures)))
        for culture in cultures:
            write_ue_ascii_string(handle, culture)


def build_locres(args: argparse.Namespace, workspace_root: Path) -> Path:
    source_locres = Path(args.source_locres)
    output_locres = Path(args.output_locres)
    unreal_locres = resolve_tool(
        args.unreal_locres,
        "UNREALLOCRES_EXE",
        workspace_root / "tools" / "UnrealLocres.exe",
    )

    output_locres.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(dir=output_locres.parent) as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        temp_csv = temp_dir / f"{output_locres.stem}.tmp.csv"
        temp_locres = temp_dir / f"{output_locres.stem}.tmp{output_locres.suffix}"

        if args.translation_format == "csv":
            input_csv = Path(args.translation_csv)
        else:
            rows = load_rows_from_json(Path(args.translation_json))
            write_rows_to_csv(temp_csv, rows)
            input_csv = temp_csv

        run_command([unreal_locres, "import", "-f", "csv", str(source_locres), str(input_csv), "-o", str(temp_locres)])
        wait_file_ready(temp_locres)
        shutil.copy2(temp_locres, output_locres)

    return output_locres


def build_package(args: argparse.Namespace, workspace_root: Path, output_locres: Path) -> None:
    unreal_pak = resolve_tool(
        args.unreal_pak,
        "UNREALPAK_EXE",
        workspace_root / "tools" / "UnrealPak.exe",
    )
    retoc = resolve_tool(
        args.retoc,
        "RETOC_EXE",
        workspace_root / "tools" / "retoc" / "retoc.exe",
    )

    output_dir = Path(args.output_dir)
    staging_root = Path(args.staging_dir)
    staging_game_loc_dir = staging_root / args.game_name / "Content" / "Localization" / "Game"
    staging_culture_dir = staging_game_loc_dir / args.culture_folder
    response_file = workspace_root / "tools" / f"filelist-{args.package_name}.txt"
    pak_output = output_dir / f"{args.package_name}.pak"
    utoc_output = output_dir / f"{args.package_name}.utoc"
    ucas_output = output_dir / f"{args.package_name}.ucas"
    locmeta_output = output_dir / f"{args.localization_target}.locmeta"

    output_dir.mkdir(parents=True, exist_ok=True)
    staging_culture_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(output_locres, staging_culture_dir / f"{args.localization_target}.locres")
    build_locmeta(locmeta_output, args.culture_code)
    shutil.copy2(locmeta_output, staging_game_loc_dir / f"{args.localization_target}.locmeta")

    response_lines = [
        f'"{staging_game_loc_dir / f"{args.localization_target}.locmeta"}" "../../../{args.game_name}/Content/Localization/Game/{args.localization_target}.locmeta"',
        f'"{staging_culture_dir / f"{args.localization_target}.locres"}" "../../../{args.game_name}/Content/Localization/Game/{args.culture_folder}/{args.localization_target}.locres"',
    ]
    response_file.write_text("\n".join(response_lines) + "\n", encoding="ascii")

    for path in (pak_output, utoc_output, ucas_output):
        if path.exists():
            path.unlink()

    run_command([unreal_pak, str(pak_output), f"-create={response_file}"])
    run_command([retoc, "to-zen", "--version", args.ue_version, str(pak_output), str(utoc_output)])

    if args.deploy_to_game and args.game_paks_dir:
        game_paks_dir = Path(args.game_paks_dir)
        game_paks_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pak_output, game_paks_dir / pak_output.name)
        shutil.copy2(utoc_output, game_paks_dir / utoc_output.name)
        shutil.copy2(ucas_output, game_paks_dir / ucas_output.name)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cross-platform-ish orchestration for UELocKit builds.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--translation-format", choices=["json", "csv"], default="json")
    parser.add_argument("--source-locres", required=True)
    parser.add_argument("--translation-json")
    parser.add_argument("--translation-csv")
    parser.add_argument("--output-locres", required=True)
    parser.add_argument("--localization-target", default="Game")
    parser.add_argument("--culture-folder", default="bg")
    parser.add_argument("--culture-code", default="bg-BG")
    parser.add_argument("--package-name", default="MyUnrealGame-LocMod_P")
    parser.add_argument("--game-name", default="MyUnrealGame")
    parser.add_argument("--output-dir", default="./pak-output")
    parser.add_argument("--staging-dir", default="./pak-staging/locmod")
    parser.add_argument("--game-paks-dir")
    parser.add_argument("--ue-version", default="UE5_6")
    parser.add_argument("--unreal-locres")
    parser.add_argument("--unreal-pak")
    parser.add_argument("--retoc")
    parser.add_argument("--deploy-to-game", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.translation_format == "json" and not args.translation_json:
        parser.error("--translation-json is required when --translation-format json is used")
    if args.translation_format == "csv" and not args.translation_csv:
        parser.error("--translation-csv is required when --translation-format csv is used")

    workspace_root = Path(args.workspace_root).resolve()
    output_locres = build_locres(args, workspace_root)
    build_package(args, workspace_root, output_locres)
    print(f"Built localization package from {args.translation_format}: {output_locres}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
