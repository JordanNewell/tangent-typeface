"""Declarative glyph definitions for the Tangent alphabet.

v0.1 ships the uppercase A-Z (minus S -- deliberately deferred to v0.2
as the hero battle, spec section 3), digits 0-9, and the Newell-style
punctuation set.

Metrics: cap 700 (centerline convention -- rails centered on metric
lines, ink overshoots by half-stroke), stroke 110, bearings 90.

The arc is the fourth primitive: {"type": "arc", "cx", "cy", "r",
"a0", "a1"} -- perfect circles only (spec). Angles in degrees CCW;
spans may cross 0/360 via raw values (e.g. a0=270, a1=450).

The signature gesture is the TANGENT junction: arc-to-rail meetings
are tangent (rail along the arc's tangent) wherever the geometry
allows -- U's bowl, J's hook, D's bowl shoulder.
"""

from math import cos, radians, sin

CAP_HEIGHT = 700
BASELINE = 0
STROKE = 110
HALF = STROKE / 2
SIDE_BEARING = 90
MID = CAP_HEIGHT / 2  # 350

_COL_L = SIDE_BEARING + HALF   # 145
_COL_R = 475
_LEFT_EDGE = 90
_RIGHT_EDGE = 530


def _glyph_bbox(primitives):
    """Ink bbox over expanded primitives (pre-union, exact for bbox)."""
    from tangent.primitives import expand_primitive
    pts = [q for pr in primitives for q in expand_primitive(pr)]
    xs = [q[0] for q in pts]
    ys = [q[1] for q in pts]
    return min(xs), min(ys), max(xs), max(ys)


def _advance_bbox(primitives):
    """advance = ink_left + ink_width + right bearing (SPEC formula).

    ink_left is kept as-is (not forced to 90): asymmetric glyphs like
    nine's tail keep a right bearing of 90 and a smaller left bearing,
    which is the same trade-off Newell's marks made.
    """
    x0, _y0, x1, _y1 = _glyph_bbox(primitives)
    return round(x0) + round(x1 - x0) + SIDE_BEARING


def _arc_pt(cx, cy, r, deg):
    a = radians(deg)
    return (cx + r * cos(a), cy + r * sin(a))


# ---------------------------------------------------------------------------
# Proof trio (already gated)
# ---------------------------------------------------------------------------
_O_R = 350
_O_CX = SIDE_BEARING + _O_R + HALF   # 495
_O_CY = MID

O = {
    "name": "O",
    "unicode": "U+004F",
    "advance": _advance_bbox([
        {"type": "arc", "cx": _O_CX, "cy": _O_CY, "r": _O_R, "a0": 0, "a1": 360},
    ]),
    "primitives": [
        {"type": "arc", "cx": _O_CX, "cy": _O_CY, "r": _O_R, "a0": 0, "a1": 360},
    ],
}

_C_ARC = [
    {"type": "arc", "cx": _O_CX, "cy": _O_CY, "r": _O_R, "a0": 45, "a1": 315},
]
C = {
    "name": "C",
    "unicode": "U+0043",
    "advance": _advance_bbox(_C_ARC),
    "primitives": _C_ARC,
}

_G = _C_ARC + [
    {"type": "hline", "y": MID, "x0": _O_CX, "x1": _O_CX + _O_R + HALF - 15},
    {"type": "vline", "x": _O_CX + _O_R - 60, "y0": BASELINE + 45, "y1": MID},
]
G = {
    "name": "G",
    "unicode": "U+0047",
    "advance": _advance_bbox(_G),
    "primitives": _G,
}

