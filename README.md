# Riverlark Lesson Pipeline

**One brief in. A lesson out.** A seven-stage AI pipeline that turns one Texas reading standard (TEKS) into a reviewed, text-first video lesson. Claude drafts the passage, automated checks sort every draft into green, yellow or red, and editors make every decision.

Riverlark Learning is a fictional K-12 publisher. Texas, TEKS and STAAR are real.

**[See the full case study ↗](https://claude.ai/artifact/8cQtYZuDdt3jodLvn8Akp1)**: discovery, the seven stages, quality and governance, enablement, the evidence from two sample runs, and how it scales.

---

## Try it

| Page | What you can do there |
|---|---|
| [Case study](https://claude.ai/artifact/8cQtYZuDdt3jodLvn8Akp1) | The whole project in seven tabs |
| [Lesson Studio](https://claude.ai/artifact/7xML8iRSihrrK4vWzbYCqT) | Run one lesson through Stages 2 to 5: brief, prompt, draft, checks, editor review, lesson arc. Replay needs no sign-in; live drafting runs on your own Claude sign-in |
| [Video stage](https://claude.ai/artifact/Jrp5Xyh2dTitcADGnRmvjT) | Watch the 3:43 sample lesson, with its script, storyboard and 15 automated video checks |
| [Reviewer guide + desk card](https://claude.ai/artifact/V1DJfDBApRZKYR5bEmw3gi) | How editors work the green, yellow and red queue |
| [Onboarding + practice](https://claude.ai/artifact/DzSj4RyCXu1dxATcL7Rxhw) | Sort real sample passages into lanes and make the editor's call |
| [Rollout plan](https://claude.ai/artifact/Mn54UsCdavDtKLtTaEXMZV) | Phases, go/no-go gates, measures and a cost-per-lesson calculator |
| [Prompt change process](https://claude.ai/artifact/3yNSRnMCGus3tdPtg9aPNc) | How a prompt changes safely, with a request form and a worked example |

Backup copies of every page are in [`portfolio-static/`](portfolio-static).

---

## The seven stages

| Stage | What happens | In this repo |
|---|---|---|
| 1 · Data layer | Each TEKS standard becomes a lesson brief with its grade's targets | [`data/`](data) |
| 2 · AI generation | The renderer fills a versioned prompt; Claude drafts the passage and quotes its skill examples exactly | [`prompts/`](prompts/passage_generation), [`pipeline/render_prompt.py`](pipeline/render_prompt.py) |
| 3 · Automated checks | Six checks assign a green, yellow or red lane | [`pipeline/validate.py`](pipeline/validate.py) |
| 4 · Editor review | Editors decide every yellow and a 10% sample of green | [Reviewer guide](https://claude.ai/artifact/V1DJfDBApRZKYR5bEmw3gi) |
| 5 · Lesson script | A gradual-release script (Hook, I do, We do, You do, Recap) and a vendor-neutral storyboard | [`video/lesson_script_RL-TX-3-007.json`](video/lesson_script_RL-TX-3-007.json) |
| 6 · Video build and QA | Text-first video with captions and word highlighting, then automated checks | [`video/`](video) |
| 7 · Deploy and improve | Publish by TEKS code; send-back reasons feed the next prompt change | [Rollout plan](https://claude.ai/artifact/Mn54UsCdavDtKLtTaEXMZV) |

## What the sample runs show

Twenty lesson briefs from public TEKS, five per grade band (K-2, 3-5, 6-8, 9-12), drafted by Claude and scored by the pipeline's own checks. Every draft was saved before any check ran, and nothing was edited after scoring.

| | Prompt v2.0 | Prompt v2.1 |
|---|---|---|
| Green / yellow / red | 8 / 12 / 0 | **18 / 2 / 0** |
| Length on target | 15 of 20 | 20 of 20 |
| Sentence length on target | 14 of 20 | 20 of 20 |
| Readability estimate in range | 12 of 20 | 18 of 20 |
| Skill examples quoted exactly | 20 of 20 | 20 of 20 |
| Representation flags | 0 | 0 |

The change from v2.0 to v2.1 went through the [prompt change process](prompts/passage_generation/CHANGELOG.md): the approval bar was written before the test, then met, then approved with conditions. v2.1 overcorrected (readability now runs slightly easy), so the next change centers readability and runs on fresh holdout briefs. Full before-and-after by lesson: [`runs/comparison_v2.0_v2.1.md`](runs/comparison_v2.0_v2.1.md).

### Check the results yourself

You need Python 3.

```bash
pip install -r requirements.txt
python pipeline/validate.py data/riverlark_sample_briefs.csv runs/sample_2026-11_v2.1/outputs report.json
```

It prints each lesson's lane and writes `report.json`, which matches the saved [`validation_report.json`](runs/sample_2026-11_v2.1/validation_report.json) exactly. Swap in `runs/sample_2026-11/outputs` to check the v2.0 run.

---

## What's in this repository

| Folder | What it is |
|---|---|
| `data/` | 20 sample lesson briefs and the grade targets file |
| `prompts/passage_generation/` | Prompt v2.0 and v2.1, and the change log |
| `pipeline/` | `render_prompt.py` (Stage 2) and `validate.py` (Stage 3) |
| `runs/` | Both sample runs: every passage, every rendered prompt, the check reports and the comparison |
| `video/` | The sample lesson: script and storyboard, the video, captions, frames, the scripts that built it and its QA report. [How it was built](video/README.md) |
| `enablement/` | Source for the four enablement pages. [How to rebuild](enablement/README.md) |
| `portfolio-static/` | Backup copies of every published page |

## Good to know

- **Real:** the TEKS standards, the prompts, the checks, both sample runs and their scores, prompt change PR-2026-11-01, and the sample video and its checks.
- **Illustrative and labeled:** Riverlark and its people, the discovery conversation, editor decisions, rollout dates and bars, and cost figures.
- **Readability is an estimate.** Lexile is a licensed measure. The checks use a free Flesch-Kincaid estimate only to route passages; in production the licensed Lexile analyzer is the final gate.
- **The sample voice is a stand-in.** It sometimes says *read* in the wrong tense. The pipeline now flags words like this for the production voice, and a speech-to-text check catches anything that slips.

## About

Built by **Akeyla Peele-Tembong**, AI workflow and enablement builder.
[Case study](https://claude.ai/artifact/8cQtYZuDdt3jodLvn8Akp1) · [LinkedIn](https://www.linkedin.com/in/akeylatembong) · Also see: [Northstar Harbor Ad Review Assistant](https://github.com/aptembong/northstar-ad-review-assistant)
