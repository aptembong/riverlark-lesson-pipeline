# Sample video lesson: RL-TX-3-007

Grade 3 · TEKS ELA.3.8.C (plot: sequence, conflict and resolution) · "The Missing Library Book"

The approved v2.1 passage, turned into a lesson script and storyboard (Stage 5) and a 3:43 text-first video with captions and word highlighting, no avatar (Stage 6). [Watch it on the video stage page ↗](https://claude.ai/artifact/Jrp5Xyh2dTitcADGnRmvjT)

## Files

| File | What it is |
|---|---|
| `approved_passage_RL-TX-3-007.json` | The passage as approved in Stage 4 |
| `lesson_script_RL-TX-3-007.json` | Script and storyboard (format `riverlark-storyboard/1.0`): 7 scenes, render spec, editor review and pronunciation flags. This is what a rendering vendor receives |
| `RL-TX-3-007_sample_lesson.mp4` | The finished video, 1920x1080 at 30 fps |
| `RL-TX-3-007_sample_lesson.vtt` | Caption file (64 cues) |
| `frame_S1.jpg` … `frame_S7.jpg` | One storyboard frame per scene |
| `qa_report_RL-TX-3-007.md` | Video check results: 15 of 15 passed |
| `timeline.json` | Narration timing for every sentence and word |

## How it was built

In production a vendor renders the video from the storyboard. This sample was built in code to show the hand-off works end to end:

1. `narrate.py`: an open-source voice (Kokoro, voice `af_heart`) reads each sentence; word times are spread by syllable count. Needs the Kokoro model files in a `models/` folder (or set `KOKORO_MODELS`).
2. `render.py`: draws every frame from the storyboard and timeline with Pillow, then joins the scenes and adds the narration with ffmpeg. Uses the Inter font (set `INTER_FONT_DIR` if it isn't in the default place).
3. `captions.py`: writes the caption file from the timeline.
4. `video_checks.py`: the Stage 6 checks. They read only the finished file, the captions and the storyboard, so they run unchanged on a vendor's video.

To re-run the checks (needs ffmpeg):

```bash
cd video
python video_checks.py RL-TX-3-007_sample_lesson.mp4 RL-TX-3-007_sample_lesson.vtt lesson_script_RL-TX-3-007.json timeline.json approved_passage_RL-TX-3-007.json
```

`build_page.py` built the first version of the video stage page. The published page is in `portfolio-static/video-stage/`.

**Known issue:** the stand-in voice sometimes says *read* in the wrong tense. The script now flags words with two pronunciations for the production voice, and a speech-to-text check (production only) catches anything that slips.
