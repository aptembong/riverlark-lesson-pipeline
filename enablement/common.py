"""Shared head, header, nav and footer for the four Riverlark enablement pages."""
import json, os

CASE = "https://claude.ai/artifact/8cQtYZuDdt3jodLvn8Akp1"
STUDIO = "https://claude.ai/artifact/7xML8iRSihrrK4vWzbYCqT"
VIDEO = "https://claude.ai/artifact/Jrp5Xyh2dTitcADGnRmvjT"

_urls_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "urls.json")
URLS = json.load(open(_urls_path)) if os.path.exists(_urls_path) else {}
def url(key):
    return URLS.get(key, "#")

PAGES = [
    ("reviewer", "Reviewer guide"),
    ("onboarding", "Onboarding + practice"),
    ("rollout", "Rollout plan"),
    ("change", "Prompt change process"),
]

LOGO = '<svg viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="12" fill="#FFFFFF"/><path d="M9 34c4-3 7-3 10 0s7 3 10 0 7-3 10 0" fill="none" stroke="#5CC6D8" stroke-width="3" stroke-linecap="round"/><path d="M9 40c4-3 7-3 10 0s7 3 10 0 7-3 10 0" fill="none" stroke="#0E4D64" stroke-width="3" stroke-linecap="round"/><path d="M12 21c5-1 9 1 12 4 2-5 6-9 13-10-3 2-4 4-5 7 3 0 5 1 6 2-3 0-6 1-8 3-4 4-11 5-18-6z" fill="#0E4D64"/><circle cx="33.6" cy="18.6" r="1.1" fill="#FFFFFF"/><path d="M36.8 17.5l4-1.2-3.6 2.4z" fill="#F2765A"/></svg>'

CSS = r"""
:root{--river:#0E4D64;--sky:#5CC6D8;--coral:#F2765A;--mist:#F4F8FA;--ink:#12313D;--muted:#4E6873;--line:#D5E3E9;--card:#fff;
--sky-soft:#E3F5F8;--coral-soft:#FDECE7;--green:#2E7D4F;--green-soft:#E3F2E8;--yellow:#9A6B00;--yellow-soft:#FBF1D6;--red:#B3261E;--red-soft:#FBE4E2;
--font:"Inter",system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color-scheme:light}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
body{margin:0;background:var(--mist);color:var(--ink);font-family:var(--font);font-size:16px;line-height:1.55}
a{color:var(--river)}
h1,h2,h3,h4{margin:0;line-height:1.2;text-wrap:balance}
h1{font-size:clamp(1.9rem,4vw,2.6rem);font-weight:800;letter-spacing:-.02em;color:var(--river)}
h2{font-size:1.5rem;font-weight:800;color:var(--river)}
h3{font-size:1.08rem;font-weight:700}
h4{font-size:.98rem;font-weight:700}
p{margin:0}
:focus-visible{outline:3px solid var(--coral);outline-offset:2px;border-radius:6px}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
header.top{background:var(--river);color:#fff}
.bar{display:flex;align-items:center;gap:14px;padding:14px 0 8px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none}
.brand svg{width:36px;height:36px}
.wordmark{font-weight:700;font-size:1.05rem}.wordmark span{font-weight:500;opacity:.85}
.tool{font-weight:700;padding-left:14px;border-left:1px solid rgba(255,255,255,.35)}
.back{margin-left:auto;color:#fff;font-weight:600;font-size:.9rem}
nav.sub{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;padding-top:4px}
nav.sub::-webkit-scrollbar{display:none}
nav.sub a{color:#D6EEF3;text-decoration:none;font-weight:600;font-size:.9rem;padding:9px 14px;border-radius:10px 10px 0 0;white-space:nowrap}
nav.sub a:hover{color:#fff;background:rgba(255,255,255,.08)}
nav.sub a[aria-current="page"]{background:var(--mist);color:var(--river)}
main.wrap{padding:34px 20px 64px}
section.blk{margin-top:44px;display:flex;flex-direction:column;gap:16px}
.hero{display:flex;flex-direction:column;gap:12px}
.eyebrow{font-size:.8rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.lede{color:var(--muted);font-size:1.08rem;max-width:72ch}
.muted{color:var(--muted)}.small{font-size:.86rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px}
.stack{display:flex;flex-direction:column;gap:12px}
.pill{display:inline-flex;align-items:center;gap:6px;font-size:.78rem;font-weight:700;padding:3px 10px;border-radius:999px;white-space:nowrap}
.pill.green{background:var(--green-soft);color:var(--green)}.pill.yellow{background:var(--yellow-soft);color:var(--yellow)}.pill.red{background:var(--red-soft);color:var(--red)}
.pill.info{background:var(--sky-soft);color:var(--river)}.pill.real{background:var(--coral-soft);color:#9C3A21}.pill.illus{background:#EEF1F3;color:#4E5A61}
.dot{width:8px;height:8px;border-radius:50%;background:currentColor;display:inline-block}
.pills{display:flex;gap:8px;flex-wrap:wrap}
.stack>.pill,.lane>.pill,.st>.pill{align-self:flex-start}
.grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.grid3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.grid4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
@media (max-width:900px){.grid3,.grid4{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.grid2,.grid3,.grid4{grid-template-columns:1fr}}
.lane{border-radius:16px;padding:18px;border:1px solid var(--line);background:#fff;display:flex;flex-direction:column;gap:8px;border-top:6px solid var(--line)}
.lane.green{border-top-color:var(--green)}.lane.yellow{border-top-color:#D9A400}.lane.red{border-top-color:var(--red)}.lane.info{border-top-color:var(--sky)}
.lane .time{font-size:.84rem;font-weight:700;color:var(--muted)}
.tablewrap{overflow-x:auto;background:#fff;border:1px solid var(--line);border-radius:16px}
table{border-collapse:collapse;width:100%;font-size:.94rem}
th,td{text-align:left;vertical-align:top;padding:12px 14px;border-bottom:1px solid var(--line)}
th{font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);background:#FAFCFD}
tr:last-child td{border-bottom:0}
td b{white-space:nowrap}
ul.plain,ol.plain{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:6px}
.btn{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-size:.95rem;padding:10px 20px;border-radius:999px;text-decoration:none;border:2px solid transparent;cursor:pointer;font-family:var(--font);background:none}
.btn.primary{background:var(--coral);color:var(--ink)}.btn.ghost{color:var(--river);border-color:var(--river)}
.btn:disabled{opacity:.45;cursor:not-allowed}
.btnrow{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.callout{border-left:4px solid var(--sky);background:var(--sky-soft);border-radius:0 12px 12px 0;padding:14px 16px}
.callout.coral{border-left-color:var(--coral);background:var(--coral-soft)}
.example{background:#FAFCFD;border:1px dashed var(--line);border-radius:12px;padding:12px 14px;font-size:.94rem}
.example b{display:block;font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:4px}
.field{display:flex;flex-direction:column;gap:4px}
.field label{font-weight:600;font-size:.88rem}
input[type=text],input[type=number],input[type=date],select,textarea{font:inherit;font-size:.94rem;padding:9px 12px;border:1px solid #B9CCD4;border-radius:10px;background:#fff;color:var(--ink);width:100%}
textarea{min-height:76px;resize:vertical}
pre{margin:0;background:#0F2E3A;color:#DDEFF4;border-radius:14px;padding:16px;overflow:auto;font-size:.8rem;line-height:1.5;max-height:480px;white-space:pre-wrap}
code{font-size:.88em;background:#EAF2F5;padding:1px 5px;border-radius:5px}
pre code{background:none;padding:0}
.view{display:none}.view.active{display:block}
.viewtabs{display:flex;gap:8px;flex-wrap:wrap;margin-top:6px}
.viewtabs a{font-weight:700;font-size:.92rem;padding:8px 16px;border-radius:999px;text-decoration:none;border:2px solid var(--river);color:var(--river)}
.viewtabs a[aria-current="page"]{background:var(--river);color:#fff}
.num{font-variant-numeric:tabular-nums}
footer.pg{border-top:1px solid var(--line);margin-top:56px;padding-top:22px;display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.next-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;width:100%}
@media (max-width:760px){.next-grid{grid-template-columns:1fr}}
.next-grid a{display:block;background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 16px;text-decoration:none;color:var(--ink)}
.next-grid a span{display:block;font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.next-grid a b{color:var(--river)}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
"""

