# -*- coding: utf-8 -*-
# figs_crc.py — Figures 1-2 and Supplementary Fig. S1, redrawn from the result tables and the district boundary file (no hand-entered numbers).
#  11/10·11/12 규칙: 패널 문자 모두 같은 크기(PANEL_LABEL_PT 하나)·대문자·48 pt, 방위표 3배(N 24 pt·화살표 lw 2.4), 지도 컬러 유지, 재포매팅 때도 다시 그림.
#  그림은 TIFF 따로, Arial/Helvetica, 폭 166 mm(두 단), 선화 ≥1200 dpi → 1200 dpi RGB TIFF LZW. 그림 안 설명문 없음, 한글 없음.
#  Fig 1 (a) 전 기간 잔차 공간 RR 지도 (b) 조율·연령표준화율 추이 · Fig 2 강건 4개 변수의 모형별 RR · 보충 그림 (a) EHSA (b) 세 창 핫·콜드스팟 횟수
import os, unicodedata, numpy as np, pandas as pd, geopandas as gpd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
from numbers_crc import load, ROB, SHP
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.dirname(os.path.dirname(HERE)); RS = os.path.join(B, "results_std3")
FIG = os.path.join(HERE, "figs"); OUTF = os.path.join(os.path.dirname(HERE), "out", "Figures"); os.makedirs(FIG, exist_ok=True); os.makedirs(OUTF, exist_ok=True)
MM = 1 / 25.4; W = 166 * MM; DPI = 1200; LW = 0.3
plt.rcParams.update({"font.family": "Arial", "font.size": 8, "legend.fontsize": 7.5, "legend.title_fontsize": 8, "axes.linewidth": 0.5, "pdf.fonttype": 42})
NFC = lambda s: unicodedata.normalize("NFC", str(s)).strip()
N = load()
G = gpd.read_file(SHP); G["cd"] = G.sigungu_cd.astype(str); G["sido"] = G.cd.str[:2]; SIDO = G.dissolve("sido")   # 결합은 시군구 코드(cd)로만, 이름 결합 금지
XL = (G.total_bounds[0], G.total_bounds[2]); YL = (G.total_bounds[1], G.total_bounds[3])
rd = lambda f: pd.read_csv(os.path.join(RS, f), encoding="utf-8-sig", dtype={"sigungu_cd": str})
PANEL_LABEL_PT = 48   # 11/10 규칙: 모든 패널 같은 크기·대문자·약 48-64 pt, 그림 좌표(fig.text) 하나의 상수
def letter(fig, ch, x, y):   # 그림 좌표 (x, y) = 문자 왼쪽 위
    fig.text(x, y, ch.upper(), fontsize=PANEL_LABEL_PT, fontweight="bold", va="top", ha="left")
def mapax(ax):
    SIDO.boundary.plot(ax=ax, color="#404040", linewidth=0.45); ax.set_xlim(*XL); ax.set_ylim(*YL); ax.set_axis_off(); ax.set_aspect("equal")
    x0, x1 = XL; y0, y1 = YL; W_ = x1 - x0; H_ = y1 - y0   # 방위표·축척(좌표 단위 m)
    bx, by = x0 + 0.62 * W_, y0 + 0.04 * H_
    ax.plot([bx, bx + 100000], [by, by], color="black", lw=1.2, solid_capstyle="butt"); ax.text(bx + 50000, by + 0.012 * H_, "100 km", ha="center", va="bottom", fontsize=7)
    ax.annotate("", xy=(x0 + 0.93 * W_, y0 + 0.99 * H_), xytext=(x0 + 0.93 * W_, y0 + 0.85 * H_), arrowprops=dict(arrowstyle="-|>,head_width=0.6,head_length=1.2", color="black", lw=2.4))
    ax.text(x0 + 0.93 * W_, y0 + 0.835 * H_, "N", ha="center", va="top", fontsize=24, fontweight="bold")   # 방위표 3배(글자와 화살표 분리)
def save(fig, k):
    p = os.path.join(FIG, f"Fig{k}.png"); fig.savefig(p, dpi=DPI, facecolor="white"); plt.close(fig)   # 폭 166 mm 고정(bbox tight 쓰지 않음)
    im = Image.open(p).convert("RGB"); im.save(p, dpi=(DPI, DPI))
    if k != "S1": im.save(os.path.join(OUTF, f"Figure_{k}.tif"), dpi=(DPI, DPI), compression="tiff_lzw")   # 보충 그림은 보충 파일 안에만
    return im.size

