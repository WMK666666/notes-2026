# -*- coding: utf-8 -*-
"""组装单文件 index.html：双模块（速查 40 卡 / 手册 79 题）· 深色 · 原生折叠 · 可搜索"""
import html as H
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import part0
import part1
import part2
import recite_data
import handbook_data as HB

RECITE = recite_data.RECITE

# 备查卡：内容是清单 / 工具表 / 自检项，对着查有用，但没法当回答念。
# 渲染成橙色「备查 · 别照着念」，且不进背诵模式。
REF_ONLY = {"Q0.7", "Q0.9", "Q2.11", "Q2.12"}

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "index.html")

TITLE = "场景题与项目表达 · 速查"
SUBTITLE = "两个模块：速查 40 卡 · 手册 79 题"

CSS = r"""
:root{
  --bg:#0d1117; --bg2:#161b22; --bg3:#1c2128; --line:#30363d; --line2:#21262d;
  --fg:#e6edf3; --dim:#8b949e; --dim2:#6e7681;
  --blue:#58a6ff; --orange:#d29922; --red:#f85149; --green:#3fb950; --purple:#bc8cff;
  --fg2:#c9d1d9; --strong:#ffffff; --red2:#ff9b95; --amber2:#e3b341;
  --purple2:#d2a8ff; --green2:#9fd8a8; --okfg:#7ee08a;
  --hover:rgba(255,255,255,.02); --hover2:rgba(255,255,255,.02); --hover3:rgba(255,255,255,.015);
  --headbg:rgba(13,17,23,.95);
  --fs:16px;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg);color:var(--fg)}
body{font-family:-apple-system,"Segoe UI","Microsoft YaHei",system-ui,sans-serif;font-size:var(--fs);line-height:1.72;-webkit-text-size-adjust:100%;transition:background .18s,color .18s}
body.small{--fs:14.5px}
body.big{--fs:17.5px}

/* ---------- 浅色主题 ---------- */
body.light{
  --bg:#ffffff; --bg2:#f6f8fa; --bg3:#eef1f4; --line:#cfd6dd; --line2:#e1e6eb;
  --fg:#1f2328; --dim:#59636e; --dim2:#7d8896;
  --blue:#0969da; --orange:#9a6700; --red:#cf222e; --green:#1a7f37; --purple:#8250df;
  --fg2:#24292f; --strong:#101418; --red2:#cf222e; --amber2:#8a5a00;
  --purple2:#8250df; --green2:#1a7f37; --okfg:#1a7f37;
  --hover:rgba(0,0,0,.035); --hover2:rgba(0,0,0,.03); --hover3:rgba(0,0,0,.02);
  --headbg:rgba(255,255,255,.92);
}
.wrap{max-width:960px;margin:0 auto;padding:0 20px}

/* ---------- 顶栏 ---------- */
header{position:sticky;top:0;z-index:50;background:var(--headbg);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.htop{display:flex;align-items:center;gap:12px;padding:11px 0 9px;flex-wrap:wrap}
.brand{font-size:1em;font-weight:700;letter-spacing:.02em;white-space:nowrap}
.brand em{font-style:normal;color:var(--dim);font-weight:400;font-size:.76em;margin-left:10px}
.tools{margin-left:auto;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
input#q{width:210px;background:var(--bg3);border:1px solid var(--line);color:var(--fg);border-radius:8px;padding:7px 11px;font-size:.86em;font-family:inherit;outline:none}
input#q:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(88,166,255,.12)}
input#q::placeholder{color:var(--dim2)}
.btn{background:var(--bg3);border:1px solid var(--line);color:var(--dim);border-radius:8px;padding:7px 11px;font-size:.82em;cursor:pointer;font-family:inherit;transition:.15s;white-space:nowrap}
.btn:hover{color:var(--fg);border-color:var(--dim2)}
.btn.recite-btn.on{background:rgba(63,185,80,.15);border-color:var(--green);color:var(--green)}
.btn.recite-btn.on:hover{color:var(--green)}

/* 两个大模块 */
.modes{display:flex;gap:7px;padding-bottom:9px;flex-wrap:wrap}
.mode-btn{background:var(--bg2);border:1px solid var(--line);color:var(--dim);border-radius:9px;padding:8px 15px;font-size:.88em;cursor:pointer;font-family:inherit;transition:.15s;display:flex;align-items:center;gap:7px}
.mode-btn b{font-weight:700}
.mode-btn span{font-size:.85em;color:var(--dim2)}
.mode-btn:hover{color:var(--fg);border-color:var(--dim2)}
.mode-btn.on{background:rgba(88,166,255,.13);border-color:var(--blue);color:var(--blue)}
.mode-btn.on span{color:rgba(88,166,255,.7)}

.tabs{display:flex;gap:6px;overflow-x:auto;padding-bottom:9px;scrollbar-width:none}
.tabs::-webkit-scrollbar{display:none}
.tab{font-size:.8em;color:var(--dim);text-decoration:none;padding:5px 11px;border-radius:999px;border:1px solid var(--line2);white-space:nowrap}
.tab:hover{color:var(--fg);border-color:var(--dim2)}

/* ---------- 板块 ---------- */
main{padding:24px 0 80px}
.hero{padding:6px 0 20px;border-bottom:1px solid var(--line2);margin-bottom:24px}
.hero h1{margin:0 0 6px;font-size:1.45em}
.hero p{margin:0;color:var(--dim);font-size:.88em}
.hero .note{margin-top:12px;font-size:.84em;color:var(--dim);border-left:2px solid var(--line);padding-left:12px}

section.blk{margin-bottom:36px;scroll-margin-top:150px}
.blkhead{margin-bottom:4px}
.blkhead h2{margin:0;font-size:1.14em}
.blksub{color:var(--dim);font-size:.84em;margin:0 0 14px}

/* ---------- 卡片 ---------- */
details.card{background:var(--bg2);border:1px solid var(--line2);border-radius:10px;margin-bottom:9px;overflow:hidden;transition:border-color .15s}
details.card:hover{border-color:var(--line)}
details.card.hide{display:none}
summary{list-style:none;cursor:pointer;padding:13px 16px;display:flex;align-items:center;gap:11px;user-select:none}
summary::-webkit-details-marker{display:none}
summary:hover{background:var(--hover)}
.qid{font-family:ui-monospace,Consolas,monospace;font-size:.76em;color:var(--dim2);min-width:44px;flex:none}
.qt{font-size:.95em;font-weight:600;flex:1;line-height:1.5}
.tag{font-size:.68em;padding:1px 7px;border-radius:4px;flex:none;letter-spacing:.04em}
.tag.must{color:var(--red);background:rgba(248,81,73,.12);border:1px solid rgba(248,81,73,.3)}
.tag.core{color:var(--orange);background:rgba(210,153,34,.12);border:1px solid rgba(210,153,34,.3)}
.tag.todo{color:var(--purple);background:rgba(188,140,255,.12);border:1px solid rgba(188,140,255,.3)}
.chev{color:var(--dim2);font-size:1.1em;transition:transform .2s;flex:none}
details[open] .chev{transform:rotate(90deg)}
.cbody{padding:2px 16px 18px;border-top:1px solid var(--line2)}

/* 段落块 */
.seg{margin-top:15px}
.lab{display:inline-block;font-size:.7em;letter-spacing:.1em;color:var(--dim2);margin-bottom:6px}
.seg.ask .lab{color:var(--purple)}
.seg.say .lab{color:var(--blue)}
.seg.det .lab{color:var(--dim)}
.seg.probe .lab{color:var(--orange)}
.seg.red .lab{color:var(--red)}
.seg.ask p{margin:0;font-size:.94em}
.seg.say blockquote{margin:0 0 8px;padding:12px 15px;background:rgba(88,166,255,.07);border-left:2px solid var(--blue);border-radius:0 7px 7px 0;font-size:.95em}
.seg.say blockquote:last-child{margin-bottom:0}
.seg.det{font-size:.9em;color:var(--fg2)}
.seg.det p{margin:0 0 10px}
.seg.det p:last-child{margin-bottom:0}
.seg.probe ul,.seg.red ul{margin:0;padding-left:18px;font-size:.88em;color:var(--dim)}
.seg.red ul{color:var(--red2)}
.seg.probe li,.seg.red li{margin-bottom:7px}
.seg.probe li:last-child,.seg.red li:last-child{margin-bottom:0}

/* ---------- 背诵版 ---------- */
.seg.recite .lab{color:var(--green)}
.vwrap{margin:0;padding:15px 17px;background:rgba(63,185,80,.055);border:1px solid rgba(63,185,80,.24);border-radius:9px;font-size:1em;line-height:1.85;color:var(--fg)}
.vwrap p{margin:0 0 11px}
.vwrap p:last-child{margin-bottom:0}
.vwrap[hidden]{display:none!important}
.vtabs{display:flex;gap:6px;margin:0 0 11px;flex-wrap:wrap}
.vtab{background:var(--bg3);border:1px solid var(--line);color:var(--dim);border-radius:999px;padding:5px 14px;font-size:.8em;font-family:inherit;cursor:pointer;transition:.14s}
.vtab:hover{color:var(--fg);border-color:var(--dim2)}
.vtab.on{background:rgba(63,185,80,.14);border-color:var(--green);color:var(--green);font-weight:700}
.recite-meta{margin-top:7px;font-size:.76em;color:var(--dim2);letter-spacing:.02em}
.recite-meta b{color:var(--green);font-weight:600}

/* 备查版（清单，不背） */
.seg.recite.ref .lab{color:var(--orange)}
.vwrap.ref{background:rgba(210,153,34,.06);border-color:rgba(210,153,34,.32)}
.vwrap.ref .recite-meta b{color:var(--amber2)}
.reftip{margin-top:8px;font-size:.8em;color:var(--amber2);line-height:1.6}

/* ---------- 背诵模式 ---------- */
body.recite-mode{--fs:17px}
body.recite-mode .hero,body.recite-mode .blksub,body.recite-mode .blkhead,body.recite-mode footer{display:none}
body.recite-mode #nav-quick{display:none!important}
body.recite-mode .seg.det,body.recite-mode .seg.probe,body.recite-mode .seg.red{display:none}
body.recite-mode .hide,body.recite-mode .norec{display:none!important}
body.recite-mode main{padding-bottom:110px}
body.recite-mode details.card{background:transparent;border:none;border-bottom:1px dashed var(--line);border-radius:0;margin:0;padding:3vh 0 4vh}
body.recite-mode details.card:hover{background:transparent}
body.recite-mode summary{padding:0 0 12px;cursor:default;pointer-events:none}
body.recite-mode summary:hover{background:transparent}
body.recite-mode .chev{display:none}
body.recite-mode .qid{font-size:.84em;color:var(--dim)}
body.recite-mode .qt{font-size:1.16em}
body.recite-mode .cbody{border-top:none;padding:0}
body.recite-mode .seg.ask{margin-top:0}
body.recite-mode .seg.ask p{font-size:.92em;color:var(--dim)}
body.recite-mode .seg.say blockquote{font-size:.92em;background:transparent;border-left:2px solid var(--line);color:var(--dim);padding:6px 14px}
body.recite-mode .seg.recite{margin-top:16px}
body.recite-mode .vwrap{padding:20px 22px;font-size:1.04em;line-height:2}
.rbar{display:none;position:fixed;left:0;right:0;bottom:0;z-index:80;background:var(--headbg);backdrop-filter:blur(8px);border-top:1px solid var(--line);padding:9px 16px;font-size:.8em;color:var(--dim);justify-content:center;align-items:center;gap:18px}
body.recite-mode .rbar{display:flex!important}
.rbar #rnum{font-family:ui-monospace,Consolas,monospace;color:var(--fg)}
.rbar #rtag{color:var(--green);font-size:.95em;font-weight:600}
.rbar .rhint{color:var(--dim2)}
.rbar .rbtn{background:var(--bg3);border:1px solid var(--line);color:var(--fg);border-radius:8px;padding:6px 16px;font-size:.95em;font-family:inherit;cursor:pointer;transition:.12s}
.rbar .rbtn:hover{border-color:var(--dim2)}
.rbar .rbtn:disabled{opacity:.35;cursor:default}

/* 正文内元素 */
.tw{overflow-x:auto;margin:10px 0;-webkit-overflow-scrolling:touch}
.cbody table{width:100%;border-collapse:collapse;margin:10px 0;font-size:.86em}
.tw table{margin:0}
.cbody th,.cbody td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top;word-break:break-word}
.cbody th{background:var(--bg3);color:var(--dim);font-weight:600;font-size:.95em}
.cbody td{color:var(--fg2)}
.cbody,.cbody p,.cbody li,.cbody blockquote,.cbody td,.cbody th{overflow-wrap:anywhere}
.cbody ul,.cbody ol{margin:8px 0;padding-left:20px}
.cbody li{margin-bottom:5px}
.cbody strong,b{color:var(--strong);font-weight:600}
.cbody blockquote{margin:10px 0;padding:9px 14px;border-left:2px solid var(--line);color:var(--dim);background:var(--hover2)}
.src{display:block;color:var(--dim2);font-size:.86em;margin-top:2px}
.warn{margin-top:12px;padding:11px 14px;border-radius:8px;background:rgba(188,140,255,.08);border:1px solid rgba(188,140,255,.25);font-size:.88em;color:var(--purple2)}
.tip{padding:10px 14px;border-radius:8px;background:rgba(63,185,80,.07);border-left:2px solid var(--green);font-size:.9em;color:var(--green2)}
.note{margin-top:16px;padding:13px 16px;border-radius:9px;background:var(--bg3);border:1px solid var(--line);font-size:.9em}
.note b{color:var(--orange)}
.lead{color:var(--dim);font-size:.9em;margin:0 0 14px}

/* 九问：嵌套折叠 */
details.sub{background:var(--bg3);border:1px solid var(--line);border-radius:9px;margin-bottom:8px}
details.sub summary{padding:11px 14px;font-size:.9em;gap:8px}
details.sub summary .hint{color:var(--dim2);font-size:.84em;margin-left:auto;font-weight:400}
.subbody{padding:4px 14px 14px;border-top:1px solid var(--line2)}
.qa{margin-top:12px;padding-left:12px;border-left:2px solid var(--line)}
.qa .q{font-weight:600;font-size:.92em;margin-bottom:4px}
.qa .a{color:var(--dim);font-size:.86em}
.qa .a b{color:var(--fg);font-weight:600}

/* 打分器 */
.scorer{margin:14px 0;border:1px solid var(--line);border-radius:10px;overflow:hidden}
.dim{display:flex;align-items:center;gap:12px;padding:10px 14px;border-bottom:1px solid var(--line2);flex-wrap:wrap}
.dim:last-child{border-bottom:none}
.dname{min-width:110px;font-size:.88em;font-weight:600}
.dname span{display:block;font-weight:400;font-size:.78em;color:var(--dim2)}
.opts{display:flex;gap:6px;flex-wrap:wrap}
.opts button{background:var(--bg);border:1px solid var(--line);color:var(--dim);border-radius:7px;padding:5px 10px;font-size:.78em;cursor:pointer;font-family:inherit;transition:.12s}
.opts button:hover{color:var(--fg);border-color:var(--dim2)}
.opts button.on{background:rgba(88,166,255,.15);border-color:var(--blue);color:var(--blue)}
.verdict{margin:12px 0 0;padding:13px 16px;border-radius:9px;background:var(--bg3);border:1px solid var(--line);font-size:.9em;color:var(--dim)}
.verdict.ok{border-color:rgba(63,185,80,.45);background:rgba(63,185,80,.09);color:var(--okfg)}
.verdict.mid{border-color:rgba(210,153,34,.45);background:rgba(210,153,34,.09);color:var(--amber2)}
.verdict.no{border-color:rgba(248,81,73,.45);background:rgba(248,81,73,.09);color:var(--red2)}

footer{border-top:1px solid var(--line2);padding:20px 0 40px;color:var(--dim2);font-size:.8em;text-align:center}
.empty{display:none;padding:26px 0;color:var(--dim);text-align:center;font-size:.9em}
.empty a{color:var(--blue);cursor:pointer;text-decoration:underline}

@media (max-width:640px){
  .wrap{padding:0 14px}
  .htop{padding:10px 0 8px;gap:8px}
  .brand em{display:none}
  .tools{margin-left:0;width:100%}
  input#q{flex:1 0 100%;order:-1;width:100%;padding:9px 12px;font-size:.92em}
  .btn{padding:7px 9px}
  .mode-btn{padding:7px 12px;font-size:.84em}
  summary{padding:12px 13px;gap:9px}
  .qid{min-width:40px}
  .cbody{padding:2px 13px 16px}
  .dim{gap:8px}
  .dname{min-width:100%}
  .hero h1{font-size:1.28em}
  section.blk{scroll-margin-top:170px}

  .tw{overflow:visible}
  .cbody table,.cbody tbody,.cbody tr,.cbody td,.cbody th{display:block;width:auto}
  .cbody tr:has(th){display:none}
  .cbody tr{border:1px solid var(--line);border-radius:9px;padding:6px 10px;margin-bottom:9px;background:var(--hover3)}
  .cbody td{border:none;padding:4px 0;font-size:.9em}
  .cbody td[data-l]::before{content:attr(data-l);display:block;font-size:.76em;color:var(--dim2);margin-bottom:1px}
  .cbody td:empty{display:none}

  body.recite-mode input#q,body.recite-mode #expand,body.recite-mode #collapse{display:none}
  body.recite-mode .tools{width:auto;margin-left:auto}
  body.recite-mode .seg.say{display:none}
  .rbar{gap:14px}
  .rbar .rhint{display:none}
  .rbar .rbtn{padding:8px 22px}
}
"""

