import argparse
import json
from pathlib import Path

from .parser import parse_description


def main() -> None:
    parser = argparse.ArgumentParser(description="Przekształca kontrolowany opis sieci w graf JSON.")
    parser.add_argument("path", type=Path, help="Plik UTF-8 z opisem sieci")
    args = parser.parse_args()
    graph = parse_description(args.path.read_text(encoding="utf-8"))
    print(json.dumps(graph.as_property_graph(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
