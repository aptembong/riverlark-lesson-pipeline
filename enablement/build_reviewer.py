import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

EXTRA = r"""
.desk{max-width:860px;margin:0 auto;background:#fff;border:2px solid var(--river);border-radius:20px;padding:24px;display:flex;flex-direction:column;gap:16px}
.desk h2{font-size:1.25rem}
.desk .row{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
@media (max-width:640px){.desk .row{grid-template-columns:1fr}}
.desk .cell{border-radius:12px;padding:10px 12px;font-size:.9rem}
.desk .cell b{display:block;margin-bottom:2px}
.cell.green{background:var(--green-soft)}.cell.yellow{background:var(--yellow-soft)}.cell.red{background:var(--red-soft)}
.desk table{font-size:.88rem}.desk th,.desk td{padding:7px 10px}
.desk ol{margin:0;padding-left:20px;font-size:.9rem;columns:2;column-gap:28px}
@media (max-width:640px){.desk ol{columns:1}}
.rubric{counter-reset:r;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
@media (max-width:640px){.rubric{grid-template-columns:1fr}}
.rubric div{background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 14px;display:flex;gap:10px}
.rubric div::before{counter-increment:r;content:counter(r);flex:none;width:26px;height:26px;border-radius:50%;background:var(--sky-soft);color:var(--river);font-weight:800;display:grid;place-items:center;font-size:.85rem}
.rubric div.rep::before{background:var(--green-soft);color:var(--green)}
.formula{display:flex;gap:8px;flex-wrap:wrap;align-items:center;font-weight:700}
.formula span{background:var(--sky-soft);color:var(--river);padding:6px 12px;border-radius:999px}
@media print{header.top,footer.pg,.viewtabs,.noprint{display:none!important}body{background:#fff}.desk{border:1px solid #999}}
"""

CHECKS = [
 ("Schema", "Every field the lesson needs is there, including the four lesson hooks.", "The draft is broken. It goes red and is redrafted, so you won't see it.", "Nothing. If one ever reaches you, report a wrong lane."),
 ("Length", "Word count, against the grade's target range plus or minus 10 words.", "The passage is too thin to carry the skill, or too long for the grade.", "Close to range and still teaching well: approve with notes. Far off: regenerate."),
 ("Average sentence", "Words per sentence, against the grade's range plus or minus 2. Not checked for poems.", "Sentences are too long for the grade, which makes the text harder than its words.", "Name the paragraphs with the longest sentences in your note. Regenerate if most of it runs long."),
 ("Skill evidence", "How many skill examples the passage carries, and whether each one is quoted exactly.", "Too few examples (yellow), or a quote that isn't in the passage word for word (red).", "The script counts examples. You decide whether each one actually shows the skill."),
 ("Readability estimate", "A free Flesch-Kincaid grade estimate, against the grade's expected range.", "Words or sentences sit above or below the grade. It's an estimate and only routes the passage.", "Run the licensed Lexile check. Lexile decides. If they disagree, log it."),
 ("Representation flags", "Words on the red and yellow lists (deficit framing, stereotypes, ableist language, savior stories).", "A word that often signals a problem. Red-list words, or three or more yellow-list words, send it red.", "Read the whole sentence. A list can only match words. Whether the story treats people well is your call."),
]

DECISIONS = [
 ("Approve", "Meets the rubric and the Lexile check is in range.", "Optional", "Moves to the lesson script (Stage 5)."),
 ("Approve with notes", "Good passage, small fixes: a few word choices, one long sentence, a clearer example.", "Required: what to change and where", "A writer makes the fix, the checks run again, then it moves to the script."),
 ("Regenerate", "A redraft can fix it: too short, sentences too long, a skill named but not taught.", "Required: what the next draft must fix", "Goes back to Claude with your note, then through the checks again."),
 ("Reject", "A redraft won't fix it: the brief is wrong, the approach doesn't fit the standard, or you have an originality concern.", "Required: why it can't be redrafted", "Stops. The Managing Editor sees every reject in the weekly send-back review."),
]

RUBRIC_FIT = ["The skill is taught, not just mentioned", "Clear enough for the grade", "Fits the grade's length and reading level"]
RUBRIC_REP = ["The main character solves their own problem", "Culture, family and place read as everyday life", "No stereotypes or deficit language", "Disability, if present, uses person-first or neutral words"]