JS = r"""
(function(){
  var q = document.getElementById('q');
  var empty = document.getElementById('empty');
  var emptyTxt = document.getElementById('empty-txt');
  var cur = 'quick';
  var reciteMode = false, rIdx = 0, rUnits = [];

  function cardsOf(mode){
    return [].slice.call(document.querySelectorAll('#mode-' + mode + ' details.card'));
  }

  function doSearch(){
    var kw = q.value.trim().toLowerCase();
    var shown = 0, other = 0, otherMode = cur === 'quick' ? 'handbook' : 'quick';
    cardsOf(cur).forEach(function(c){
      var hit = !kw || (c.dataset.search || '').indexOf(kw) > -1;
      c.classList.toggle('hide', !hit);
      if (hit) shown++;
      if (kw && hit && !reciteMode) c.open = false;
    });
    if (kw) {
      cardsOf(otherMode).forEach(function(c){
        if ((c.dataset.search || '').indexOf(kw) > -1) other++;
      });
    }
    document.querySelectorAll('#mode-' + cur + ' section.blk').forEach(function(s){
      var any = s.querySelectorAll('details.card:not(.hide)').length;
      s.style.display = any ? '' : 'none';
    });
    if (!shown) {
      empty.style.display = 'block';
      emptyTxt.innerHTML = other
        ? '这一段没有，但另一个模块有 <b>' + other + '</b> 条 —— <a data-jump="' + otherMode + '">切过去看</a>'
        : '没找到。换个词试试，比如「评测」「追问」「数据」。';
    } else {
      empty.style.display = 'none';
    }
    if (reciteMode) rebuildRUnits();
  }

  function setMode(m, keepScroll){
    if (m !== 'quick' && reciteMode) setRecite(false);
    cur = m;
    document.querySelectorAll('.mode-btn').forEach(function(b){
      b.classList.toggle('on', b.dataset.mode === m);
    });
    ['quick','handbook'].forEach(function(x){
      document.getElementById('mode-' + x).style.display = (x === m) ? 'block' : 'none';
      var nav = document.getElementById('nav-' + x);
      if (nav) nav.style.display = (x === m) ? 'flex' : 'none';
    });
    if (history.replaceState) history.replaceState(null, '', '#' + m);
    if (!keepScroll) window.scrollTo({top:0});
    doSearch();
  }

  document.querySelectorAll('.mode-btn').forEach(function(b){
    b.addEventListener('click', function(){ setMode(b.dataset.mode); });
  });

  q.addEventListener('input', doSearch);
  q.addEventListener('keydown', function(e){ if(e.key==='Escape'){ q.value=''; doSearch(); }});

  document.getElementById('expand').addEventListener('click', function(){
    cardsOf(cur).forEach(function(c){ if(!c.classList.contains('hide')) c.open = true; });
  });
  document.getElementById('collapse').addEventListener('click', function(){
    cardsOf(cur).forEach(function(c){ c.open = false; });
    document.querySelectorAll('details.sub').forEach(function(s){ s.open = false; });
    window.scrollTo({top:0, behavior:'smooth'});
  });

  var sizes = ['', 'big', 'small'], si = 0;
  document.getElementById('font').addEventListener('click', function(){
    si = (si + 1) % 3;
    document.body.classList.remove('big','small');
    if (sizes[si]) document.body.classList.add(sizes[si]);
  });

  /* 深色 / 浅色 */
  var themeBtn = document.getElementById('theme');
  function applyTheme(t){
    document.body.classList.toggle('light', t === 'light');
    document.documentElement.style.colorScheme = (t === 'light' ? 'light' : 'dark');
    themeBtn.textContent = (t === 'light') ? '深色' : '浅色';
    themeBtn.title = (t === 'light') ? '切到深色' : '切到浅色';
    try { localStorage.setItem('theme', t); } catch(e){}
  }
  themeBtn.addEventListener('click', function(){
    applyTheme(document.body.classList.contains('light') ? 'dark' : 'light');
  });
  var saved = null;
  try { saved = localStorage.getItem('theme'); } catch(e){}
  applyTheme(saved === 'light' ? 'light' : 'dark');

  document.addEventListener('click', function(e){
    var j = (e.target.closest ? e.target.closest('[data-jump]') : null);
    if (j) { e.preventDefault(); setMode(j.dataset.jump); }
  });

  /* 打分器 */
  document.querySelectorAll('[data-scorer]').forEach(function(sc){
    var verdict = document.querySelector('[data-verdict]');
    var btns = [].slice.call(sc.querySelectorAll('button'));
    var names = ['频率','流程','数据','结果','工具','风险','ROI'];
    function calc(){
      var dims = [].slice.call(sc.querySelectorAll('.dim'));
      var vals = dims.map(function(d){
        var on = d.querySelector('button.on');
        return on ? parseInt(on.dataset.v, 10) : null;
      });
      var left = vals.filter(function(v){ return v === null; }).length;
      if (left) { verdict.className='verdict'; verdict.textContent = '还有 ' + left + ' 项没勾。'; return; }
      var tip = '';
      if (vals[2] === 0 || vals[3] === 0) {
        verdict.className = 'verdict no';
        tip = '数据或结果评测这一项是「低」，是硬前提——先把数据打通、把验收标准定下来，别急着上 Agent。';
      } else if (vals[5] === 0) {
        verdict.className = 'verdict mid';
        tip = '能做，但「做错不可逆」——必须在动作前加人工闸门和审计，工具层就不要给直接执行的能力。';
      } else if (vals[0] === 0 && vals[6] === 0) {
        verdict.className = 'verdict no';
        tip = '低频、价值又说不清——这件事不做。做了也没人认。';
      } else if (vals.every(function(v){ return v === 2; })) {
        verdict.className = 'verdict ok';
        tip = '七项都高，可以直接做 POC。先定通过线，再动手。';
      } else {
        var lowIdx = [];
        vals.forEach(function(v,i){ if (v === 1 || v === 0) lowIdx.push(names[i]); });
        verdict.className = 'verdict mid';
        tip = '可以做，但先补最短的那块：' + lowIdx.join('、') + '。补不动的，就把目标降到「辅助」不做到「替代」。';
      }
      verdict.innerHTML = tip;
    }
    btns.forEach(function(b){
      b.addEventListener('click', function(){
        [].slice.call(b.parentNode.querySelectorAll('button')).forEach(function(x){ x.classList.remove('on'); });
        b.classList.add('on');
        calc();
      });
    });
  });

  /* ---------- 背诵版：投研 / 跨境 切换 ---------- */
  function setVer(card, i){
    [].slice.call(card.querySelectorAll('.vwrap')).forEach(function(w){
      w.hidden = (parseInt(w.dataset.v, 10) !== i);
    });
    [].slice.call(card.querySelectorAll('.vtab')).forEach(function(t){
      t.classList.toggle('on', parseInt(t.dataset.v, 10) === i);
    });
  }

  function curVer(card){
    var w = card.querySelector('.vwrap:not([hidden])');
    return w ? parseInt(w.dataset.v, 10) : 0;
  }

  document.addEventListener('click', function(e){
    var t = (e.target.closest ? e.target.closest('.vtab') : null);
    if (!t) return;
    var card = t.closest('details.card');
    if (!card) return;
    var v = parseInt(t.dataset.v, 10);
    setVer(card, v);
    if (reciteMode) syncUnit(card, v);
  });

  /* ---------- 背诵模式 ---------- */
  var rBtn = document.getElementById('recite');
  var rNum = document.getElementById('rnum');
  var rTag = document.getElementById('rtag');
  var rPrev = document.getElementById('rprev');
  var rNext = document.getElementById('rnext');

  function paintNum(){
    var n = rUnits.length;
    rNum.textContent = n ? (rIdx + 1) + ' / ' + n : '0 / 0';
    rPrev.disabled = (rIdx <= 0);
    rNext.disabled = (rIdx >= n - 1);
    if (!rTag) return;
    if (!n) { rTag.textContent = ''; return; }
    var u = rUnits[Math.min(rIdx, n - 1)];
    var tabs = u.card.querySelectorAll('.vtab');
    rTag.textContent = tabs.length ? tabs[u.v].textContent : '';
  }

  function rebuildRUnits(){
    rUnits = [];
    [].slice.call(document.querySelectorAll('#mode-quick details.card')).forEach(function(c){
      if (c.classList.contains('hide') || c.classList.contains('refonly')) return;
      var n = c.querySelectorAll('.vwrap').length;
      for (var i = 0; i < n; i++) rUnits.push({card: c, v: i});
    });
    if (rIdx >= rUnits.length) rIdx = Math.max(0, rUnits.length - 1);
    paintNum();
  }

  function syncUnit(card, v){
    for (var i = 0; i < rUnits.length; i++) {
      if (rUnits[i].card === card && rUnits[i].v === v) { gotoUnit(i); return; }
    }
  }

  function gotoUnit(i){
    if (!rUnits.length) return;
    rIdx = Math.max(0, Math.min(rUnits.length - 1, i));
    var u = rUnits[rIdx];
    setVer(u.card, u.v);
    var hh = document.querySelector('header').offsetHeight + 8;
    var y = u.card.getBoundingClientRect().top + window.pageYOffset - hh;
    window.scrollTo({top: Math.max(0, y), behavior: 'auto'});
    paintNum();
  }

  function setRecite(on){
    reciteMode = on;
    document.body.classList.toggle('recite-mode', on);
    rBtn.classList.toggle('on', on);
    rBtn.textContent = on ? '退出背诵' : '背诵模式';
    rBtn.title = on ? '回到完整内容' : '只显示背诵稿，上下键翻卡';
    if (on) {
      if (cur !== 'quick') setMode('quick', true);
      cardsOf('quick').forEach(function(c){
        c.classList.toggle('norec', !c.querySelector('.vwrap') || c.classList.contains('refonly'));
        c.open = true;
      });
      rIdx = 0;
      rebuildRUnits();
      window.scrollTo({top: 0, behavior: 'auto'});
      gotoUnit(0);
    } else {
      rUnits = [];
      paintNum();
    }
  }

  rBtn.addEventListener('click', function(){ setRecite(!reciteMode); });
  rPrev.addEventListener('click', function(){ gotoUnit(rIdx - 1); });
  rNext.addEventListener('click', function(){ gotoUnit(rIdx + 1); });

  document.addEventListener('keydown', function(e){
    if (!reciteMode) return;
    if (e.target && e.target.tagName === 'INPUT') return;
    if (e.key === 'Escape') { setRecite(false); return; }
    if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === ' ') {
      e.preventDefault(); gotoUnit(rIdx + 1);
    } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
      e.preventDefault(); gotoUnit(rIdx - 1);
    }
  });

  var rTick = false;
  window.addEventListener('scroll', function(){
    if (!reciteMode || rTick || !rUnits.length) return;
    rTick = true;
    requestAnimationFrame(function(){
      rTick = false;
      var hh = document.querySelector('header').offsetHeight + 8;
      var bestCard = null, bd = 1e9, seen = [];
      rUnits.forEach(function(u){
        if (seen.indexOf(u.card) > -1) return;
        seen.push(u.card);
        var d = Math.abs(u.card.getBoundingClientRect().top - hh);
        if (d < bd) { bd = d; bestCard = u.card; }
      });
      if (!bestCard) return;
      var v = curVer(bestCard);
      for (var i = 0; i < rUnits.length; i++) {
        if (rUnits[i].card === bestCard && rUnits[i].v === v) {
          if (i !== rIdx) { rIdx = i; paintNum(); }
          break;
        }
      }
    });
  }, {passive: true});

  setMode((location.hash.replace('#','') === 'handbook') ? 'handbook' : 'quick', true);
})();
"""


