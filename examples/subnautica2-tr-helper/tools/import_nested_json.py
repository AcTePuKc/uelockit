import argparse
import json
from pathlib import Path


def flatten_dict(data, prefix=""):
    out = {}
    for key, value in data.items():
        full_key = f"{prefix}/{key}" if prefix else key
        if isinstance(value, dict):
            out.update(flatten_dict(value, full_key))
        else:
            out[full_key] = value
    return out


def build_rows(source_nested, target_nested):
    source_flat = flatten_dict(source_nested)
    target_flat = flatten_dict(target_nested)
    rows = []
    for key, source_value in source_flat.items():
        rows.append(
            {
                "key": key,
                "source": source_value,
                "target": target_flat.get(key, ""),
            }
        )
    return rows


def main():
    parser = argparse.ArgumentParser(
        description="Convert nested UnrealLocres-style JSON into row-based working JSON."
    )
    parser.add_argument("--source", required=True, type=Path, help="Nested source Game.json")
    parser.add_argument("--translation", required=True, type=Path, help="Nested translated Game.json")
    parser.add_argument("--output", required=True, type=Path, help="Row-based output JSON")
    args = parser.parse_args()

    source_nested = json.loads(args.source.read_text(encoding="utf-8"))
    translation_nested = json.loads(args.translation.read_text(encoding="utf-8"))
    rows = build_rows(source_nested, translation_nested)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
