"""Stage 3: automated validation for Riverlark passages.

Checks every generated passage against its lesson brief and assigns a triage
lane (green, yellow or red). Rules are fixed before a batch runs and are not
tuned to the batch they score.

Readability note: Lexile is a licensed MetaMetrics measure. This module uses
Flesch-Kincaid grade level (textstat) as a free estimate. In production the
licensed Lexile analyzer is the gate; this estimate only routes passages.
"""

import csv
import json
import re
import sys
from pathlib import Path

import textstat

# Expected Flesch-Kincaid grade range per grade (estimate only, see note above).
FK_RANGE = {
    "K": (-3.0, 1.5), "1": (-2.0, 2.5), "2": (0.5, 3.5),
    "3": (1.5, 4.5), "4": (2.5, 5.5), "5": (3.5, 6.5),
    "6": (4.5, 7.5), "7": (5.5, 8.5), "8": (6.5, 9.5),
    "E1": (7.5, 10.5), "E2": (8.5, 11.5), "E3": (9.5, 12.5), "E4": (10.5, 13.5),
}

WORD_TOLERANCE = 10          # from the grade-band spec: plus or minus 10 words
SENTENCE_TOLERANCE = 2.0     # words per sentence, either side of the target range

# Representation flags. Red = reject and regenerate. Yellow = human review.
# v2 change: removed the v1 pattern that flagged "authentic ... culture",
# which penalized the language the framework asks writers to use.
RED_FLAGS = {
    "deficit_framing": [r"\b(disadvantaged|at-risk|broken home|inner[- ]city)\b",
                        r"\b(overcome (?:their|his|her) (?:circumstances|background))\b"],
    "stereotype": [r"\b(naturally (?:good at|gifted))\b", r"\b(exotic|primitive)\b"],
    "ableist_language": [r"\b(wheelchair[- ]bound|confined to a wheelchair|suffers from|victim of)\b",
                         r"\b(handicapped|crippled)\b"],
}
YELLOW_FLAGS = {
    "deficit_framing_moderate": [r"\b(needy|underprivileged)\b",
                                 r"\b(poor (?:family|families|kids|children|neighborhood))\b"],
    "savior_narrative": [r"\b(taught them how|showed them how to|helped them become)\b"],
}

REQUIRED_KEYS = {"title", "passage_text", "skill_instances", "protagonist", "setting", "lesson_hooks"}
HOOK_KEYS = {"hook_question", "i_do", "we_do", "you_do_question"}


def count_words(text):
    return len(re.findall(r"[A-Za-z0-9’']+(?:[-’'][A-Za-z0-9]+)*", text))


def sentences(text):
    # Poems: treat each non-empty line as a unit when lines lack end punctuation.
    parts = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [p for p in parts if count_words(p) > 0]


def check(brief, out):
    issues, flags = [], {"red": [], "yellow": []}

    # 1. Structure
    missing = REQUIRED_KEYS - set(out)
    if missing:
        issues.append(f"schema: missing {sorted(missing)}")
    hooks_missing = HOOK_KEYS - set(out.get("lesson_hooks", {}))
    if hooks_missing:
        issues.append(f"schema: lesson_hooks missing {sorted(hooks_missing)}")
    text = out.get("passage_text", "")

    # 2. Length
    words = count_words(text)
    wmin, wmax = int(brief["words_min"]), int(brief["words_max"])
    words_ok = wmin - WORD_TOLERANCE <= words <= wmax + WORD_TOLERANCE
    if not words_ok:
        issues.append(f"length: {words} words (target {wmin}-{wmax} ±{WORD_TOLERANCE})")

    # 3. Sentence length (skipped for poems, where lines are not sentences)
    sents = sentences(text)
    avg_len = round(words / max(len(sents), 1), 1)
    slmin, slmax = float(brief["sentence_len_min"]), float(brief["sentence_len_max"])
    if brief["text_type"] == "poem":
        sent_ok = True
    else:
        sent_ok = slmin - SENTENCE_TOLERANCE <= avg_len <= slmax + SENTENCE_TOLERANCE
        if not sent_ok:
            issues.append(f"sentence length: {avg_len} avg (target {slmin:g}-{slmax:g} ±{SENTENCE_TOLERANCE:g})")

    # 4. Skill evidence: count, and every quote must appear verbatim
    inst = out.get("skill_instances", [])
    imin, imax = int(brief["instances_min"]), int(brief["instances_max"])
    not_found = [i.get("quote", "") for i in inst if i.get("quote", "") not in text]
    count_ok = imin <= len(inst) <= imax
    if not count_ok:
        issues.append(f"skill evidence: {len(inst)} instances (target {imin}-{imax})")
    if not_found:
        issues.append(f"skill evidence: {len(not_found)} quote(s) not found verbatim")

    # 5. Readability estimate
    fk = round(textstat.flesch_kincaid_grade(text), 1)
    lo, hi = FK_RANGE[brief["grade"]]
    read_ok = lo <= fk <= hi
    if not read_ok:
        issues.append(f"readability estimate: FK grade {fk} (expected {lo:g} to {hi:g})")

    # 6. Representation flags
    for level, table in (("red", RED_FLAGS), ("yellow", YELLOW_FLAGS)):
        for category, patterns in table.items():
            for p in patterns:
                for m in re.finditer(p, text, re.IGNORECASE):
                    flags[level].append({"category": category, "match": m.group(0)})

    # Triage
    technical_fail = bool(missing or hooks_missing or not_found)
    if flags["red"] or len(flags["yellow"]) >= 3 or technical_fail:
        lane = "red"
    elif flags["yellow"] or issues:
        lane = "yellow"
    else:
        lane = "green"

    return {
        "lesson_id": brief["lesson_id"], "grade": brief["grade"], "band": brief["band"],
        "teks_code": brief["teks_code"], "text_type": brief["text_type"], "title": out.get("title"),
        "words": words, "words_ok": words_ok, "avg_sentence_len": avg_len, "sentence_ok": sent_ok,
        "instances": len(inst), "instances_ok": count_ok and not not_found,
        "fk_grade": fk, "readability_ok": read_ok,
        "flags": flags, "issues": issues, "lane": lane,
    }


def main(briefs_csv, outputs_dir, report_path):
    briefs = list(csv.DictReader(open(briefs_csv)))
    results = []
    for b in briefs:
        f = Path(outputs_dir) / f"{b['lesson_id']}.json"
        if not f.exists():
            results.append({"lesson_id": b["lesson_id"], "lane": "red", "issues": ["no output"]})
            continue
        try:
            out = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            results.append({"lesson_id": b["lesson_id"], "lane": "red", "issues": [f"invalid JSON: {e}"]})
            continue
        results.append(check(b, out))
    Path(report_path).write_text(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    res = main(*sys.argv[1:4])
    for r in res:
        print(f"{r['lesson_id']:<14} {r['lane']:<6} " + "; ".join(r.get("issues", [])))
