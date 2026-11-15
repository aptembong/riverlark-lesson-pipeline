# Riverlark sample run · November 2026

- 20 lesson briefs (5 per grade band) built from public TEKS standards: `data/riverlark_sample_briefs.csv`
- Prompt: `prompts/passage_generation/v2.0.md`
- Passages: first drafts written by Claude (Opus 5.5) from that prompt, one per brief,
  saved before any checks ran (`generate_batch_*.py` -> `outputs/`)
- Checks: `pipeline/validate.py` (rules fixed before the run). Readability is a
  Flesch-Kincaid estimate (textstat 0.7.3), not a licensed Lexile measure.
- Results: `validation_report.json`

Result: 8 green, 12 yellow, 0 red. Skill evidence 20/20, schema 20/20,
length 15/20, sentence length 14/20, readability estimate 12/20,
representation flags 0. Misses cluster in grades 5-12: passages run short
and sentences run long.