# ---------------------------------------------------------------------------
# Rails-only caps (Newell geometry, same grid)
# ---------------------------------------------------------------------------
E = {
    "name": "E",
    "unicode": "U+0045",
    "advance": 620,
    "primitives": [
        {"type": "vline", "x": _COL_L, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": CAP_HEIGHT, "x0": _COL_L, "x1": _COL_R},
        {"type": "hline", "y": MID, "x0": _COL_L, "x1": _COL_R},
        {"type": "hline", "y": BASELINE, "x0": _COL_L, "x1": _COL_R},
    ],
}

F = {
    "name": "F",
    "unicode": "U+0046",
    "advance": 620,
    "primitives": [
        {"type": "vline", "x": _COL_L, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": CAP_HEIGHT, "x0": _COL_L, "x1": _COL_R},
        {"type": "hline", "y": MID, "x0": _COL_L, "x1": _COL_R},
    ],
}

H = {
    "name": "H",
    "unicode": "U+0048",
    "advance": 620,
    "primitives": [
        {"type": "vline", "x": _COL_L, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "vline", "x": _COL_R, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": MID, "x0": _COL_L, "x1": _COL_R},
    ],
}

I = {
    "name": "I",
    "unicode": "U+0049",
    "advance": 290,
    "primitives": [
        {"type": "vline", "x": _COL_L, "y0": BASELINE, "y1": CAP_HEIGHT},
    ],
}

L = {
    "name": "L",
    "unicode": "U+004C",
    "advance": 560,
    "primitives": [
        {"type": "vline", "x": _COL_L, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": BASELINE, "x0": _COL_L, "x1": 470},
    ],
}

T = {
    "name": "T",
    "unicode": "U+0054",
    "advance": 620,
    "primitives": [
        {"type": "hline", "y": CAP_HEIGHT, "x0": _COL_L, "x1": _COL_R},
        {"type": "vline", "x": 310, "y0": BASELINE, "y1": CAP_HEIGHT},
    ],
}

# ---------------------------------------------------------------------------
# Diagonal caps (Newell geometry: 45-degree throws span wide)
# ---------------------------------------------------------------------------
_A_LEG_DX = CAP_HEIGHT
_A_APEX_X = _LEFT_EDGE + _A_LEG_DX + HALF  # 845
A = {
    "name": "A",
    "unicode": "U+0041",
    "advance": _advance_bbox([
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": _A_APEX_X - HALF - 1,
         "top_x1": _A_APEX_X + HALF + 1, "bot_y": BASELINE,
         "bot_x0": _A_APEX_X - _A_LEG_DX - HALF - 1, "bot_x1": _A_APEX_X - _A_LEG_DX + HALF + 1},
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": _A_APEX_X - HALF - 1,
         "top_x1": _A_APEX_X + HALF + 1, "bot_y": BASELINE,
         "bot_x0": _A_APEX_X + _A_LEG_DX - HALF - 1, "bot_x1": _A_APEX_X + _A_LEG_DX + HALF + 1},
        {"type": "hline", "y": 200, "x0": _A_APEX_X - 500, "x1": _A_APEX_X + 500},
    ]),
    "primitives": [
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": _A_APEX_X - HALF - 1,
         "top_x1": _A_APEX_X + HALF + 1, "bot_y": BASELINE,
         "bot_x0": _A_APEX_X - _A_LEG_DX - HALF - 1, "bot_x1": _A_APEX_X - _A_LEG_DX + HALF + 1},
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": _A_APEX_X - HALF - 1,
         "top_x1": _A_APEX_X + HALF + 1, "bot_y": BASELINE,
         "bot_x0": _A_APEX_X + _A_LEG_DX - HALF - 1, "bot_x1": _A_APEX_X + _A_LEG_DX + HALF + 1},
        {"type": "hline", "y": 200, "x0": _A_APEX_X - 500, "x1": _A_APEX_X + 500},
    ],
}

V = {
    "name": "V",
    "unicode": "U+0056",
    "advance": 1690,
    "primitives": [
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": _LEFT_EDGE, "top_x1": 200,
         "bot_y": BASELINE, "bot_x0": 790, "bot_x1": 900},
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": 1490, "top_x1": 1600,
         "bot_y": BASELINE, "bot_x0": 790, "bot_x1": 900},
    ],
}

