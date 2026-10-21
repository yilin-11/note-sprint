"""Dimensioned drawing of the stand (matches magsafe_stand.scad defaults).

Usage: python3 drawing.py   ->  drawing.pdf, drawing.png   (needs matplotlib, numpy)
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Polygon

# ---- Parameters (keep in sync with magsafe_stand.scad) ----
PUCK_D, PUCK_H, FIT, PROUD = 60.0, 8.1, 0.3, 0.6
ANGLE = 70
PLATE_W, PLATE_L, PLATE_T, PLATE_R = 74, 125, 11, 12
PUCK_C = 88
BASE_W, BASE_D, BASE_H, BASE_R = 92, 100, 7, 10
PUSH_D, SLOT_W, GROOVE_W, GROOVE_H = 24, 6.5, 5.0, 4.5
FILLET_R = 15

POCKET_D = PUCK_D + FIT
POCKET_DEPTH = PUCK_H - PROUD
a = math.radians(ANGLE)
D = np.array([math.cos(a), math.sin(a)])      # up the slope
N = np.array([-math.sin(a), math.cos(a)])     # out of the front face
O = np.array([0.0, BASE_H])
BACK_Y = PLATE_T * math.sin(a)                 # slot through base ends at BACK_Y + 1


def w2(u, w):
    """Plate frame (u along slope, w out of face) -> side view (Y, Z)."""
    return O + u * D + w * N


INK, THIN, DIM = "#111", 0.6, "#1f5fa8"
fig = plt.figure(figsize=(16.54, 11.69))       # A3 landscape
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 640)
ax.set_ylim(0, 452)
ax.set_aspect("equal")
ax.axis("off")


def line(p, q, ls="-", lw=1.4, c=INK, off=(0, 0)):
    ax.plot([p[0] + off[0], q[0] + off[0]], [p[1] + off[1], q[1] + off[1]], ls=ls, lw=lw, c=c,
            solid_capstyle="round")


def poly(pts, off, **kw):
    pts = np.asarray(pts) + off
    ax.add_patch(Polygon(pts, closed=True, **kw))


def text(x, y, s, size=9, **kw):
    ax.text(x, y, s, fontsize=size, color=kw.pop("c", INK), ha=kw.pop("ha", "center"),
            va=kw.pop("va", "center"), **kw)


def dim(p, q, off, label=None, off0=(0, 0), tside=1, size=8.5):
    """Aligned dimension between p and q, pushed `off` mm along the left normal of p->q."""
    p, q = np.asarray(p, float) + off0, np.asarray(q, float) + off0
    t = (q - p) / np.linalg.norm(q - p)
    n = np.array([-t[1], t[0]])
    p2, q2 = p + n * off, q + n * off
    for s, e in ((p, p2), (q, q2)):
        line(s + n * math.copysign(1, off), e + n * math.copysign(1.5, off), lw=0.5, c=DIM)
    ax.annotate("", p2, q2, arrowprops=dict(arrowstyle="<|-|>", color=DIM, lw=0.7,
                                             mutation_scale=7, shrinkA=0, shrinkB=0))
    m = (p2 + q2) / 2 + n * 3.2 * tside
    ang = math.degrees(math.atan2(t[1], t[0]))
    if ang > 90.1 or ang < -89.9:
        ang -= 180
    label = label or f"{np.linalg.norm(q - p):.1f}".removesuffix(".0")
    text(m[0], m[1], label, size, c=DIM, rotation=ang)


def leader(p, q, label, off0=(0, 0), ha="left"):
    p, q = np.asarray(p) + off0, np.asarray(q) + off0
    ax.annotate("", p, q, arrowprops=dict(arrowstyle="-|>", color=DIM, lw=0.6, mutation_scale=7))
    text(q[0] + (1.5 if ha == "left" else -1.5), q[1], label, 8.5, c=DIM, ha=ha)


def title(x, y, s, sub=None):
    text(x, y, s, 11, weight="bold")
    if sub:
        text(x, y - 6, sub, 8, c="#555")


# ---------------- Shared side-profile geometry ----------------
P0, P1 = w2(0, 0), w2(PLATE_L, 0)
P2, P3 = w2(PLATE_L, -PLATE_T), w2(0, -PLATE_T)
nb = -N                                        # normal pointing behind the plate
cy = P3[0] + (FILLET_R - nb[1] * (BASE_H + FILLET_R - P3[1])) / nb[0]
FC = np.array([cy, BASE_H + FILLET_R])         # fillet centre
FT_BASE = np.array([cy, BASE_H])
FT_BACK = FC - FILLET_R * nb
arc_a0 = math.degrees(math.atan2(*(FT_BACK - FC)[::-1]))


def fillet_pts(n=24):
    angs = np.linspace(math.radians(arc_a0), math.radians(270), n)
    return [FC + FILLET_R * np.array([math.cos(t), math.sin(t)]) for t in angs]


def profile(pocket_half_chord=None):
    """Outer side profile; optionally notched by the pocket (for the section)."""
    pts = [(0, 0), (BASE_D, 0), (BASE_D, BASE_H)]
    pts += fillet_pts()[::-1]
    pts += [P2, P1]
    if pocket_half_chord:
        u0, u1 = PUCK_C - pocket_half_chord, PUCK_C + pocket_half_chord
        pts += [w2(u1, 0), w2(u1, -POCKET_DEPTH), w2(u0, -POCKET_DEPTH), w2(u0, 0)]
    pts += [P0]
    return np.array(pts)


# ---------------- 1. Side view ----------------
S = np.array([45, 235])
poly(profile(), S, fill=False, ec=INK, lw=1.4)
# hidden: pocket, push hole, groove, base slot
hid = dict(ls=(0, (4, 2)), lw=0.7, c="#666", off=S)
u0, u1 = PUCK_C - POCKET_D / 2, PUCK_C + POCKET_D / 2
line(w2(u0, 0), w2(u0, -POCKET_DEPTH), **hid)
line(w2(u1, 0), w2(u1, -POCKET_DEPTH), **hid)
line(w2(u0, -POCKET_DEPTH), w2(u1, -POCKET_DEPTH), **hid)
for u in (PUCK_C - PUSH_D / 2, PUCK_C + PUSH_D / 2):
    line(w2(u, -POCKET_DEPTH), w2(u, -PLATE_T), **hid)
line((0, GROOVE_H), (BASE_D, GROOVE_H), **hid)
line((BACK_Y + 1, 0), (BACK_Y + 1, BASE_H), **hid)
line(w2(PUCK_C, 14), w2(PUCK_C, -PLATE_T - 6), ls=(0, (10, 2, 2, 2)), lw=0.5, c=INK, off=S)
# dims
dim((0, 0), (BASE_D, 0), -12, off0=S, tside=-1)
dim((BASE_D, 0), (BASE_D, BASE_H), -7, off0=S, tside=-1)
dim((BASE_D + 4, 0), (BASE_D + 4, P1[1]), -14, f"{P1[1]:.1f}", off0=S, tside=-1)
dim(P0, P1, 12, f"{PLATE_L}", off0=S)
dim(w2(PLATE_L, 0), w2(PLATE_L, -PLATE_T), 7, f"{PLATE_T}", off0=S)
dim(P0, w2(PUCK_C, 0), 26, f"{PUCK_C} (puck centre)", off0=S)
ax.add_patch(Arc(S + P0, 44, 44, theta1=0, theta2=ANGLE, color=DIM, lw=0.7))
text(*(S + P0 + 26 * np.array([math.cos(a / 2), math.sin(a / 2)])), f"{ANGLE}°", 9, c=DIM)
leader(FC + FILLET_R * np.array([math.cos(math.radians(215)), math.sin(math.radians(215))]),
       FC + np.array([18, 22]), f"R{FILLET_R}", off0=S)
leader((BACK_Y + 1, 3), (BACK_Y + 40, 17), f"slot thru base to {BACK_Y + 1:.1f}", off0=S)
title(S[0] + 50, 205, "SIDE VIEW", "hidden lines: pocket, push hole, cable groove")

# ---------------- 2. Section B-B (X = 15) ----------------
X = 15
half = math.sqrt((POCKET_D / 2) ** 2 - X ** 2)
B = np.array([205, 235])
poly(profile(half), B, fill=False, ec=INK, lw=1.4, hatch="////")
# puck phantom
pk = [w2(PUCK_C - half, -POCKET_DEPTH), w2(PUCK_C + half, -POCKET_DEPTH),
      w2(PUCK_C + half, PROUD), w2(PUCK_C - half, PROUD)]
poly(pk, B, fill=True, fc="#dbe7f5", ec="#3b6fb6", lw=0.8, ls="--")
text(*(B + w2(PUCK_C, -POCKET_DEPTH / 2 + 0.3)), "puck", 7.5, c="#3b6fb6", rotation=ANGLE)
leader(w2(PUCK_C + 10, -POCKET_DEPTH), w2(PUCK_C + 25, -PLATE_T - 30),
       f"pocket floor: {POCKET_DEPTH} deep", off0=B)
leader(w2(PUCK_C - 10, -PLATE_T), w2(PUCK_C - 20, -PLATE_T - 30),
       f"{PLATE_T - POCKET_DEPTH:g} wall behind puck", off0=B)
leader(w2(PUCK_C - half + 2, PROUD), w2(PUCK_C - half - 5, 18), f"puck {PROUD} proud",
       off0=B, ha="right")
title(B[0] + 50, 205, "SECTION B-B  (X = 15 mm)", "pocket depth; puck shown dashed")

# ---------------- 3. View A (normal to plate face) ----------------
A = np.array([418, 235])
r = PLATE_R
outline = [(-PLATE_W / 2, 0), (PLATE_W / 2, 0)]
for cx, a0, a1 in ((PLATE_W / 2 - r, 0, 90), (-PLATE_W / 2 + r, 90, 180)):
    for t in np.linspace(math.radians(a0), math.radians(a1), 16):
        outline.append((cx + r * math.cos(t), PLATE_L - r + r * math.sin(t)))
poly(outline, A, fill=False, ec=INK, lw=1.4)
ax.add_patch(plt.Circle(A + (0, PUCK_C), POCKET_D / 2, fill=False, ec=INK, lw=1.2))
ax.add_patch(plt.Circle(A + (0, PUCK_C), PUSH_D / 2, fill=True, fc="#eee", ec=INK, lw=1.2))
y_hole = PUCK_C - math.sqrt((PUSH_D / 2) ** 2 - (SLOT_W / 2) ** 2)
for sx in (-SLOT_W / 2, SLOT_W / 2):
    line((sx, 0), (sx, y_hole), off=A, lw=1.2)
ax.add_patch(Polygon(A + np.array([(-SLOT_W / 2, 0), (SLOT_W / 2, 0), (SLOT_W / 2, y_hole),
                                   (-SLOT_W / 2, y_hole)]), fc="#eee", ec="none"))
cl = dict(ls=(0, (10, 2, 2, 2)), lw=0.5, c=INK, off=A)
line((-POCKET_D / 2 - 5, PUCK_C), (POCKET_D / 2 + 5, PUCK_C), **cl)
line((0, PUCK_C - POCKET_D / 2 - 5), (0, PUCK_C + POCKET_D / 2 + 5), **cl)
line((X, PUCK_C - 40), (X, PUCK_C + 40), ls="-.", lw=0.8, c="#b03030", off=A)
text(A[0] + X + 3, A[1] + PUCK_C + 42, "B", 9, c="#b03030", weight="bold")
dim((-PLATE_W / 2, 0), (PLATE_W / 2, 0), -10, off0=A, tside=-1)
dim((-PLATE_W / 2, 0), (-PLATE_W / 2, PLATE_L), 10, off0=A)
dim((-PLATE_W / 2, 0), (-PLATE_W / 2, PUCK_C), 22, off0=A)
dim((-SLOT_W / 2, 20), (SLOT_W / 2, 20), -6, f"{SLOT_W}", off0=A, tside=-1, size=7.5)
leader((POCKET_D / 2 * math.cos(0.9), PUCK_C + POCKET_D / 2 * math.sin(0.9)),
       (42, PUCK_C + 18), f"Ø{POCKET_D:g} pocket ↓{POCKET_DEPTH}", off0=A)
leader((PUSH_D / 2 * math.cos(2.4), PUCK_C + PUSH_D / 2 * math.sin(2.4)),
       (-30, PUCK_C + 50), f"Ø{PUSH_D} thru", off0=A, ha="right")
leader((PLATE_W / 2 - r + r * math.cos(0.8), PLATE_L - r + r * math.sin(0.8)),
       (PLATE_W / 2 + 4, PLATE_L + 8), f"R{PLATE_R}", off0=A)
leader((SLOT_W / 2, 45), (22, 40), "slot thru plate", off0=A)
title(A[0], 205, "VIEW A", "looking straight at the plate face")

# ---------------- 4. Bottom view ----------------
U = np.array([540, 255])
br = BASE_R
pts = []
for (cx, cyy), (a0, a1) in zip(((BASE_W / 2 - br, br), (BASE_W / 2 - br, BASE_D - br),
                                (-BASE_W / 2 + br, BASE_D - br), (-BASE_W / 2 + br, br)),
                               ((270, 360), (0, 90), (90, 180), (180, 270))):
    for t in np.linspace(math.radians(a0), math.radians(a1), 12):
        pts.append((cx + br * math.cos(t), cyy + br * math.sin(t)))
poly(pts, U, fill=False, ec=INK, lw=1.4)
slot_end = BACK_Y + 1
cut = [(-SLOT_W / 2, 0), (SLOT_W / 2, 0), (SLOT_W / 2, slot_end), (GROOVE_W / 2, slot_end),
       (GROOVE_W / 2, BASE_D), (-GROOVE_W / 2, BASE_D), (-GROOVE_W / 2, slot_end),
       (-SLOT_W / 2, slot_end)]
poly(cut, U, fill=True, fc="#eee", ec=INK, lw=1.1)
foot = 11.7
line((-PLATE_W / 2, foot), (PLATE_W / 2, foot), ls=(0, (4, 2)), lw=0.7, c="#666", off=U)
dim((-BASE_W / 2, 0), (BASE_W / 2, 0), -10, off0=U, tside=-1)
dim((BASE_W / 2, 0), (BASE_W / 2, BASE_D), -9, off0=U, tside=-1)
dim((-SLOT_W / 2, 0), (-SLOT_W / 2, slot_end), 12, f"{slot_end:.1f}", off0=U, size=7.5)
dim((-GROOVE_W / 2, 70), (GROOVE_W / 2, 70), 6, f"{GROOVE_W:g}", off0=U, size=7.5)
leader((BASE_W / 2 - br + br * math.cos(0.8), BASE_D - br + br * math.sin(0.8)),
       (BASE_W / 2 - 4, BASE_D + 10), f"R{BASE_R}  (×4)", off0=U)
leader((GROOVE_W / 2, 40), (20, 46), f"groove ↓{GROOVE_H}", off0=U)
text(U[0], U[1] - 22, "FRONT", 8, c="#555")
title(U[0], 205, "BOTTOM VIEW", "dashed: plate back at base top")

# ---------------- 5. Detail C: groove cross-section (3:1) ----------------
C, k = np.array([555, 95]), 3.0
shape = [(-12, 0), (-GROOVE_W / 2, 0), (-GROOVE_W / 2, GROOVE_H), (GROOVE_W / 2, GROOVE_H),
         (GROOVE_W / 2, 0), (12, 0), (12, BASE_H), (-12, BASE_H)]
poly(np.array(shape) * k, C, fill=False, ec=INK, lw=1.3, hatch="////")
dim(np.array((-GROOVE_W / 2, 0)) * k, np.array((GROOVE_W / 2, 0)) * k, -7, f"{GROOVE_W:g}",
    off0=C, tside=-1)
dim(np.array((GROOVE_W / 2, 0)) * k, np.array((GROOVE_W / 2, GROOVE_H)) * k, 9, f"{GROOVE_H}",
    off0=C)
dim(np.array((12, 0)) * k, np.array((12, BASE_H)) * k, -7, f"{BASE_H}", off0=C, tside=-1)
title(C[0], 72, "DETAIL C  (3:1)", "cable groove, seen from the back")

# ---------------- Parameter table + notes ----------------
rows = [
    ("Puck (Amazon Basics Qi2.2, LACC175)", f"Ø{PUCK_D:g} × {PUCK_H}  — measure yours"),
    ("Pocket", f"Ø{POCKET_D:g} (fit +{FIT}) × {POCKET_DEPTH} deep, puck {PROUD} proud"),
    ("Plate", f"{PLATE_W} × {PLATE_L} × {PLATE_T}, tilt {ANGLE}°, top corners R{PLATE_R}"),
    ("Puck centre", f"{PUCK_C} along slope from base top"),
    ("Base", f"{BASE_W} × {BASE_D} × {BASE_H}, corners R{BASE_R}"),
    ("Push-out hole / cable slot", f"Ø{PUSH_D} thru / {SLOT_W} wide thru plate + base"),
    ("Groove under base", f"{GROOVE_W:g} × {GROOVE_H}, open, full depth to back edge"),
    ("Plate-to-base fillet", f"R{FILLET_R}"),
]
x0, y0 = 30, 165
text(x0, y0, "PARAMETERS (mm)", 11, ha="left", weight="bold")
for i, (k_, v) in enumerate(rows):
    y = y0 - 11 - i * 8.5
    text(x0, y, k_, 8.5, ha="left")
    text(x0 + 135, y, v, 8.5, ha="left")
    line((x0, y - 4.2), (x0 + 290, y - 4.2), lw=0.3, c="#bbb")
notes = ["NOTES",
         "1. Print flat on the base, no supports. PLA/PETG, 0.2 mm layers, 3 walls, 15–20 % infill.",
         "2. Cable leaving the puck edge: rotate puck so the cable drops into the slot.",
         "   Cable leaving the puck back: pass it through the Ø24 hole, then down the slot.",
         "3. Magnet pull can lift a loose puck: use fit 0.1–0.2 or tape on the pocket floor.",
         "4. Overall 92 × 100 × 124.5. Phone CoG ≈ 26 behind the front edge."]
for i, s in enumerate(notes):
    text(x0 + 300, y0 - i * 9, s, 8.5 if i else 11, ha="left", weight="bold" if i == 0 else None)

# Title block
ax.add_patch(plt.Rectangle((448, 6), 186, 20, fill=False, ec=INK, lw=1))
text(452, 19, "MagSafe / Qi2 Phone Stand", 11, ha="left", weight="bold")
text(452, 11, "Units mm · not to scale except Detail C ratio · ref. Printables 44465", 7.5,
     ha="left", c="#444")
ax.add_patch(plt.Rectangle((4, 4), 632, 444, fill=False, ec=INK, lw=1.2))

fig.savefig("drawing.pdf")
fig.savefig("drawing.png", dpi=130)
print("wrote drawing.pdf, drawing.png")
