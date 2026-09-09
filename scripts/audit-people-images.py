#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "content" / "book1"


def main() -> None:
    used_urls: set[str] = set()
    for path in sorted(BOOK.glob("day-*/chapter.json")):
        ch = json.loads(path.read_text(encoding="utf-8"))
        day = ch["day"]
        conv = ch.get("conversation", {}).get("imageId")
        facts = [f.get("imageId") for f in ch.get("funFacts", []) if f.get("imageId")]
        print(
            f"L{day:02d}  conv={conv or '-':20}  funFacts={facts or '-'}  "
            f"title={ch.get('titleEn', '')[:40]}"
        )
        for img in ch.get("images", []):
            url = (img.get("sourceUrl") or "").split("?")[0]
            if url:
                used_urls.add(url)
    print(f"\n{len(used_urls)} unique source URLs in book 1")


if __name__ == "__main__":
    main()