K = {
    "name": "K",
    "unicode": "U+004B",
    "advance": 740,
    "primitives": [
        {"type": "vline", "x": _COL_L, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": 439, "top_x1": 551,
         "bot_y": MID, "bot_x0": 89, "bot_x1": 201},
        {"type": "diag", "top_y": MID, "top_x0": 89, "top_x1": 201,
         "bot_y": BASELINE, "bot_x0": 439, "bot_x1": 551},
    ],
}

X = {
    "name": "X",
    "unicode": "U+0058",
    "advance": 990,
    "primitives": [
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": 90, "top_x1": 200,
         "bot_y": BASELINE, "bot_x0": 790, "bot_x1": 900},
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": 790, "top_x1": 900,
         "bot_y": BASELINE, "bot_x0": 90, "bot_x1": 200},
    ],
}

Y = {
    "name": "Y",
    "unicode": "U+0059",
    "advance": 990,
    "primitives": [
        {"type": "vline", "x": 495, "y0": BASELINE, "y1": MID},
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": 90, "top_x1": 200,
         "bot_y": MID, "bot_x0": 440, "bot_x1": 550},
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": 790, "top_x1": 900,
         "bot_y": MID, "bot_x0": 440, "bot_x1": 550},
    ],
}

M = {
    "name": "M",
    "unicode": "U+004D",
    "advance": 1000,
    "primitives": [
        {"type": "vline", "x": _COL_L, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "vline", "x": 855, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": 90, "top_x1": 200,
         "bot_y": 350, "bot_x0": 440, "bot_x1": 550},
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": 790, "top_x1": 900,
         "bot_y": 350, "bot_x0": 440, "bot_x1": 550},
    ],
}

N = {
    "name": "N",
    "unicode": "U+004E",
    "advance": 990,
    "primitives": [
        {"type": "vline", "x": _COL_L, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "vline", "x": 845, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": 90, "top_x1": 200,
         "bot_y": BASELINE, "bot_x0": 790, "bot_x1": 900},
    ],
}

Z = {
    "name": "Z",
    "unicode": "U+005A",
    "advance": 990,
    "primitives": [
        {"type": "hline", "y": CAP_HEIGHT, "x0": _LEFT_EDGE, "x1": 900},
        {"type": "hline", "y": BASELINE, "x0": _LEFT_EDGE, "x1": 900},
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": 790, "top_x1": 900,
         "bot_y": BASELINE, "bot_x0": 90, "bot_x1": 200},
    ],
}

# W: the Newell W construction ported verbatim (45-degree outer legs
# dy=700, inner peak at mid-height) -- the tangent vocabulary does not
# touch the all-diagonal letters.
_W_APEX1_X = 846
_W_APEX2_X = 1546
_W_CENTER_TOP_X = 1196
W = {
    "name": "W",
    "unicode": "U+0057",
    "advance": 2392,
    "primitives": [
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": 90, "top_x1": 200,
         "bot_y": BASELINE, "bot_x0": 790, "bot_x1": 900},
        {"type": "diag", "top_y": 350, "top_x0": 1140, "top_x1": 1250,
         "bot_y": BASELINE, "bot_x0": 790, "bot_x1": 900},
        {"type": "diag", "top_y": 350, "top_x0": 1140, "top_x1": 1250,
         "bot_y": BASELINE, "bot_x0": 1490, "bot_x1": 1600},
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": 2190, "top_x1": 2300,
         "bot_y": BASELINE, "bot_x0": 1490, "bot_x1": 1600},
    ],
}

# ---------------------------------------------------------------------------
# Arc-bowl caps (tangent junctions)
# ---------------------------------------------------------------------------
_D_ARC = [{"type": "arc", "cx": _COL_L, "cy": MID, "r": _O_R, "a0": 270, "a1": 450},
          {"type": "vline", "x": _COL_L, "y0": BASELINE, "y1": CAP_HEIGHT}]