def guide_view():
    checks = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a,b,c,d in CHECKS)
    dec = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a,b,c,d in DECISIONS)
    rub = "".join(f"<div>{t}</div>" for t in RUBRIC_FIT) + "".join(f'<div class="rep">{t}</div>' for t in RUBRIC_REP)
    return f"""
<div class="view" id="guide">
  <section class="blk" aria-labelledby="h-queue" style="margin-top:28px">
    <h2 id="h-queue">Your queue at a glance</h2>
    <p class="lede">The automated checks sort every passage before you see it. The lane tells you how closely to read. It never makes the decision for you.</p>
    <div class="grid4">
      <div class="lane green"><span class="pill green"><span class="dot"></span>Green</span><h3>Spot-check</h3><span class="time">About 30 seconds · 10% random sample</span><p>Every check passed. A random 10% of greens come to you. Skim the passage, read the highlighted examples, and run the rubric. If anything feels off, pull it into a full review.</p></div>
      <div class="lane yellow"><span class="pill yellow"><span class="dot"></span>Yellow</span><h3>Full review</h3><span class="time">About 3 minutes · every yellow</span><p>A fit issue, or one or two yellow-list words. Read the whole passage, the check results and the full rubric, then choose a decision.</p></div>
      <div class="lane red"><span class="pill red"><span class="dot"></span>Red</span><h3>Not in your queue</h3><span class="time">Redrafted automatically</span><p>A red-list word, three or more yellow-list words, a broken schema, or a misquoted example. It's redrafted and checked again. You see reds only in the weekly send-back review.</p></div>
      <div class="lane info"><span class="pill info">Script</span><h3>Lesson script review</h3><span class="time">About 5 minutes · every lesson</span><p>After a passage is approved, you review its lesson script before video. See the <a href="{VIDEO}">video stage</a> for what a finished script looks like.</p></div>
    </div>
    <p class="muted small">Times are planning estimates from the quality plan, used in the case study's editor-hours calculator.</p>
  </section>

  <section class="blk" aria-labelledby="h-week">
    <h2 id="h-week">How the week runs</h2>
    <div class="grid3">
      <div class="card stack"><h3>Work oldest yellow first</h3><p class="muted">Yellows hold up a batch. Clear them before spot-checks, oldest first, so no lesson waits more than two working days.</p></div>
      <div class="card stack"><h3>Stop at the time cap</h3><p class="muted">About 12 editor hours a week across three editors during production. When you reach your share, stop and tell the Managing Editor what's left. Tired reading misses things.</p></div>
      <div class="card stack"><h3>Calibrate before production</h3><p class="muted">All three editors decide the same 10 sample passages on their own, then compare. Talk through every disagreement before the first batch. Repeat when the prompt changes.</p></div>
    </div>
  </section>

  <section class="blk" aria-labelledby="h-checks">
    <h2 id="h-checks">Reading the automated results</h2>
    <p class="lede">Each passage arrives with six check results. Here's what each one measures and what to do when it misses. The rules match <code>pipeline/validate.py</code> and are fixed before a batch runs.</p>
    <div class="tablewrap"><table>
      <thead><tr><th scope="col">Check</th><th scope="col">What it measures</th><th scope="col">What a miss usually means</th><th scope="col">What you do</th></tr></thead>
      <tbody>{checks}</tbody>
    </table></div>
    <div class="callout"><b>Lexile decides readability.</b> The Flesch-Kincaid number only routes passages. Riverlark's licensed Lexile analyzer runs before you approve, against the brief's Lexile range. If the estimate and Lexile disagree, Lexile wins, and you log the gap so the team can track it by grade band.</div>
  </section>

  <section class="blk" aria-labelledby="h-rubric">
    <h2 id="h-rubric">The rubric</h2>
    <p class="lede">Seven checks for every passage you open. On a full review, also score teaching quality from 1 to 5. Checks 4 to 7 come from the representation framework and need a person every time.</p>
    <div class="rubric">{rub}</div>
    <div class="grid2">
      <div class="example"><b>Teaching quality, 1 to 5</b>5 means a teacher could use it tomorrow as is. 3 means it teaches the skill but needs your notes. 1 means it doesn't teach the skill.</div>
      <div class="example"><b>Where these come from</b>The representation framework on the case study's <a href="{CASE}#quality">Quality and governance</a> tab. The same rules are written into the prompt.</div>
    </div>
  </section>

  <section class="blk" aria-labelledby="h-decide">
    <h2 id="h-decide">Choosing a decision</h2>
    <div class="tablewrap"><table>
      <thead><tr><th scope="col">Decision</th><th scope="col">Use it when</th><th scope="col">Note</th><th scope="col">What happens next</th></tr></thead>
      <tbody>{dec}</tbody>
    </table></div>
    <div class="card stack">
      <h3>Writing a note the writer can act on</h3>
      <div class="formula"><span>What to change</span>+<span>Where</span>+<span>Why</span></div>
      <div class="grid2">
        <div class="example"><b>Hard to act on</b>Too easy. Fix the reading level.</div>
        <div class="example"><b>Easy to act on (illustrative, RL-TX-E1-016)</b>Strong theme and setting work, and Teresa makes her own choice. Readability estimate is just under the grade 9 floor, so raise a few word choices to grade level in paragraphs 1 and 2, then confirm with the licensed Lexile check before video.</div>
      </div>
    </div>
  </section>

  <section class="blk" aria-labelledby="h-overrule">
    <h2 id="h-overrule">When to overrule the lane</h2>
    <p class="lede">You always can. A lane is the checks' best guess. When yours is different, make your call and log the wrong lane, so the rules get better instead of you working around them.</p>
    <div class="grid3">
      <div class="card stack"><span class="pill green"><span class="dot"></span>Green, but…</span><h3>Pull it into a full review</h3><p class="muted">Every check passed, but an example is quoted exactly and still doesn't show the skill, or the character is rescued by someone else. Checks can't see either one.</p></div>
      <div class="card stack"><span class="pill yellow"><span class="dot"></span>Yellow, but fine</span><h3>Approve it</h3><p class="muted">The estimate missed but Lexile is in range, or the passage is a few words over and reads well. Approve and log that the check disagreed with you.</p></div>
      <div class="card stack"><span class="pill info">Flag, but fair</span><h3>Approve and report the list</h3><p class="muted">A flagged word is used fairly in context. This happened for real: an early validator flagged “authentic” near “culture,” the exact language the framework asks for, so the pattern was removed and the reason recorded in the code.</p></div>
    </div>
    <div class="callout coral"><b>Never change a check yourself.</b> Validator rules change only through the Managing Editor, and only between batches, so a rule is never tuned to the batch it scores. Your wrong-lane reports are the evidence for the next change.</div>
  </section>

  <section class="blk" aria-labelledby="h-report">
    <h2 id="h-report">Report a wrong lane</h2>
    <p class="lede">Fill this in, copy the line, and paste it into the review log. It takes under a minute. The AI Workflow team reads the log every week.</p>
    <div class="card stack">
      <div class="grid3">
        <div class="field"><label for="w-id">Lesson ID</label><input id="w-id" type="text" placeholder="RL-TX-6-012"></div>
        <div class="field"><label for="w-got">Lane it got</label><select id="w-got"><option>Green</option><option selected>Yellow</option><option>Red</option></select></div>
        <div class="field"><label for="w-should">Lane it should have been</label><select id="w-should"><option selected>Green</option><option>Yellow</option><option>Red</option></select></div>
        <div class="field"><label for="w-check">Which check</label><select id="w-check"><option>Schema</option><option>Length</option><option>Average sentence</option><option>Skill evidence</option><option selected>Readability estimate</option><option>Representation flags</option><option>None (checks passed, judgment didn't)</option></select></div>
        <div class="field"><label for="w-dec">Your decision</label><select id="w-dec"><option>Approve</option><option>Approve with notes</option><option>Regenerate</option><option>Reject</option></select></div>
        <div class="field"><label for="w-lex">Lexile result, if run</label><input id="w-lex" type="text" placeholder="e.g. 820L, in range"></div>
      </div>
      <div class="field"><label for="w-what">What happened, in one sentence</label><input id="w-what" type="text" placeholder="Estimate said too easy, but Lexile is in range and it reads at grade level."></div>
      <pre id="w-out" aria-live="polite"></pre>
      <div class="btnrow"><button class="btn primary" type="button" id="w-copy">Copy log line</button><span class="small muted" id="w-msg"></span></div>
    </div>
  </section>

  <section class="blk" aria-labelledby="h-esc">
    <h2 id="h-esc">Who to bring in</h2>
    <div class="tablewrap"><table>
      <thead><tr><th scope="col">If you see</th><th scope="col">Bring in</th><th scope="col">Meanwhile</th></tr></thead>
      <tbody>
        <tr><td>A representation question you're not sure about</td><td>The representation consultant</td><td>Hold the passage. Don't approve it to keep the batch moving.</td></tr>
        <tr><td>Fewer than 90% of the passages you review in a batch get approved</td><td>Managing Editor. Generation pauses for a prompt change</td><td>Finish the passages already in your queue.</td></tr>
        <tr><td>The same send-back reason three or more times in a week</td><td>Managing Editor and AI Workflow, as a <a href="{url('change')}">prompt change request</a></td><td>Keep deciding each passage on its own.</td></tr>
        <tr><td>A passage that might not be original</td><td>Managing Editor</td><td>Reject with the reason. Don't regenerate it.</td></tr>
        <tr><td>A check that looks broken (a schema error reaching you, a quote marked missing that's there)</td><td>AI Workflow</td><td>Decide the passage on its merits and log the wrong lane.</td></tr>
      </tbody>
    </table></div>
  </section>
</div>
"""