# Fig 1
S6 = rd("S6_spatial_RR.csv"); assert len(S6) == 229
BR = [0, 0.8, 0.9, 0.95, 1, 1.05, 1.1, 1.2, 99]; LB = ["<0.80", "0.80-0.89", "0.90-0.94", "0.95-0.99", "1.00-1.04", "1.05-1.09", "1.10-1.19", "≥1.20"]
PAL = ["#2166AC", "#4393C3", "#92C5DE", "#D1E5F0", "#FDDBC7", "#F4A582", "#D6604D", "#B2182B"]
fig = plt.figure(figsize=(W, 4.6)); a0 = fig.add_axes([0.05, 0.17, 0.47, 0.66]); a1 = fig.add_axes([0.66, 0.27, 0.32, 0.54])
d = S6.set_index("sigungu_cd"); gg = G.copy(); gg["v"] = gg.cd.map(d.RR); gg["c"] = gg.cd.map(d["class"]); assert gg.v.notna().all()
gg.plot(ax=a0, column="v", cmap=ListedColormap(PAL), norm=BoundaryNorm(BR, len(PAL)), edgecolor="#a0a0a0", linewidth=LW); mapax(a0)
gg[gg.c == "coldspot"].boundary.plot(ax=a0, color="#2171B5", linewidth=0.6, linestyle=(0, (2.0, 1.2))); gg[gg.c == "hotspot"].boundary.plot(ax=a0, color="black", linewidth=0.6); letter(fig, "a", 0.01, 0.995)
h = [Patch(facecolor=c, edgecolor="#777777", linewidth=LW, label=l) for c, l in zip(PAL, LB)] + [Patch(facecolor="none", edgecolor="black", linewidth=0.8, label="Hot spot"), Patch(facecolor="none", edgecolor="#2171B5", linewidth=0.8, linestyle="--", label="Cold spot")]
a0.legend(handles=h, title="Residual spatial RR", loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=3, frameon=False, columnspacing=0.8, handlelength=1.3)
yrs = sorted(N["asr"]); P = pd.read_csv(os.path.join(B, "panel_CRC_std3.csv")); y = P.groupby("year")[["cases", "offset"]].sum(); cr = 1e5 * y.cases / y.offset
assert abs(cr[2011] - N["crude_2011"]) < 1e-6 and abs(cr[2024] - N["crude_2024"]) < 1e-6
a1.plot(yrs, [cr[t] for t in yrs], color="#404040", marker="o", ms=2.5, lw=0.9, label="Crude")
a1.plot(yrs, [N["asr"][t] for t in yrs], color="#b2182b", marker="s", ms=2.5, lw=0.9, label="Age-standardised")
lo = min(min(cr), min(N["asr"].values())); hi = max(max(cr), max(N["asr"].values())); assert 200 < lo and hi < 360
a1.set_xticks([2011, 2014, 2017, 2020, 2024]); a1.set_ylim(200, 360); a1.set_ylabel("Treated persons per 100,000 population"); a1.set_xlabel("Year")
a1.spines[["top", "right"]].set_visible(False); a1.legend(frameon=False, loc="upper left"); letter(fig, "b", 0.56, 0.995)
s1 = save(fig, 1)

# 보충 그림
EH = rd("S11_ehsa.csv")
CATS = [f"{a} {b}" for b in ("hot", "cold") for a in ("New", "Consecutive", "Intensifying", "Persistent", "Diminishing", "Sporadic", "Oscillating", "Historical")] + ["No pattern"]
EPAL = {"New hot": "#fdd0a2", "Consecutive hot": "#fdae6b", "Intensifying hot": "#a50f15", "Persistent hot": "#de2d26", "Diminishing hot": "#fc9272", "Sporadic hot": "#fee0d2", "Oscillating hot": "#d6a5c9", "Historical hot": "#bcbddc",
        "New cold": "#c6dbef", "Consecutive cold": "#9ecae1", "Intensifying cold": "#08519c", "Persistent cold": "#3182bd", "Diminishing cold": "#6baed6", "Sporadic cold": "#deebf7", "Oscillating cold": "#a1d99b", "Historical cold": "#c7e9c0", "No pattern": "#f7f7f7"}
