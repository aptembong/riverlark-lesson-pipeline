"""Stage 2: fill the passage prompt template for each lesson brief.

Usage: python pipeline/render_prompt.py <prompt.md> <briefs.csv> <out.jsonl>
Writes one rendered user message per brief so every run keeps a record of the
exact prompt each passage was written from.
"""

import csv
import json
import re
import sys
from pathlib import Path

VOCAB = {
    "K-2": "Everyday words of one or two syllables. Name things concretely. One new word at most, explained by the picture or sentence around it.",
    "3-5": "Mostly everyday words. Use up to three content words the lesson needs (such as \"evidence\" or \"drought\"), each explained in the sentence or the next one. Avoid long Latin-based words when a short one works (\"use,\" not \"utilize\").",
    "6-8": "Plain, precise words with some grade-level academic words (such as \"argue,\" \"impact,\" \"contrast\"). Explain any technical term the first time. Keep most words at two syllables or fewer.",
    "9-12": "Grade-level academic and literary vocabulary is expected (such as \"concede,\" \"ambivalent,\" \"consequence\"). Vary word choice, and don't write down to the reader.",
}


def derived(b):
    wmin, wmax = int(b["words_min"]), int(b["words_max"])
    target = int(round((wmin + wmax) / 2 / 5) * 5)
    per = 35 if b["band"] == "K-2" else 80
    paras = max(2, round(target / per))
    return {
        "words_target": target,
        "paragraphs": paras,
        "words_per_paragraph": int(round(target / paras / 5) * 5),
        "sentence_cap": int(b["sentence_len_max"]) + 8,
        "vocab_guidance": VOCAB[b["band"]],
    }


def render(template, b):
    values = {**b, **derived(b)}
    return re.sub(r"\{\{(\w+)\}\}", lambda m: str(values[m.group(1)]), template)


def main(prompt_md, briefs_csv, out_path):
    doc = Path(prompt_md).read_text()
    template = doc.split("## User template", 1)[1].split("## Template values", 1)[0].strip()
    with open(out_path, "w") as f:
        for b in csv.DictReader(open(briefs_csv)):
            f.write(json.dumps({"lesson_id": b["lesson_id"], "user_message": render(template, b)}) + "\n")


if __name__ == "__main__":
    main(*sys.argv[1:4])
