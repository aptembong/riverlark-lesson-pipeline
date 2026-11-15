import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import *

EXTRA = r"""
.steps4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
@media (max-width:900px){.steps4{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.steps4{grid-template-columns:1fr}}
.st{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px;display:flex;flex-direction:column;gap:8px;border-top:6px solid var(--sky)}
.st .n{width:30px;height:30px;border-radius:50%;background:var(--river);color:#fff;font-weight:800;display:grid;place-items:center}
.st dl{margin:0;display:grid;gap:4px;font-size:.88rem}.st dt{font-weight:700}.st dd{margin:0 0 4px;color:var(--muted)}
.form{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:18px}
@media (max-width:900px){.form{grid-template-columns:1fr}}
.fgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
@media (max-width:560px){.fgrid{grid-template-columns:1fr}}
.fgrid .wide{grid-column:1/-1}
.barrow{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr) 36px;gap:8px;align-items:center}
.barrow button{font:inherit;border:1px solid var(--line);background:#fff;border-radius:8px;height:38px;cursor:pointer;color:var(--muted)}
.sticky{position:sticky;top:12px;display:flex;flex-direction:column;gap:10px}
.met{color:var(--green);font-weight:700}
"""

EXAMPLE = {
 "id": "PR-2026-11-01", "title": "Grade fit for grades 3-12", "by": "AI Workflow & Automation", "date": "2026-11-15",
 "from": "v2.0", "to": "v2.1",
 "saw": "v2.0 on the 20 sample briefs: 8 green, 12 yellow, 0 red. Every yellow came from fit checks, not content or safety: 5 passages under the word range, 6 with sentences too long, 7 reading too hard and 1 too easy.",
 "cause": "The prompt gave a range and nothing else, so drafts aimed at the bottom of it. It gave an average sentence length with no cap. A Lexile number alone doesn't tell the writer what to change.",
 "change": "1. A target word count and a paragraph plan, in place of a bare range.\n2. A per-sentence cap, with an instruction to split long sentences.\n3. Vocabulary guidance by grade band, in place of a bare Lexile number.\n4. A self-check on counts before returning.",
 "same": "Output schema, content rules, representation guidance and the validator. No other file changes.",
 "test": "The same 20 sample briefs, the same validate.py, fresh first drafts saved before scoring. No edits after scoring.",
 "bars": [["Green lessons", "At least 14 of 20"], ["Red lessons and representation flags", "Stay at 0"], ["Schema and skill evidence", "Stay at 20/20"], ["No regressions", "None of the 8 v2.0 greens drops"]],
 "rollback": "v2.0.md stays in the repo. Rolling back means pointing the renderer at v2.0. No other file changes.",
}