D = {
    "name": "D",
    "unicode": "U+0044",
    "advance": _advance_bbox(_D_ARC),
    "primitives": _D_ARC,
}

# P: stem + upper bowl (right semicircle, r=175, cy=525: top 700, bottom 350)
_P_BOWL = [{"type": "vline", "x": _COL_L, "y0": BASELINE, "y1": CAP_HEIGHT},
           {"type": "arc", "cx": _COL_L, "cy": 525, "r": 175, "a0": 270, "a1": 450}]
P = {
    "name": "P",
    "unicode": "U+0050",
    "advance": _advance_bbox(_P_BOWL),
    "primitives": _P_BOWL,
}

# R: P + 45-degree leg from bowl bottom to baseline
_R = _P_BOWL + [
    {"type": "diag", "top_y": 350, "top_x0": 195, "top_x1": 305,
     "bot_y": BASELINE, "bot_x0": 545, "bot_x1": 655},
]
R = {
    "name": "R",
    "unicode": "U+0052",
    "advance": _advance_bbox(_R),
    "primitives": _R,
}

# B: stem + two stacked right-semicircle bowls (r=175, tangent at waist)
_B = [{"type": "vline", "x": _COL_L, "y0": BASELINE, "y1": CAP_HEIGHT},
      {"type": "arc", "cx": _COL_L, "cy": 525, "r": 175, "a0": 270, "a1": 450},
      {"type": "arc", "cx": _COL_L, "cy": 175, "r": 175, "a0": 270, "a1": 450}]
B = {
    "name": "B",
    "unicode": "U+0042",
    "advance": _advance_bbox(_B),
    "primitives": _B,
}

# U: two arms descending into a tangent bottom bowl (the signature gesture)
_U_ARC_R = 165
_U_ARC_CY = BASELINE + _U_ARC_R  # 165
_U = [
    {"type": "vline", "x": _COL_L, "y0": _U_ARC_CY, "y1": CAP_HEIGHT},
    {"type": "vline", "x": _COL_R, "y0": _U_ARC_CY, "y1": CAP_HEIGHT},
    {"type": "arc", "cx": 310, "cy": _U_ARC_CY, "r": _U_ARC_R, "a0": 180, "a1": 360},
]
U = {
    "name": "U",
    "unicode": "U+0055",
    "advance": _advance_bbox(_U),
    "primitives": _U,
}

# J: right stem + tangent bottom-left hook + top extension to cap
_J_ARC_R = 165
_J_ARC_CY = BASELINE + _J_ARC_R  # 165
_J_ARC_CX = _COL_R - _J_ARC_R    # 310
J = {
    "name": "J",
    "unicode": "U+004A",
    "advance": 620,
    "primitives": [
        {"type": "vline", "x": _COL_R, "y0": _J_ARC_CY, "y1": CAP_HEIGHT},
        {"type": "arc", "cx": _J_ARC_CX, "cy": _J_ARC_CY, "r": _J_ARC_R, "a0": 180, "a1": 360},
    ],
}

# Q: the circular O + 45-degree tail breaking the ring at bottom-right
_Q_TAIL = [
    {"type": "diag", "top_y": 200, "top_x0": 595, "top_x1": 705,
     "bot_y": -100, "bot_x0": 895, "bot_x1": 1005},
]
Q = {
    "name": "Q",
    "unicode": "U+0051",
    "advance": _advance_bbox(O["primitives"] + _Q_TAIL),
    "primitives": O["primitives"] + _Q_TAIL,
}

# ---------------------------------------------------------------------------
# Digits (0 = the circle, documented; arcs for 3 6 8 9; rails elsewhere)
# ---------------------------------------------------------------------------
D0 = dict(O, name="zero", unicode="U+0030")

