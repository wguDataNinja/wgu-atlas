#!/usr/bin/env python3
"""Build course_cards.json and write to data/atlas_qa/."""
import json
import sys
from pathlib import Path

# Ensure repo root is on the path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from atlas_qa.qa.builders.course_card import build_course_cards

OUTPUT_PATH = REPO_ROOT / "data" / "atlas_qa" / "course_cards.json"


def main() -> None:
    print("Building course cards...")
    cards = build_course_cards()
    output = {code: card.model_dump() for code, card in cards.items()}
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"  Wrote {len(output)} course cards → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
