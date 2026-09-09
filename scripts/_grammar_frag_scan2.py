# -*- coding: utf-8 -*-
import json, re, glob

# Simple finite-verb heuristic using common English auxiliaries + -s/-ed/-ing on content words is too loose.
# Instead flag: (1) single-token English sentence (2) NP-only starting with The/Same/No/Another without auxiliaries (3) "X versus Y." (4) colon dumps

AUX = re.compile(r"\b(am|is|are|was|were|be|been|being|have|has|had|do|does|did|will|would|can|could|should|must|may|might|need|needs|means|mean|says|say|said|keeps|keep|kept|shows|show|files|file|dresses|dress|picks|pick|wants|want|lives|live|sits|sit|takes|take|gives|give|calls|call|puts|put|comes|come|goes|go|works|work|hears|hear|sees|see|knows|know|teaches|teach|refuses|refuse|forces|force|stays|stay|becomes|become|opens|open|walks|walk|hangs|hang|rides|ride|matches|match|parks|park|leans|lean|stands|stand|follows|follow|names|name|ignores|ignore|proves|prove|trips|trip|treats|treat|invents|invent|asks|ask|joins|join|splits|split|wears|wear|wore|drops|drop|fires|fire|prints|print|points|point|reuses|reuse|reads|read|closes|close|starts|start|indexes|index|changes|change|freezes|freeze|tries|try|drinks|drink|eats|eat|speaks|speak|loves|love|likes|like|owns|own|gets|get|makes|make|tells|tell|feels|feel|looks|look|seems|seem|lets|let|moves|move|adds|add|loses|lose|lost|rebuilds|rebuild|rebuilt|wanders|wander|carries|carry|marks|mark|shares|share|uses|use|used|learns|learn|learned|gives|gave|took|came|went|left|held|felt|thought|brought|bought|caught|taught|understood|began|begun|chose|chosen|broke|broken|wrote|written|spoke|spoken|drove|driven|flew|flown|grew|grown|threw|thrown|drew|drawn|sang|sung|rang|rung|swam|swum|woke|woken|forgot|forgotten|forgave|forgiven|hid|hidden|bit|bitten|beat|beaten|ate|eaten|drank|drunk|ran|run|sat|stood|slept|dreamed|dreamt|paid|laid|lied|died|tried|played|stayed|needed|wanted|called|asked|answered|helped|worked|lived|loved|liked|hated|hoped|wished|seemed|looked|sounded|appeared|happened|existed|included|excluded|required|allowed|expected|preferred|decided|noticed|realized|remembered|reminded|explained|described|repeated|practiced|reviewed|mapped|charted|labeled|labelled|stored|saved|pressed|tapped|clicked|listened|watched|studied|visited|traveled|travelled|arrived|returned|finished|continued|stopped|skipped|checked|guessed|proved|ignored|named|followed|matched|parked|leaned|dressed|filed|shown|kept|said|meant|been)\b", re.I)

suspects = []

def scan(path, text, kind):
    if not isinstance(text, str) or not text.strip():
        return
    # colon dump: colon followed by list-ish
    if re.search(r":\s+\S+", text) and kind in ("teaching","try_expl","quiz_expl","caption","theme","try_prompt","quiz_q"):
        suspects.append(("colon", path, text.strip()[:280]))
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", text.strip()) if p.strip()]
    for p in parts:
        # skip if mostly bosnian example (has diacritic word and short)
        words = re.findall(r"[A-Za-zšđčćžŠĐČĆŽ']+", p)
        if not words:
            continue
        # single word English sentence label
        if re.fullmatch(r"[A-Z][a-z]+\.", p):
            suspects.append(("label-sentence", path, p))
            continue
        # versus slogan
        if re.search(r"\bversus\b", p, re.I) and not AUX.search(p) and p.endswith("."):
            suspects.append(("versus-fragment", path, p))
        # The/Same/Another/No + no aux
        if re.match(r"^(The|Same|Another|No|Not a|Not the|One|Both|Each)\b", p) and p.endswith(".") and not AUX.search(p) and len(words) <= 12:
            # allow "The trap is..." covered by AUX is
            suspects.append(("np-fragment", path, p))
        # parallel comma list as sentence without verb
        if p.endswith(".") and p.count(",") >= 2 and not AUX.search(p) and len(words) <= 14:
            suspects.append(("list-fragment", path, p))
    # stacked short slogan pattern: 3+ consecutive sentences each <= 5 words
    short = [p for p in parts if len(re.findall(r"[A-Za-z']+", p)) <= 5]
    if len(short) >= 3 and len(parts) >= 3:
        # if majority short
        if len(short) / len(parts) >= 0.5:
            suspects.append(("stacked-short", path, " | ".join(short[:5])))

files = sorted(glob.glob("content/grammar/chapter-*/chapter.json"))
for f in files:
    data = json.load(open(f, encoding="utf-8"))
    base = f.replace("\\", "/")
    for block in ("whyHere","englishLies","knownLine","pattern","howYouGuess","trick","nerd"):
        scan(f"{base}.{block}.body", (data.get(block) or {}).get("body"), "teaching")
    scan(f"{base}.next.body", (data.get("next") or {}).get("body"), "teaching")
    scan(f"{base}.theme", data.get("theme"), "theme")
    for i, item in enumerate((data.get("try") or {}).get("items") or []):
        scan(f"{base}.try.items[{i}].prompt", item.get("prompt"), "try_prompt")
        scan(f"{base}.try.items[{i}].explanation", item.get("explanation"), "try_expl")
    for i, q in enumerate((data.get("quiz") or {}).get("questions") or []):
        scan(f"{base}.quiz.questions[{i}].question", q.get("question"), "quiz_q")
        scan(f"{base}.quiz.questions[{i}].explanation", q.get("explanation"), "quiz_expl")
    for i, item in enumerate((data.get("look") or {}).get("items") or []):
        scan(f"{base}.look.items[{i}].english", item.get("english"), "look_en")
    for i, img in enumerate(data.get("images") or []):
        scan(f"{base}.images[{i}].grammarCaption", img.get("grammarCaption"), "caption")

# outline
outline = json.load(open("content/grammar/outline.json", encoding="utf-8"))
scan("content/grammar/outline.json.summary", outline.get("summary"), "teaching")
for c in outline["chapters"]:
    scan(f"content/grammar/outline.json#chapter-{c['chapter']}.theme", c.get("theme"), "theme")

print("COUNT", len(suspects))
from collections import Counter
print(Counter(s[0] for s in suspects))
for s in suspects:
    print(s[0], "|", s[1], "|", s[2].replace("\n"," ")[:200])