D1 = {
    "name": "one",
    "unicode": "U+0031",
    "advance": 620,
    "primitives": [
        {"type": "vline", "x": 310, "y0": BASELINE, "y1": CAP_HEIGHT},
        {"type": "hline", "y": BASELINE, "x0": 155, "x1": 465},
    ],
}

D2 = {
    "name": "two",
    "unicode": "U+0032",
    "advance": _advance_bbox([
        {"type": "arc", "cx": 310, "cy": 525, "r": 175, "a0": 0, "a1": 225},
        {"type": "diag", "top_y": 350, "top_x0": 184, "top_x1": 294,
         "bot_y": BASELINE, "bot_x0": 534, "bot_x1": 644},
        {"type": "hline", "y": BASELINE, "x0": _LEFT_EDGE, "x1": 654},
    ]),
    "primitives": [
        # top bowl opening right-down: arc from 0deg CCW to 225deg
        {"type": "arc", "cx": 310, "cy": 525, "r": 175, "a0": 0, "a1": 225},
        # diagonal from the arc's 225deg end down-right to baseline (45deg)
        {"type": "diag", "top_y": 350, "top_x0": 184, "top_x1": 294,
         "bot_y": BASELINE, "bot_x0": 534, "bot_x1": 644},
        {"type": "hline", "y": BASELINE, "x0": _LEFT_EDGE, "x1": 654},
    ],
}

# 3: two stacked right-opening bowls (both open left)
_D3_PRIMS = [
    {"type": "arc", "cx": 90, "cy": 525, "r": 175, "a0": 270, "a1": 450},
    {"type": "arc", "cx": 90, "cy": 175, "r": 175, "a0": 270, "a1": 450},
]
D3 = {
    "name": "three",
    "unicode": "U+0033",
    "advance": _advance_bbox(_D3_PRIMS),
    "primitives": _D3_PRIMS,
}

D4 = {
    "name": "four",
    "unicode": "U+0034",
    "advance": _advance_bbox([
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": 90, "top_x1": 200,
         "bot_y": 250, "bot_x0": 540, "bot_x1": 650},
        {"type": "hline", "y": 250, "x0": _LEFT_EDGE, "x1": 650},
        {"type": "vline", "x": 475, "y0": BASELINE, "y1": 550},
    ]),
    "primitives": [
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": 90, "top_x1": 200,
         "bot_y": 250, "bot_x0": 540, "bot_x1": 650},
        {"type": "hline", "y": 250, "x0": _LEFT_EDGE, "x1": 650},
        {"type": "vline", "x": 475, "y0": BASELINE, "y1": 550},
    ],
}

D5 = {
    "name": "five",
    "unicode": "U+0035",
    "advance": 620,
    "primitives": [
        {"type": "hline", "y": CAP_HEIGHT, "x0": _COL_R, "x1": 195},
        {"type": "vline", "x": _COL_L, "y0": 350, "y1": CAP_HEIGHT},
        {"type": "hline", "y": 350, "x0": _COL_L, "x1": 400},
        {"type": "arc", "cx": 245, "cy": 175, "r": 175, "a0": 270, "a1": 450},
    ],
}

# 6: circle + tangent tail arc rising to cap (both CCW arcs, tangent at join)
D6 = {
    "name": "six",
    "unicode": "U+0036",
    "advance": _advance_bbox([
        {"type": "arc", "cx": 310, "cy": 175, "r": 175, "a0": 0, "a1": 360},
        {"type": "arc", "cx": 485, "cy": 350, "r": 175, "a0": 90, "a1": 225},
    ]),
    "primitives": [
        {"type": "arc", "cx": 310, "cy": 175, "r": 175, "a0": 0, "a1": 360},
        {"type": "arc", "cx": 485, "cy": 350, "r": 175, "a0": 90, "a1": 225},
    ],
}

