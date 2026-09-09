# -*- coding: utf-8 -*-
import json

def show(ch, *paths):
    data = json.load(open(f"content/grammar/chapter-{ch:02d}/chapter.json", encoding="utf-8"))
    print("="*20, "CH", ch)
    for p in paths:
        cur = data
        for part in p.split("."):
            if part.endswith("]"):
                name, idx = part[:-1].split("[")
                cur = cur[name][int(idx)]
            else:
                cur = cur[part]
        print(f"-- {p} --")
        print(cur if not isinstance(cur, (dict,list)) else json.dumps(cur, ensure_ascii=False, indent=2)[:800])
        print()

# ch0 mrvica quiz context
show(0, "quiz.questions[1]", "quiz.questions[5]")
show(1, "whyHere.body", "try.items[3].prompt", "try.items[4].prompt", "try.items[4].explanation", "try.items[5].explanation", "try.items[9].explanation", "quiz.questions[0].explanation", "quiz.questions[4].question", "look.items[11].english")
show(3, "try.items[0].explanation", "try.items[5].explanation")
show(4, "try.items[8].explanation", "try.items[9].explanation", "quiz.questions[2].question")
show(5, "quiz.questions[1].explanation", "quiz.questions[2].question", "quiz.questions[5].explanation")
show(6, "try.items[5].explanation", "quiz.questions[2].explanation")
show(7, "try.items[8].explanation")
show(8, "theme", "knownLine.body")
show(9, "theme", "try.items[0].prompt", "try.items[2].prompt", "try.items[9].explanation")
show(10, "theme", "try.items[0].prompt", "try.items[2].prompt", "quiz.questions[0].explanation")
show(11, "try.items[3].prompt", "try.items[9].explanation", "quiz.questions[0].explanation")
show(13, "try.items[9].explanation", "quiz.questions[0]", "theme")
