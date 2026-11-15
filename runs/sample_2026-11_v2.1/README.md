# Riverlark sample run · v2.1 · November 2026

Change test for PR-2026-11-01 (`prompts/passage_generation/CHANGELOG.md`).

- Briefs: the same 20 as the v2.0 run (`data/riverlark_sample_briefs.csv`)
- Prompt: `prompts/passage_generation/v2.1.md`, filled per brief by
  `pipeline/render_prompt.py` (exact messages in `prompts_rendered.jsonl`)
- Passages: fresh first drafts written by Claude (Opus 5.5) from those prompts,
  one per brief, saved before any checks ran (`generate_batch_*.py` -> `outputs/`).
  No edits after scoring.
- Checks: `pipeline/validate.py`, unchanged from the v2.0 run. Readability is a
  Flesch-Kincaid estimate (textstat 0.7.3), not a licensed Lexile measure.
- Results: `validation_report.json`. Before and after by lesson: `../comparison_v2.0_v2.1.md`

Result: 18 green, 2 yellow, 0 red (v2.0: 8 / 12 / 0). Length 20/20, sentence
length 20/20, readability estimate 18/20, skill evidence 20/20, schema 20/20,
representation flags 0. No v2.0 green regressed. Both remaining yellows are
grade 9-12 passages that read slightly too easy. v2.1 overcorrected,
so the next change centers readability instead of only passing it.