def body():
    ex = EXAMPLE
    bars = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td class='met'>{c}</td></tr>" for (a,b),c in zip(ex["bars"], ["18 of 20 · met", "0 and 0 · met", "20/20 and 20/20 · met", "All 8 stayed green · met"]))
    return f"""
  <section class="blk" aria-labelledby="h-when" style="margin-top:28px">
    <h2 id="h-when">When to open a change</h2>
    <div class="grid2">
      <div class="card stack"><span class="pill info">Open a change request</span>
        <ul class="plain"><li>Fewer than 90% of reviewed passages in a batch are approved. Generation pauses until a change is approved.</li><li>The same send-back reason shows up three or more times in a week.</li><li>A band's first-pass green rate falls below its bar for a batch.</li><li>The monthly readability audit shows drift in a band.</li><li>A new grade band, state or subject is added.</li><li>The model version changes. A new model is a prompt change too.</li><li>A wrong-lane pattern points to a validator rule. Rule changes follow the same steps.</li></ul></div>
      <div class="card stack"><span class="pill illus">Not a change request</span>
        <ul class="plain"><li>One weak passage. Regenerate it with a note.</li><li>A one-off fix an editor can make with Approve with notes.</li><li>Anything that would change a rule to pass a batch already scored.</li></ul>
        <p class="small muted">Anyone can ask for a change: writers, editors, the consultant or the Managing Editor. AI Workflow writes it up and runs the test.</p></div>
    </div>
  </section>

  <section class="blk" aria-labelledby="h-steps">
    <h2 id="h-steps">Four steps</h2>
    <div class="steps4">
      <div class="st"><span class="n">1</span><h3>Propose</h3><dl><dt>Who</dt><dd>AI Workflow writes it, from anyone's request</dd><dt>Write down</dt><dd>What the last run showed, the likely cause, the exact change, what stays the same, and the approval bar</dd><dt>Done when</dt><dd>The bar is written before any test runs</dd></dl></div>
      <div class="st"><span class="n">2</span><h3>Test</h3><dl><dt>Who</dt><dd>AI Workflow</dd><dt>How</dt><dd>Same sample briefs, same validator, fresh first drafts saved before scoring</dd><dt>Done when</dt><dd>A comparison report shows every check, old version against new, with no edits after scoring</dd></dl></div>
      <div class="st"><span class="n">3</span><h3>Approve</h3><dl><dt>Who</dt><dd>Managing Editor, ELA</dd><dt>Choices</dt><dd>Approve, approve with conditions, or reject, judged against the bar from step 1</dd><dt>Done when</dt><dd>The decision, its date and any conditions are in the change log</dd></dl></div>
      <div class="st"><span class="n">4</span><h3>Roll back</h3><dl><dt>Who</dt><dd>AI Workflow, on the Managing Editor's call</dd><dt>When</dt><dd>A production batch falls below the bar the change was approved on</dd><dt>How</dt><dd>Point the renderer at the old version. It never leaves the repo.</dd></dl></div>
    </div>
    <div class="card stack"><h3>Rules that keep the test honest</h3>
      <div class="grid3">
        <p class="muted"><b style="color:var(--ink)">The bar comes first.</b> It's written before the run, so a result can't move the goalposts.</p>
        <p class="muted"><b style="color:var(--ink)">One change at a time.</b> A prompt and a validator rule never change in the same request, or you can't tell which one worked.</p>
        <p class="muted"><b style="color:var(--ink)">Then fresh briefs.</b> A change designed from the sample set is confirmed on holdout briefs before production.</p>
      </div>
    </div>
  </section>

  <section class="blk" aria-labelledby="h-form">
    <h2 id="h-form">Change request form</h2>
    <p class="lede">Fill this in and copy the entry into <code>prompts/passage_generation/CHANGELOG.md</code>. The preview updates as you type. Load the real example to see a finished one.</p>
    <div class="form">
      <div class="card stack">
        <div class="btnrow"><button class="btn ghost" type="button" id="f-load">Load PR-2026-11-01 as an example</button><button class="btn ghost" type="button" id="f-clear">Clear</button></div>
        <div class="fgrid">
          <div class="field"><label for="f-id">Change ID</label><input id="f-id" type="text" placeholder="PR-YYYY-MM-NN"></div>
          <div class="field"><label for="f-title">Short title</label><input id="f-title" type="text" placeholder="What the change does"></div>
          <div class="field"><label for="f-by">Requested by</label><input id="f-by" type="text" placeholder="Name and role"></div>
          <div class="field"><label for="f-date">Date</label><input id="f-date" type="date"></div>
          <div class="field"><label for="f-from">Current version</label><input id="f-from" type="text" placeholder="v2.1"></div>
          <div class="field"><label for="f-to">Proposed version</label><input id="f-to" type="text" placeholder="v2.2"></div>
          <div class="field wide"><label for="f-saw">What the last run showed</label><textarea id="f-saw" placeholder="Numbers from the validator report, and where the misses cluster"></textarea></div>
          <div class="field wide"><label for="f-cause">Likely cause</label><textarea id="f-cause" placeholder="What in the prompt (or rule) produces the miss"></textarea></div>
          <div class="field wide"><label for="f-change">The exact change</label><textarea id="f-change" placeholder="One line per change"></textarea></div>
          <div class="field wide"><label for="f-same">What stays the same</label><textarea id="f-same" placeholder="Schema, rules, representation guidance, validator..."></textarea></div>
          <div class="field wide"><label for="f-test">Test set</label><input id="f-test" type="text" placeholder="Which briefs, which validator, how drafts are saved"></div>
          <div class="field wide"><label>Approval bar, set before the run</label><div id="f-bars" class="stack" style="gap:8px"></div><div><button class="btn ghost" type="button" id="f-addbar" style="padding:6px 14px;font-size:.86rem">+ Add a bar</button></div></div>
          <div class="field wide"><label for="f-rollback">Roll-back plan</label><input id="f-rollback" type="text" placeholder="Which version to point back to"></div>
        </div>
      </div>
      <div class="sticky">
        <pre id="f-out" tabindex="0" aria-label="Change log entry preview" aria-live="polite" style="max-height:640px"></pre>
        <div class="btnrow"><button class="btn primary" type="button" id="f-copy">Copy change log entry</button><span class="small muted" id="f-msg"></span></div>
        <p class="small muted">Steps 2 to 4 are added to the same entry after the test: the result against each bar, the decision and its date.</p>
      </div>
    </div>
  </section>

  <section class="blk" aria-labelledby="h-ex">
    <div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:center"><h2 id="h-ex">Worked example: PR-2026-11-01</h2><span class="pill real">Real change, run Nov 2026</span></div>
    <div class="grid2">
      <div class="card stack"><h3>Proposal · v2.0 → v2.1</h3>
        <p><b>What the last run showed.</b> <span class="muted">{ex['saw']}</span></p>
        <p><b>Likely cause.</b> <span class="muted">{ex['cause']}</span></p>
        <div><b>The change.</b><ol class="plain muted" style="margin-top:4px"><li>A target word count and a paragraph plan, in place of a bare range.</li><li>A per-sentence cap (top of the range plus 8 words), with an instruction to split long sentences.</li><li>Vocabulary guidance by grade band, in place of a bare Lexile number.</li><li>A self-check on counts before returning.</li></ol></div>
        <p><b>What stays the same.</b> <span class="muted">{ex['same']}</span></p></div>
      <div class="stack">
        <div class="tablewrap"><table><thead><tr><th scope="col">Bar, set before the run</th><th scope="col">Bar</th><th scope="col">Result</th></tr></thead><tbody>{bars}</tbody></table></div>
        <div class="callout"><b>Decision, Nov 15, 2026: approved with conditions.</b> Approved for the next pilot batch. First, run v2.1 on fresh briefs it wasn't designed from. Second, open the next change to center readability, because v2.1 overcorrected and now reads slightly easy.</div>
        <p class="small muted">The full before-and-after scores are on the case study's <a href="{CASE}#evidence">Evidence</a> tab.</p>
      </div>
    </div>
  </section>

  <section class="blk" aria-labelledby="h-log">
    <h2 id="h-log">Change log</h2>
    <div class="tablewrap"><table>
      <thead><tr><th scope="col">ID</th><th scope="col">Change</th><th scope="col">Status</th><th scope="col">Date</th></tr></thead>
      <tbody>
        <tr><td><b>PR-2026-11-01</b></td><td>v2.0 → v2.1 · grade fit for grades 3-12</td><td><span class="pill green">Approved with conditions</span></td><td>Nov 15, 2026</td></tr>
        <tr><td><b>Next</b></td><td>v2.1 → v2.2 · center readability, after the holdout run</td><td><span class="pill illus">Planned, not yet proposed</span></td><td>Dec 2026</td></tr>
      </tbody>
    </table></div>
  </section>
"""

