import json, html, re, shutil

script = json.load(open("lesson_script_RL-TX-3-007.json"))
tl = json.load(open("timeline.json"))
qa = open("qa_report_RL-TX-3-007.md").read()
passage = json.load(open("approved_passage_RL-TX-3-007.json"))["passage_text"]
paras = passage.split("\n\n")
E = html.escape
for f in ["RL-TX-3-007_sample_lesson.mp4", "RL-TX-3-007_sample_lesson.vtt"]: shutil.copy(f, "site/" + f)

def mmss(s): return f"{int(s // 60)}:{int(s % 60):02d}"

PHASE_CLASS = {"Title": "t-title", "Hook": "t-hook", "Read aloud": "t-read", "I do": "t-ido", "We do": "t-wedo", "You do": "t-youdo", "Recap": "t-recap"}
rows = []
for sc, S in zip(script["scenes"], tl["scenes"]):
    lines = []
    for g in sc["segments"]:
        n = g["narration"]
        if n.startswith("paragraph:"):
            k = int(n.split(":")[1]); txt = f'<span class="read">Reads paragraph {k} aloud</span> <span class="muted">“{E(" ".join(paras[k-1].split()[:9]))}…”</span>'
        else: txt = E(n)
        h = g.get("highlight"); cue = ""
        if h == "word-by-word": cue = "each word highlighted as read"
        elif h == "steps-in-turn": cue = "recap cards fill in, one per sentence"
        elif isinstance(h, dict):
            if "quote" in h: cue = f'highlight “{E(h["quote"])}” · tag {E(h["tag"])}'
            elif "paragraph" in h: cue = f'show paragraph {h["paragraph"]}' + (f' · {E(h["tag"])}' if h.get("tag") else "")
            elif "choice" in h: cue = f'reveal answer {E(h["choice"])}'
        extra = []
        if g.get("pause_after"): extra.append(f'{g["pause_after"]:g} s think time' + (" with countdown" if g.get("timer") else ""))
        lines.append(f'<li>{txt}' + (f'<span class="cue">{cue}</span>' if cue else "") + "".join(f'<span class="cue pause">{x}</span>' for x in extra) + "</li>")
    os_ = sc["on_screen"]
    screen = os_.get("heading") or os_.get("show") or ""
    actual = S["end"] - S["start"]
    rows.append(f'''<tr><td><span class="phase {PHASE_CLASS[sc["phase"]]}">{E(sc["phase"])}</span><div class="muted small">{sc["id"]} · {mmss(S["start"])}</div></td>
<td class="small">{E(os_["layout"])}<div class="muted">{E(screen)}</div></td><td><ul class="narr">{"".join(lines)}</ul></td>
<td class="num">{sc["target_seconds"]} s<div class="muted">{actual:.0f} s actual</div></td></tr>''')

thumbs = []
for sc, S in zip(script["scenes"], tl["scenes"]):
    thumbs.append(f'''<figure class="thumb"><button type="button" data-seek="{S["start"] + 0.5:.1f}" aria-label="Play from {E(sc["phase"])}"><img src="frame_{sc["id"]}.jpg" alt="Storyboard frame: {E(sc["phase"])}"></button>
<figcaption><b>{sc["id"]} · {E(sc["phase"])}</b><span>{mmss(S["start"])}–{mmss(S["end"])}</span></figcaption></figure>''')

qrows = []
for line in qa.splitlines():
    m = re.match(r"\| (.+?) \| (Pass|Fail) \| (.+?) \|$", line)
    if m: qrows.append(f'<tr><td>{E(m[1])}</td><td><span class="pill {"green" if m[2]=="Pass" else "red"}"><span class="dot"></span>{m[2]}</span></td><td class="muted">{E(m[3])}</td></tr>')
npass = sum("Pass" in r for r in qrows)

s4 = json.dumps(script["scenes"][3], indent=2, ensure_ascii=False)
s4 = re.sub(r'\[\s+"Beginning",\s+"Problem",\s+"Solution",\s+"End"\s+\]', '["Beginning", "Problem", "Solution", "End"]', s4)
spec = script["render_spec"]
dur = tl["duration"]
vtt = open("RL-TX-3-007_sample_lesson.vtt").read().split("\n\n")
import base64
VTT64 = base64.b64encode(open("RL-TX-3-007_sample_lesson.vtt","rb").read()).decode()
vtt_ex = "\n\n".join(vtt[18:21])

