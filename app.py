#!/usr/bin/env python3
"""GardenPlanner AI — hosted web demo (pure Python standard library).

Serves a small bilingual (English default, 中文 toggle) planning UI:

    GET  /            -> the planning form + result cards
    GET  /api/plan?city=..&month=..&space=..&level=..&lang=en|zh -> JSON
    GET  /healthz     -> liveness probe for Render / uptime checks

Design notes:
- Zero dependencies (no gradio, no flask) so the free Render instance
  builds in seconds and the demo can never break on a dependency bump.
- Reads PORT from the environment and binds 0.0.0.0 (platform contract).
- The knowledge base lives in main.py (CLI) and i18n.py (English layer);
  this file is presentation only.
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import urllib.parse

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import main as GP
import i18n as I18N

PORT = int(os.environ.get("PORT", "10000"))
CITY_CHOICES = sorted({c.title() for c in GP.CITIES})

_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GardenPlanner AI — offline gardening planner</title>
<style>
:root{--green:#2e7d32;--green-d:#1b5e20;--sand:#f6f3ea;--ink:#22301f;--line:#d9d2bd}
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--sand);color:var(--ink)}
.wrap{max-width:880px;margin:0 auto;padding:1.6rem 1.2rem 3rem}
h1{font-size:1.5rem;margin:.2rem 0}
h1 .leaf{color:var(--green)}
.sub{color:#5c6b58;font-size:.92rem;margin-bottom:1.2rem}
.bar{display:flex;gap:.6rem;flex-wrap:wrap;align-items:end;background:#fff;border:1px solid var(--line);
     border-radius:12px;padding:1rem;box-shadow:0 1px 3px rgba(0,0,0,.05)}
.fld{display:flex;flex-direction:column;gap:.25rem;font-size:.78rem;color:#5c6b58}
.fld input,.fld select{padding:.5rem .6rem;border:1px solid var(--line);border-radius:8px;font-size:.95rem;background:#fff;min-width:9rem}
button{padding:.55rem 1.1rem;border:0;border-radius:8px;background:var(--green);color:#fff;font-size:.95rem;cursor:pointer}
button:hover{background:var(--green-d)}
button.ghost{background:#fff;color:var(--green);border:1px solid var(--green)}
#lang{margin-left:auto}
.head{display:flex;justify-content:space-between;align-items:baseline;margin:1.4rem 0 .6rem}
.head h2{margin:0;font-size:1.15rem}
.meta{color:#5c6b58;font-size:.85rem}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:.9rem 1rem;margin-bottom:.7rem}
.card h3{margin:0 0 .35rem;font-size:1.02rem;display:flex;gap:.5rem;align-items:center}
.tag{font-size:.72rem;background:#e8f1e6;color:var(--green-d);border-radius:99px;padding:.12rem .55rem;font-weight:600}
.row{font-size:.88rem;margin:.18rem 0;color:#3d4a3a}
.row b{color:#22301f;font-weight:600}
.tasks{background:#fff;border:1px solid var(--line);border-radius:12px;padding:.9rem 1rem}
.tasks li{margin:.3rem 0;font-size:.92rem}
.empty{color:#5c6b58;font-style:italic}
.foot{margin-top:2rem;color:#7a8778;font-size:.8rem;text-align:center}
.spin{color:#5c6b58}
@media(max-width:640px){.fld input,.fld select{min-width:0;width:100%}.bar{flex-direction:column;align-items:stretch}#lang{margin-left:0}}
</style>
</head>
<body>
<div class="wrap">
  <h1><span class="leaf">🌱</span> GardenPlanner AI</h1>
  <div class="sub" id="sub">Offline gardening planner — built-in agronomy knowledge base, zero network, zero accounts.</div>
  <div class="bar">
    <label class="fld" id="l-city">City<input id="city" list="cities" value="Shanghai" autocomplete="off">
      <datalist id="cities">__CITIES__</datalist></label>
    <label class="fld" id="l-month">Month<select id="month">__MONTHS__</select></label>
    <label class="fld" id="l-space">Space<select id="space">
      <option value="any">any</option><option value="balcony">balcony</option>
      <option value="garden">garden</option><option value="indoor">indoor</option></select></label>
    <label class="fld" id="l-level">Skill level<select id="level">
      <option value="any">any</option><option value="easy">easy</option>
      <option value="medium">medium</option><option value="hard">hard</option></select></label>
    <button id="go">Plan my month</button>
    <button id="lang" class="ghost">中文</button>
  </div>
  <div class="head"><h2 id="out-title">Your plan</h2><span class="meta" id="out-meta"></span></div>
  <div id="out"><span class="spin">…</span></div>
  <div class="foot">Rule engine, fully offline · optional local Ollama open-weight rewrite in the CLI ·
  <a href="https://github.com/Zhiyilang/hacktoberfest-2026-ai">open source (MIT)</a></div>
</div>
<script>
const T={
 en:{sub:"Offline gardening planner — built-in agronomy knowledge base, zero network, zero accounts.",
     city:"City",month:"Month",space:"Space",level:"Skill level",go:"Plan my month",
     title:"Your plan",none:"Nothing matches — tend what you have or plan ahead.",lang:"中文"},
 zh:{sub:"离线园艺规划器 — 内置农艺知识库，零网络、零账号。",
     city:"城市",month:"月份",space:"空间",level:"难度",go:"生成计划",
     title:"你的计划",none:"本月暂无完全匹配项 — 养护现有作物或规划下月。",lang:"EN"}};
let lang="en";
const $=id=>document.getElementById(id);
const MONTHS=["January","February","March","April","May","June","July","August","September","October","November","December"];
const MONTHS_ZH=["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"];
function fillMonths(){const s=$("month");s.innerHTML="";const names=lang==="en"?MONTHS:MONTHS_ZH;
 for(let i=0;i<12;i++){const o=document.createElement("option");o.value=i+1;o.textContent=names[i];s.appendChild(o);}
 s.value=String(__MONTH__);}
function esc(s){return String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]))}
function applyT(){const t=T[lang];
 $("sub").textContent=t.sub;$("l-city").firstChild.textContent=t.city;$("l-month").firstChild.textContent=t.month;
 $("l-space").firstChild.textContent=t.space;$("l-level").firstChild.textContent=t.level;
 $("go").textContent=t.go;$("lang").textContent=t.lang;$("out-title").textContent=t.title;fillMonths();}
function render(d){
 const L=d.labels||{};
 if(!d.picks.length){$("out").innerHTML='<div class="card empty">'+esc(L.no_picks||T[lang].none)+'</div>';}
 else{
  $("out").innerHTML=d.picks.map(p=>{
   const zh=p.name_zh?` <span class="tag">${esc(p.name_zh)}</span>`:"";
   return `<div class="card"><h3>${esc(p.name)}${zh}<span class="tag">${esc(p.level)} · ${esc(p.space)}</span></h3>`+
    `<div class="row"><b>${esc(L.companions||"Companions")}:</b> ${p.companions.map(esc).join(", ")||"—"}</div>`+
    `<div class="row"><b>${esc(L.foes||"Keep apart")}:</b> ${p.foes.map(esc).join(", ")||"—"}</div>`+
    `<div class="row"><b>${esc(L.tip||"Tip")}:</b> ${esc(p.tip)}</div>`+
    `<div class="row"><b>${esc(L.pests||"Pests")}:</b> ${esc(p.pests)}</div></div>`;}).join("");}
 const tasks=(d.tasks||[]).map(t=>`<li>☐ ${esc(t)}</li>`).join("");
 const note=d.city_note?` · ${esc(d.city_note)}`:"";
 $("out-meta").textContent=`${esc(d.city)}${note} · ${esc(d.season)} · ${esc(d.hemisphere)} · ${esc(d.zone_label||"zone")} ~${d.zone}`;
 $("out").insertAdjacentHTML("beforeend",
   `<div class="tasks"><b>${esc(L.tasks||"This month's checklist")}</b><ul>${tasks}</ul></div>`);}
async function plan(){
 $("out").innerHTML='<span class="spin">…</span>';
 const q=new URLSearchParams({city:$("city").value||"Shanghai",month:$("month").value,
   space:$("space").value,level:$("level").value,lang});
 try{const r=await fetch("/api/plan?"+q);const d=await r.json();
  if(!d.ok){$("out").innerHTML='<div class="card empty">'+esc(d.error||"error")+'</div>';return;}
  render(d.plan);}
 catch(e){$("out").innerHTML='<div class="card empty">network error</div>';}}
$("go").onclick=plan;$("lang").onclick=()=>{lang=lang==="en"?"zh":"en";applyT();plan();};
applyT();plan();
</script>
</body>
</html>
"""


