import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import *

L = {x["brief"]["lesson_id"]: x for x in json.load(open(os.path.join(HERE, "lessons.json")))}

def checks_rows(brief, r, flags=None, notfound=0):
    """Rows: [label, ok, result, target] from a real validator report."""
    poem = brief["text_type"] == "poem"
    rows = [
        ["Schema", True, "All fields and lesson hooks present", "All fields, 4 hooks"],
        ["Length", r["words_ok"], f'{r["words"]} words', f'{brief["words_min"]}-{brief["words_max"]} (±10)'],
        ["Average sentence", r["sentence_ok"], f'{r["avg_sentence_len"]} words', f'{brief["sentence_len_min"]}-{brief["sentence_len_max"]} (±2)'],
        ["Skill evidence", r["instances_ok"] and not notfound,
         f'{r["instances"]} examples, ' + (f"{notfound} not found exactly" if notfound else "all found exactly"),
         f'{brief["instances_min"]}-{brief["instances_max"]}, quoted exactly'],
        ["Readability estimate", r["readability_ok"], f'FK grade {r["fk_grade"]}', None],
        ["Representation flags", not flags, flags or "None", "No red- or yellow-list words"],
    ]
    return rows

DRILL = []
def real(lid, run="v20"):
    x = L[lid]; b = x["brief"]; r = x[run]
    rows = checks_rows(b, r)
    rows[4][3] = f'{x["fk_range"][0]} to {x["fk_range"][1]}'
    return {"id": lid, "title": r["title"], "grade": b["grade"], "skill": b["skill"], "rows": rows, "lane": r["lane"],
            "source": f"Real: prompt {run.replace('v2','v2.')} result from the November sample run", "real": True}

d = real("RL-TX-1-003"); d["why"] = "Every check passed, so it's green. A random 10% of greens still reach an editor."; DRILL.append(d)
d = real("RL-TX-2-005"); d["why"] = "One fit issue (readability ran a little hard) makes it yellow. An editor reads it in full and runs Lexile."; DRILL.append(d)
d = real("RL-TX-E2-017"); d["why"] = "Three fit issues, and it's still yellow. Length, sentence length and readability never make a passage red, however many miss. Red is only for flagged words, a broken schema or a misquoted example."; DRILL.append(d)

def variation(lid, why, flags=None, notfound=0, lane="red", note=""):
    x = L[lid]; b = x["brief"]; r = x["v21"]
    rows = checks_rows(b, r, flags=flags, notfound=notfound)
    rows[4][3] = f'{x["fk_range"][0]} to {x["fk_range"][1]}'
    return {"id": lid + "-T", "title": r["title"] + " (training copy)", "grade": b["grade"], "skill": b["skill"], "rows": rows,
            "lane": lane, "why": why, "source": "Training variation: real v2.1 numbers with one change made for practice. " + note, "real": False}

DRILL.append(variation("RL-TX-5-010", "One red-list word sends a passage red, even when everything else passes. It never reaches review: it's redrafted.",
    flags="Red list: “disadvantaged” (deficit framing)", note="One sentence was changed to include a red-list word."))
DRILL.append(variation("RL-TX-4-009", "A skill example that isn't in the passage word for word is red. Exact quotes are how the lesson script and video highlight the right sentence.",
    notfound=1, note="One skill example was reworded so it no longer matches the passage."))
DRILL.append(variation("RL-TX-7-013", "One or two yellow-list words make it yellow, so an editor reads the sentence in context. Three or more would make it red.",
    flags="Yellow list: “underprivileged” (deficit framing, moderate)", lane="yellow", note="One sentence was changed to include a yellow-list word."))
d = real("RL-TX-E1-016"); d["why"] = "Average sentence length ran over the band's range, which is a fit issue, so it's yellow. (Prompt v2.1 fixed this one.)"; DRILL.append(d)

