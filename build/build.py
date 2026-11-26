# -*- coding: utf-8 -*-
"""把 part0/1/2 组装成单文件 index.html（深色、原生折叠、可搜索）"""
import html as H
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import part0
import part1
import part2

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "index.html")

BLOCKS = [part0.BLOCK, part1.BLOCK, part2.BLOCK]

TITLE = "场景题与项目表达 · 速查"
SUBTITLE = "40 张卡 · 点开才看答案 · 手机也能用"

CSS = r"""
:root{
  --bg:#0d1117; --bg2:#161b22; --bg3:#1c2128; --line:#30363d; --line2:#21262d;
  --fg:#e6edf3; --dim:#8b949e; --dim2:#6e7681;
  --blue:#58a6ff; --orange:#d29922; --red:#f85149; --green:#3fb950; --purple:#bc8cff;
  --fs:16px;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg);color:var(--fg)}
body{font-family:-apple-system,"Segoe UI","Microsoft YaHei",system-ui,sans-serif;font-size:var(--fs);line-height:1.72;-webkit-text-size-adjust:100%}
body.small{--fs:14.5px}
body.big{--fs:17.5px}
.wrap{max-width:960px;margin:0 auto;padding:0 20px}

/* ---------- 顶栏 ---------- */
header{position:sticky;top:0;z-index:50;background:rgba(13,17,23,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.htop{display:flex;align-items:center;gap:14px;padding:12px 0 10px;flex-wrap:wrap}
.brand{font-size:1.02em;font-weight:700;letter-spacing:.02em;white-space:nowrap}
.brand em{font-style:normal;color:var(--dim);font-weight:400;font-size:.8em;margin-left:8px}
.tools{margin-left:auto;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
input#q{width:230px;background:var(--bg3);border:1px solid var(--line);color:var(--fg);border-radius:8px;padding:7px 11px;font-size:.86em;font-family:inherit;outline:none}
input#q:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(88,166,255,.12)}
input#q::placeholder{color:var(--dim2)}
.btn{background:var(--bg3);border:1px solid var(--line);color:var(--dim);border-radius:8px;padding:7px 11px;font-size:.82em;cursor:pointer;font-family:inherit;transition:.15s;white-space:nowrap}
.btn:hover{color:var(--fg);border-color:var(--dim2)}
.btn.on{color:var(--blue);border-color:var(--blue)}
.tabs{display:flex;gap:6px;overflow-x:auto;padding-bottom:9px;scrollbar-width:none}
.tabs::-webkit-scrollbar{display:none}
.tab{font-size:.8em;color:var(--dim);text-decoration:none;padding:5px 11px;border-radius:999px;border:1px solid var(--line2);white-space:nowrap}
.tab:hover{color:var(--fg);border-color:var(--dim2)}

/* ---------- 板块 ---------- */
main{padding:26px 0 80px}
.hero{padding:8px 0 22px;border-bottom:1px solid var(--line2);margin-bottom:26px}
.hero h1{margin:0 0 6px;font-size:1.5em;letter-spacing:.01em}
.hero p{margin:0;color:var(--dim);font-size:.88em}
.hero .note{margin-top:12px;font-size:.84em;color:var(--dim);border-left:2px solid var(--line);padding-left:12px}

section.blk{margin-bottom:38px;scroll-margin-top:110px}
.blkhead{display:flex;align-items:baseline;gap:10px;margin-bottom:4px;flex-wrap:wrap}
.blkno{font-size:.72em;color:var(--blue);border:1px solid rgba(88,166,255,.35);border-radius:5px;padding:1px 7px;letter-spacing:.06em}
.blkhead h2{margin:0;font-size:1.16em}
.blksub{color:var(--dim);font-size:.84em;margin:0 0 16px}

/* ---------- 卡片 ---------- */
details.card{background:var(--bg2);border:1px solid var(--line2);border-radius:10px;margin-bottom:9px;overflow:hidden;transition:border-color .15s}
details.card:hover{border-color:var(--line)}
details.card[open]{border-color:var(--line);background:var(--bg2)}
details.card.hide{display:none}
summary{list-style:none;cursor:pointer;padding:13px 16px;display:flex;align-items:center;gap:11px;user-select:none}
summary::-webkit-details-marker{display:none}
summary:hover{background:rgba(255,255,255,.02)}
.qid{font-family:ui-monospace,Consolas,monospace;font-size:.76em;color:var(--dim2);min-width:42px;flex:none}
.qt{font-size:.95em;font-weight:600;flex:1}
.tag{font-size:.68em;padding:1px 7px;border-radius:4px;flex:none;letter-spacing:.04em}
.tag.must{color:var(--red);background:rgba(248,81,73,.12);border:1px solid rgba(248,81,73,.3)}
.tag.core{color:var(--orange);background:rgba(210,153,34,.12);border:1px solid rgba(210,153,34,.3)}
.tag.todo{color:var(--purple);background:rgba(188,140,255,.12);border:1px solid rgba(188,140,255,.3)}
.chev{color:var(--dim2);font-size:1.1em;transition:transform .2s;flex:none}
details[open] .chev{transform:rotate(90deg)}
.cbody{padding:2px 16px 18px;border-top:1px solid var(--line2)}

/* 四段 */
.seg{margin-top:15px}
.lab{display:inline-block;font-size:.7em;letter-spacing:.1em;color:var(--dim2);margin-bottom:6px}
.seg.ask .lab{color:var(--purple)}
.seg.say .lab{color:var(--blue)}
.seg.det .lab{color:var(--dim)}
.seg.probe .lab{color:var(--orange)}
.seg.ask p{margin:0;color:var(--fg);font-size:.94em}
.seg.say blockquote{margin:0;padding:12px 15px;background:rgba(88,166,255,.07);border-left:2px solid var(--blue);border-radius:0 7px 7px 0;font-size:.95em}
.seg.det{font-size:.9em;color:#c9d1d9}
.seg.det p{margin:0 0 10px}
.seg.det p:last-child{margin-bottom:0}
.seg.probe ul{margin:0;padding-left:18px;font-size:.88em;color:var(--dim)}
.seg.probe li{margin-bottom:7px}
.seg.probe li:last-child{margin-bottom:0}

/* 正文内元素 */
.tw{overflow-x:auto;margin:10px 0;-webkit-overflow-scrolling:touch}
.cbody table{width:100%;border-collapse:collapse;margin:10px 0;font-size:.86em}
.tw table{margin:0}
.cbody th,.cbody td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top;word-break:break-word}
.cbody th{background:var(--bg3);color:var(--dim);font-weight:600;font-size:.95em}
.cbody td{color:#c9d1d9}
.cbody,.cbody p,.cbody li,.cbody blockquote,.cbody td,.cbody th{overflow-wrap:anywhere}
.cbody ul,.cbody ol{margin:8px 0;padding-left:20px}
.cbody li{margin-bottom:5px}
.cbody strong,b{color:#fff;font-weight:600}
.cbody blockquote{margin:10px 0;padding:9px 14px;border-left:2px solid var(--line);color:var(--dim);background:rgba(255,255,255,.02)}
.src{display:block;color:var(--dim2);font-size:.86em;margin-top:2px}
.warn{margin-top:12px;padding:11px 14px;border-radius:8px;background:rgba(188,140,255,.08);border:1px solid rgba(188,140,255,.25);font-size:.88em;color:#d2a8ff}
.tip{padding:10px 14px;border-radius:8px;background:rgba(63,185,80,.07);border-left:2px solid var(--green);font-size:.9em;color:#9fd8a8}
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
.verdict.ok{border-color:rgba(63,185,80,.45);background:rgba(63,185,80,.09);color:#7ee08a}
.verdict.mid{border-color:rgba(210,153,34,.45);background:rgba(210,153,34,.09);color:#e3b341}
.verdict.no{border-color:rgba(248,81,73,.45);background:rgba(248,81,73,.09);color:#ff7b72}
.verdict b{color:inherit}

footer{border-top:1px solid var(--line2);padding:20px 0 40px;color:var(--dim2);font-size:.8em;text-align:center}
.empty{display:none;padding:30px 0;color:var(--dim);text-align:center;font-size:.9em}

@media (max-width:640px){
  .wrap{padding:0 14px}
  .htop{padding:10px 0 8px;gap:8px}
  .brand em{display:none}
  .tools{margin-left:0;width:100%}
  input#q{flex:1;width:auto;min-width:0}
  .btn{padding:7px 9px}
  summary{padding:12px 13px;gap:9px}
  .qid{min-width:38px}
  .cbody{padding:2px 13px 16px}
  .dim{gap:8px}
  .dname{min-width:100%}
  .hero h1{font-size:1.3em}

  /* 窄屏：表格改成卡片式堆叠，避免挤成竖排单字 */
  .tw{overflow:visible}
  .cbody table,.cbody tbody,.cbody tr,.cbody td,.cbody th{display:block;width:auto}
  .cbody tr:has(th){display:none}
  .cbody tr{border:1px solid var(--line);border-radius:9px;padding:6px 10px;margin-bottom:9px;background:rgba(255,255,255,.015)}
  .cbody td{border:none;padding:4px 0;font-size:.9em}
  .cbody td[data-l]::before{content:attr(data-l);display:block;font-size:.76em;color:var(--dim2);margin-bottom:1px}
  .cbody td:empty{display:none}
}
"""