D7 = {
    "name": "seven",
    "unicode": "U+0037",
    "advance": 990,
    "primitives": [
        {"type": "hline", "y": CAP_HEIGHT, "x0": _LEFT_EDGE, "x1": 900},
        {"type": "diag", "top_y": CAP_HEIGHT, "top_x0": 790, "top_x1": 900,
         "bot_y": BASELINE, "bot_x0": 90, "bot_x1": 200},
    ],
}

# 8: two stacked circles tangent at the waist
D8 = {
    "name": "eight",
    "unicode": "U+0038",
    "advance": _advance_bbox([
        {"type": "arc", "cx": 350, "cy": 525, "r": 175, "a0": 0, "a1": 360},
        {"type": "arc", "cx": 350, "cy": 175, "r": 175, "a0": 0, "a1": 360},
    ]),
    "primitives": [
        {"type": "arc", "cx": 350, "cy": 525, "r": 175, "a0": 0, "a1": 360},
        {"type": "arc", "cx": 350, "cy": 175, "r": 175, "a0": 0, "a1": 360},
    ],
}

# 9: mirrored 6
_D9_PRIMS = [
    {"type": "arc", "cx": 380, "cy": 525, "r": 175, "a0": 0, "a1": 360},
    {"type": "arc", "cx": 205, "cy": 350, "r": 175, "a0": 315, "a1": 450},
]
D9 = {
    "name": "nine",
    "unicode": "U+0039",
    "advance": _advance_bbox(_D9_PRIMS),
    "primitives": _D9_PRIMS,
}


def _port(name, uni, advance, primitives):
    return {"name": name, "unicode": uni, "advance": advance, "primitives": primitives}


PERIOD = _port("period", "U+002E", 290, [{"type": "vline", "x": 145, "y0": 0, "y1": 55},
                                         {"type": "hline", "y": 0, "x0": 90, "x1": 200},
                                         {"type": "vline", "x": 145, "y0": -55, "y1": 55}])
COMMA = _port("comma", "U+002C", 400, [
    {"type": "vline", "x": 256, "y0": -56, "y1": 311},
    {"type": "hline", "y": 256, "x0": 201, "x1": 311},
    {"type": "diag", "top_y": 0, "top_x0": 200, "top_x1": 312,
     "bot_y": -110, "bot_x0": 90, "bot_x1": 202},
])
EXCLAM = _port("exclam", "U+0021", 290, [
    {"type": "vline", "x": 145, "y0": 250, "y1": 755},
    {"type": "vline", "x": 145, "y0": 0, "y1": 55},
    {"type": "hline", "y": 0, "x0": 90, "x1": 200},
    {"type": "vline", "x": 145, "y0": -55, "y1": 55},
])
QUESTION = _port("question", "U+003F", _advance_bbox([
    {"type": "arc", "cx": 310, "cy": 525, "r": 175, "a0": 0, "a1": 270},
    {"type": "vline", "x": 310, "y0": 250, "y1": 350},
    {"type": "vline", "x": 310, "y0": 0, "y1": 55},
    {"type": "hline", "y": 0, "x0": 255, "x1": 365},
    {"type": "vline", "x": 310, "y0": -55, "y1": 55},
]), [
    {"type": "arc", "cx": 310, "cy": 525, "r": 175, "a0": 0, "a1": 270},
    {"type": "vline", "x": 310, "y0": 250, "y1": 350},
    {"type": "vline", "x": 310, "y0": 0, "y1": 55},
    {"type": "hline", "y": 0, "x0": 255, "x1": 365},
    {"type": "vline", "x": 310, "y0": -55, "y1": 55},
    ])