EDITOR = {
 "RL-TX-K-001": {"decision": "Approve", "note": "Mia fixes the problem herself by tugging the string slowly. Three short examples cover the problem, the attempt and the solution. Spot-check passed.",
   "notice": "In kindergarten stories, agency is easy to check: who solves the problem? Here it's Mia, not an adult."},
 "RL-TX-3-007": {"decision": "Approve", "note": "Clear sequence, conflict and resolution for grade 3. Rosa solves her own problem. Spot-check passed.",
   "notice": "This is the passage that went on to become the sample video lesson."},
 "RL-TX-6-012": {"decision": "Approve", "note": "All five examples point to the same audience, new sixth graders, and the paragraph about being too busy answers a worry this audience really has. The estimate sits exactly on the grade 6 floor, so the Lexile check decides. Logged for the readability change.",
   "notice": "Green isn't the same as centered. FK 4.5 is the very bottom of the grade 6 range. This is the pattern the next prompt change is aimed at."},
 "RL-TX-E1-016": {"decision": "Approve with notes", "note": "Strong theme and setting work, and Teresa makes her own choice. Readability estimate is just under the grade 9 floor, so raise a few word choices to grade level in paragraphs 1 and 2, then confirm with the licensed Lexile check before video.",
   "notice": "The miss is small and the teaching is strong, so a redraft would throw away good work. Notes, then Lexile."},
 "RL-TX-E4-020": {"decision": "Approve with notes", "note": "Thesis, ethos, logos, pathos and the call to action are all clear and quoted exactly. The estimate is 0.1 under the grade 12 floor. Sharpen word choice in paragraphs 3 and 4 rather than lengthening sentences, which are already on target, then confirm with Lexile.",
   "notice": "The word lists didn't flag “the families least able to absorb them,” and an editor should still read it closely. Here it's about who carries a cost, not a judgment about who those families are, so it passes. That's a call only a person can make."},
}

CASES = []
for lid in ["RL-TX-K-001", "RL-TX-3-007", "RL-TX-6-012", "RL-TX-E1-016", "RL-TX-E4-020"]:
    x = L[lid]; b = x["brief"]; r = x["v21"]; p = x["passage"]
    rows = checks_rows(b, r); rows[4][3] = f'{x["fk_range"][0]} to {x["fk_range"][1]}'
    why = {"green": "Every check passed, so it's green." , "yellow": "; ".join(r["issues"]) + ". That's a fit issue, so it's yellow."}[r["lane"]]
    CASES.append({"id": lid, "grade": b["grade"], "teks": b["teks_code"], "skill": b["skill"], "type": b["text_type"], "title": p["title"],
                  "text": p["passage_text"], "quotes": [i["quote"] for i in p["skill_instances"]],
                  "rows": rows, "lane": r["lane"], "why": why, "lexile": f'{b["lexile_min"]}L-{b["lexile_max"]}L', **EDITOR[lid]})

