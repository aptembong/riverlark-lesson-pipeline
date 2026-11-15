# Prompt v2.0 vs v2.1 · same 20 briefs, same checks

Change record and approval decision: `prompts/passage_generation/CHANGELOG.md` (PR-2026-11-01).

| | v2.0 | v2.1 |
|---|---|---|
| Green / yellow / red | 8 / 12 / 0 | 18 / 2 / 0 |
| Length in range | 15/20 | 20/20 |
| Sentence length in range | 14/20 | 20/20 |
| Readability estimate in range | 12/20 | 18/20 |
| Skill evidence / schema | 20/20 / 20/20 | 20/20 / 20/20 |
| Representation flags | 0 | 0 |

## By lesson

| Lesson | Type | v2.0 | v2.1 | Words | Avg sentence | FK estimate | v2.1 issue |
|---|---|---|---|---|---|---|---|
| RL-TX-K-001 | narrative | green | green | 62 → 60 | 4.4 → 4.3 | -1.7 → -0.9 | none |
| RL-TX-1-002 | poem | green | green | 71 → 94 | 5.9 → 5.9 | 0.9 → 0.9 | none |
| RL-TX-1-003 | informational | green | green | 71 → 86 | 7.9 → 7.2 | 0.5 → 0.2 | none |
| RL-TX-2-004 | informational | green | green | 104 → 122 | 11.6 → 8.1 | 3.1 → 1.7 | none |
| RL-TX-2-005 | persuasive | yellow | green | 104 → 122 | 10.4 → 7.6 | 3.8 → 1.5 | none |
| RL-TX-3-006 | informational | yellow | green | 170 → 165 | 14.2 → 9.7 | 6.5 → 2.2 | none |
| RL-TX-3-007 | narrative | green | green | 168 → 174 | 11.2 → 9.2 | 2.7 → 2.2 | none |
| RL-TX-4-008 | poem | green | green | 180 → 193 | 8.2 → 7.4 | 5.0 → 2.7 | none |
| RL-TX-4-009 | narrative | green | green | 190 → 188 | 15.8 → 11.1 | 4.7 → 4.1 | none |
| RL-TX-5-010 | persuasive | yellow | green | 209 → 225 | 20.9 → 14.1 | 7.7 → 4.1 | none |
| RL-TX-6-011 | narrative | yellow | green | 263 → 296 | 21.9 → 15.6 | 8.3 → 4.7 | none |
| RL-TX-6-012 | argumentative | yellow | green | 261 → 302 | 17.4 → 15.1 | 8.8 → 4.5 | none |
| RL-TX-7-013 | informational | yellow | green | 276 → 338 | 19.7 → 16.1 | 8.6 → 6.0 | none |
| RL-TX-7-014 | argumentative | green | green | 290 → 368 | 17.1 → 16.0 | 8.0 → 7.2 | none |
| RL-TX-8-015 | narrative | yellow | green | 304 → 359 | 23.4 → 17.9 | 9.4 → 6.8 | none |
| RL-TX-E1-016 | narrative | yellow | yellow | 409 → 433 | 22.7 → 18.0 | 8.6 → 6.8 | readability estimate: FK grade 6.8 (expected 7.5 to 10.5) |
| RL-TX-E2-017 | argumentative | yellow | green | 427 → 462 | 25.1 → 19.2 | 11.9 → 9.6 | none |
| RL-TX-E3-018 | informational | yellow | green | 451 → 521 | 23.7 → 21.7 | 11.4 → 11.8 | none |
| RL-TX-E3-019 | narrative | yellow | green | 514 → 518 | 20.6 → 22.5 | 9.0 → 9.7 | none |
| RL-TX-E4-020 | argumentative | yellow | yellow | 497 → 678 | 23.7 → 24.2 | 12.5 → 10.4 | readability estimate: FK grade 10.4 (expected 10.5 to 13.5) |

## Reading the results

- **Fixed:** every length and sentence-length miss. Upper-grade drafts now reach
  their word ranges, and no average sentence runs over target.
- **New pattern:** readability moved down in every band. The two remaining
  yellows read *too easy* (E1, E4), and five more greens sit within half a grade
  of the floor. v2.0 ran too hard, and v2.1 runs slightly easy.
- **Not tested here:** generalization. The fix was designed from these briefs,
  and the writer knew the checks. A fresh brief set comes before production.
- Readability is a free Flesch-Kincaid estimate used for routing. The licensed
  Lexile analyzer remains the production gate.