def _month_options() -> str:
    names = ["January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"]
    return "".join('<option value="%d">%s</option>' % (i + 1, n) for i, n in enumerate(names))


def _page_html() -> bytes:
    now_month = _dt.datetime.now().month
    html = (_PAGE
            .replace("__CITIES__", "".join("<option value='%s'>" % c for c in CITY_CHOICES))
            .replace("__MONTHS__", _month_options())
            .replace("__MONTH__", str(now_month)))
    return html.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    server_version = "GardenPlanner/1.0"

    def log_message(self, fmt, *args):  # keep the demo logs quiet
        pass

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code: int = 200) -> None:
        self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"),
                   "application/json; charset=utf-8")

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self._send(200, _page_html(), "text/html; charset=utf-8")
            return
        if parsed.path == "/healthz":
            self._json({"ok": True, "service": "gardenplanner-ai"})
            return
        if parsed.path == "/api/plan":
            self._api_plan(urllib.parse.parse_qs(parsed.query))
            return
        self._json({"ok": False, "error": "not found"}, 404)

    # -- API ----------------------------------------------------------------
    def _api_plan(self, qs: dict) -> None:
        def one(key, default):
            v = qs.get(key) or [default]
            return urllib.parse.unquote(v[0])

        city = one("city", "Shanghai")[:64] or "Shanghai"
        try:
            month = int(one("month", str(_dt.datetime.now().month)))
        except ValueError:
            month = _dt.datetime.now().month
        space = one("space", "any")
        level = one("level", "any")
        lang = one("lang", "en")

        if not 1 <= month <= 12:
            self._json({"ok": False, "error": "month must be 1-12"}, 400)
            return
        if space not in ("any", "balcony", "garden", "indoor"):
            self._json({"ok": False, "error": "unknown space"}, 400)
            return
        if level not in ("any", "easy", "medium", "hard"):
            self._json({"ok": False, "error": "unknown level"}, 400)
            return

        plan = GP.build_plan(city, month, space, level)
        if lang == "zh":
            # Chinese view: reuse the CLI renderer as preformatted text.
            text = GP.render(plan)
            self._json({"ok": True, "lang": "zh", "text": text,
                        "plan": {"picks": [{"name": p["name"]} for p in plan["picks"]],
                                 "tasks": plan["tasks"]}})
            return
        en = I18N.en_plan(plan)
        en["zone_label"] = "Hardiness zone"
        self._json({"ok": True, "lang": "en", "plan": en})


def make_server(port: int = 0, host: str = "127.0.0.1") -> ThreadingHTTPServer:
    """Build (but do not start) the server — used by tests and __main__."""
    return ThreadingHTTPServer((host, port), Handler)


def main() -> int:
    srv = make_server(PORT, "0.0.0.0")
    print("GardenPlanner AI web demo listening on 0.0.0.0:%d" % srv.server_address[1],
          flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
