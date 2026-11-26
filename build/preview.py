# -*- coding: utf-8 -*-
"""单独渲染 Q1.1 / Q1.2 两张特殊卡，用于截图检查"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B
import part1

import part0
_all = part0.BLOCK["cards"] + part1.BLOCK["cards"]
cards = [c for c in _all if c["id"] in ("Q0.4", "Q1.2")]
html_parts = []
for c in cards:
    s = B.render_card(c)
    s = s.replace('<details class="card"', '<details class="card" open', 1)
    html_parts.append(s)

doc = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>preview</title><style>%s</style></head><body>
<main class="wrap" style="padding-top:24px">%s</main><script>%s</script></body></html>""" % (
    B.CSS, "".join(html_parts), B.JS)

out = os.path.join(B.BASE, "build", "_preview.html")
open(out, "w", encoding="utf-8").write(doc)
print("ok", len(doc))
