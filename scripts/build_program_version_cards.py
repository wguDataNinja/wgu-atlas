#!/usr/bin/env python3
"""Build program_version_cards.json and write to data/atlas_qa/."""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from atlas_qa.qa.builders.program_version_card import build_program_version_cards

OUTPUT_PATH = REPO_ROOT / "data" / "atlas_qa" / "program_version_cards.json"


def main() -> None:
    print("Building program version cards...")
    cards = build_program_version_cards()
    output = {code: card.model_dump() for code, card in cards.items()}
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"  Wrote {len(output)} program version cards → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