def strip(h):
    t = re.sub(r"<[^>]+>", " ", h or "")
    t = H.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def wrap_tables(h):
    """给表格套滚动容器，并给每个 td 打上列名（窄屏转卡片式堆叠用）"""
    def repl(m):
        tbl = m.group(0)
        ths = re.findall(r"<th>(.*?)</th>", tbl, re.S)
        labels = [strip(t) for t in ths] if ths else []
        head_end = tbl.find("</tr>")
        if not labels or head_end < 0:
            return '<div class="tw">' + tbl + "</div>"
        head, rest = tbl[:head_end + 5], tbl[head_end + 5:]
        counter = [0]

        def td_repl(mm):
            lab = labels[counter[0] % len(labels)]
            counter[0] += 1
            return '<td data-l="%s">' % H.escape(lab)

        return '<div class="tw">' + head + re.sub(r"<td>", td_repl, rest) + "</div>"

    return re.sub(r"<table>.*?</table>", repl, h, flags=re.S)


def md(s):
    """纯文本 → HTML（转义 + **加粗**）"""
    s = H.escape(s)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)


def recite_html(versions, ref=False):
    """versions: [(版本名, 文本), ...]。单版不出标签，多版出「投研 / 跨境」切换。
    ref=True 表示这是备查清单，渲染成橙色并写明别照着念。"""
    if not versions:
        return ""
    tabs = ""
    if len(versions) > 1:
        tabs = '<div class="vtabs">' + "".join(
            '<button class="vtab%s" data-v="%d">%s</button>' % (
                " on" if i == 0 else "", i, H.escape(n))
            for i, (n, _) in enumerate(versions)) + "</div>"
    wraps = []
    for i, (_name, s) in enumerate(versions):
        paras = [p.strip() for p in s.strip().split("\n\n") if p.strip()]
        plain = strip(s)
        n = len(re.sub(r"\s+", "", plain))
        sec = int(round(n / 4.2))
        body = "".join("<p>%s</p>" % md(p) for p in paras)
        if ref:
            meta = '<div class="recite-meta">全文 <b>%d</b> 字 · 这份是对着查的清单，不用背</div>' % n
        else:
            meta = ('<div class="recite-meta">全文 <b>%d</b> 字 · 正常语速念一遍约 <b>%d</b> 秒</div>'
                    % (n, sec))
        wraps.append('<div class="vwrap%s" data-v="%d"%s>%s%s</div>' % (
            " ref" if ref else "", i, "" if i == 0 else " hidden", body, meta))
    if ref:
        return ('<div class="seg recite ref"><span class="lab">备查 · 别照着念</span>%s%s'
                '<div class="reftip">这几条是清单，面试时用来对照自己漏没漏，念出来会像背书。</div></div>'
                % (tabs, "".join(wraps)))
    return ('<div class="seg recite"><span class="lab">背诵版 · 照着念</span>%s%s</div>'
            % (tabs, "".join(wraps)))



