import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import *

EXTRA = r"""
.base{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
@media (max-width:860px){.base{grid-template-columns:repeat(2,minmax(0,1fr))}}
.base div{background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 16px}
.base b{display:block;font-size:1.7rem;font-weight:800;color:var(--river)}
.base span{font-size:.86rem;color:var(--muted)}
.phases{display:flex;flex-direction:column;gap:14px}
.phase{display:grid;grid-template-columns:150px minmax(0,1fr) minmax(0,1fr);gap:18px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px;border-left:6px solid var(--sky)}
.phase.pilot{border-left-color:var(--coral)}
@media (max-width:860px){.phase{grid-template-columns:1fr}}
.phase .when{font-weight:800;color:var(--river)}
.phase .when span{display:block;font-weight:600;font-size:.84rem;color:var(--muted)}
.phase h4{font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:6px}
.phase ul{margin:0;padding-left:18px;font-size:.93rem;display:flex;flex-direction:column;gap:4px}
.gate{background:var(--mist);border-radius:12px;padding:12px 14px}
.calc{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:18px}
@media (max-width:860px){.calc{grid-template-columns:1fr}}
.fields{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.result{background:var(--river);color:#fff;border-radius:16px;padding:20px;display:flex;flex-direction:column;gap:10px}
.result b.big{font-size:2.2rem;font-weight:800}
.result table{font-size:.9rem;color:#fff}.result td{border-bottom:1px solid rgba(255,255,255,.18);padding:6px 4px}
.result td:last-child{text-align:right;font-variant-numeric:tabular-nums}
"""

MEASURES = [
 ("Schedule", "Lessons approved vs plan", "Lessons through editor approval, against the batch plan", "Review log", "On plan, or under 5% behind", "Managing Editor", "Weekly"),
 ("Quality", "First-pass green rate, by band", "Share of first drafts that come back green", "Validator reports", "70% or more", "AI Workflow", "Each batch"),
 ("Quality", "Send-back reasons", "Top three reasons for Regenerate and Approve with notes", "Review log", "No reason above 15% of passages", "AI Workflow", "Weekly"),
 ("Quality", "Estimate vs Lexile agreement", "Passages where the free estimate and licensed Lexile agree on in or out of range", "Validator + Lexile analyzer", "85% or more, tracked by band", "AI Workflow", "Monthly"),
 ("Quality", "Wrong-lane reports", "Lanes editors overruled, by check", "Review log", "Under 15% of reviewed passages", "AI Workflow", "Weekly"),
 ("Quality", "Representation issues after approval", "Issues found by the consultant, teachers or users once a passage was approved", "Consultant sample, teacher feedback", "0", "Representation consultant", "Each batch"),
 ("Quality", "Teacher “ready to use” rating", "Pilot lessons rated ready to use by advisory-panel teachers", "Teacher review form", "90% or more", "VP of Curriculum", "Pilot only"),
 ("Time", "Editor minutes per lesson", "Passage review plus script review, from the review log", "Review log", "Within the 12 hours a week budget", "Managing Editor", "Weekly"),
 ("Time", "Drafts per lesson", "First draft plus regenerations", "Pipeline logs", "1.3 or fewer", "AI Workflow", "Each batch"),
 ("Cost", "Cost per lesson", "AI drafting plus editor time plus video, per published lesson", "Pipeline logs, review log, video tool licenses and producer time", "Set at pilot kickoff from real rates", "VP of Curriculum", "Monthly"),
 ("Video", "Video checks passed first time", "Finished videos passing all automated checks before the human spot-check", "video_checks.py reports", "90% or more", "Video Production Lead", "Each batch"),
]

PHASES = [
 ("", "Dec 2026", "Readiness", [
    "Run v2.1 on 20 fresh holdout briefs it wasn't designed from",
    "Propose and test v2.2 to center readability, through the change process",
    "Editor calibration: 10 sample passages, decided separately, then compared",
    "Connect the licensed Lexile analyzer to the review step"],
  "Go to pilot when: holdout has at least 14 of 20 green and 0 red, the v2.2 decision is recorded, and editors agree on at least 8 of 10 calibration passages."),
 ("pilot", "Jan-Feb 2027", "Pilot · grades 3-5", [
    "43 lessons, where STAAR reading starts",
    "Every passage gets a full editor review, not only yellows, so the lanes can be checked against people",
    "Licensed Lexile check on every passage",
    "6 advisory-panel teachers rate a set of finished lessons"],
  "Expand when the pilot gate below is met. If not: hold, open a prompt change for the top send-back reason, and re-run a 10-lesson pilot batch."),
 ("", "Mar-May 2027", "Expand · remaining 135", [
    "Batches by band: K-2, then 6-8, then 9-12",
    "Normal lanes: every yellow plus a 10% green spot-check",
    "Managing Editor approves each batch before video",
    "Generation pauses for a prompt change if a band falls below its first-pass bar, or fewer than 90% of reviewed passages are approved"],
  "Go to video when: all 178 passages are approved, every batch is signed off, and representation issues after approval stay at 0."),
 ("", "Jun-Jul 2027", "Video", [
    "The video team builds each lesson from its storyboard in Lumen5 or Camtasia, in batches",
    "Automated video checks on every file, then a 10% human spot-check",
    "Speech-to-text pronunciation check on every video"],
  "Publish when: every video passes its checks and the spot-checks are clean."),
 ("", "Aug 2027", "Publish and improve", [
    "Publish to the classroom platform by TEKS code",
    "Weekly send-back review and monthly readability audit begin",
    "Teacher feedback routes to the Managing Editor"],
  "Ongoing: monthly report to the VP of Curriculum."),
]

