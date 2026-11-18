"""Declarative glyph definitions for the Tangent alphabet.

v0.1 ships the uppercase A-Z + digits + punctuation (S is deliberately
deferred to v0.2 as the hero battle -- spec section 3).

Metrics: cap 700 (centerline convention), stroke 110, bearings 90.
The arc joins the vocabulary as the fourth primitive:
{"type": "arc", "cx", "cy", "r", "a0", "a1"} -- perfect circles only.
"""

CAP_HEIGHT = 700
BASELINE = 0
STROKE = 110
HALF = STROKE / 2
SIDE_BEARING = 90

def _glyph_bbox(primitives):
    """Ink bbox over expanded primitives (pre-union, exact for bbox)."""
    from tangent.primitives import expand_primitive
    pts = [q for pr in primitives for q in expand_primitive(pr)]
    xs = [q[0] for q in pts]
    ys = [q[1] for q in pts]
    return min(xs), min(ys), max(xs), max(ys)


def _advance_bbox(primitives):
    """advance = left bearing + ink width + right bearing (SPEC)."""
    x0, _y0, x1, _y1 = _glyph_bbox(primitives)
    return SIDE_BEARING + round(x1 - x0) + SIDE_BEARING


# ---------------------------------------------------------------------------
# Proof trio (spec section 3): the circular O spans the full cap throw --
# stroke-centerline radius 350 centered on the cap mid-height (350) puts
# the ink at -55..755, exactly the uppercase centerline convention.
# ---------------------------------------------------------------------------
_O_R = 350
_O_CX = SIDE_BEARING + _O_R + HALF   # 495: ink starts at the 90 bearing
_O_CY = CAP_HEIGHT / 2           # 350
_O = [
    {"type": "arc", "cx": _O_CX, "cy": _O_CY, "r": _O_R, "a0": 0, "a1": 360},
]
O = {
    "name": "O",
    "unicode": "U+004F",
    "advance": _advance_bbox(_O),
    "primitives": _O,
}

# C: O's arc with a right opening; terminals at +-45deg (radial cuts on
# the diagonal vocabulary -- the 45-degree rule reaches the round letters).
_C = [
    {"type": "arc", "cx": _O_CX, "cy": _O_CY, "r": _O_R, "a0": 45, "a1": 315},
]
C = {
    "name": "C",
    "unicode": "U+0043",
    "advance": _advance_bbox(_C),
    "primitives": _C,
}

# G: C's arc + mid bar entering the opening + squared spur down toward
# the lower terminal (junctions here are 45-degree-squared, per spec --
# tangency preferred but not forced).
_G = _C + [
    {"type": "hline", "y": CAP_HEIGHT / 2, "x0": _O_CX, "x1": _O_CX + _O_R + HALF - 15},
    {"type": "vline", "x": _O_CX + _O_R - 60, "y0": BASELINE + 45, "y1": CAP_HEIGHT / 2},
]
G = {
    "name": "G",
    "unicode": "U+0047",
    "advance": _advance_bbox(_G),
    "primitives": _G,
}

GLYPHS = [C, G, O]