JS = r"""
(function(){
  var cards = [].slice.call(document.querySelectorAll('details.card'));
  var q = document.getElementById('q');
  var empty = document.getElementById('empty');

  // 搜索
  q.addEventListener('input', function(){
    var kw = q.value.trim().toLowerCase();
    var shown = 0;
    cards.forEach(function(c){
      var hit = !kw || (c.dataset.search || '').indexOf(kw) > -1;
      c.classList.toggle('hide', !hit);
      if (hit) shown++;
    });
    empty.style.display = shown ? 'none' : 'block';
    if (kw) cards.forEach(function(c){ if(!c.classList.contains('hide')) c.open = true; });
  });
  q.addEventListener('keydown', function(e){ if(e.key==='Escape'){ q.value=''; q.dispatchEvent(new Event('input')); }});

  // 全展开 / 全收
  document.getElementById('expand').addEventListener('click', function(){
    cards.forEach(function(c){ if(!c.classList.contains('hide')) c.open = true; });
  });
  document.getElementById('collapse').addEventListener('click', function(){
    cards.forEach(function(c){ c.open = false; });
    document.querySelectorAll('details.sub').forEach(function(s){ s.open = false; });
    window.scrollTo({top:0, behavior:'smooth'});
  });

  // 字号三档
  var sizes = ['', 'big', 'small'];
  var si = 0;
  document.getElementById('font').addEventListener('click', function(){
    si = (si + 1) % 3;
    document.body.classList.remove('big','small');
    if (sizes[si]) document.body.classList.add(sizes[si]);
  });

  // 打分器
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
})();
"""