GATE = [
 ("First-pass green rate, grades 3-5", "70% or more", "v2.1 sample: 5 of 5 grades 3-5 green"),
 ("Red lessons reaching review", "0", "v2.0 and v2.1 samples: 0"),
 ("Representation issues after approval", "0", "Not yet measured"),
 ("Estimate vs Lexile agreement", "85% or more", "Not yet measured (needs the licensed analyzer)"),
 ("Editors overrule a green", "15% of spot-checks or fewer", "Not yet measured"),
 ("Teachers rate “ready to use”", "90% of rated lessons", "Not yet measured"),
 ("Editor time", "Inside 12 hours a week", "Planning estimate: about 8 minutes a pilot lesson"),
]

def body():
    meas = "".join(f"<tr><td><span class='pill info'>{a}</span></td><td><b>{b}</b><div class='small muted'>{c}</div></td><td class='small'>{d}</td><td>{e}</td><td class='small'>{f}</td><td class='small'>{g}</td></tr>" for a,b,c,d,e,f,g in MEASURES)
    ph = "".join(f"""<div class="phase {c}"><div class="when">{w}<span>{t}</span></div><div><h4>What happens</h4><ul>{''.join(f'<li>{x}</li>' for x in items)}</ul></div><div class="gate"><h4>Gate to the next phase</h4><p class="small">{g}</p></div></div>""" for c,w,t,items,g in PHASES)
    gate = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td class='small muted'>{c}</td></tr>" for a,b,c in GATE)
    return f"""
  <section class="blk" aria-labelledby="h-base" style="margin-top:28px">
    <div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:center"><h2 id="h-base">Where we start</h2><span class="pill real">Real · November 2026 sample run</span></div>
    <div class="base">
      <div><b>18 / 20</b><span>green on prompt v2.1, up from 8 on v2.0</span></div>
      <div><b>0</b><span>red lessons and representation flags, both runs</span></div>
      <div><b>20 / 20</b><span>skill examples quoted exactly, both runs</span></div>
      <div><b>2</b><span>yellows left, both grades 9-12 reading slightly easy</span></div>
    </div>
    <p class="muted small">A baseline, not a forecast. The fix was designed from the same 20 briefs, which is why fresh holdout briefs come first.</p>
  </section>

  <section class="blk" aria-labelledby="h-phases">
    <div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:center"><h2 id="h-phases">Five phases to fall 2027</h2><span class="pill illus">Illustrative timeline and bars</span></div>
    <p class="lede">Each phase ends at a gate. The bars are written down before the phase starts, the same rule the prompt change process uses, so a result can't move the goalposts.</p>
    <div class="phases">{ph}</div>
  </section>

  <section class="blk" aria-labelledby="h-gate">
    <h2 id="h-gate">The pilot gate</h2>
    <p class="lede">The VP of Curriculum makes the go or no-go call with the Managing Editor, against these bars. All must be met to expand.</p>
    <div class="tablewrap"><table>
      <thead><tr><th scope="col">Measure</th><th scope="col">Bar, set before the pilot</th><th scope="col">What we know today</th></tr></thead>
      <tbody>{gate}</tbody>
    </table></div>
  </section>

  <section class="blk" aria-labelledby="h-meas">
    <h2 id="h-meas">Measures</h2>
    <p class="lede">Eleven measures, each with a source the team already has. None needs a new tool: they come from the validator reports, the review log, the Lexile analyzer and video production records.</p>
    <div class="tablewrap"><table>
      <thead><tr><th scope="col">Area</th><th scope="col">Measure</th><th scope="col">Source</th><th scope="col">Target <span class="pill illus" style="margin-left:4px">illustrative</span></th><th scope="col">Owner</th><th scope="col">How often</th></tr></thead>
      <tbody>{meas}</tbody>
    </table></div>
  </section>

  <section class="blk" aria-labelledby="h-cost">
    <div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:center"><h2 id="h-cost">Cost per lesson</h2><span class="pill illus">Illustrative inputs</span></div>
    <p class="lede">Three parts: AI drafting, editor time and video. Video is estimated from two common tools, Lumen5 and Camtasia. Both are subscriptions, so the license spreads thin across 178 lessons and producer time drives the cost. Replace every input with Riverlark's real rates at pilot kickoff.</p>
    <div class="calc">
      <div class="card"><div class="fields">
        <div class="field"><label for="k-draft">AI cost per draft ($)</label><input id="k-draft" type="number" min="0" step="0.01" value="0.10"></div>
        <div class="field"><label for="k-drafts">Drafts per lesson</label><input id="k-drafts" type="number" min="1" step="0.05" value="1.2"></div>
        <div class="field"><label for="k-mode">Review mode</label><select id="k-mode"><option value="pilot">Pilot: full review of every passage</option><option value="prod" selected>Production: lanes</option></select></div>
        <div class="field"><label for="k-yellow">Yellow (%)</label><input id="k-yellow" type="number" min="0" max="100" value="10"></div>
        <div class="field"><label for="k-rate">Editor cost per hour ($)</label><input id="k-rate" type="number" min="0" step="1" value="45"></div>
        <div class="field"><label for="k-tool">Video tool</label><select id="k-tool"><option value="lumen5" selected>Lumen5 Professional</option><option value="camtasia">Camtasia Create</option><option value="custom">Custom</option></select></div>
        <div class="field"><label for="k-lic">Video license per lesson ($)</label><input id="k-lic" type="number" min="0" step="0.01" value="2.24"></div>
        <div class="field"><label for="k-vh">Producer hours per lesson</label><input id="k-vh" type="number" min="0" step="0.25" value="1"></div>
        <div class="field"><label for="k-vrate">Producer cost per hour ($)</label><input id="k-vrate" type="number" min="0" step="1" value="40"></div>
        <div class="field"><label for="k-n">Lessons</label><input id="k-n" type="number" min="1" value="178"></div>
      </div>
      <p class="small muted" style="margin-top:12px">Review times match the reviewer guide: 30 seconds per green spot-check, 3 minutes per full review, 5 minutes per lesson script.</p>
      <p class="small muted" id="k-toolnote" style="margin-top:8px"></p></div>
      <div class="result" aria-live="polite"><span>Cost per lesson</span><b class="big" id="k-total">–</b><table id="k-break"></table><span class="small" style="color:#CDE8EE" id="k-lib"></span></div>
    </div>
  </section>

  <section class="blk" aria-labelledby="h-report">
    <h2 id="h-report">Monthly report</h2>
    <p class="lede">One page for the VP of Curriculum, the same shape every month. Copy the template into the team's report doc.</p>
    <div class="grid2">
      <pre id="tpl" tabindex="0" aria-label="Monthly report template">## Riverlark Texas lessons · monthly report · [Month YYYY]

**Status:** [On track / At risk / Off track], [one sentence why]

### Schedule
- Lessons approved this month: [n] (plan [n]), total [n] of 178
- Batches signed off: [list]

### Quality
- First-pass green rate by band: K-2 [x]% · 3-5 [x]% · 6-8 [x]% · 9-12 [x]%
- Top send-back reasons: 1. [reason] ([x]%) 2. [reason] 3. [reason]
- Estimate vs Lexile agreement: [x]%
- Wrong-lane reports: [n], mostly [check]
- Representation issues after approval: [n]

### Time and cost
- Editor hours: [h] of [h] budget
- Drafts per lesson: [x]
- Cost per lesson: $[x] (AI $[x] · editor $[x] · video $[x])

### Changes made
- [PR-ID]: [prompt or rule change], [decision]

### Decisions needed
- [What, from whom, by when]</pre>
      <div class="stack">
        <div class="card stack"><h3>Reading it</h3><ul class="plain muted"><li>Status comes first, in one sentence.</li><li>Every number has a plan or a bar next to it.</li><li>Changes link to their change record, so anyone can see what was tested.</li><li>“Decisions needed” is the reason the report exists.</li></ul></div>
        <div class="btnrow"><button class="btn primary" type="button" id="tpl-copy">Copy template</button><span class="small muted" id="tpl-msg"></span></div>
      </div>
    </div>
  </section>

  <section class="blk" aria-labelledby="h-who">
    <h2 id="h-who">Who does what in the rollout</h2>
    <div class="tablewrap"><table>
      <thead><tr><th scope="col">Role</th><th scope="col">In the rollout</th></tr></thead>
      <tbody>
        <tr><td><b>VP of Curriculum, Texas</b></td><td>Owns scope and deadline. Makes the pilot go or no-go call. Reads the monthly report.</td></tr>
        <tr><td><b>Managing Editor, ELA</b></td><td>Approves each batch and every prompt change. Runs the weekly send-back review.</td></tr>
        <tr><td><b>Editors (3)</b></td><td>Review the queue inside the weekly time budget. Log wrong lanes. Join calibration.</td></tr>
        <tr><td><b>Representation consultant</b></td><td>Reviews a deep sample of each batch and the framework itself.</td></tr>
        <tr><td><b>Video Production Lead</b></td><td>Runs video production from the storyboards and the video spot-checks.</td></tr>
        <tr><td><b>AI Workflow &amp; Automation</b></td><td>Runs the pipeline, proposes and tests changes, builds the reports.</td></tr>
      </tbody>
    </table></div>
    <p class="small muted">Risks and how we handle them are on the case study's <a href="{CASE}#quality">Quality and governance</a> tab.</p>
  </section>
"""

