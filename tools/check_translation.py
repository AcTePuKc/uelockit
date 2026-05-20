from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
WORKING_DIR = ROOT / "working"
INPUT_PATH = next(
    (
        path
        for path in (
            WORKING_DIR / "Game.bg.json",
            WORKING_DIR / "Game.bg.csv",
        )
        if path.exists()
    ),
    WORKING_DIR / "Game.bg.json",
)


def main() -> int:
    tool = Path(__file__).resolve().with_name("translation_io.py")
    command = [sys.executable, str(tool), "stats", "--input", str(INPUT_PATH)]
    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())