def strip(h):
    t = re.sub(r"<[^>]+>", " ", h or "")
    t = H.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def wrap_tables(h):
    """给表格套滚动容器，并给每个 td 打上列名（窄屏下转卡片式堆叠用）"""
    def repl(m):
        tbl = m.group(0)
        ths = re.findall(r"<th>(.*?)</th>", tbl, re.S)
        if not ths:
            return '<div class="tw">' + tbl + "</div>"
        labels = [strip(t) for t in ths]
        head_end = tbl.find("</tr>")
        if head_end < 0:
            return '<div class="tw">' + tbl + "</div>"
        head, rest = tbl[:head_end + 5], tbl[head_end + 5:]
        counter = [0]

        def td_repl(mm):
            lab = labels[counter[0] % len(labels)]
            counter[0] += 1
            return '<td data-l="%s">' % H.escape(lab)

        rest = re.sub(r"<td>", td_repl, rest)
        return '<div class="tw">' + head + rest + "</div>"

    return re.sub(r"<table>.*?</table>", repl, h, flags=re.S)


def render_card(c):
    kids = []
    if c.get("todo"):
        kids.append('<span class="tag todo">待你填</span>')
    if c.get("tag"):
        cls = {"必背": "must", "必做": "must", "核心": "core"}.get(c["tag"], "core")
        kids.append('<span class="tag %s">%s</span>' % (cls, H.escape(c["tag"])))

    search = strip(c.get("title", "")) + " " + strip(c.get("ask", "")) + " " + \
             strip(c.get("say", "")) + " " + strip(c.get("detail", "")) + " " + \
             strip(c.get("body", ""))
    for p in c.get("probe", []):
        search += " " + strip(p)

    head = ('<summary><span class="qid">%s</span><span class="qt">%s</span>%s'
            '<span class="chev">›</span></summary>') % (
        H.escape(c["id"]), H.escape(c["title"]), "".join(kids))

    if c.get("kind") == "custom":
        body = '<div class="cbody">'
        if c.get("ask"):
            body += '<div class="seg ask"><span class="lab">他在测什么</span><p>%s</p></div>' % c["ask"]
        body += wrap_tables(c.get("body", "")) + "</div>"
    else:
        body = '<div class="cbody">'
        if c.get("ask"):
            body += '<div class="seg ask"><span class="lab">面试官原话</span><p>%s</p></div>' % c["ask"]
        if c.get("say"):
            body += '<div class="seg say"><span class="lab">20 秒答法</span><blockquote>%s</blockquote></div>' % c["say"]
        if c.get("detail"):
            body += '<div class="seg det"><span class="lab">展开讲</span>%s</div>' % wrap_tables(c["detail"])
        if c.get("probe"):
            lis = "".join("<li>%s</li>" % p for p in c["probe"])
            body += '<div class="seg probe"><span class="lab">他可能追什么</span><ul>%s</ul></div>' % lis
        body += "</div>"

    return ('<details class="card" data-search="%s" id="%s">%s%s</details>'
            % (H.escape(search.lower()), H.escape(c["id"].replace(".", "-")), head, body))