JS = r"""
const K=id=>document.getElementById(id);
function money(n){return '$'+n.toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2})}
function calc(){
  const draft=+K('k-draft').value||0, drafts=+K('k-drafts').value||0, rate=+K('k-rate').value||0, lic=+K('k-lic').value||0, vh=+K('k-vh').value||0, vrate=+K('k-vrate').value||0, video=lic+vh*vrate, n=+K('k-n').value||0, y=Math.min(100,Math.max(0,+K('k-yellow').value||0))/100;
  const pilot=K('k-mode').value==='pilot';
  K('k-yellow').disabled=pilot;
  const passMin = pilot ? 3 : (y*3 + (1-y)*0.10*0.5);
  const minutes = passMin + 5;
  const ai=draft*drafts, ed=minutes/60*rate, total=ai+ed+video;
  K('k-total').textContent=money(total);
  K('k-break').innerHTML=`<tr><td>AI drafting</td><td>${money(ai)}</td></tr><tr><td>Editor time (${minutes.toFixed(1)} min)</td><td>${money(ed)}</td></tr><tr><td>Video license</td><td>${money(lic)}</td></tr><tr><td>Video producer (${vh} h)</td><td>${money(vh*vrate)}</td></tr>`;
  K('k-lib').textContent=`About ${money(total*n)} for ${n.toLocaleString()} lessons. Illustrative inputs only.`;
}
const TOOLS={
  lumen5:{lic:2.24,h:1,note:"Lumen5 Professional: about $199 a month, billed monthly, with unlimited videos. Two production months (Jun-Jul) is about $398, or $2.24 a lesson across 178. Template-driven, so about 1 producer hour a lesson. Check that it can do word-by-word highlighting before committing."},
  camtasia:{lic:2.80,h:2,note:"Camtasia Create: about $249 per user a year, with AI voiceover. Two seats is about $498, or $2.80 a lesson across 178. A manual timeline editor, so about 2 producer hours a lesson to build highlights and captions from the storyboard."},
  custom:{note:"Custom: enter the license share and producer hours for another tool or a rendering vendor's per-lesson quote."}};
function setTool(){const t=TOOLS[K('k-tool').value]; if(t.lic!=null){K('k-lic').value=t.lic; K('k-vh').value=t.h;} K('k-toolnote').textContent=t.note+" Producer hours are planning estimates: time one pilot lesson to confirm."; calc();}
K('k-tool').addEventListener('change',setTool);
['k-lic','k-vh'].forEach(id=>K(id).addEventListener('input',()=>{K('k-tool').value='custom'; K('k-toolnote').textContent=TOOLS.custom.note; calc();}));
['k-draft','k-drafts','k-mode','k-yellow','k-rate','k-vrate','k-n'].forEach(id=>K(id).addEventListener('input',calc)); setTool();
K('tpl-copy').addEventListener('click',()=>copyText(K('tpl').textContent,K('tpl-msg')));
"""

html = head("Riverlark Rollout Plan", EXTRA) + header("rollout") + f"""
<main class="wrap">
  <div class="hero">
    <span class="eyebrow">Enablement · For leaders</span>
    <h1>Rollout plan with measures</h1>
    <p class="lede">Pilot one grade band, measure it against bars set in advance, then expand to all 178 lessons by fall 2027. The plan answers the three questions leaders ask: is it on time, on budget, and good enough to put in front of students?</p>
    <div class="pills"><span class="pill real">Baselines are real</span><span class="pill illus">Dates, bars and costs are illustrative</span></div>
  </div>
  {body()}
  {footer("rollout")}
</main>
""" + tail(JS)

open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "portfolio-static", "rollout-plan", "index.html"), "w").write(html)
print("ok", len(html))