# ---------- 速查模块的卡 ----------
def render_quick_card(c):
    rc = RECITE.get(c["id"]) or c.get("recite") or []
    if isinstance(rc, str):
        rc = [("两段一起讲", rc)]
    kids = []
    if c.get("todo"):
        kids.append('<span class="tag todo">待你填</span>')
    if c.get("tag"):
        cls = {"必背": "must", "必做": "must", "核心": "core"}.get(c["tag"], "core")
        kids.append('<span class="tag %s">%s</span>' % (cls, H.escape(c["tag"])))

    rc_text = " ".join(t for _n, t in rc)
    is_ref = c["id"] in REF_ONLY
    search = " ".join(strip(x or "") for x in (
        c.get("title"), c.get("ask"), c.get("say"), rc_text,
        c.get("detail"), c.get("body")))
    search += " " + " ".join(strip(p) for p in c.get("probe", []))

    head = ('<summary><span class="qid">%s</span><span class="qt">%s</span>%s'
            '<span class="chev">›</span></summary>') % (
        H.escape(c["id"]), H.escape(c["title"]), "".join(kids))

    if c.get("kind") == "custom":
        body = '<div class="cbody">'
        if c.get("ask"):
            body += '<div class="seg ask"><span class="lab">他在测什么</span><p>%s</p></div>' % c["ask"]
        if rc:
            body += recite_html(rc, is_ref)
        body += wrap_tables(c.get("body", "")) + "</div>"
    else:
        body = '<div class="cbody">'
        if c.get("ask"):
            body += '<div class="seg ask"><span class="lab">面试官原话</span><p>%s</p></div>' % c["ask"]
        if c.get("say"):
            body += '<div class="seg say"><span class="lab">20 秒答法</span><blockquote>%s</blockquote></div>' % c["say"]
        if rc:
            body += recite_html(rc, is_ref)
        if c.get("detail"):
            body += '<div class="seg det"><span class="lab">展开讲</span>%s</div>' % wrap_tables(c["detail"])
        if c.get("probe"):
            lis = "".join("<li>%s</li>" % p for p in c["probe"])
            body += '<div class="seg probe"><span class="lab">他可能追什么</span><ul>%s</ul></div>' % lis
        body += "</div>"

    return ('<details class="card%s" data-search="%s" id="%s">%s%s</details>'
            % (" refonly" if is_ref else "", H.escape(search.lower()),
               H.escape(c["id"].replace(".", "-")), head, body))


