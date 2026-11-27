# -*- coding: utf-8 -*-
"""从 73题版-v6.docx 提取结构化数据 → handbook_data.py
原则：逐字搬运，不改写。仅做三件事：
  1) 私人信息留空（姓名/学校/届别）
  2) 章节八↔九互换（连带题号 Q8.x↔Q9.x 与交叉引用）
  3) 目录/总数按实际算（79 题），不沿用文档里过期的 73
"""
import os
import re

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get("HB_SRC") or \
    r"D:/下载/飞书/05.3-Folio（金融投研）/output/qa-20261103/stage3/AI应用开发岗面试问答手册-73题版-v6.docx"
OUT = os.path.join(BASE, "build", "handbook_data.py")

# ---------- 替换规则 ----------
PRIVATE = [
    ("我叫王铭楷，岭南师范学院软件工程，2028 届。", "我叫【】，【】软件工程，【】届。"),
]

CHAPTER_RENAME = {
    "九、工程基础补篇": "八、工程基础补篇",
    "八、收尾": "九、收尾",
}


def remap_q(text):
    """Q9.x → Q8.x，Q8.x → Q9.x，一次扫描完成，避免二次污染"""
    def f(m):
        ch, num = m.group(1), m.group(2)
        if ch == "9":
            return "Q8." + num
        if ch == "8":
            return "Q9." + num
        return m.group(0)
    return re.sub(r"Q([89])\.(\d+)", f, text)


def clean(text):
    for a, b in PRIVATE:
        text = text.replace(a, b)
    return remap_q(text)


def para_md(p):
    """段落 → 带 **加粗** 标记的文本；命中私人信息时整段走纯文本，避免标记打断句子"""
    raw = p.text.strip()
    for a, b in PRIVATE:
        if a in raw:
            return clean(raw)
    out = []
    for r in p.runs:
        t = r.text
        if not t:
            continue
        if r.bold and t.strip():
            lead = " " if t[:1].isspace() else ""
            tail = " " if t[-1:].isspace() else ""
            out.append(lead + "**" + t.strip() + "**" + tail)
        else:
            out.append(t)
    s = "".join(out)
    if not s.strip():
        s = raw
    return clean(s.strip())


def table_html(tb):
    rows = []
    for ri, row in enumerate(tb.rows):
        cells = []
        for c in row.cells:
            txt = clean(" ".join(x.text.strip() for x in c.paragraphs if x.text.strip()))
            tag = "th" if ri == 0 else "td"
            cells.append("<%s>%s</%s>" % (tag, esc(txt), tag))
        rows.append("<tr>%s</tr>" % "".join(cells))
    return "<table>%s</table>" % "".join(rows)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace("**", ""))


LABELS = ("他在测什么", "照着说", "这是什么", "他要追的话", "红线")


def split_label(t):
    """返回 (标签, 剩余内容)；不是标签行返回 (None, None)"""
    for L in LABELS:
        if t.startswith(L):
            rest = t[len(L):].lstrip("　 :：")
            return L, rest
        if t.startswith("**" + L + "**"):
            rest = t[len(L) + 4:].lstrip("　 :：")
            return L, rest
    return None, None