JS = "const EX=" + json.dumps(EXAMPLE) + ";\n" + r"""
const F=id=>document.getElementById('f-'+id);
const FIELDS=['id','title','by','date','from','to','saw','cause','change','same','test','rollback'];
let bars=[["",""]];
function renderBars(){
  F('bars').innerHTML=bars.map((b,i)=>`<div class="barrow"><input type="text" aria-label="Measure ${i+1}" data-bar="${i}" data-k="0" value="${esc(b[0])}" placeholder="Measure"><input type="text" aria-label="Bar ${i+1}" data-bar="${i}" data-k="1" value="${esc(b[1])}" placeholder="Bar"><button type="button" aria-label="Remove bar ${i+1}" data-rm="${i}">×</button></div>`).join('');
}
function v(k){return F(k).value.trim()}
function entry(){
  const ph=(s,p)=>s||`[${p}]`;
  const change=v('change')?v('change').split('\n').map(l=>l.trim()).filter(Boolean).map(l=>/^(\d+\.|-)\s/.test(l)?l:'- '+l).join('\n'):'- [the exact change]';
  const b=bars.filter(x=>x[0]||x[1]);
  const table=b.length?b.map(x=>`| ${ph(x[0],'measure')} | ${ph(x[1],'bar')} | _pending_ |`).join('\n'):'| [measure] | [bar] | _pending_ |';
  return `## ${ph(v('id'),'PR-YYYY-MM-NN')} · ${ph(v('from'),'current')} → ${ph(v('to'),'proposed')} · ${ph(v('title'),'short title')}

**Requested by:** ${ph(v('by'),'name and role')} · **Date:** ${ph(v('date'),'YYYY-MM-DD')} · **Status:** Proposed

### 1. Propose
**What the last run showed.** ${ph(v('saw'),'numbers from the validator report')}

**Likely cause.** ${ph(v('cause'),'what produces the miss')}

**The change.**
${change}

**What stays the same.** ${ph(v('same'),'everything else')}

**Approval bar (set before the run):**

| Measure | Bar | Result |
|---|---|---|
${table}

### 2. Test
${ph(v('test'),'test set')}

### 3. Approve
_Decision, date and any conditions, by the Managing Editor, ELA._

### 4. Roll back
${ph(v('rollback'),'roll-back plan')}
`;
}
function render(){F('out').textContent=entry();}
document.querySelector('.form').addEventListener('input',e=>{
  const t=e.target; if(t.dataset.bar!=null){bars[+t.dataset.bar][+t.dataset.k]=t.value;} render();
});
F('bars').addEventListener('click',e=>{const r=e.target.closest('[data-rm]'); if(!r) return; bars.splice(+r.dataset.rm,1); if(!bars.length) bars=[["",""]]; renderBars(); render();});
F('addbar').addEventListener('click',()=>{bars.push(["",""]); renderBars(); render();});
F('load').addEventListener('click',()=>{FIELDS.forEach(k=>F(k).value=EX[k==='from'?'from':k==='to'?'to':k]||''); bars=EX.bars.map(x=>x.slice()); renderBars(); render();});
F('clear').addEventListener('click',()=>{FIELDS.forEach(k=>F(k).value=''); bars=[["",""]]; renderBars(); render();});
F('copy').addEventListener('click',()=>copyText(entry(),F('msg')));
renderBars(); render();
"""

html = head("Riverlark Prompt Change Process", EXTRA) + header("change") + f"""
<main class="wrap">
  <div class="hero">
    <span class="eyebrow">Enablement · For everyone who changes prompts</span>
    <h1>Prompt change process</h1>
    <p class="lede">No prompt reaches production without a written proposal, a test on the sample set, a recorded decision and a way back. The same steps apply to validator rules. Used once so far, for PR-2026-11-01.</p>
    <div class="pills"><span class="pill green">Process in use</span><span class="pill real">Worked example is the real v2.0 → v2.1 change</span></div>
  </div>
  {body()}
  {footer("change")}
</main>
""" + tail(JS)

open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "portfolio-static", "prompt-change-process", "index.html"), "w").write(html)
print("ok", len(html))
