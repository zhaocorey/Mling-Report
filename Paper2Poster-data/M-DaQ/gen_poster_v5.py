#!/usr/bin/env python3
"""M-DaQ Poster v5 for SIGIR 2026.
Fixes from v4:
  1. Larger fonts, less whitespace
  2. Logos stacked vertically on top-right
  3. Use new SIGIR logo (SVG→PNG)
  4. Fix overlaps with proper zone layout
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Cm, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

PAPER_PDF = "paper.pdf"
OUTPUT_DIR = "_output"
W = 33.1; H = 46.8

C_DARK   = RGBColor(0x1B, 0x3A, 0x5C)
C_ACCENT = RGBColor(0xE8, 0x79, 0x2B)
C_WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
C_BLACK  = RGBColor(0x22, 0x22, 0x22)
C_GRAY   = RGBColor(0x66, 0x66, 0x66)
C_BG     = RGBColor(0xF0, 0xF4, 0xF8)
C_DIVIDER = RGBColor(0xDD, 0xDD, 0xDD)

LOGO_DIR = "logos"
SIGIR_LOGO = os.path.join(LOGO_DIR, "SIGIR_2026_N_Odate_pos_73a5d01432.png")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Extract figures ──
import fitz
print("📄 Extracting figures...")
doc = fitz.open(PAPER_PDF)
figs = {}
for pi in range(len(doc)):
    page = doc[pi]
    for ii, info in enumerate(page.get_images(full=True)):
        base = doc.extract_image(info[0])
        if base and base["width"] > 200 and base["height"] > 150:
            key = f"fig_p{pi}_{ii}"
            path = os.path.join(OUTPUT_DIR, f"{key}.png")
            with open(path, "wb") as f:
                f.write(base["image"])
            figs[key] = {"path": path, "w": base["width"], "h": base["height"]}
doc.close()
print(f"  {len(figs)} figures")

# ── Presentation ──
print("🎨 Building poster v5...")
prs = Presentation()
prs.slide_width = Inches(W); prs.slide_height = Inches(H)
sl = prs.slides.add_slide(prs.slide_layouts[6])

def sc(run, rgb):
    hv = str(rgb)
    rPr = run._r.get_or_add_rPr()
    for old in rPr.findall(qn('a:solidFill')): rPr.remove(old)
    sf = etree.SubElement(rPr, qn('a:solidFill'))
    srgb = etree.SubElement(sf, qn('a:srgbClr'))
    srgb.set('val', hv)

def tb(l, t, w, h, text, sz=24, bold=False, color=C_BLACK, al=PP_ALIGN.LEFT, font="Arial", fill=None):
    box = sl.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; run = p.add_run()
    run.text = text; run.font.size = Pt(sz); run.font.bold = bold; run.font.name = font
    sc(run, color); p.alignment = al
    if fill: box.fill.solid(); box.fill.fore_color.rgb = fill
    return box

def multi(l, t, w, h, paras, fill=None):
    box = sl.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame; tf.word_wrap = True
    for i, (txt, sz, b, col, al, sp) in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        if txt:
            run = p.add_run(); run.text = txt; run.font.size = Pt(sz)
            run.font.bold = b; run.font.name = "Arial"; sc(run, col)
        p.alignment = al; p.space_after = Pt(sp)
    if fill: box.fill.solid(); box.fill.fore_color.rgb = fill
    return box

def blt(l, t, w, h, items, sz=24, color=C_BLACK, sp=Pt(10)):
    box = sl.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame; tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        run = p.add_run(); run.text = f"• {item}"; run.font.size = Pt(sz)
        run.font.name = "Arial"; sc(run, color); p.space_after = sp
    return box

def hdr(x, y, text, num=None):
    label = f"{num}  {text}" if num else text
    tb(x, y, CW, 0.5, label, sz=34, bold=True, color=C_DARK)
    line = sl.shapes.add_shape(1, Inches(x), Inches(y+0.5), Inches(CW), Inches(0.05))
    line.fill.solid(); line.fill.fore_color.rgb = C_ACCENT; line.line.fill.background()
    return y + 0.7

def img(path, left, top, width=None, height=None):
    if not os.path.exists(path): return 0
    kw = {"image_file": path, "left": Inches(left), "top": Inches(top)}
    if width: kw["width"] = Inches(width)
    if height: kw["height"] = Inches(height)
    sl.shapes.add_picture(**kw)
    for v in figs.values():
        if v["path"] == path and width:
            return v["h"] * width / v["w"]
    from PIL import Image
    im = Image.open(path)
    if height: return height
    if width: return im.size[1] * width / im.size[0]
    return 0

# ── Layout: 2 columns ──
MARGIN = 0.8; GAP = 0.5
CW = (W - 2*MARGIN - GAP) / 2  # ~15.5"
C1 = MARGIN
C2 = MARGIN + CW + GAP

# ══ TITLE BAR (light, 3.2") ═══
TH = 3.2
bg = sl.shapes.add_shape(1, Inches(0), Inches(0), Inches(W), Inches(TH))
bg.fill.solid(); bg.fill.fore_color.rgb = C_WHITE; bg.line.fill.background()

# Bottom border
bd = sl.shapes.add_shape(1, Inches(0), Inches(TH), Inches(W), Inches(0.04))
bd.fill.solid(); bd.fill.fore_color.rgb = C_DARK; bd.line.fill.background()

# ── Logos stacked vertically on TOP-RIGHT ──
# Right edge area: from W-5.0 to W-0.5 (4.5" wide)
logo_x = W - 4.8
logo_w = 3.5
logo_gap = 0.15
# Stack: Huawei (top), SIGIR (middle), USTC (bottom)
logos = [
    ("huawei_logo.png", 0.25, 0.6),       # y, height
    (SIGIR_LOGO, 0.95, 1.0),               # SIGIR logo
    ("ustc_logo.png", 2.05, 0.6),          # USTC
]
for lp, ly, lh in logos:
    p = os.path.join(LOGO_DIR, lp) if not lp.endswith('.png') and 'SIGIR' not in lp else lp
    if not os.path.exists(p):
        p = os.path.join(LOGO_DIR, os.path.basename(lp))
    if os.path.exists(p):
        img(p, logo_x, ly, height=lh)

# ── Title (left-aligned, below logos area) ──
title_w = W - 6.0  # Leave space for logos on right
tb(0.8, 0.3, title_w, 1.0,
   "M-DaQ: Retrieving Samples with Multilingual Diversity and Quality for Instruction Fine-Tuning Datasets",
   sz=42, bold=True, color=C_DARK, al=PP_ALIGN.LEFT)

# Authors (single line, smaller)
tb(0.8, 1.35, title_w, 0.4,
   "Chunguang Zhao¹, Yilun Liu¹, Pufan Zeng², Yuanchang Luo¹, Shimin Tao¹, Minggui He¹, Weibin Meng¹, Song Xu², Chen Liu¹, Hongxia Ma¹, Li Zhang¹, Boxing Chen¹, Daimeng Wei¹",
   sz=18, color=C_BLACK, al=PP_ALIGN.LEFT)

# Affiliations + conference
tb(0.8, 1.75, title_w, 0.35,
   "¹ Huawei Technologies Ltd.  ² University of Science and Technology of China  |  SIGIR 2026 · Melbourne · July 20–24",
   sz=17, color=C_GRAY, al=PP_ALIGN.LEFT)

YS = TH + 0.25   # 3.45
FY = H - 0.4     # 46.4
AVAIL = FY - YS  # ~43"

# ═══════════════════════════════════════
# COLUMN 1: Motivation → Method → Pipeline
# ═══════════════════════════════════════
y = YS

# 1. MOTIVATION
y = hdr(C1, y, "MOTIVATION", "1")
blt(C1, y, CW, 4.0, [
    "Multilingual IFT data is scarce, skewed toward English, lacks systematic curation",
    "Llama-3 IFT dataset: only 3.01% multilingual samples",
    "No language-agnostic quality scoring for multilingual data",
    "Data diversity studied only in English settings",
    "Superficial Alignment Hypothesis (SAH) unverified in multilingual contexts",
], sz=22, sp=Pt(8))
y += 4.5

# Challenges
tb(C1, y, CW, 0.35, "Three Challenges Addressed:", sz=22, bold=True, color=C_DARK)
y += 0.45
for cid, ch, sol in [
    ("C1", "No extensible quality scoring for multilingual IFT", "→ QSM with triplet loss"),
    ("C2", "Diversity selection limited to English", "→ DAS inspired by MMR"),
    ("C3", "SAH unverified in multilingual settings", "→ 1K→52K study, 8 langs"),
]:
    badge = sl.shapes.add_shape(1, Inches(C1), Inches(y), Inches(0.45), Inches(0.32))
    badge.fill.solid(); badge.fill.fore_color.rgb = C_ACCENT; badge.line.fill.background()
    tb(C1+0.02, y+0.01, 0.42, 0.3, cid, sz=16, bold=True, color=C_WHITE, al=PP_ALIGN.CENTER)
    multi(C1+0.55, y, CW-0.55, 0.7, [
        (ch, 20, False, C_BLACK, PP_ALIGN.LEFT, 1),
        (sol, 19, True, C_ACCENT, PP_ALIGN.LEFT, 2),
    ])
    y += 0.75
y += 0.2

# 2. METHOD
y = hdr(C1, y, "METHOD: M-DaQ FRAMEWORK", "2")
tb(C1, y, CW, 0.35, "Stage 1: Quality Scoring Model (QSM)", sz=24, bold=True, color=C_ACCENT)
y += 0.4
blt(C1, y, CW, 2.5, [
    "Fine-tuned on ~2.3K expert-revised samples × 18 languages (from MIDB)",
    "Triplet loss: instruction → positive (expert-revised) vs negative (original/MT)",
    "Language-agnostic quality signal from embedding space",
], sz=20, sp=Pt(8))
y += 2.8
tb(C1, y, CW, 0.35, "Stage 2: Diversity-Aware Selection (DAS)", sz=24, bold=True, color=C_ACCENT)
y += 0.4
blt(C1, y, CW, 3.5, [
    "MMR-inspired: Quality ≈ Relevance, Diversity ≈ Novelty",
    "Two-stage pipeline reduces O(n²) → O(n log n)",
    "  Stage A: Select top-n by QSM score (quality subset)",
    "  Stage B: Greedily augment from uncovered clusters (diversity subset)",
    "Ratio n_quality : n_diversity = 6:1 (empirically tuned)",
], sz=20, sp=Pt(8))
y += 3.8

# Pipeline figure (fills rest of col1)
pipe = figs.get("fig_p1_1")
if pipe:
    remain = FY - y - 0.5
    aspect = pipe["h"] * CW / pipe["w"]
    fh = min(remain, aspect)
    fh = max(fh, 4.0)
    img(pipe["path"], C1, y, width=CW)
    tb(C1, y+fh+0.05, CW, 0.35,
       "Figure: M-DaQ two-stage pipeline (QSM + DAS)",
       sz=16, color=C_GRAY, al=PP_ALIGN.CENTER)

# ═══════════════════════════════════════
# COLUMN 2: Results → HumanEval → SAH → Conclusion → Contact
# ═══════════════════════════════════════
y = YS

# 3. KEY RESULTS
y = hdr(C2, y, "KEY RESULTS", "3")

# Stats card
card = sl.shapes.add_shape(1, Inches(C2), Inches(y), Inches(CW), Inches(1.2))
card.fill.solid(); card.fill.fore_color.rgb = C_BG; card.line.fill.background()
multi(C2+0.2, y+0.08, CW-0.4, 1.0, [
    ("LLM-as-Judge: Avg Win Rate (M-DaQ vs Vanilla)", 22, True, C_DARK, PP_ALIGN.CENTER, 8),
    ("Alpaca-Eval: 60.2%  ·  MT-Bench R1: 62.6%  ·  MT-Bench R2: 62.9%",
     22, True, C_ACCENT, PP_ALIGN.CENTER, 2),
])
y += 1.4

# Win rate figure
wrf = figs.get("fig_p1_0")
if wrf:
    aspect = wrf["h"] * CW / wrf["w"]
    fh = min(7.0, aspect)
    fh = max(fh, 4.5)
    img(wrf["path"], C2, y, width=CW)
    tb(C2, y+fh+0.05, CW, 0.35,
       "Cross-lingual win rates across 18 languages (Alpaca-Eval + MT-Bench)",
       sz=16, color=C_GRAY, al=PP_ALIGN.CENTER)
    y += fh + 0.5

# Key observations
blt(C2, y, CW, 2.0, [
    "Consistent improvement across all 18 languages",
    "Gains MORE pronounced in low-resource languages (Tagalog, Malay)",
    "M-DaQ mitigates linguistic imbalance and data scarcity",
], sz=20, sp=Pt(8))
y += 2.5

# 4. HUMAN EVALUATION
y = hdr(C2, y, "HUMAN EVALUATION", "4")
tb(C2, y, CW, 0.35, "6 Languages · 900 Samples · 58 Person-Hours", sz=20, bold=True, color=C_DARK)
y += 0.4

rows = [
    ("Language", "Alpaca-Eval", "MT-Bench R1", "MT-Bench R2"),
    ("Japanese", "86%", "84%", "80%"), ("Korean", "94%", "94%", "94%"),
    ("Russian", "70%", "86%", "84%"), ("Portuguese", "80%", "78%", "84%"),
    ("Greek", "58%", "76%", "82%"), ("French", "80%", "92%", "88%"),
    ("Average", "78.0%", "85.0%", "85.3%"),
]
nr = len(rows); rh = 0.40
tbl_s = sl.shapes.add_table(nr, 4, Inches(C2), Inches(y), Inches(CW), Inches(rh*nr))
tbl = tbl_s.table
for ci, cw in enumerate([CW*0.30, CW*0.24, CW*0.23, CW*0.23]):
    tbl.columns[ci].width = Inches(cw)
for ci, h in enumerate(rows[0]):
    cell = tbl.cell(0, ci); cell.text = h
    for p in cell.text_frame.paragraphs:
        p.alignment = PP_ALIGN.CENTER
        for r in p.runs: r.font.size=Pt(18); r.font.bold=True; r.font.name="Arial"; sc(r, C_WHITE)
    cell.fill.solid(); cell.fill.fore_color.rgb = C_DARK
for ri, row in enumerate(rows[1:], 1):
    for ci, val in enumerate(row):
        cell = tbl.cell(ri, ci); cell.text = val
        for p in cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            for r in p.runs:
                r.font.size=Pt(17); r.font.name="Arial"
                r.font.bold = (ri==nr-1); sc(r, C_DARK if (ci==0 or ri==nr-1) else C_BLACK)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_BG if ri%2==0 else C_WHITE
y += rh*nr + 0.3

# 5. SAH
y = hdr(C2, y, "SAH IN MULTILINGUAL SETTINGS", "5")
tb(C2, y, CW, 0.4,
   "First systematic investigation of SAH across languages.", sz=20)
y += 0.5

sah = figs.get("fig_p4_1")
if sah:
    aspect = sah["h"] * CW / sah["w"]
    fh = min(5.5, aspect)
    fh = max(fh, 3.0)
    img(sah["path"], C2, y, width=CW)
    tb(C2, y+fh+0.05, CW, 0.35,
       "Win rate vs IFT dataset scale (1K–52K), 8 languages",
       sz=16, color=C_GRAY, al=PP_ALIGN.CENTER)
    y += fh + 0.5

blt(C2, y, CW, 3.5, [
    "✅  Diminishing returns: 1K curated > 52K unfiltered — SAH holds",
    "     10K → −10.1% avg win rate;  52K → −6.2% vs 1K baseline",
    "⚠️  Language-dependent: Arabic flatter than French",
    "  A few thousand high-quality samples suffice for multilingual alignment",
], sz=20, sp=Pt(8))
y += 3.5

# 6. CONCLUSION
y = hdr(C2, y, "CONCLUSION", "6")
blt(C2, y, CW, 4.0, [
    "M-DaQ = QSM + DAS: compact, high-fidelity multilingual IFT subsets",
    "60%+ avg win rate across 18 languages on Alpaca-Eval & MT-Bench",
    "Human eval confirms cultural relevance & instruction-following gains",
    "First empirical validation of SAH in multilingual settings",
    "Code: github.com/zhaocorey/M-DaQ",
], sz=20, sp=Pt(10))
y += 4.2

# CONTACT CARD
ch = 3.0
if y + ch > FY:
    y = FY - ch - 0.2
card = sl.shapes.add_shape(1, Inches(C2), Inches(y), Inches(CW), Inches(ch))
card.fill.solid(); card.fill.fore_color.rgb = C_BG; card.line.fill.background()
multi(C2+0.3, y+0.2, CW-0.6, ch-0.3, [
    ("📎  Code & Resources", 22, True, C_DARK, PP_ALIGN.LEFT, 8),
    ("     github.com/zhaocorey/M-DaQ", 18, False, C_BLACK, PP_ALIGN.LEFT, 10),
    ("  Paper", 22, True, C_DARK, PP_ALIGN.LEFT, 8),
    ("     DOI: 10.1145/3805712.3809946   |   arXiv: 2509.15549", 18, False, C_BLACK, PP_ALIGN.LEFT, 10),
    ("📧  Contact", 22, True, C_DARK, PP_ALIGN.LEFT, 8),
    ("     zhaochunguang6@huawei.com   |   +86-15501192353", 18, False, C_BLACK, PP_ALIGN.LEFT, 4),
])

# ── Footer ──
tb(0, FY, W, 0.35, "SIGIR 2026  ·  Melbourne, VIC, Australia  ·  July 20–24, 2026",
   sz=16, color=C_GRAY, al=PP_ALIGN.CENTER)

# ── Column divider ──
dx = C1 + CW + GAP/2 - 0.015
dv = sl.shapes.add_shape(1, Inches(dx), Inches(YS), Inches(0.03), Inches(AVAIL))
dv.fill.solid(); dv.fill.fore_color.rgb = C_DIVIDER; dv.line.fill.background()

# ── Save ──
out = os.path.join(OUTPUT_DIR, "M-DaQ_poster_v5.pptx")
prs.save(out)
print(f"\n✅ PPTX: {out}")

import subprocess
try:
    subprocess.run(["libreoffice","--headless","--convert-to","pdf","--outdir",OUTPUT_DIR,out],
                    timeout=60, capture_output=True)
    pdf = out.replace(".pptx",".pdf")
    if os.path.exists(pdf):
        print(f"✅ PDF:  {pdf}")
        subprocess.run(["libreoffice","--headless","--convert-to","png","--outdir",OUTPUT_DIR,pdf],
                        timeout=60, capture_output=True)
        png = out.replace(".pptx","_preview.png")
        raw = out.replace(".pptx",".png")
        if os.path.exists(raw): os.rename(raw, png)
        if os.path.exists(png): print(f"✅ PNG:  {png}")
except Exception as e:
    print(f"⚠️  LibreOffice: {e}")