EXTRA = r"""
.stages{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:10px}
@media (max-width:980px){.stages{grid-template-columns:repeat(2,minmax(0,1fr))}}
.stg{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px;display:flex;flex-direction:column;gap:6px;border-top:5px solid var(--sky)}
.stg.auto{border-top-color:var(--river)}.stg.human{border-top-color:var(--green)}.stg.hand{border-top-color:#6B7C85}
.stg .n{font-size:.78rem;font-weight:800;color:var(--muted)}
.stg p{font-size:.86rem;color:var(--muted)}
.key{display:flex;gap:14px;flex-wrap:wrap;font-size:.84rem;color:var(--muted)}
.key i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:5px;vertical-align:-1px}
dl.brief{display:grid;grid-template-columns:max-content 1fr;gap:6px 16px;margin:0;font-size:.92rem}dl.brief dt{font-weight:700}dl.brief dd{margin:0;color:var(--muted)}
.drill{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
@media (max-width:760px){.drill{grid-template-columns:1fr}}
.dcard{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px;display:flex;flex-direction:column;gap:10px}
.dcard table{font-size:.86rem}.dcard th,.dcard td{padding:6px 9px}
.ok{color:var(--green);font-weight:700}.miss{color:var(--red);font-weight:700}
.choose{display:flex;gap:8px;flex-wrap:wrap}
.choose button{font:inherit;font-weight:700;font-size:.9rem;padding:8px 16px;border-radius:999px;border:2px solid var(--line);background:#fff;color:var(--ink);cursor:pointer}
.choose button[aria-pressed="true"]{border-color:var(--river);background:var(--river);color:#fff}
.choose button:disabled{cursor:default}
.choose button.right{border-color:var(--green)}.choose button.wrong[aria-pressed="true"]{background:var(--red);border-color:var(--red)}
.fb{border-radius:12px;padding:10px 12px;font-size:.92rem}
.fb.good{background:var(--green-soft)}.fb.bad{background:var(--yellow-soft)}
.src{font-size:.78rem;color:var(--muted)}
.case{background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px;display:flex;flex-direction:column;gap:14px}
.case .head{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:baseline}
.passage{background:#FAFCFD;border:1px solid var(--line);border-radius:12px;padding:14px 16px;max-height:340px;overflow:auto;font-size:.96rem;display:flex;flex-direction:column;gap:10px}
mark{background:#D8F0F5;border-bottom:2px solid var(--sky);padding:0 2px;border-radius:3px;color:inherit}
.steplabel{font-size:.78rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--river)}
.checks{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 16px;font-size:.92rem}
@media (max-width:640px){.checks{grid-template-columns:1fr}}
.checks label{display:flex;gap:8px;align-items:flex-start}
.locked{opacity:.5;pointer-events:none}
.score{display:flex;gap:14px;flex-wrap:wrap}
.score div{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 18px}
.score b{display:block;font-size:1.6rem;font-weight:800;color:var(--river)}
.casenav{display:flex;gap:8px;flex-wrap:wrap}
.casenav button{font:inherit;font-weight:700;font-size:.86rem;padding:7px 14px;border-radius:999px;border:1px solid var(--line);background:#fff;cursor:pointer;color:var(--ink)}
.casenav button[aria-current="true"]{background:var(--river);color:#fff;border-color:var(--river)}
.casenav button.done::after{content:" ✓";color:var(--green)}
.casenav button[aria-current="true"].done::after{color:#BDEBD0}
"""

STAGES = [
 ("auto", "1", "Data layer", "Each TEKS standard becomes a brief with its grade's targets."),
 ("ai", "2", "AI generation", "Claude drafts the passage and quotes its skill examples."),
 ("auto", "3", "Automated checks", "Six checks sort the draft green, yellow or red."),
 ("human", "4", "Editor review", "Editors decide every yellow and a 10% sample of green."),
 ("ai", "5", "Lesson script", "The approved passage becomes a gradual-release script. Editors review it."),
 ("hand", "6", "Video build and QA", "A vendor renders the video. Automated checks, then a 10% spot-check."),
 ("auto", "7", "Deploy and improve", "Publish by TEKS code. Send-back reasons feed the next prompt change."),
]

