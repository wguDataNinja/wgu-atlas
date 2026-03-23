#!/usr/bin/env python3
"""Build guide_section_cards.json and write to data/atlas_qa/."""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from atlas_qa.qa.builders.guide_section_card import build_guide_section_cards

OUTPUT_PATH = REPO_ROOT / "data" / "atlas_qa" / "guide_section_cards.json"


def main() -> None:
    print("Building guide section cards...")
    cards = build_guide_section_cards()
    output = [card.model_dump() for card in cards]
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"  Wrote {len(output)} guide section cards → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