# ---------- 手册模块的卡 ----------
def blocks_html(items):
    out = []
    for kind, val in items:
        if kind == "table":
            out.append(wrap_tables(val))
        else:
            out.append("<p>%s</p>" % md(val))
    return "".join(out)


def render_hb_card(c, idx, key=""):
    qid = c["id"] or "%02d" % idx
    search = c["title"] + " " + c.get("ask", "")
    for k in ("say", "detail", "probe", "red"):
        for kind, val in c.get(k, []):
            search += " " + strip(val)
    search = re.sub(r"\s+", " ", search)

    head = ('<summary><span class="qid">%s</span><span class="qt">%s</span>'
            '<span class="chev">›</span></summary>') % (H.escape(qid), H.escape(c["title"]))

    body = '<div class="cbody">'
    if c.get("ask"):
        body += '<div class="seg ask"><span class="lab">他在测什么</span><p>%s</p></div>' % md(c["ask"])

    if c.get("say"):
        seg = '<div class="seg say"><span class="lab">照着说</span>'
        for kind, val in c["say"]:
            if kind == "table":
                seg += wrap_tables(val)
            else:
                seg += "<blockquote>%s</blockquote>" % md(val)
        body += seg + "</div>"

    if c.get("detail"):
        lab = "正文" if c.get("kind") == "ref" else "这是什么"
        body += '<div class="seg det"><span class="lab">%s</span>%s</div>' % (lab, blocks_html(c["detail"]))

    if c.get("probe"):
        lis = "".join("<li>%s</li>" % md(v) for k, v in c["probe"])
        body += '<div class="seg probe"><span class="lab">他要追的话</span><ul>%s</ul></div>' % lis

    if c.get("red"):
        lis = "".join("<li>%s</li>" % md(v) for k, v in c["red"])
        body += '<div class="seg red"><span class="lab">红线</span><ul>%s</ul></div>' % lis

    body += "</div>"
    anchor = H.escape(re.sub(r"[^\w]", "-", (key + "-" if key else "") + qid))
    return ('<details class="card" data-search="%s" id="%s">%s%s</details>'
            % (H.escape(search.lower()), anchor, head, body))