def guide_view():
    b = L["RL-TX-3-007"]["brief"]
    stg = "".join(f'<div class="stg {c}"><span class="n">STAGE {n}</span><h4>{t}</h4><p>{d}</p></div>' for c,n,t,d in STAGES)
    return f"""
<div class="view" id="guide">
  <section class="blk" aria-labelledby="h-min" style="margin-top:28px">
    <h2 id="h-min">The pipeline in one minute</h2>
    <p class="lede">One brief goes in, one reviewed video lesson comes out. Claude drafts, scripts check, and people make every decision.</p>
    <div class="stages">{stg}</div>
    <div class="key"><span><i style="background:var(--sky)"></i>AI step</span><span><i style="background:var(--river)"></i>Automated</span><span><i style="background:var(--green)"></i>People decide</span><span><i style="background:#6B7C85"></i>Vendor hand-off</span></div>
  </section>

  <section class="blk" aria-labelledby="h-roles">
    <h2 id="h-roles">Where you come in</h2>
    <div class="grid2">
      <div class="card stack"><span class="pill info">Writers</span><h3>You make the fixes and shape the scripts</h3>
        <ul class="plain muted"><li>Revise a passage after an editor's “Approve with notes,” then send it back through the checks.</li><li>Tighten lesson scripts in Stage 5 so the I do, We do and You do steps teach the same skill.</li><li>Tell the Managing Editor when the same fix keeps coming up. That's how prompt changes start.</li></ul></div>
      <div class="card stack"><span class="pill green">Editors</span><h3>You decide</h3>
        <ul class="plain muted"><li>Review every yellow and a random 10% of greens, using the rubric.</li><li>Approve, approve with notes, regenerate, or reject. Every decision but Approve needs a note.</li><li>Review every lesson script before video.</li></ul>
        <p class="small"><a href="{url('reviewer')}">Read the reviewer guide →</a></p></div>
    </div>
  </section>

  <section class="blk" aria-labelledby="h-brief">
    <h2 id="h-brief">What's in a brief</h2>
    <p class="lede">Every draft starts from a brief. The targets come from the grade targets file, so two lessons for the same grade get the same bar.</p>
    <div class="card"><dl class="brief">
      <dt>Lesson ID</dt><dd>{b['lesson_id']}</dd>
      <dt>Grade and TEKS</dt><dd>Grade {b['grade']} · {b['teks_code']}: {b['standard']}</dd>
      <dt>Skill</dt><dd>{b['skill']}</dd>
      <dt>Text type</dt><dd>{b['text_type']}</dd>
      <dt>Length</dt><dd>{b['words_min']}-{b['words_max']} words</dd>
      <dt>Sentences</dt><dd>{b['sentence_len_min']}-{b['sentence_len_max']} words on average</dd>
      <dt>Skill examples</dt><dd>{b['instances_min']}-{b['instances_max']}, each quoted exactly from the passage</dd>
      <dt>Lexile</dt><dd>{b['lexile_min']}L-{b['lexile_max']}L, checked by the licensed analyzer</dd>
    </dl><p class="small muted" style="margin-top:10px">A real brief from the November sample run. Its passage became the <a href="{VIDEO}">sample video lesson</a>.</p></div>
  </section>

  <section class="blk" aria-labelledby="h-fix">
    <h2 id="h-fix">Fixing a yellow</h2>
    <p class="lede">Most yellows are routine. Fix the cause, not the number.</p>
    <div class="tablewrap"><table>
      <thead><tr><th scope="col">The check says</th><th scope="col">Usually because</th><th scope="col">Fix it by</th><th scope="col">Don't</th></tr></thead>
      <tbody>
        <tr><td><b>Too short</b></td><td>The passage ends before the skill has room</td><td>Adding a paragraph that carries another skill example</td><td>Pad with description</td></tr>
        <tr><td><b>Too long</b></td><td>Extra scenes or a second idea</td><td>Cutting the part that doesn't serve the skill</td><td>Cut the examples</td></tr>
        <tr><td><b>Sentences too long</b></td><td>Ideas joined with “and,” “but,” “because”</td><td>Splitting at the joins</td><td>Make choppy fragments</td></tr>
        <tr><td><b>Reads too hard</b></td><td>Rare words or long sentences</td><td>Swapping in grade-level words, then shorter sentences</td><td>Simplify the skill itself</td></tr>
        <tr><td><b>Reads too easy</b> <span class="small muted">(often grades 9-12)</span></td><td>Plain words throughout</td><td>Choosing more precise words for key ideas</td><td>Lengthen sentences past the cap</td></tr>
        <tr><td><b>Too few examples</b></td><td>The skill is named but not shown enough</td><td>Writing one more moment that shows it</td><td>Quote the same sentence twice</td></tr>
        <tr><td><b>Quote not found</b></td><td>The example was paraphrased</td><td>Copying the sentence from the passage exactly</td><td>Edit the passage to match the quote</td></tr>
        <tr><td><b>Flagged word</b></td><td>A word that often signals deficit framing or a stereotype</td><td>Rewriting the phrase in asset-based language</td><td>Swap in a synonym that means the same thing</td></tr>
      </tbody>
    </table></div>
  </section>

  <section class="blk" aria-labelledby="h-rules">
    <h2 id="h-rules">Four rules</h2>
    <div class="grid4">
      <div class="card stack"><h3>Checks sort, people decide</h3><p class="muted">A lane is a guess about how closely to read. An editor makes every call.</p></div>
      <div class="card stack"><h3>Quotes are exact</h3><p class="muted">Skill examples are copied word for word, so the script and video highlight the right sentence.</p></div>
      <div class="card stack"><h3>Lexile decides</h3><p class="muted">The free estimate only routes. The licensed analyzer is the readability gate.</p></div>
      <div class="card stack"><h3>Every edit is rechecked</h3><p class="muted">After any fix, the passage runs through the checks again before approval.</p></div>
    </div>
    <div class="btnrow"><a class="btn primary" href="#practice">Start the practice →</a></div>
  </section>
</div>
"""

