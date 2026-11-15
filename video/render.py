"""Stage 6 step 2: draw the storyboard to video (stand-in for the rendering vendor).

Reads the storyboard and the narration timeline, draws 1920x1080 frames at
30 fps with Pillow, encodes one file per scene, then joins them and adds the
narration. Text-first: no avatar; captions are burnt in, and passage words
are highlighted as they are read.
"""
import json, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
RIVER, SKY, CORAL, MIST, INK, MUTED, LINE = "#0E4D64", "#5CC6D8", "#F2765A", "#F4F8FA", "#12313D", "#4E6873", "#D5E3E9"
SKY_SOFT, CORAL_SOFT, GREEN, GREEN_SOFT = "#E3F5F8", "#FDECE7", "#2E7D4F", "#E3F2E8"
WORD_HI = "#A9E2EB"
TAG = {"Beginning": (RIVER, SKY_SOFT), "Problem": ("#B4462B", CORAL_SOFT), "Solution": (GREEN, GREEN_SOFT),
       "End": (RIVER, "#DCE9EE"), "Look here": (MUTED, "#EEF3F5")}
FD = os.path.join(os.environ.get("INTER_FONT_DIR", "/usr/share/fonts/opentype/inter"), "")  # folder with Inter-*.otf
_fc = {}
def F(size, w="Regular"):
    k = (size, w)
    if k not in _fc: _fc[k] = ImageFont.truetype(FD + f"Inter-{w}.otf", size)
    return _fc[k]

script = json.load(open(sys.argv[1]))
tl = json.load(open(sys.argv[2]))
passage = json.load(open(sys.argv[3]))["passage_text"]
PARAS = [p.strip() for p in passage.split("\n\n")]
ONLY = sys.argv[4].split(",") if len(sys.argv) > 4 and sys.argv[4] != "all" else None
STILLS = sys.argv[5].split(",") if len(sys.argv) > 5 else None
LOGO = Image.open("logo.png").convert("RGBA").resize((64, 64), Image.LANCZOS)
PHASES = ["Hook", "Read aloud", "I do", "We do", "You do", "Recap"]
TRACK = ["Beginning", "Problem", "Solution", "End"]

def tw(d, s, f): return d.textlength(s, font=f)

# ---------- chrome ----------
def base(phase):
    im = Image.new("RGB", (W, H), MIST); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 112], fill=RIVER)
    im.paste(LOGO, (72, 24), LOGO)
    d.text((152, 56), "riverlark", font=F(34, "Bold"), fill="white", anchor="lm")
    x = 152 + tw(d, "riverlark ", F(34, "Bold"))
    d.text((x, 56), "learning", font=F(34, "Medium"), fill="#CFE6EE", anchor="lm")
    # gradual-release stepper
    f = F(24, "SemiBold"); x = W - 72
    cur = PHASES.index(phase) if phase in PHASES else -1
    for i in range(len(PHASES) - 1, -1, -1):
        p = PHASES[i]; w = tw(d, p, f) + 40; x0 = x - w
        if i == cur:   d.rounded_rectangle([x0, 34, x, 78], 22, fill=CORAL); col = INK
        elif i < cur:  d.rounded_rectangle([x0, 34, x, 78], 22, fill="#2C6A80"); col = "white"
        else:          d.rounded_rectangle([x0, 34, x, 78], 22, outline="#4D8397", width=2); col = "#A9CBD6"
        d.text(((x0 + x) / 2, 56), p, font=f, fill=col, anchor="mm"); x = x0 - 12
    return im

def caption(d, text):
    if not text: return
    f = F(40, "Medium"); maxw = 1600
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if tw(d, t, f) > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    lines.append(cur)
    lh = 56; h = lh * len(lines) + 40; y0 = 1040 - h
    bw = max(tw(d, l, f) for l in lines) + 80
    d.rounded_rectangle([(W - bw) / 2, y0, (W + bw) / 2, 1040], 24, fill="#12313D")
    for i, l in enumerate(lines):
        d.text((W / 2, y0 + 20 + lh * i + lh / 2), l, font=f, fill="white", anchor="mm")

