#!/usr/bin/env python3
"""Build Book 1 section tests + final from lesson quiz banks."""
from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "content" / "book1"
OUT = ROOT / "assessments"

SECTIONS = {
    1: list(range(1, 8)),
    2: list(range(8, 15)),
    3: list(range(15, 22)),
    4: list(range(22, 31)),
}

SECTION_META = {
    1: ("Survive day one", "Greetings, identity, numbers, family, place, and time"),
    2: ("Daily life", "Food, shopping, home, weather, invitations, and identity"),
    3: (
        "Getting around",
        "Directions, bus, restaurant, hobbies, holidays, and phone",
    ),
    4: (
        "Travel and longer stay",
        "Travnik, routines, nature, health, housing, work, Mostar, writing, and finale",
    ),
}


def load_day(day: int) -> dict:
    return json.loads((ROOT / f"day-{day:02d}" / "chapter.json").read_text())


def collect(days: list[int]) -> list[dict]:
    items = []
    for d in days:
        ch = load_day(d)
        for q in ch.get("sectionQuiz", {}).get("questions", []):
            qq = dict(q)
            if not qq.get("question") and qq.get("prompt"):
                qq["question"] = qq["prompt"]
            if not qq.get("question") or not qq.get("options"):
                continue
            qq["sourceDay"] = d
            items.append(qq)
    return items


def pick_balanced(items: list[dict], n: int, seed: int) -> list[dict]:
    by: dict[str, list[dict]] = {}
    for q in items:
        by.setdefault(q.get("skill") or "vocabulary", []).append(q)
    skills = list(by.keys())
    rng = random.Random(seed)
    for s in skills:
        rng.shuffle(by[s])
    chosen: list[dict] = []
    idx = {s: 0 for s in skills}
    while len(chosen) < n and any(idx[s] < len(by[s]) for s in skills):
        for s in skills:
            if len(chosen) >= n:
                break
            if idx[s] < len(by[s]):
                chosen.append(by[s][idx[s]])
                idx[s] += 1
    rest = [q for q in items if q not in chosen]
    rng.shuffle(rest)
    while len(chosen) < n and rest:
        chosen.append(rest.pop())
    out = []
    for i, q in enumerate(chosen[:n], 1):
        out.append(
            {
                "id": f"q{i}",
                "question": q["question"],
                "options": q["options"],
                "correctIndex": q["correctIndex"],
                "explanation": q.get("explanation") or "",
                "skill": q.get("skill") or "vocabulary",
                "remediationDay": q.get("sourceDay"),
            }
        )
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for sec, days in SECTIONS.items():
        title, focus = SECTION_META[sec]
        qs = pick_balanced(collect(days), 12, seed=42 + sec)
        data = {
            "id": f"section-{sec}",
            "book": 1,
            "kind": "section",
            "section": sec,
            "coversDays": days,
            "title": f"Section {sec} test",
            "titleEn": f"Section {sec} test · {title}",
            "intro": (
                f"This test covers Lessons {days[0]} to {days[-1]}. {focus}. "
                "Pass with 70% or higher."
            ),
            "passPercent": 70,
            "questions": qs,
        }
        path = OUT / f"section-{sec}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        print("wrote", path, len(qs))

    final_qs: list[dict] = []
    for sec, days in SECTIONS.items():
        final_qs.extend(pick_balanced(collect(days), 5, seed=100 + sec))
    for i, q in enumerate(final_qs, 1):
        q["id"] = f"q{i}"
    final = {
        "id": "final",
        "book": 1,
        "kind": "final",
        "coversDays": list(range(1, 31)),
        "title": "Book 1 final test",
        "titleEn": "Book 1 final test",
        "intro": (
            "This final covers Lessons 1 to 30 across all four sections. "
            "Pass with 70% or higher."
        ),
        "passPercent": 70,
        "questions": final_qs,
    }
    (OUT / "final.json").write_text(
        json.dumps(final, ensure_ascii=False, indent=2) + "\n"
    )
    print("wrote final", len(final_qs))
    (OUT / "index.json").write_text(
        json.dumps(
            {
                "book": 1,
                "sectionTests": [f"section-{s}" for s in SECTIONS],
                "finalTest": "final",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
