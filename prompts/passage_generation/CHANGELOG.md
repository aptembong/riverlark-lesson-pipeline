# Passage prompt change log

Every prompt change follows the same four steps: **propose, test on the sample
set, approve, roll back if needed.** The approval bar is written down before
the test runs.

---

## PR-2026-11-01 · v2.0 → v2.1 · grade fit for grades 3-12

**1. Propose** (written before the v2.1 run)

*What the v2.0 sample run showed* (`runs/sample_2026-11/`): 8 green, 12 yellow,
0 red. Every yellow came from fit checks, not content or safety checks:

| Miss | Count | Where |
|---|---|---|
| Passage under the word range | 5 | grades 7, 8, E2, E3, E4. All five came in below the minimum |
| Average sentence too long | 6 | grades 3, 5, 6, 8, E1, E2. Overshoot of 2 to 6 words |
| Readability estimate too high | 7 | grades 2-7 and E2 |
| Readability estimate too low | 1 | E3 narrative (FK 9.0, floor 9.5) |

*Likely causes*
- The prompt gave a range and nothing else, so drafts aimed at the bottom of it.
- It gave an average sentence length with no cap, and upper-grade drafts piled
  clauses into single sentences.
- A Lexile number alone doesn't tell the writer what to change. In grades 3-7,
  long sentences and long words together pushed the estimate up.

*Change*
- Target word count (middle of the range) plus a paragraph plan.
- Per-sentence cap (top of the range plus 8 words), and an instruction to split.
- Vocabulary guidance by grade band in place of a bare Lexile number. For 9-12
  it asks for grade-level academic vocabulary, which addresses the one "too low" miss.
- A self-check on counts before returning.
- No change to the schema, rules, representation guidance or validator.

**2. Test plan**
- Same 20 briefs, same `pipeline/validate.py` (no rule changes), one fresh
  first draft per brief, saved before any checks run. No edits after scoring.
- Rendered prompts saved to `runs/sample_2026-11_v2.1/prompts_rendered.jsonl`.

**Approval bar (all must hold)**
1. Green count rises from 8 to at least 14 of 20.
2. Red stays at 0, and representation flags stay at 0.
3. Schema and skill evidence stay at 20/20.
4. No regression: none of the 8 v2.0 greens drops to yellow or red. If one
   does, it gets a written reason before approval.

**Known limits.** The same writer (Claude) drafted both batches knowing what
the validator checks, so neither run is blind. The fix was also designed from these same 20 briefs, so passing
here can overstate how well it generalizes. Before v2.1 goes to production
batches, run it on a fresh set of briefs it wasn't designed from.

**3. Test results** (`runs/sample_2026-11_v2.1/`, scored 2026-11-15 with the
same validator and textstat 0.7.3; re-scoring the v2.0 outputs reproduced the
original v2.0 report exactly)

| Check | v2.0 | v2.1 |
|---|---|---|
| Green / yellow / red | 8 / 12 / 0 | **18 / 2 / 0** |
| Length in range | 15/20 | 20/20 |
| Sentence length in range | 14/20 | 20/20 |
| Readability estimate in range | 12/20 | 18/20 |
| Skill evidence (count + verbatim quotes) | 20/20 | 20/20 |
| Schema | 20/20 | 20/20 |
| Representation flags | 0 | 0 |

Against the approval bar: (1) 18 green, bar was 14. Met. (2) 0 red, 0 flags.
Met. (3) 20/20 and 20/20. Met. (4) All 8 v2.0 greens stayed green. Met.

**What still misses.** Both yellows are now readability estimates that are too
*low*, both in grades 9-12: E1 narrative (FK 6.8, floor 7.5) and E4
argumentative (FK 10.4, floor 10.5). That is the opposite of v2.0's main
problem.

**Watch item: overcorrection.** v2.1 pulled readability down in every band.
Seven of 20 passages now sit within half a grade of the readability floor or
below it (grades 4, 6, 6, 8, E1, E3, E4), and four drafts in grades 2-4 average
shorter sentences than their target range (still inside the ±2 tolerance). v2.0 ran too hard. v2.1 runs slightly easy. Passing and centered
are not the same thing.

**Decision: approved 2026-11-15** for the next pilot batch, with two conditions:
- Run v2.1 on a fresh set of briefs before production (see Known limit).
- Open the next change to center readability, not just pass it. Candidate:
  for 6-12, ask for the middle of the Lexile range and raise the 9-12
  vocabulary guidance. It goes through the same four steps and its own approval bar.

**4. Roll back.** v2.0 stays in the repo with only its status line changed.
Rolling back means pointing `render_prompt.py` back at `v2.0.md`. No other
file changes.
