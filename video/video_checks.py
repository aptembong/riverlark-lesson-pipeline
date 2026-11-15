"""Stage 6 automated checks: run on every rendered lesson before the 10% human spot-check.

Checks: file integrity, resolution and frame rate, duration, audio/video sync,
caption timing and readability, and that the video says what the approved
storyboard says. Prints a Markdown report; exits 1 if any check fails.
"""
import json, re, subprocess, sys

video, vtt, script_p, tl_p, passage_p = sys.argv[1:6]
script = json.load(open(script_p)); tl = json.load(open(tl_p)); passage = json.load(open(passage_p))["passage_text"]
results = []
def check(name, ok, detail): results.append((name, ok, detail))

probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", video],
                                  capture_output=True, text=True).stdout)
v = next(s for s in probe["streams"] if s["codec_type"] == "video")
a = [s for s in probe["streams"] if s["codec_type"] == "audio"]
dec = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-f", "null", "-"], capture_output=True, text=True)
check("File integrity", dec.returncode == 0 and not dec.stderr.strip(), "decodes end to end with no errors" if not dec.stderr.strip() else dec.stderr[:200])

w, h = v["width"], v["height"]; fps = eval(v["r_frame_rate"])
check("Resolution", (w, h) == (1920, 1080), f"{w}x{h} (spec 1920x1080)")
check("Frame rate", abs(fps - 30) < 0.01, f"{fps:g} fps (spec 30)")
check("Codec", v["codec_name"] == "h264" and v.get("pix_fmt") == "yuv420p" and a and a[0]["codec_name"] == "aac",
      f"{v['codec_name']} {v.get('pix_fmt')}, audio {a[0]['codec_name'] if a else 'missing'}")

dur = float(probe["format"]["duration"]); target = sum(s["target_seconds"] for s in script["scenes"])
check("Duration", 0.75 * target <= dur <= 1.25 * target and dur <= 300, f"{dur:.1f} s against a {target} s storyboard target (within 25%, under 5 min)")
vd, ad = float(v["duration"]), float(a[0]["duration"]) if a else 0
check("Audio and video sync", abs(vd - ad) < 0.1, f"video {vd:.2f} s, audio {ad:.2f} s")

# scenes: each within 40% of its storyboard target
off = []
for sc, S in zip(script["scenes"], tl["scenes"]):
    d = S["end"] - S["start"]
    if not 0.6 * sc["target_seconds"] <= d <= 1.4 * sc["target_seconds"]: off.append(f"{sc['id']} {d:.0f}s vs {sc['target_seconds']}s")
check("Scene pacing", not off, "every scene within 40% of its target" if not off else "; ".join(off))

# captions
cues = []
for block in open(vtt).read().strip().split("\n\n")[1:]:
    ls = block.split("\n"); m = re.match(r"(\S+) --> (\S+)", ls[1])
    tsec = lambda x: sum(float(p) * 60 ** i for i, p in enumerate(reversed(x.split(":"))))
    cues.append((tsec(m[1]), tsec(m[2]), ls[2:]))
order = all(cues[i][1] <= cues[i + 1][0] + 0.001 for i in range(len(cues) - 1))
check("Caption order", order, f"{len(cues)} cues, in order, no overlaps")
lens = [c[1] - c[0] for c in cues]
check("Caption duration", min(lens) >= 0.8 and max(lens) <= 7.0, f"shortest {min(lens):.1f} s, longest {max(lens):.1f} s (0.8 to 7 s)")
lines_ok = all(len(c[2]) <= 2 and all(len(l) <= 42 for l in c[2]) for c in cues)
check("Caption lines", lines_ok, "two lines at most, 42 characters per line at most")
cps = [len(" ".join(c[2])) / (c[1] - c[0]) for c in cues]
check("Caption reading speed", max(cps) <= 20, f"fastest cue {max(cps):.1f} characters per second (limit 20)")
check("Captions cover the video", cues[-1][1] <= dur, f"last cue ends {cues[-1][1]:.1f} s, video ends {dur:.1f} s")

# content matches the approved storyboard and passage
spoken = " ".join(" ".join(c[2]) for c in cues)
norm = lambda s: re.sub(r"\s+", " ", s).strip()
missing = [p[:40] for p in passage.split("\n\n") if norm(p) not in norm(spoken)]
check("Passage read in full", not missing, "all 5 paragraphs appear word for word in the captions" if not missing else f"missing: {missing}")
quotes = [g["highlight"]["quote"] for sc in script["scenes"] for g in sc["segments"] if isinstance(g.get("highlight"), dict) and "quote" in g["highlight"]]
bad = [q for q in quotes if q not in passage]
check("Highlight quotes", not bad, f"{len(quotes)} highlighted quotes, each found exactly in the approved passage")
narr = [g["narration"] for sc in script["scenes"] for g in sc["segments"] if not g["narration"].startswith("paragraph:")]
miss = [n[:40] for n in narr if norm(n) not in norm(spoken)]
check("Narration matches script", not miss, f"{len(narr)} scripted lines, all spoken as written" if not miss else f"differs: {miss}")

passed = sum(1 for r in results if r[1])
print(f"# Stage 6 video checks: {script['lesson_id']}\n")
print(f"File: `{video.split('/')[-1]}` · {dur:.1f} s · {w}x{h} · {fps:g} fps\n")
print(f"**Result: {passed} of {len(results)} checks passed.** " + ("Ready for the 10% human spot-check pool." if passed == len(results) else "Sent back to the video team."))
print("\n| Check | Result | Detail |\n|---|---|---|")
for n, ok, d in results: print(f"| {n} | {'Pass' if ok else 'Fail'} | {d} |")
sys.exit(0 if passed == len(results) else 1)