WM = rd("S4b_window_spatialRR.csv")
nh = WM[WM["class"] == "hotspot"].groupby("sigungu_cd").size(); nc = WM[WM["class"] == "coldspot"].groupby("sigungu_cd").size()
assert int((nh == 3).sum()) == N["hot_all_windows"] and int((nc == 3).sum()) == N["cold_all_windows"]
fig, (a0, a1) = plt.subplots(1, 2, figsize=(W, 4.4)); fig.subplots_adjust(left=0.01, right=0.99, top=0.84, bottom=0.27, wspace=0.04); fig.set_size_inches(W, 5.0)
gg = G.copy(); gg["c"] = gg.cd.map(EH.set_index("sigungu_cd").EHSA); assert gg.c.notna().all()
gg.plot(ax=a0, color=[EPAL[c] for c in gg.c], edgecolor="#a0a0a0", linewidth=LW); mapax(a0); letter(fig, "a", 0.01, 0.995)
cnt = EH.EHSA.value_counts(); pres = [c for c in CATS if c in cnt.index]
a0.legend(handles=[Patch(facecolor=EPAL[c], edgecolor="#777777", linewidth=LW, label=f"{c} ({cnt[c]})") for c in pres], title="Category (districts)", loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=2, frameon=False, columnspacing=0.8, handlelength=1.2)
hh = gg.cd.map(nh).fillna(0).astype(int); cc = gg.cd.map(nc).fillna(0).astype(int)
gg["k"] = np.where((hh > 0) & (cc > 0), 9, hh - cc)
KP = {-3: "#2166AC", -2: "#67A9CF", -1: "#D1E5F0", 0: "#f7f7f7", 1: "#FDDBC7", 2: "#EF8A62", 3: "#B2182B", 9: "#c2a5cf"}
KL = {-3: "Cold spot in 3 windows", -2: "Cold spot in 2", -1: "Cold spot in 1", 0: "Neither", 1: "Hot spot in 1", 2: "Hot spot in 2", 3: "Hot spot in 3 windows", 9: "Hot or cold by window"}
gg.plot(ax=a1, color=[KP[k] for k in gg.k], edgecolor="#a0a0a0", linewidth=LW); mapax(a1); letter(fig, "b", 0.51, 0.995)
kc = gg.k.value_counts()
a1.legend(handles=[Patch(facecolor=KP[k], edgecolor="#777777", linewidth=LW, label=f"{KL[k]} ({kc.get(k, 0)})") for k in (3, 2, 1, 0, -1, -2, -3, 9) if kc.get(k, 0)], title="Windows 2011-2015, 2016-2019, 2020-2024", loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=2, frameon=False, columnspacing=0.8, handlelength=1.2)
s2 = save(fig, "S1")

# Fig 2 — 부분집합 안정 4개 변수의 모형별 RR
LAB = {"screening_normalB_diabetes_share": "Borderline glucose\n(attendees)", "screening_normalB_obesity_share": "Borderline obesity\n(attendees)",
       "walking_practice_rate": "Walking practice", "older_single_household_share": "Older-adult single-person\nhouseholds"}
ORD = ["screening_normalB_diabetes_share", "screening_normalB_obesity_share", "walking_practice_rate", "older_single_household_share"]
assert set(ORD) == set(ROB)
MOD = [("Principal model", lambda v: (N["main"][v]["IRR"], N["main"][v]["lo"], N["main"][v]["hi"]), "#000000", "o"),
       ("Knorr-Held type II (best fitting)", lambda v: N["s43"][("KH_typeII", v)][:3], "#2166AC", "s"),
       ("Knorr-Held type IV", lambda v: N["s43"][("KH_typeIV", v)][:3], "#B2182B", "D"),
       ("Within-district component", lambda v: N["bw"][v + "__within"][:3], "#1b7837", "v"),
       ("Between-district component", lambda v: N["bw"][v + "__between"][:3], "#E08214", "P"),
       ("Gastric cancer (comparison outcome)", lambda v: N["nco"][("GCA", v)][:3], "#7f7f7f", "^")]
lo_all = min(f(v)[1] for v in ORD for _, f, _, _ in MOD); hi_all = max(f(v)[2] for v in ORD for _, f, _, _ in MOD)
fig, ax = plt.subplots(figsize=(W, 3.5)); fig.subplots_adjust(left=0.27, right=0.98, top=0.97, bottom=0.25)
off = np.linspace(-0.32, 0.32, len(MOD))
for i, v in enumerate(ORD):
    for (lab, f, col, mk), o in zip(MOD, off):
        e, lo, hi = f(v); ax.plot([lo, hi], [i + o] * 2, color=col, lw=0.8); ax.plot(e, i + o, marker=mk, color=col, ms=3.2, mew=0, ls="none")
ax.axvline(1, color="#404040", lw=0.5, ls=":"); ax.set_yticks(range(len(ORD))); ax.set_yticklabels([LAB[v] for v in ORD]); ax.invert_yaxis()
xt = [0.92, 0.94, 0.96, 0.98, 1.00, 1.02, 1.04]; assert xt[0] <= lo_all and hi_all <= xt[-1], (lo_all, hi_all)
ax.set_xlim(xt[0], xt[-1]); ax.set_xticks(xt); ax.set_xticklabels([f"{x:.2f}" for x in xt]); ax.minorticks_off()
ax.set_xlabel("Rate ratio per 1 SD (95% credible interval)"); ax.spines[["top", "right"]].set_visible(False)
ax.legend(handles=[Line2D([0], [0], color=c, marker=m, lw=0.8, ms=3.2, mew=0, label=l) for l, _, c, m in MOD], loc="upper center", bbox_to_anchor=(0.36, -0.16), ncol=3, frameon=False)
s3 = save(fig, 2)
for k, s in zip((1, "S1", 2), (s1, s2, s3)): print(f"Fig{k}: {s[0]}x{s[1]} px = {s[0]/DPI*25.4:.0f} x {s[1]/DPI*25.4:.0f} mm")