def desk_view():
    dec = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c.split(':')[0]}</td></tr>" for a,b,c,d in DECISIONS)
    rub = "".join(f"<li>{t}</li>" for t in RUBRIC_FIT + RUBRIC_REP)
    return f"""
<div class="view" id="desk-card">
  <div class="desk" style="margin-top:24px" id="desk">
    <div style="display:flex;justify-content:space-between;gap:10px;align-items:center;flex-wrap:wrap"><h2>Riverlark review desk card</h2><span class="muted small">Keep beside the queue</span></div>
    <div class="row">
      <div class="cell green"><b>Green · 30 s · 10% sample</b>Skim, read the examples, run the rubric. Anything off? Full review.</div>
      <div class="cell yellow"><b>Yellow · 3 min · every one</b>Whole passage, check results, full rubric, score 1 to 5.</div>
      <div class="cell red"><b>Red · not yours</b>Redrafted automatically. Seen only in the weekly send-back review.</div>
    </div>
    <div><h3 style="margin-bottom:6px">Rubric</h3><ol>{rub}</ol></div>
    <div class="tablewrap" style="border-radius:12px"><table><thead><tr><th>Decision</th><th>When</th><th>Note</th></tr></thead><tbody>{dec}</tbody></table></div>
    <div class="row">
      <div class="cell" style="background:var(--sky-soft)"><b>Good note</b>What to change + where + why.</div>
      <div class="cell" style="background:var(--sky-soft)"><b>Lexile decides</b>The estimate only routes. Run Lexile before you approve.</div>
      <div class="cell" style="background:var(--coral-soft)"><b>Disagree with a lane?</b>Make your call, then log the wrong lane. Never change a check.</div>
    </div>
    <p class="small muted">Representation doubt: hold and ask the consultant. Same send-back reason 3+ times a week: tell the Managing Editor.</p>
  </div>
  <div class="btnrow noprint" style="justify-content:center;margin-top:16px"><button class="btn primary" type="button" id="d-copy">Copy as text</button><a class="btn ghost" href="#guide">Read the full guide</a><span class="small muted" id="d-msg"></span></div>
</div>
"""