def practice_view():
    return f"""
<div class="view" id="practice">
  <section class="blk" aria-labelledby="h-drill" style="margin-top:28px">
    <span class="steplabel">Part 1 · about 5 minutes</span>
    <h2 id="h-drill">Lane drill</h2>
    <p class="lede">Read each set of check results and pick the lane the validator would give. Four come straight from the sample run. Three are training copies with one change each, so you can see what sends a passage red.</p>
    <div class="card stack" style="padding:16px"><h3>The lane rules</h3>
      <ul class="plain muted"><li><b class="ok">Green:</b> every check passed.</li><li><b style="color:var(--yellow)">Yellow:</b> any fit issue (length, sentence length, example count, readability), or one or two yellow-list words.</li><li><b class="miss">Red:</b> any red-list word, three or more yellow-list words, a broken schema, or an example that isn't quoted exactly.</li></ul></div>
    <div class="drill" id="drill"></div>
    <p id="drill-score" class="small muted" aria-live="polite"></p>
  </section>

  <section class="blk" aria-labelledby="h-cases">
    <span class="steplabel">Part 2 · about 15 minutes</span>
    <h2 id="h-cases">Five real passages</h2>
    <p class="lede">These are v2.1 passages from the November sample run, with the validator's real results. First call the lane. Then review it as an editor and compare your decision with an editor's.</p>
    <div class="callout small">The editor decisions here are illustrative, written to show how the rubric applies. In calibration, editors often differ on Approve versus Approve with notes, and that's the conversation worth having.</div>
    <div class="casenav" id="casenav" role="tablist" aria-label="Practice passages"></div>
    <div id="case"></div>
  </section>

  <section class="blk" aria-labelledby="h-score">
    <h2 id="h-score">Your results</h2>
    <div class="score" id="score" aria-live="polite"></div>
    <p class="muted small">Nothing is saved or sent. In onboarding, bring your Part 2 decisions to the calibration session and compare them with the other editors' decisions.</p>
  </section>
</div>
"""