def head(title, extra_css=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
/* Riverlark enablement pages: same tokens as the case study, Studio and video stage. One page per audience; a sub-nav joins the four. */
{CSS}
{extra_css}
</style>
</head>
<body>
"""

def header(current):
    links = "".join(
        f'<a href="{url(k)}"{" aria-current=\"page\"" if k == current else ""}>{label}</a>'
        for k, label in PAGES)
    return f"""<header class="top"><div class="wrap">
  <div class="bar">
    <a class="brand" href="{CASE}" aria-label="Riverlark case study">{LOGO}<span class="wordmark">riverlark <span>learning</span></span></a>
    <span class="tool">Enablement</span>
    <a class="back" href="{CASE}#enablement">← Back to case study</a>
  </div>
  <nav class="sub" aria-label="Enablement pages">{links}</nav>
</div></header>
"""

def footer(current):
    cards = "".join(
        f'<a href="{url(k)}"><span>Enablement</span><b>{label} →</b></a>'
        for k, label in PAGES if k != current)
    return f"""<footer class="pg">
  <div class="next-grid">{cards}</div>
  <div class="btnrow" style="width:100%">
    <a class="btn primary" href="{CASE}#enablement">Back to the case study</a>
    <a class="btn ghost" href="{STUDIO}">Open Lesson Studio</a>
    <span class="muted small">Riverlark Learning is a fictional publisher. Texas, TEKS and STAAR are real. People and decisions marked illustrative are written to show how the process works.</span>
  </div>
</footer>
"""

VIEW_JS = r"""
/* hash views: show the view named in location.hash, else the first */
(function(){
  const views=[...document.querySelectorAll('.view')], tabs=[...document.querySelectorAll('.viewtabs a')];
  if(!views.length) return;
  function show(){
    const h=(location.hash||'').slice(1); const v=views.find(x=>x.id===h)||views[0];
    views.forEach(x=>x.classList.toggle('active',x===v));
    tabs.forEach(a=>{ if(a.getAttribute('href')==='#'+v.id) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current'); });
  }
  window.addEventListener('hashchange',()=>{show();window.scrollTo(0,0)}); show();
})();
async function copyText(text, msgEl){
  try{ await navigator.clipboard.writeText(text); if(msgEl) msgEl.textContent='Copied.'; }
  catch(e){ if(msgEl) msgEl.textContent='Your browser blocked copying. Select the text in the box and copy it.'; }
}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
"""

def tail(js=""):
    return f"<script>{VIEW_JS}\n{js}</script>\n</body>\n</html>\n"