QUOTESINGLE = _port("quotesingle", "U+2019", 290, [
    {"type": "vline", "x": 145, "y0": 590, "y1": 700},
    {"type": "hline", "y": 645, "x0": 90, "x1": 200},
    {"type": "vline", "x": 145, "y0": 590, "y1": 700},
])
QUOTELEFT = _port("quoteleft", "U+2018", 290, list(QUOTESINGLE["primitives"]))
QUOTEDBLLEFT = _port("quotedblleft", "U+201C", 460, [
    {"type": "vline", "x": 145, "y0": 590, "y1": 700},
    {"type": "hline", "y": 645, "x0": 90, "x1": 200},
    {"type": "vline", "x": 145, "y0": 590, "y1": 700},
    {"type": "vline", "x": 315, "y0": 590, "y1": 700},
    {"type": "hline", "y": 645, "x0": 260, "x1": 370},
    {"type": "vline", "x": 315, "y0": 590, "y1": 700},
])
QUOTEDBLRIGHT = _port("quotedblright", "U+201D", 460, list(QUOTEDBLLEFT["primitives"]))
COLON = _port("colon", "U+003A", 290, [
    {"type": "vline", "x": 145, "y0": 295, "y1": 405},
    {"type": "hline", "y": 350, "x0": 90, "x1": 200},
    {"type": "vline", "x": 145, "y0": 295, "y1": 405},
    {"type": "vline", "x": 145, "y0": -55, "y1": 55},
    {"type": "hline", "y": 0, "x0": 90, "x1": 200},
    {"type": "vline", "x": 145, "y0": -55, "y1": 55},
])
SEMICOLON = _port("semicolon", "U+003B", 400, [
    {"type": "vline", "x": 256, "y0": 295, "y1": 405},
    {"type": "hline", "y": 350, "x0": 201, "x1": 311},
    {"type": "vline", "x": 256, "y0": 295, "y1": 405},
    {"type": "vline", "x": 256, "y0": -56, "y1": 311},
    {"type": "hline", "y": 256, "x0": 201, "x1": 311},
    {"type": "diag", "top_y": 0, "top_x0": 200, "top_x1": 312,
     "bot_y": -110, "bot_x0": 90, "bot_x1": 202},
])
HYPHEN = _port("hyphen", "U+002D", 540, [
    {"type": "hline", "y": 350, "x0": 90, "x1": 410},
])
EMDASH = _port("emdash", "U+2014", 1010, [
    {"type": "hline", "y": 350, "x0": 90, "x1": 810},
])
ENDASH = _port("endash", "U+2013", 540, [
    {"type": "hline", "y": 350, "x0": 90, "x1": 450},
])
LPAREN = _port("parenleft", "U+0028", 585, [
    # left half-circle, ink 90..495, y -55..755 (full cap + overshoot)
    {"type": "arc", "cx": 495, "cy": 350, "r": 350, "a0": 90, "a1": 270},
])
RPAREN = _port("parenright", "U+0029", 585, [
    # right half-circle, mirror of LPAREN
    {"type": "arc", "cx": 90, "cy": 350, "r": 350, "a0": 270, "a1": 450},
])
SLASH = _port("slash", "U+002F", 992, [
    {"type": "diag", "top_y": 700, "top_x0": 789, "top_x1": 901,
     "bot_y": 0, "bot_x0": 89, "bot_x1": 201},
])
AT = _port("at", "U+0040", _advance_bbox(O["primitives"] + [
    {"type": "hline", "y": 350, "x0": 310, "x1": 690},
    {"type": "vline", "x": 690, "y0": 350, "y1": 560},
    ]), O["primitives"] + [
    {"type": "hline", "y": 350, "x0": 310, "x1": 690},
    {"type": "vline", "x": 690, "y0": 350, "y1": 560},
    ])