def tracker(d, found, current=None, y=150):
    f = F(30, "Bold"); gap = 24; ws = [tw(d, t, f) + 64 for t in TRACK]
    arrow = 34; total = sum(ws) + (gap * 2 + arrow) * 3; x = (W - total) / 2
    for i, t in enumerate(TRACK):
        x1 = x + ws[i]
        if t == current:  d.rounded_rectangle([x, y, x1, y + 64], 32, fill=CORAL); c = INK
        elif t in found:  d.rounded_rectangle([x, y, x1, y + 64], 32, fill=RIVER); c = "white"
        else:             d.rounded_rectangle([x, y, x1, y + 64], 32, outline=LINE, width=3, fill="white"); c = MUTED
        d.text(((x + x1) / 2, y + 32), t, font=f, fill=c, anchor="mm")
        x = x1
        if i < 3:
            ax = x + gap; d.polygon([(ax, y + 22), (ax + arrow, y + 32), (ax, y + 42)], fill="#9DB7C1"); x = ax + arrow + gap

def ring(d, cx, cy, frac, n):
    r = 54
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=LINE, width=10)
    if frac > 0: d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * frac, fill=CORAL, width=10)
    d.text((cx, cy), str(n), font=F(46, "Bold"), fill=INK, anchor="mm")

# ---------- paragraph layout with word boxes ----------
def layout(text, f, maxw, lh):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    sp = tw(d, " ", f); x = y = 0; out = []
    for w in text.split():
        ww = tw(d, w, f)
        if x and x + ww > maxw: x = 0; y += lh
        out.append([w, x, y, ww]); x += ww + sp
    return out, y + lh

def quote_range(words, quote):
    q = quote.split(); n = len(q); ws = [w[0] for w in words]
    for i in range(len(ws) - n + 1):
        if ws[i:i + n] == q: return range(i, i + n)
    raise ValueError("quote not found: " + quote)

def draw_para(im, text, top, size=56, current=None, hi=None, hi_tag=None, card=True, label=None):
    """current: index of word being read. hi: range of word indexes to mark with hi_tag colors."""
    d = ImageDraw.Draw(im); f = F(size, "Medium"); lh = int(size * 1.62)
    maxw = 1520; words, th = layout(text, f, maxw, lh)
    x0 = (W - maxw) / 2; pad = 56
    y0 = top
    if card:
        d.rounded_rectangle([x0 - pad, y0 - pad + 10, x0 + maxw + pad, y0 + th + pad - 10], 28, fill="white", outline=LINE, width=2)
    if label:
        lf = F(26, "SemiBold"); d.text((x0 - pad + 4, y0 - pad - 30), label, font=lf, fill=MUTED, anchor="ls")
    fg, bg = TAG.get(hi_tag, (RIVER, CORAL_SOFT))
    if hi:
        rows = {}
        for i in hi:
            w, x, y, ww = words[i]; rows.setdefault(y, [x, x + ww]); rows[y][1] = x + ww
        for y, (a, b) in rows.items():
            d.rounded_rectangle([x0 + a - 12, y0 + y + 4, x0 + b + 12, y0 + y + lh - 8], 14, fill=bg)
            d.rectangle([x0 + a - 4, y0 + y + lh - 14, x0 + b + 4, y0 + y + lh - 9], fill=fg)
    for i, (w, x, y, ww) in enumerate(words):
        if i == current:
            d.rounded_rectangle([x0 + x - 10, y0 + y + 8, x0 + x + ww + 10, y0 + y + lh - 12], 14, fill=WORD_HI)
        d.text((x0 + x, y0 + y + lh / 2), w, font=f, fill=INK, anchor="lm")
    if hi and hi_tag:
        cf = F(26, "Bold"); cw = tw(d, hi_tag, cf) + 36
        lx = x0 - pad + 4 + (tw(d, label, F(26, "SemiBold")) + 18 if label else 0)
        cy = y0 - pad - 58
        d.rounded_rectangle([lx, cy, lx + cw, cy + 40], 20, fill=fg)
        d.text((lx + cw / 2, cy + 20), hi_tag, font=cf, fill="white", anchor="mm")
    return y0 + th