# 速查三个板块的导航短名（板块标题太长，tab 上放不下）
QUICK_TAB = {"0": "考前速扫", "1": "场景题 12 步", "2": "项目全链路"}


def render_block(b, mode):
    if mode == "quick":
        cards = "".join(render_quick_card(c) for c in b["cards"])
    else:
        cards = "".join(render_hb_card(c, i + 1, b["key"]) for i, c in enumerate(b["cards"]))
    if mode == "handbook":
        label = b["title"].split("：")[0]
    else:
        label = QUICK_TAB.get(str(b["key"]), b["title"])
    tab = '<a class="tab" href="#%s-%s">%s</a>' % (mode, b["key"], H.escape(label))
    sec = ('<section class="blk" id="%s-%s">'
           '<div class="blkhead"><h2>%s</h2></div>'
           '<p class="blksub">%s <span style="color:var(--dim2)">· %d 张</span></p>'
           '%s</section>') % (mode, b["key"], H.escape(b["title"]), b["sub"],
                              len(b["cards"]), cards)
    return tab, sec


def main():
    quick_blocks = [part0.BLOCK, part1.BLOCK, part2.BLOCK]
    hb_blocks = HB.BLOCKS

    q_tabs, q_secs = [], []
    for b in quick_blocks:
        t, s = render_block(b, "quick")
        q_tabs.append(t)
        q_secs.append(s)

    h_tabs, h_secs = [], []
    for b in hb_blocks:
        t, s = render_block(b, "handbook")
        h_tabs.append(t)
        h_secs.append(s)

    n_quick = sum(len(b["cards"]) for b in quick_blocks)
    n_hb = sum(len(b["cards"]) for b in hb_blocks)

    doc = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title>%(title)s</title>
