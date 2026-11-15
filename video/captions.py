"""Stage 6: write the WebVTT sidecar from the narration timeline (one cue per sentence, two lines of 42 characters at most)."""
import json, sys, textwrap

tl = json.load(open(sys.argv[1]))
def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"
cues = []
for S in tl["scenes"]:
    for g in S["segments"]:
        for s in g["sentences"]:
            lines = textwrap.wrap(s["text"], 42)
            if len(lines) > 2:   # split long sentences into two cues at a word boundary
                words = s["words"]; mid = len(words) // 2
                for part in (words[:mid], words[mid:]):
                    txt = " ".join(w["w"] for w in part)
                    cues.append((part[0]["start"] - 0.04, part[-1]["end"] + 0.06, textwrap.wrap(txt, 42)))
            else:
                cues.append((s["start"], s["end"] + 0.25, lines))
out = ["WEBVTT", ""]
for i, (a, b, lines) in enumerate(cues, 1):
    out += [str(i), f"{ts(a)} --> {ts(b)}", *lines, ""]
open(sys.argv[2], "w").write("\n".join(out))
print(len(cues), "cues")
