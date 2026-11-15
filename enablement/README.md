# Enablement pages: source

The four enablement pages are built by small Python scripts. Each writes its page into `portfolio-static/`.

| Page | Script | Live |
|---|---|---|
| Reviewer guide + desk card | `build_reviewer.py` | [open ↗](https://claude.ai/artifact/V1DJfDBApRZKYR5bEmw3gi) |
| Onboarding + practice | `build_onboarding.py` | [open ↗](https://claude.ai/artifact/DzSj4RyCXu1dxATcL7Rxhw) |
| Rollout plan | `build_rollout.py` | [open ↗](https://claude.ai/artifact/Mn54UsCdavDtKLtTaEXMZV) |
| Prompt change process | `build_change.py` | [open ↗](https://claude.ai/artifact/3yNSRnMCGus3tdPtg9aPNc) |

- `common.py`: shared Riverlark styles, header, page menu and footer
- `urls.json`: the live link for each page, used for the menu between them
- `lessons.json`: the 20 sample lessons (briefs, v2.0 and v2.1 check results, v2.1 passages), used by the practice round

To rebuild a page: `python enablement/build_reviewer.py` (no extra packages needed).

**Real:** the passages, check results, lane rules (from `pipeline/validate.py`) and PR-2026-11-01. **Illustrative and labeled:** editor decisions, rollout dates and bars, cost inputs, and the three training copies in the lane drill.
