import json
from pathlib import Path

from analyser import analyse_log


def main() -> None:
    result = analyse_log("sample.log")

    with Path("summary.json").open("w", encoding="utf-8") as file:
        json.dump(result, file, indent=2)


if __name__ == "__main__":
    main()