def main():
    d = Document(SRC)
    body = d.element.body

    blocks = []          # 顺序化的内容单元
    cur_chapter = None   # 当前章节 dict
    cur_card = None      # 当前题目 dict
    cur_field = None     # 当前字段
    in_pre = False

    pre_cards = []
    chapters = []
    appendix = []

    def push_card(card):
        if cur_chapter is not None:
            cur_chapter["cards"].append(card)
        elif in_pre:
            pre_cards.append(card)
        else:
            appendix.append(card)

    for child in body.iterchildren():
        tag = child.tag.split("}")[-1]
        if tag == "tbl":
            tb = Table(child, d)
            html = table_html(tb)
            target = cur_card or (pre_cards[-1] if in_pre and pre_cards else (appendix[-1] if appendix else None))
            if target is None:
                continue
            if cur_field in ("detail", "say", "probe", "red"):
                target[cur_field].append(("table", html))
            else:
                target["detail"].append(("table", html))
            continue

        if tag != "p":
            continue
        p = Paragraph(child, d)
        raw = p.text.strip()
        if not raw:
            continue
        style = p.style.name
        txt = para_md(p)

        # ---- 章节标题 ----
        if style == "Heading 2":
            name = clean(raw)
            name = CHAPTER_RENAME.get(name, name)
            cur_card, cur_field = None, None
            if re.match(r"^[一二三四五六七八九十]、", name):
                cur_chapter = {"key": "c%d" % (len(chapters) + 1), "title": name, "cards": []}
                chapters.append(cur_chapter)
                in_pre = False
            elif name.startswith("附录"):
                cur_chapter = {"key": "apx", "title": name, "cards": []}
                chapters.append(cur_chapter)
                in_pre = False
            else:
                # 前置小节
                in_pre = True
                cur_chapter = None
                pre_cards.append({"id": "", "title": name, "kind": "ref",
                                  "ask": "", "say": [], "detail": [], "probe": [], "red": []})
            continue

        if style == "Heading 3":
            m = re.match(r"^(Q\d+\.\d+)\s*[「『]?(.*?)[」』]?$", clean(raw))
            if m:
                card = {"id": m.group(1), "title": m.group(2).strip(),
                        "kind": "q", "ask": "", "say": [], "detail": [],
                        "probe": [], "red": []}
                push_card(card)
                cur_card = card
                cur_field = None
            else:
                # 附录里的清单标题
                card = {"id": "", "title": clean(raw), "kind": "ref",
                        "ask": "", "say": [], "detail": [], "probe": [], "red": []}
                if cur_chapter is not None:
                    cur_chapter["cards"].append(card)
                else:
                    appendix.append(card)
                cur_card = card
                cur_field = None
            continue

        # ---- 正文 ----
        if raw.strip() in ("---", "——", "***"):
            continue
        if raw.startswith("以上。") and cur_chapter is not None:
            card = {"id": "", "title": "结尾：真正要背的只有三句", "kind": "ref",
                    "ask": "", "say": [], "detail": [], "probe": [], "red": []}
            cur_chapter["cards"].append(card)
            cur_card, cur_field = card, "detail"
            cur_card["detail"].append(("p", txt.replace("73 题", "79 题")))
            continue

        L, rest = split_label(txt)
        if L:
            cur_field = {"他在测什么": "ask", "照着说": "say", "这是什么": "detail",
                         "他要追的话": "probe", "红线": "red"}[L]
            if cur_field == "ask":
                if cur_card is not None:
                    cur_card["ask"] = rest
                cur_field = "detail"
            elif rest:
                tgt = cur_card or (pre_cards[-1] if in_pre and pre_cards else (appendix[-1] if appendix else None))
                if tgt is not None:
                    tgt[cur_field].append(("p", rest))
            continue

        tgt = cur_card or (pre_cards[-1] if in_pre and pre_cards else (appendix[-1] if appendix else None))
        if tgt is None:
            continue
        tgt[cur_field or "detail"].append(("p", txt))

    # ---- 修正前置卡标题（标题行本身被当作卡片标题，正文第一段是导语）----
    # ---- 组装 ----
    total = sum(len(c["cards"]) for c in chapters if re.match(r"^[一二三四五六七八九十]、", c["title"]))

    def rng(cards):
        ids = [c["id"] for c in cards if c["id"]]
        if not ids:
            return ""
        return "%s – %s" % (ids[0], ids[-1])

    blocks = [{"key": "pre", "title": "前置：怎么用 + 索引",
               "sub": "技能栏对照、组合问法、导读、贡献矩阵", "cards": pre_cards}]
    for c in chapters:
        n = len(c["cards"])
        sub = "%s · %d 题" % (rng(c["cards"]), n) if rng(c["cards"]) else "%d 张" % n
        blocks.append({"key": c["key"], "title": c["title"], "sub": sub, "cards": c["cards"]})

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write('"""自动生成，勿手改。源：AI应用开发岗面试问答手册-73题版-v6.docx"""\n\n')
        f.write("TOTAL = %d\n\n" % total)
        f.write("BLOCKS = " + repr(blocks) + "\n")

    print("blocks:", len(blocks), "cards:", sum(len(b["cards"]) for b in blocks), "题目:", total)
    for b in blocks:
        print("  -", b["key"], b["title"], "|", b["sub"], "|", len(b["cards"]))


if __name__ == "__main__":
    main()