JS = "const DRILL=" + json.dumps(DRILL) + ";\nconst CASES=" + json.dumps(CASES) + ";\n" + r"""
const LANES=['green','yellow','red'], CAP=s=>s[0].toUpperCase()+s.slice(1);
const state={drill:{}, lane:{}, dec:{}, rub:{}, cur:0};
function tbl(rows){
  return `<table><thead><tr><th>Check</th><th>Result</th><th>Target</th></tr></thead><tbody>${rows.map(([l,ok,res,t])=>`<tr><td>${esc(l)}</td><td class="${ok?'ok':'miss'}">${ok?'✓':'✗'} ${esc(res)}</td><td>${esc(t)}</td></tr>`).join('')}</tbody></table>`;
}
function pills(name, chosen, answer){
  return `<div class="choose" role="group" aria-label="Pick a lane">${LANES.map(l=>{
    const done=chosen!=null; const cls=done?(l===answer?'right':(l===chosen?'wrong':'')):'';
    return `<button type="button" data-${name}="${l}" aria-pressed="${chosen===l}" class="${cls}" ${done?'disabled':''}>${CAP(l)}</button>`}).join('')}</div>`;
}
function renderDrill(){
  document.getElementById('drill').innerHTML=DRILL.map((d,i)=>{
    const c=state.drill[i];
    return `<div class="dcard"><div style="display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap"><b>${i+1}. ${esc(d.title)}</b><span class="src">Grade ${esc(d.grade)} · ${esc(d.skill)}</span></div>
      <div class="tablewrap" style="border-radius:10px">${tbl(d.rows)}</div>
      <div data-drill-i="${i}">${pills('dl',c,d.lane)}</div>
      ${c!=null?`<div class="fb ${c===d.lane?'good':'bad'}"><b>${c===d.lane?'Right':'Not quite'}: ${CAP(d.lane)}.</b> ${esc(d.why)}</div>`:''}
      <span class="src">${esc(d.source)}</span></div>`;}).join('');
  const n=Object.keys(state.drill).length, r=Object.entries(state.drill).filter(([i,c])=>DRILL[i].lane===c).length;
  document.getElementById('drill-score').textContent=n?`${r} of ${n} right so far, out of ${DRILL.length}.`:'';
  renderScore();
}
document.getElementById('drill').addEventListener('click',e=>{
  const b=e.target.closest('button[data-dl]'); if(!b) return;
  const i=+b.closest('[data-drill-i]').dataset.drillI; state.drill[i]=b.dataset.dl; renderDrill();
});
function hl(text,quotes){
  let h=esc(text); quotes.map(esc).filter(Boolean).sort((a,b)=>b.length-a.length).forEach(q=>{h=h.split(q).join('\u0001'+q+'\u0002')});
  h=h.replace(/\u0001/g,'<mark>').replace(/\u0002/g,'</mark>');
  return h.split(/\n\n+/).map(p=>'<p>'+p.replace(/\n/g,'<br>')+'</p>').join('');
}
const RUB=["The skill is taught, not just mentioned","Clear enough for the grade","Fits the grade's length and reading level","The main character solves their own problem","Culture, family and place read as everyday life","No stereotypes or deficit language","Disability, if present, uses person-first or neutral words"];
const DEC=["Approve","Approve with notes","Regenerate","Reject"];
function renderNav(){
  document.getElementById('casenav').innerHTML=CASES.map((c,i)=>`<button type="button" role="tab" aria-current="${i===state.cur}" aria-selected="${i===state.cur}" class="${state.dec[i]?'done':''}" data-case="${i}">${i+1}. Grade ${esc(c.grade)}</button>`).join('');
}
function renderCase(){
  const i=state.cur, c=CASES[i], lane=state.lane[i], dec=state.dec[i], rub=state.rub[i]||[];
  const laneFb = lane!=null ? `<div class="fb ${lane===c.lane?'good':'bad'}"><b>The validator said ${CAP(c.lane)}.</b> ${esc(c.why)}</div>` : '';
  const decBtns = `<div class="choose" role="group" aria-label="Your decision">${DEC.map(d=>`<button type="button" data-dec="${d}" aria-pressed="${dec===d}" ${dec?'disabled':''}>${d}</button>`).join('')}</div>`;
  const reveal = dec ? `<div class="fb ${dec===c.decision?'good':'bad'}"><b>An editor's call (illustrative): ${esc(c.decision)}.</b> ${esc(c.note)}</div>
     <div class="example"><b>What to notice</b>${esc(c.notice)}</div>
     <p class="small muted">You ticked ${rub.filter(Boolean).length} of ${RUB.length} rubric checks. ${dec===c.decision?'Your decision matches.':'Different from the example. Bring your reason to calibration.'}</p>` : '';
  document.getElementById('case').innerHTML=`<div class="case">
    <div class="head"><h3>${esc(c.title)}</h3><span class="src">${esc(c.id)} · Grade ${esc(c.grade)} · ${esc(c.teks)} · ${esc(c.skill)} · ${esc(c.type)}</span></div>
    <div class="passage">${hl(c.text,c.quotes)}</div>
    <p class="src">Highlighted: the skill examples Claude quoted. Real v2.1 passage, unedited.</p>
    <div class="tablewrap" style="border-radius:12px">${tbl(c.rows)}</div>
    <div class="stack" style="gap:8px"><span class="steplabel">Step 1 · Which lane?</span><div data-case-lane>${pills('cl',lane,c.lane)}</div>${laneFb}</div>
    <div class="stack ${lane==null?'locked':''}" style="gap:10px" aria-disabled="${lane==null}">
      <span class="steplabel">Step 2 · Your call as the editor</span>
      <p class="small muted">${c.lane==='green'?'This green was drawn for the 10% spot-check.':'Yellow: full review.'} The licensed Lexile check would run here against ${esc(c.lexile)}.</p>
      <div class="checks">${RUB.map((t,k)=>`<label><input type="checkbox" data-rub="${k}" ${rub[k]?'checked':''} ${dec?'disabled':''}> ${t}</label>`).join('')}</div>
      ${decBtns}
      ${reveal}
    </div>
    <div class="btnrow">${i>0?`<button class="btn ghost" type="button" data-go="${i-1}">← Previous</button>`:''}${i<CASES.length-1?`<button class="btn primary" type="button" data-go="${i+1}">Next passage →</button>`:`<a class="btn primary" href="#h-score">See your results</a>`}</div>
  </div>`;
  renderNav(); renderScore();
}
document.getElementById('casenav').addEventListener('click',e=>{const b=e.target.closest('[data-case]'); if(b){state.cur=+b.dataset.case; renderCase();}});
document.getElementById('case').addEventListener('click',e=>{
  const i=state.cur;
  const l=e.target.closest('button[data-cl]'); if(l){state.lane[i]=l.dataset.cl; return renderCase();}
  const d=e.target.closest('button[data-dec]'); if(d){state.dec[i]=d.dataset.dec; return renderCase();}
  const g=e.target.closest('[data-go]'); if(g){state.cur=+g.dataset.go; renderCase(); document.getElementById('h-cases').scrollIntoView({block:'start'});}
});
document.getElementById('case').addEventListener('change',e=>{
  const r=e.target.closest('[data-rub]'); if(!r) return; const i=state.cur; (state.rub[i]=state.rub[i]||[])[+r.dataset.rub]=r.checked;
});
function renderScore(){
  const dn=Object.keys(state.drill).length, dr=Object.entries(state.drill).filter(([i,c])=>DRILL[i].lane===c).length;
  const ln=Object.keys(state.lane).length, lr=Object.entries(state.lane).filter(([i,c])=>CASES[i].lane===c).length;
  const en=Object.keys(state.dec).length, er=Object.entries(state.dec).filter(([i,c])=>CASES[i].decision===c).length;
  document.getElementById('score').innerHTML=`<div><b>${dr}/${DRILL.length}</b><span class="small muted">lane drill right${dn<DRILL.length?` (${dn} answered)`:''}</span></div>
   <div><b>${lr}/${CASES.length}</b><span class="small muted">passage lanes match the validator${ln<CASES.length?` (${ln} answered)`:''}</span></div>
   <div><b>${er}/${CASES.length}</b><span class="small muted">decisions match the example${en<CASES.length?` (${en} answered)`:''}</span></div>`;
}
renderDrill(); renderCase();
"""

html = head("Riverlark Onboarding and Practice", EXTRA) + header("onboarding") + f"""
<main class="wrap">
  <div class="hero">
    <span class="eyebrow">Enablement · For writers and editors</span>
    <h1>Onboarding and practice</h1>
    <p class="lede">A short guide to how a lesson moves through the pipeline and how to fix a draft, then a practice round: sort real sample passages into lanes, make the editor's call, and compare yours with the validator's and an editor's.</p>
    <div class="pills"><span class="pill real">Real passages and results from the November sample run</span><span class="pill illus">Editor decisions are illustrative</span></div>
    <nav class="viewtabs" aria-label="Views"><a href="#guide">Guide</a><a href="#practice">Practice</a></nav>
  </div>
  {guide_view()}
  {practice_view()}
  {footer("onboarding")}
</main>
""" + tail(JS)

open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "portfolio-static", "onboarding-and-practice", "index.html"), "w").write(html)
print("ok", len(html), len(DRILL), len(CASES))