# ---------- timeline lookups ----------
def seg_at(S, t):
    for i, g in enumerate(S["segments"]):
        if t < g["end"]: return i, g
    return len(S["segments"]) - 1, S["segments"][-1]

def sentence_at(g, t):
    ss = g["sentences"]
    for i, s in enumerate(ss):
        nxt = ss[i + 1]["start"] if i + 1 < len(ss) else g["speech_end"] + 0.25
        if s["start"] - 0.05 <= t < nxt: return i, s
    return None, None

def word_at(g, t):
    k = 0
    for s in g["sentences"]:
        for w in s["words"]:
            if w["start"] <= t < w["end"] + 0.12: return k
            k += 1
    return None

def find_para(quote):
    for i, p in enumerate(PARAS):
        if quote in p: return i
    raise ValueError(quote)

# ---------- scene drawing ----------
def draw_scene(sc, S, t):
    """Return (key, draw_fn). key identifies the visual state so identical frames are reused."""
    phase = sc["phase"]; os_ = sc["on_screen"]
    gi, g = seg_at(S, t); si, s = sentence_at(g, t)
    cap = s["text"] if s else None
    hl = g.get("highlight")
    timer = None
    if g.get("timer") and t >= g["speech_end"]:
        left = g["end"] - 0.55 - t
        if left > 0: timer = (round(left * 10) / 10, int(left) + 1)

    if phase == "Title":
        key = ("T", cap)
        def fn(im, d):
            d.text((W / 2, 400), os_["heading"], font=F(104, "ExtraBold"), fill=RIVER, anchor="mm")
            d.text((W / 2, 500), os_["subheading"], font=F(40, "Medium"), fill=MUTED, anchor="mm")
            chip = f"TEKS {script['teks_code']}  ·  Grade {script['grade']}"
            cf = F(28, "SemiBold"); cw = tw(d, chip, cf) + 48
            d.rounded_rectangle([(W - cw) / 2, 572, (W + cw) / 2, 620], 24, fill=SKY_SOFT)
            d.text((W / 2, 596), chip, font=cf, fill=RIVER, anchor="mm")
            for k, col in enumerate([SKY, RIVER]):
                y = 700 + k * 26; pts = []
                for x in range(560, 1361, 8):
                    import math; pts.append((x, y + 12 * math.sin((x - 560) / 80 * math.pi)))
                d.line(pts, fill=col, width=9, joint="curve")
            caption(d, cap)
        return key, fn

    if phase == "Hook":
        key = ("H", cap, gi >= 1)
        def fn(im, d):
            d.text((W / 2, 400), os_["heading"], font=F(84, "ExtraBold"), fill=RIVER, anchor="mm")
            if gi >= 1:
                pf = F(40, "SemiBold"); pw = tw(d, os_["prompt"], pf) + 64
                d.rounded_rectangle([(W - pw) / 2, 500, (W + pw) / 2, 572], 36, fill=CORAL_SOFT)
                d.text((W / 2, 536), os_["prompt"], font=pf, fill="#9C3A21", anchor="mm")
            caption(d, cap)
        return key, fn

    if phase == "Read aloud":
        p = g["paragraph"]; cw = word_at(g, t)
        key = ("R", p, cw)
        def fn(im, d):
            lbl = f"Paragraph {p} of {len(PARAS)}"
            d.text((W / 2, 178), "Read along with me", font=F(44, "Bold"), fill=RIVER, anchor="mm")
            text = PARAS[p - 1]
            f = F(58, "Medium"); _, th = layout(text, f, 1520, int(58 * 1.62))
            top = 260 + max(0, (640 - th) / 2)
            draw_para(im, text, top, 58, current=cw, label=lbl)
        return key, fn

    # I do / We do / You do / Recap share the plot tracker
    found = []
    for j, sg in enumerate(S["segments"]):
        h = sg.get("highlight")
        if isinstance(h, dict) and h.get("tag") in TRACK and j <= gi:
            if j < gi or t >= sg["sentences"][0]["start"]: found.append(h["tag"])
    prior = {"I do": [], "We do": ["Beginning", "Problem"], "You do": TRACK, "Recap": TRACK}[phase]
    found = list(dict.fromkeys(prior + found))
    current = hl.get("tag") if isinstance(hl, dict) and hl.get("tag") in TRACK else None

    if phase in ("I do", "We do"):
        heading = os_["heading"]
        prompt = os_.get("prompt") if phase == "We do" else None
        key = (phase, gi, cap, tuple(found), current, timer[1] if timer else None, timer[0] if timer else None)
        def fn(im, d):
            tracker(d, found, current)
            d.text((W / 2, 290), heading, font=F(52, "ExtraBold"), fill=RIVER, anchor="mm")
            if prompt and gi == 0:
                d.text((W / 2, 356), prompt, font=F(36, "SemiBold"), fill="#9C3A21", anchor="mm")
            if isinstance(hl, dict) and ("quote" in hl or "paragraph" in hl):
                if "quote" in hl:
                    pi = find_para(hl["quote"]); text = PARAS[pi]
                    words, _ = layout(text, F(50, "Medium"), 1520, 81)
                    rng = quote_range(words, hl["quote"]); tag = hl["tag"]
                    show_hi = t >= g["sentences"][0]["start"] - 0.05
                else:
                    pi = hl["paragraph"] - 1; text = PARAS[pi]; rng = None; tag = None; show_hi = False
                draw_para(im, text, 470, 50, hi=rng if show_hi else None, hi_tag=tag if show_hi else None,
                          label=f"Paragraph {pi + 1}")
            if timer: ring(d, W - 200, 300, timer[0] / 5.0, timer[1])
            caption(d, cap)
        return key, fn

    if phase == "You do":
        reveal = isinstance(hl, dict) and hl.get("choice")
        key = ("Y", gi, cap, timer[1] if timer else None, timer[0] if timer else None)
        def fn(im, d):
            d.text((W / 2, 200), os_["heading"].upper(), font=F(30, "Bold"), fill=MUTED, anchor="mm")
            d.text((W / 2, 280), os_["question"], font=F(72, "ExtraBold"), fill=RIVER, anchor="mm")
            cw, ch, gx, gy = 700, 150, 40, 36; x0 = (W - 2 * cw - gx) / 2; y0 = 390
            for i, c in enumerate(os_["choices"]):
                x = x0 + (i % 2) * (cw + gx); y = y0 + (i // 2) * (ch + gy)
                ok = reveal and c["key"] == os_["answer"]; dim = reveal and not ok
                d.rounded_rectangle([x, y, x + cw, y + ch], 28, fill=GREEN_SOFT if ok else "white",
                                    outline=GREEN if ok else LINE, width=5 if ok else 3)
                kc = GREEN if ok else (LINE if dim else RIVER)
                d.ellipse([x + 36, y + 39, x + 108, y + 111], fill=kc)
                d.text((x + 72, y + 75), c["key"], font=F(36, "Bold"), fill="white", anchor="mm")
                d.text((x + 140, y + 75), c["text"], font=F(46, "SemiBold"), fill="#9DB0B8" if dim else INK, anchor="lm")
                if ok:
                    d.line([(x + cw - 100, y + 78), (x + cw - 80, y + 98), (x + cw - 44, y + 54)], fill=GREEN, width=10, joint="curve")
            if timer: ring(d, W - 200, 280, timer[0] / 5.0, timer[1])
            caption(d, cap)
        return key, fn

    if phase == "Recap":
        steps = os_["steps"]
        if gi == 0: shown = 0
        elif gi == 1: shown = (si + 1) if si is not None else 4
        else: shown = 4
        key = ("C", gi, cap, shown)
        def fn(im, d):
            d.text((W / 2, 210), os_["heading"], font=F(56, "ExtraBold"), fill=RIVER, anchor="mm")
            cw, gap = 380, 36; x0 = (W - 4 * cw - 3 * gap) / 2; y = 330
            for i, stp in enumerate(steps):
                x = x0 + i * (cw + gap); on = i < shown or gi == 0
                fg, bg = TAG[stp["tag"]]
                d.rounded_rectangle([x, y, x + cw, y + 420], 30, fill="white" if on else "#EEF3F5",
                                    outline=fg if (gi >= 1 and i < shown) else LINE, width=4 if (gi >= 1 and i < shown) else 2)
                d.rounded_rectangle([x + 30, y + 34, x + 30 + tw(d, stp["tag"], F(30, "Bold")) + 44, y + 90], 28, fill=fg if on else LINE)
                d.text((x + 52, y + 62), stp["tag"], font=F(30, "Bold"), fill="white", anchor="lm")
                d.text((x + 30, y + 130), str(i + 1), font=F(84, "ExtraBold"), fill=bg if on else "#E1E9ED", anchor="lt")
                if gi >= 1 and i < shown:
                    words, yy, lines, cur = stp["text"].split(), y + 250, [], ""
                    for w_ in words:
                        tt = (cur + " " + w_).strip()
                        if tw(d, tt, F(38, "SemiBold")) > cw - 60 and cur: lines.append(cur); cur = w_
                        else: cur = tt
                    lines.append(cur)
                    for k, l in enumerate(lines): d.text((x + 30, yy + k * 52), l, font=F(38, "SemiBold"), fill=INK, anchor="lt")
            caption(d, cap)
        return key, fn
    raise ValueError(phase)

def frame(sc, S, t, cache):
    key, fn = draw_scene(sc, S, t)
    if key not in cache:
        im = base(sc["phase"]); fn(im, ImageDraw.Draw(im)); cache.clear(); cache[key] = im
    return cache[key]

FADE = 0.35
os.makedirs("scenes", exist_ok=True)
files = []
for sc, S in zip(script["scenes"], tl["scenes"]):
    fname = f"scenes/{sc['id']}.mp4"; files.append(fname)
    if ONLY and sc["id"] not in ONLY: continue
    f0, f1 = round(S["start"] * FPS), round(S["end"] * FPS)
    if STILLS:
        for ts in STILLS:
            sid, tt = ts.split("@")
            if sid == sc["id"]:
                frame(sc, S, S["start"] + float(tt), {}).save(f"still_{sid}_{tt}.png")
        continue
    tmp = fname.replace(".mp4", ".part.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                          "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    cache, bg = {}, base(sc["phase"]); last_key, buf = None, None
    for fi in range(f0, f1):
        t = fi / FPS; im = frame(sc, S, t, cache)
        a = (t - S["start"]) / FADE
        if a < 1: p.stdin.write(Image.blend(bg, im, max(0, a)).tobytes()); continue
        k = id(im)
        if k != last_key: buf = im.tobytes(); last_key = k
        p.stdin.write(buf)
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, fname); print("rendered", fname, f1 - f0, "frames")
    else: sys.exit("ffmpeg failed on " + fname)

if not STILLS and not ONLY:
    open("scenes/list.txt", "w").write("".join(f"file '{os.path.basename(f)}'\n" for f in files))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "scenes/list.txt",
                    "-c", "copy", "video_only.mp4"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "video_only.mp4", "-i", "narration.wav", "-map", "0:v",
                    "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
                    f"{script['lesson_id']}_sample_lesson.part.mp4"], check=True)
    os.replace(f"{script['lesson_id']}_sample_lesson.part.mp4", f"{script['lesson_id']}_sample_lesson.mp4")
    print("done")