<style>%(css)s</style>
</head>
<body>
<script>try{if(localStorage.getItem('theme')==='light'){document.body.className+=' light';document.documentElement.style.colorScheme='light';}}catch(e){}</script>
<header>
  <div class="wrap">
    <div class="htop">
      <div class="brand">%(title)s<em>%(sub)s</em></div>
      <div class="tools">
        <input id="q" type="search" placeholder="搜关键词：九问 / 幂等 / 时间粒度" autocomplete="off">
        <button class="btn" id="expand">全展开</button>
        <button class="btn" id="collapse">全收起</button>
        <button class="btn" id="font">字号</button>
        <button class="btn" id="theme" title="切到浅色">浅色</button>
        <button class="btn recite-btn" id="recite" title="只显示背诵稿，上下键翻卡">背诵模式</button>
      </div>
    </div>
    <div class="modes">
      <button class="mode-btn on" data-mode="quick"><b>速查</b><span>%(nq)d 张 · 现场用</span></button>
      <button class="mode-btn" data-mode="handbook"><b>手册</b><span>%(nt)d 题 · 备查用</span></button>
    </div>
    <nav class="tabs" id="nav-quick">%(qtabs)s<a class="tab" href="#top">回到顶部</a></nav>
    <nav class="tabs" id="nav-handbook" style="display:none">%(htabs)s<a class="tab" href="#top">回到顶部</a></nav>
  </div>