def render_block(b):
    tabs = ('<a class="tab" href="#b%s">%s · %s</a>'
            % (b["key"], b["key"], H.escape(b["title"])))
    inner = "".join(render_card(c) for c in b["cards"])
    sec = ('<section class="blk" id="b%s">'
           '<div class="blkhead"><span class="blkno">板块 %s</span><h2>%s</h2></div>'
           '<p class="blksub">%s <span style="color:var(--dim2)">· %d 张</span></p>'
           '%s</section>') % (b["key"], b["key"], H.escape(b["title"]),
                              b["sub"], len(b["cards"]), inner)
    return tabs, sec


def main():
    tabs, secs = [], []
    total = 0
    for b in BLOCKS:
        t, s = render_block(b)
        tabs.append(t)
        secs.append(s)
        total += len(b["cards"])

    doc = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title>%s</title>
<style>%s</style>
</head>
<body>
<header>
  <div class="wrap">
    <div class="htop">
      <div class="brand">%s<em>%s</em></div>
      <div class="tools">
        <input id="q" type="search" placeholder="搜关键词：九问 / 幂等 / 时间粒度" autocomplete="off">
        <button class="btn" id="expand">全展开</button>
        <button class="btn" id="collapse">全收起</button>
        <button class="btn" id="font">字号</button>
      </div>
    </div>
    <nav class="tabs">%s<a class="tab" href="#top">回到顶部</a></nav>
  </div>
</header>
<main class="wrap" id="top">
  <div class="hero">
    <h1>%s</h1>
    <p>%s</p>
    <div class="note">用法：先看板块 0（考前十分钟），再用板块 1 应付现场给场景。
    每张卡都是「面试官原话 → 20 秒答法 → 展开讲 → 他可能追什么」。
    标 <b style="color:var(--purple)">待你填</b> 的三张需要你自己补事实。</div>
  </div>
  %s
  <div class="empty" id="empty">没找到。换个词试试，比如「评测」「追问」「数据」。</div>
</main>
<footer>个人技术笔记 · 共 %d 张卡 · 内容以本人实际经历为准</footer>
<script>%s</script>
</body>
</html>""" % (TITLE, CSS, TITLE, SUBTITLE, "".join(tabs), TITLE, SUBTITLE,
             "".join(secs), total, JS)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    # 关掉 Jekyll，避免多走一遍处理
    open(os.path.join(BASE, ".nojekyll"), "w").close()

    print("written:", OUT)
    print("blocks:", len(BLOCKS), "cards:", total,
          "size:", len(doc.encode("utf-8")), "bytes")


if __name__ == "__main__":
    main()
