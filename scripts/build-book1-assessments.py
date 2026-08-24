#!/usr/bin/env python3
"""Assessments are hand-authored in content/book1/assessments/.

Do not regenerate them from lesson quiz banks. A random skill mix
is not a section test. Edit the JSON files directly.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "content" / "book1" / "assessments"


def main() -> None:
    raise SystemExit(
        "Book 1 assessments are authored, not generated.\n"
        f"Edit files in {ROOT}\n"
        "Then run: node scripts/sync-content.cjs"
    )


if __name__ == "__main__":
    main()