</header>
<main class="wrap" id="top">
  <div id="mode-quick">
    <div class="hero">
      <h1>速查：现场答卷用的 %(nq)d 张卡</h1>
      <p>面试官扔场景时照这个走：先问 → 判断值不值得做 → 12 步。</p>
      <div class="note">三个板块：考前速扫 / 场景题 12 步 / 项目全链路。
      标 <b style="color:var(--purple)">待你填</b> 的几张需要你自己补事实；
      带 <b style="color:var(--green)">绿框背诵版</b> 的 %(nr)d 张、共 %(nu)d 段（投研 / 跨境各一版，卡内可切换）可以直接照念；
      标 <b style="color:var(--orange)">橙框备查</b> 的 %(nref)d 张是清单和自检项，用来对着查、念出来反而像背书；
      点右上角「背诵模式」只留稿子、按段翻（备查卡不进）；其余是没有定稿的口播、只给现场思路。</div>
    </div>
    %(qsecs)s
  </div>
  <div id="mode-handbook" style="display:none">
    <div class="hero">
      <h1>手册：%(nt)d 题完整版</h1>
      <p>逐题四段：他在测什么 → 照着说 → 这是什么 → 他要追的话 / 红线。</p>
      <div class="note">内容逐字来自手册原稿，未改写。姓名、学校、届别已留空为【】。</div>
    </div>
    %(hsecs)s
  </div>
  <div class="empty" id="empty"><span id="empty-txt"></span></div>
</main>
<footer>个人技术笔记 · 速查 %(nq)d 张 ＋ 手册 %(nt)d 题（另含前置 %(pre)d 张、附录 %(apx)d 张）</footer>
<div class="rbar" id="rbar"><button class="rbtn" id="rprev">上一段</button><span id="rnum">1 / 1</span><span id="rtag"></span><button class="rbtn" id="rnext">下一段</button><span class="rhint">↑ ↓ 翻段 · Esc 退出</span></div>
<script>%(js)s</script>
</body>
</html>""" % dict(title=TITLE, sub=SUBTITLE, css=CSS, js=JS, nq=n_quick, nh=n_hb,
                 qtabs="".join(q_tabs), htabs="".join(h_tabs), nt=HB.TOTAL,
                 qsecs="".join(q_secs), hsecs="".join(h_secs),
                 pre=len(hb_blocks[0]["cards"]), apx=len(hb_blocks[-1]["cards"]),
                 nr=len([k for k in RECITE if k not in REF_ONLY]),
                 nu=sum(len(v) for k, v in RECITE.items() if k not in REF_ONLY),
                 nref=len([k for k in RECITE if k in REF_ONLY]))

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    open(os.path.join(BASE, ".nojekyll"), "w").close()

    print("written:", OUT)
    print("quick blocks:", len(quick_blocks), "cards:", n_quick)
    print("handbook blocks:", len(hb_blocks), "cards:", n_hb)
    print("size:", len(doc.encode("utf-8")), "bytes")


if __name__ == "__main__":
    main()
