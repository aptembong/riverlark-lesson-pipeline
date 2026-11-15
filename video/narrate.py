"""Stage 6 step 1: narrate the storyboard and build a word-level timeline.

Each sentence is synthesized on its own so sentence boundaries are exact.
Inside a sentence, word times are spread by syllable weight (plus pauses
for commas), which is close enough for a reading highlight.
"""
import json, re, sys
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

SR = 24000
VOICE, SPEED = "af_heart", 0.8
GAP_SENT, GAP_SEG, PAD_SCENE = 0.28, 0.55, 0.7

script = json.load(open(sys.argv[1]))
replay = json.load(open(sys.argv[2]))          # approved passage (Stage 4 output)
paras = [p.strip() for p in replay["passage_text"].split("\n\n")]
import os
MODELS = os.environ.get("KOKORO_MODELS", "models")  # folder with kokoro-v1.0.onnx and voices-v1.0.bin
k = Kokoro(os.path.join(MODELS, "kokoro-v1.0.onnx"), os.path.join(MODELS, "voices-v1.0.bin"))

def split_sentences(t):
    return [s for s in re.split(r"(?<=[.!?])\s+", t.strip()) if s]

def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1 and not w.endswith("le"): n -= 1
    return max(1, n)

def trim(a, thr=0.012):
    idx = np.where(np.abs(a) > thr)[0]
    if not len(idx): return a
    s, e = max(0, idx[0] - int(.03 * SR)), min(len(a), idx[-1] + int(.06 * SR))
    return a[s:e]

def word_times(sentence, t0, dur):
    words = sentence.split()
    wts = []
    for w in words:
        x = syl(w) + 0.35
        if re.search(r"[,;:]$", w): x += 0.9
        wts.append(x)
    tot = sum(wts); t = t0; out = []
    for w, x in zip(words, wts):
        d = dur * x / tot
        out.append({"w": w, "start": round(t, 3), "end": round(t + d, 3)})
        t += d
    return out

audio, t = [], 0.0
def add(a):
    global t
    audio.append(a); t += len(a) / SR
def silence(sec): add(np.zeros(int(sec * SR), dtype=np.float32))

timeline = {"lesson_id": script["lesson_id"], "scenes": []}
for sc in script["scenes"]:
    S = {"id": sc["id"], "phase": sc["phase"], "start": round(t, 3), "segments": []}
    silence(PAD_SCENE)
    for si, seg in enumerate(sc["segments"]):
        text = seg["narration"]
        para = None
        if text.startswith("paragraph:"):
            para = int(text.split(":")[1]); text = paras[para - 1]
        G = {"start": round(t, 3), "text": text, "paragraph": para, "highlight": seg.get("highlight"),
             "timer": seg.get("timer", False), "sentences": []}
        for s in split_sentences(text):
            a, sr = k.create(s, voice=VOICE, speed=(0.74 if para else SPEED), lang="en-us"); assert sr == SR
            a = trim(a.astype(np.float32))
            st = t; add(a); d = len(a) / SR
            G["sentences"].append({"text": s, "start": round(st, 3), "end": round(st + d, 3),
                                   "words": word_times(s, st + 0.04, d - 0.1)})
            silence(GAP_SENT + (0.25 if para else 0))
        G["speech_end"] = round(t, 3)
        if seg.get("pause_after"): silence(seg["pause_after"])
        silence(GAP_SEG)
        G["end"] = round(t, 3)
        S["segments"].append(G)
    silence(PAD_SCENE * 0.6)
    S["end"] = round(t, 3)
    timeline["scenes"].append(S)
    print(sc["id"], sc["phase"], "target", sc["target_seconds"], "actual", round(S["end"] - S["start"], 1))

full = np.concatenate(audio)
peak = np.max(np.abs(full)); full = full / peak * 0.89
sf.write("narration.wav", full, SR)
timeline["duration"] = round(t, 3)
json.dump(timeline, open("timeline.json", "w"), indent=1)
print("total", round(t, 1))