JS = r"""
const W=['w-id','w-got','w-should','w-check','w-dec','w-lex','w-what'].map(id=>document.getElementById(id));
function wline(){
  const [id,got,sh,ck,dec,lex,what]=W.map(e=>e.value.trim());
  const d=new Date().toISOString().slice(0,10);
  return `${d} | ${id||'(lesson ID)'} | wrong lane: ${got} -> should be ${sh} | check: ${ck} | decision: ${dec}${lex?` | Lexile: ${lex}`:''} | ${what||'(what happened)'}`;
}
function wrender(){document.getElementById('w-out').textContent=wline();}
W.forEach(e=>e.addEventListener('input',wrender)); wrender();
document.getElementById('w-copy').addEventListener('click',()=>copyText(wline(),document.getElementById('w-msg')));
document.getElementById('d-copy').addEventListener('click',()=>{
  const t=document.getElementById('desk').innerText.replace(/\n{3,}/g,'\n\n');
  copyText(t,document.getElementById('d-msg'));
});
"""

html = head("Riverlark Reviewer Guide", EXTRA) + header("reviewer") + f"""
<main class="wrap">
  <div class="hero">
    <span class="eyebrow">Enablement · For editors</span>
    <h1>Reviewer guide</h1>
    <p class="lede">How to work the review queue: what each lane means, how to read the automated results, which decision to choose, and when to overrule the lane. The desk card fits beside the queue on one screen.</p>
    <div class="pills"><span class="pill real">Rules match pipeline/validate.py and Lesson Studio</span><span class="pill illus">Times are planning estimates</span></div>
    <nav class="viewtabs" aria-label="Views"><a href="#guide">Full guide</a><a href="#desk-card">Desk card</a></nav>
  </div>
  {guide_view()}
  {desk_view()}
  <p class="small muted" style="margin-top:28px">Want to try it first? Practice on real sample passages in <a href="{url('onboarding')}#practice">onboarding and practice</a>, or review a live draft in <a href="{STUDIO}">Lesson Studio</a>.</p>
  {footer("reviewer")}
</main>
""" + tail(JS)

open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "portfolio-static", "reviewer-guide", "index.html"), "w").write(html)
print("ok", len(html))