NUMBERSIGN = _port("numbersign", "U+0023", 620, [
    {"type": "vline", "x": 145, "y0": 0, "y1": 700},
    {"type": "vline", "x": 475, "y0": 0, "y1": 700},
    {"type": "hline", "y": 525, "x0": 145, "x1": 475},
    {"type": "hline", "y": 175, "x0": 145, "x1": 475},
])
DOLLAR = _port("dollar", "U+0024", 700, [
    {"type": "arc", "cx": 350, "cy": 350, "r": 250, "a0": 45, "a1": 315},
    {"type": "vline", "x": 350, "y0": -55, "y1": 755},
])
PERCENT = _port("percent", "U+0025", _advance_bbox([
    {"type": "arc", "cx": 240, "cy": 560, "r": 140, "a0": 0, "a1": 360},
    {"type": "arc", "cx": 700, "cy": 140, "r": 140, "a0": 0, "a1": 360},
    {"type": "diag", "top_y": 650, "top_x0": 610, "top_x1": 720,
     "bot_y": 150, "bot_x0": 110, "bot_x1": 220},
    ]), [
    {"type": "arc", "cx": 240, "cy": 560, "r": 140, "a0": 0, "a1": 360},
    {"type": "arc", "cx": 700, "cy": 140, "r": 140, "a0": 0, "a1": 360},
    {"type": "diag", "top_y": 650, "top_x0": 610, "top_x1": 720,
     "bot_y": 150, "bot_x0": 110, "bot_x1": 220},
    ])
AMPERSAND = _port("ampersand", "U+0026", _advance_bbox([
    {"type": "arc", "cx": 330, "cy": 525, "r": 175, "a0": 0, "a1": 270},
    {"type": "diag", "top_y": 350, "top_x0": 200, "top_x1": 310,
     "bot_y": 0, "bot_x0": 550, "bot_x1": 660},
    {"type": "arc", "cx": 500, "cy": 175, "r": 175, "a0": 90, "a1": 405},
    ]), [
    {"type": "arc", "cx": 330, "cy": 525, "r": 175, "a0": 0, "a1": 270},
    {"type": "diag", "top_y": 350, "top_x0": 200, "top_x1": 310,
     "bot_y": 0, "bot_x0": 550, "bot_x1": 660},
    {"type": "arc", "cx": 500, "cy": 175, "r": 175, "a0": 90, "a1": 405},
    ])
PLUS = _port("plus", "U+002B", 620, [
    {"type": "hline", "y": 350, "x0": 90, "x1": 530},
    {"type": "vline", "x": 310, "y0": 130, "y1": 570},
])
EQUAL = _port("equal", "U+003D", 620, [
    {"type": "hline", "y": 460, "x0": 90, "x1": 530},
    {"type": "hline", "y": 240, "x0": 90, "x1": 530},
])
LESS = _port("less", "U+003C", 640, [
    {"type": "diag", "top_y": 700, "top_x0": 439, "top_x1": 551,
     "bot_y": 350, "bot_x0": 89, "bot_x1": 201},
    {"type": "diag", "top_y": 350, "top_x0": 89, "top_x1": 201,
     "bot_y": BASELINE, "bot_x0": 439, "bot_x1": 551},
])
GREATER = _port("greater", "U+003E", 640, [
    {"type": "diag", "top_y": 700, "top_x0": 89, "top_x1": 201,
     "bot_y": 350, "bot_x0": 439, "bot_x1": 551},
    {"type": "diag", "top_y": 350, "top_x0": 439, "top_x1": 551,
     "bot_y": BASELINE, "bot_x0": 89, "bot_x1": 201},
])

GLYPHS = [
    A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, T, U, V, W, X, Y, Z,
    D0, D1, D2, D3, D4, D5, D6, D7, D8, D9,
    PERIOD, COMMA, EXCLAM, QUESTION, QUOTESINGLE, QUOTEDBLLEFT, QUOTEDBLRIGHT,
    COLON, SEMICOLON, HYPHEN, EMDASH, ENDASH, LPAREN, RPAREN, SLASH, AT,
    NUMBERSIGN, DOLLAR, PERCENT, AMPERSAND, PLUS, EQUAL, LESS, GREATER,
]