LOGO = '''<svg viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="12" fill="#FFFFFF"/><path d="M9 34c4-3 7-3 10 0s7 3 10 0 7-3 10 0" fill="none" stroke="#5CC6D8" stroke-width="3" stroke-linecap="round"/><path d="M9 40c4-3 7-3 10 0s7 3 10 0 7-3 10 0" fill="none" stroke="#0E4D64" stroke-width="3" stroke-linecap="round"/><path d="M12 21c5-1 9 1 12 4 2-5 6-9 13-10-3 2-4 4-5 7 3 0 5 1 6 2-3 0-6 1-8 3-4 4-11 5-18-6z" fill="#0E4D64"/><circle cx="33.6" cy="18.6" r="1.1" fill="#FFFFFF"/><path d="M36.8 17.5l4-1.2-3.6 2.4z" fill="#F2765A"/></svg>'''

FLAGROWS = "".join('<tr><td>' + f["scene"] + '</td><td>' + E(f["line"]).replace("read", "<b>read</b>", 1) + '</td><td>' + E(f["say_as"]) + '</td></tr>' for f in script["pronunciation_flags"]["flags"])
page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Riverlark Video Stage</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
/* Layout idea: one lesson, top to bottom. The finished video first, then the script and storyboard that made it (Stage 5), then the checks it passed (Stage 6). Same Riverlark tokens as the case study and Studio. */
:root{{--river:#0E4D64;--sky:#5CC6D8;--coral:#F2765A;--mist:#F4F8FA;--ink:#12313D;--muted:#4E6873;--line:#D5E3E9;--card:#fff;
--sky-soft:#E3F5F8;--coral-soft:#FDECE7;--green:#2E7D4F;--green-soft:#E3F2E8;--red:#B3261E;--red-soft:#FBE4E2;
--font:"Inter",system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color-scheme:light}}
*{{box-sizing:border-box}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
body{{margin:0;background:var(--mist);color:var(--ink);font-family:var(--font);font-size:16px;line-height:1.55}}
a{{color:var(--river)}}
h1,h2,h3{{margin:0;line-height:1.2;text-wrap:balance}}
h1{{font-size:clamp(1.9rem,4vw,2.6rem);font-weight:800;letter-spacing:-.02em;color:var(--river)}}
h2{{font-size:1.5rem;font-weight:800;color:var(--river)}}
h3{{font-size:1.08rem;font-weight:700}}
p{{margin:0}}
:focus-visible{{outline:3px solid var(--coral);outline-offset:2px;border-radius:6px}}
.wrap{{max-width:1120px;margin:0 auto;padding:0 20px}}
header.top{{background:var(--river);color:#fff}}
.bar{{display:flex;align-items:center;gap:14px;padding:14px 20px;flex-wrap:wrap}}
.brand{{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none}}
.brand svg{{width:36px;height:36px}}
.wordmark{{font-weight:700;font-size:1.05rem}} .wordmark span{{font-weight:500;opacity:.85}}
.tool{{font-weight:700;padding-left:14px;border-left:1px solid rgba(255,255,255,.35)}}
.back{{margin-left:auto;color:#fff;font-weight:600;font-size:.9rem}}
main.wrap{{padding:34px 20px 64px}}
section{{margin-top:44px;display:flex;flex-direction:column;gap:16px}}
.eyebrow{{font-size:.8rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
.lede{{color:var(--muted);font-size:1.08rem;max-width:72ch}}
.muted{{color:var(--muted)}} .small{{font-size:.86rem}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px}}
.pill{{display:inline-flex;align-items:center;gap:6px;font-size:.78rem;font-weight:700;padding:3px 10px;border-radius:999px;white-space:nowrap}}
.pill.green{{background:var(--green-soft);color:var(--green)}} .pill.red{{background:var(--red-soft);color:var(--red)}}
.pill.info{{background:var(--sky-soft);color:var(--river)}} .pill.real{{background:var(--coral-soft);color:#9C3A21}}
.dot{{width:8px;height:8px;border-radius:50%;background:currentColor;display:inline-block}}
.pills{{display:flex;gap:8px;flex-wrap:wrap}}
.player{{display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:18px;align-items:start}}
@media (max-width:900px){{.player{{grid-template-columns:1fr}}}}
video{{width:100%;border-radius:16px;background:#0b2b38;display:block;aspect-ratio:16/9}}
.facts{{display:grid;gap:10px}}
.fact{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 16px}}
.fact b{{display:block;font-size:1.5rem;font-weight:800;color:var(--river)}}
.fact span{{font-size:.86rem;color:var(--muted)}}
.arc{{display:flex;flex-wrap:wrap;gap:8px;align-items:center}}
.arc .phase{{font-size:.85rem}} .arc .arr{{color:#9DB7C1}}
.phase{{display:inline-block;font-weight:700;font-size:.8rem;padding:3px 10px;border-radius:999px;background:var(--sky-soft);color:var(--river)}}
.t-title,.t-read{{background:#EEF3F5;color:var(--muted)}} .t-ido{{background:var(--river);color:#fff}} .t-wedo{{background:var(--sky);color:var(--ink)}}
.t-youdo{{background:var(--coral);color:var(--ink)}} .t-recap{{background:var(--green-soft);color:var(--green)}} .t-hook{{background:var(--coral-soft);color:#9C3A21}}
.tablewrap{{overflow-x:auto;background:#fff;border:1px solid var(--line);border-radius:16px}}
table{{border-collapse:collapse;width:100%;font-size:.94rem}}
th,td{{text-align:left;vertical-align:top;padding:12px 14px;border-bottom:1px solid var(--line)}}
th{{font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);background:#FAFCFD}}
tr:last-child td{{border-bottom:0}}
td.num{{white-space:nowrap;font-weight:700}} td.num .muted{{font-weight:500;font-size:.84rem}}
ul.narr{{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:6px}}
.cue{{display:block;font-size:.8rem;color:#9C3A21;margin-top:2px}} .cue::before{{content:"▸ "}} .cue.pause{{color:var(--river)}}
.read{{font-weight:600}}
.thumbs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}}
.thumb{{margin:0;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden}}
.thumb button{{all:unset;cursor:pointer;display:block;width:100%}}
.thumb button:focus-visible{{outline:3px solid var(--coral);outline-offset:-3px}}
.thumb img{{width:100%;display:block;aspect-ratio:16/9;object-fit:cover}}
.thumb figcaption{{display:flex;justify-content:space-between;padding:8px 12px;font-size:.84rem;color:var(--muted)}} .thumb b{{color:var(--ink)}}
.grid2{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.3fr);gap:18px}} @media (max-width:860px){{.grid2{{grid-template-columns:1fr}}}}
pre{{margin:0;background:#0F2E3A;color:#DDEFF4;border-radius:14px;padding:16px;overflow:auto;font-size:.8rem;line-height:1.5;max-height:420px}}
dl.spec{{display:grid;grid-template-columns:max-content 1fr;gap:6px 16px;margin:0;font-size:.92rem}} dl.spec dt{{font-weight:700}} dl.spec dd{{margin:0;color:var(--muted)}}
.result{{display:flex;align-items:center;gap:14px;flex-wrap:wrap}}
.big{{font-size:2rem;font-weight:800;color:var(--green)}}
.steps{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}} @media (max-width:860px){{.steps{{grid-template-columns:1fr}}}}
.step{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:6px}}
.step .who{{font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}}
ul.plain{{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:6px}}
.btn{{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-size:.95rem;padding:10px 20px;border-radius:999px;text-decoration:none;border:2px solid transparent}}
.btn.primary{{background:var(--coral);color:var(--ink)}} .btn.ghost{{color:var(--river);border-color:var(--river)}}
footer{{border-top:1px solid var(--line);margin-top:56px;padding-top:22px;display:flex;gap:12px;flex-wrap:wrap;align-items:center}}
</style>
</head>
<body>
<header class="top"><div class="wrap bar" style="padding-left:20px">
  <a class="brand" href="https://claude.ai/artifact/8cQtYZuDdt3jodLvn8Akp1" aria-label="Riverlark case study">{LOGO}<span class="wordmark">riverlark <span>learning</span></span></a>
  <span class="tool">Video stage</span>
  <a class="back" href="https://claude.ai/artifact/8cQtYZuDdt3jodLvn8Akp1#pipeline">← Back to case study</a>
</div></header>
<main class="wrap">
  <div class="stack" style="display:flex;flex-direction:column;gap:12px">
    <span class="eyebrow">Stages 5 and 6 · Lesson RL-TX-3-007</span>
    <h1>From an approved passage to a classroom video</h1>
    <p class="lede">This page follows one lesson the rest of the way: the grade 3 passage “{E(script["title"])}” (TEKS {script["teks_code"]}, plot) that passed the checks and editor review in the November sample run. Stage 5 turns it into a script and storyboard. Stage 6 builds the video and runs the automated checks.</p>
    <div class="pills"><span class="pill real">Real: built from the approved v2.1 passage</span><span class="pill info">Rendered in code here; a vendor renders in production</span></div>
  </div>

  <section aria-labelledby="h-video">
    <h2 id="h-video">The sample lesson</h2>
    <div class="player">
      <video id="vid" controls preload="metadata" poster="frame_S1.jpg">
        <source src="RL-TX-3-007_sample_lesson.mp4" type="video/mp4">
        <track kind="captions" src="data:text/vtt;base64,{VTT64}" srclang="en" label="English (sidecar)">
      </video>
      <div class="facts">
        <div class="fact"><b>{mmss(dur)}</b><span>runtime, 7 scenes</span></div>
        <div class="fact"><b>{npass} of {len(qrows)}</b><span>automated checks passed</span></div>
        <div class="fact"><b>1080p · 30 fps</b><span>text-first, no avatar</span></div>
        <div class="fact"><b>64 cues</b><span>captions burnt in, plus a WebVTT file</span></div>
      </div>
    </div>
    <p class="muted small">Captions are burnt into the picture except during the read-aloud, where the highlighted passage is the caption. The sidecar caption track repeats them for players that need a separate file.</p>
  </section>

  <section aria-labelledby="h-script">
    <span class="eyebrow">Stage 5 · AI step + editor</span>
    <h2 id="h-script">The lesson script</h2>
    <p class="lede">The script follows the same gradual-release arc as every Riverlark lesson. Each scene lists what's on screen, what the narrator says, what gets highlighted, and how long it should take. Every highlighted quote must match the approved passage exactly.</p>
    <div class="arc" aria-label="Lesson arc">
      <span class="phase t-hook">Hook</span><span class="arr">→</span><span class="phase t-read">Read aloud</span><span class="arr">→</span><span class="phase t-ido">I do</span><span class="arr">→</span><span class="phase t-wedo">We do</span><span class="arr">→</span><span class="phase t-youdo">You do</span><span class="arr">→</span><span class="phase t-recap">Recap</span>
    </div>
    <div class="tablewrap"><table>
      <thead><tr><th scope="col">Scene</th><th scope="col">On screen</th><th scope="col">Narration and cues</th><th scope="col">Time</th></tr></thead>
      <tbody>{"".join(rows)}</tbody>
    </table></div>
    <div class="card" style="display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap">
      <span class="pill green"><span class="dot"></span>Editor: Approved</span>
      <p style="flex:1;min-width:260px">{E(script["editor_review"]["notes"])} <span class="muted small">(Illustrative editor note.)</span></p>
    </div>
    <div class="card" style="display:flex;flex-direction:column;gap:12px">
      <div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:center"><h3>Pronunciation flags</h3><span class="pill info">{len(script["pronunciation_flags"]["flags"])} flagged in this lesson</span></div>
      <p class="muted">Some words are spelled the same but said two ways, like <i>read</i> (“reed” now, “red” in the past). The script step flags each one and records which is meant, and the list goes to the vendor with the storyboard.</p>
      <div class="tablewrap" style="border-radius:12px"><table>
        <thead><tr><th scope="col">Scene</th><th scope="col">Line</th><th scope="col">Say it as</th></tr></thead>
        <tbody>{FLAGROWS}</tbody>
      </table></div>
      <p class="small muted"><b>Known issue in this sample:</b> the stand-in voice didn’t use these flags, so you may hear <i>read</i> in the wrong tense. A production voice reads them from a pronunciation dictionary, and the speech-to-text check in Stage 6 catches anything that still slips.</p>
    </div>
  </section>

  <section aria-labelledby="h-board">
    <span class="eyebrow">Stage 5 output · hand-off to video</span>
    <h2 id="h-board">The storyboard</h2>
    <p class="lede">One frame per scene, taken from the finished video. Select a frame to play from that scene.</p>
    <div class="thumbs">{"".join(thumbs)}</div>
    <div class="grid2">
      <div class="card" style="display:flex;flex-direction:column;gap:12px">
        <h3>A vendor-neutral format</h3>
        <p class="muted">The storyboard is plain JSON. Any rendering vendor can work from it, and if Riverlark changes vendors, the format stays. Render settings for every lesson:</p>
        <dl class="spec">
          <dt>Resolution</dt><dd>{E(spec["resolution"])} at {spec["fps"]} fps</dd>
          <dt>Style</dt><dd>{E(spec["style"])}</dd>
          <dt>Voice</dt><dd>{E(spec["narration_voice"])}</dd>
          <dt>Highlight</dt><dd>{E(spec["word_highlight"])}</dd>
          <dt>Captions</dt><dd>{E(spec["captions"])}</dd>
          <dt>Brand</dt><dd>river blue, sky teal, sunrise coral, mist; Inter</dd>
        </dl>
      </div>
      <div style="display:flex;flex-direction:column;gap:8px">
        <h3>Scene S4 (I do), as the vendor receives it</h3>
        <pre tabindex="0" aria-label="Storyboard JSON for scene S4">{E(s4)}</pre>
      </div>
    </div>
  </section>

  <section aria-labelledby="h-checks">
    <span class="eyebrow">Stage 6 · hand-off + checks</span>
    <h2 id="h-checks">Automated video checks</h2>
    <p class="lede">These checks run on every video the vendor returns, before a person spot-checks 10% of them for pacing. A failed check sends the video back to the video team with the reason.</p>
    <div class="card" style="display:flex;gap:12px;align-items:flex-start;flex-wrap:wrap"><span class="pill info">Production only</span><p style="flex:1;min-width:260px"><b>Pronunciation check.</b> <span class="muted">Speech-to-text transcribes the finished audio and compares it with the script, word by word, using the pronunciation flags. Any mismatch goes to the person doing the 10% review. It needs the production voice, so it wasn’t run on this sample.</span></p></div>
    <div class="card result"><span class="big">{npass} of {len(qrows)} passed</span><span class="muted">Ready for the human spot-check pool.</span></div>
    <div class="tablewrap"><table>
      <thead><tr><th scope="col">Check</th><th scope="col">Result</th><th scope="col">Detail</th></tr></thead>
      <tbody>{"".join(qrows)}</tbody>
    </table></div>
    <details class="card"><summary><b>Caption file excerpt (WebVTT)</b></summary><pre style="margin-top:12px">{E(vtt_ex)}</pre></details>
  </section>

  <section aria-labelledby="h-how">
    <h2 id="h-how">How this sample was built</h2>
    <div class="steps">
      <div class="step"><span class="who">1 · Narrate</span><h3>Voice and word timing</h3><p class="muted">An open-source voice model (Kokoro) reads each sentence on its own, so every sentence's start and end time is exact. Word times inside a sentence are spread by syllable count, which is close enough for a reading highlight.</p></div>
      <div class="step"><span class="who">2 · Draw</span><h3>Frames from the storyboard</h3><p class="muted">A Python script draws each 1080p frame from the storyboard and the narration timeline, one encoded file per scene, then joins them and adds the sound with ffmpeg.</p></div>
      <div class="step"><span class="who">3 · Check</span><h3>Same checks as production</h3><p class="muted">The checks above read only the finished file, the caption file and the storyboard, so they run unchanged on a vendor's video.</p></div>
    </div>
    <div class="card"><h3 style="margin-bottom:8px">What this sample doesn't show</h3>
      <ul class="plain muted">
        <li>Pronunciation: the stand-in voice sometimes says <i>read</i> in the wrong tense. Production uses a commercial voice (ElevenLabs or the vendor’s narrator) with the pronunciation flags, and the speech-to-text check catches anything that still slips.</li>
        <li>The captions come from the narration timeline, so the same speech-to-text check also confirms the audio says what the captions say.</li>
        <li>The voice is a stand-in for the vendor's narrator, and word highlight timing is estimated within each sentence.</li>
        <li>The licensed Lexile check and the 10% human pacing review happen in production and weren't run here.</li>
      </ul>
    </div>
  </section>

  <footer>
    <a class="btn primary" href="https://claude.ai/artifact/8cQtYZuDdt3jodLvn8Akp1#pipeline">Back to the pipeline</a>
    <a class="btn ghost" href="https://claude.ai/artifact/7xML8iRSihrrK4vWzbYCqT">Open Lesson Studio</a>
    <span class="muted small">Riverlark Learning is a fictional publisher. TEKS and STAAR are real.</span>
  </footer>
</main>
<script>
const v=document.getElementById("vid");
document.querySelectorAll("[data-seek]").forEach(b=>b.addEventListener("click",()=>{{
  v.currentTime=parseFloat(b.dataset.seek); v.scrollIntoView({{behavior:"smooth",block:"center"}});
  const p=v.play(); if(p&&p.catch)p.catch(()=>{{}});
}}));
</script>
</body>
</html>'''
open("site/index.html", "w").write(page)
print("ok", len(page))
