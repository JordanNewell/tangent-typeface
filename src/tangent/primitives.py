"""Primitive expansion.

Tangent's primitives: vline, hline, diag (inherited from Newell) and
**arc** — the perfect-circle stroke (spec section 2). Each primitive
becomes a closed polygon of constant width STROKE_WIDTH. Polygons are
returned as a list of (x, y) tuples.

All coordinates are in font units. Stroke width is fixed at 110 in
v0.1 (static Regular only).

The arc expands to an annulus-sector polygon: outer radius r + half,
inner radius r - half, with radial cuts closing both ends (the
"squared terminal" for arcs — the cut edge is perpendicular to the
stroke direction at the endpoint). Chord segmentation derives from a
max-sagitta tolerance so large radii get more chords, small radii
fewer — never hand-picked.
"""

import math

STROKE_WIDTH = 110
_HALF = STROKE_WIDTH / 2.0

SAGITTA = 0.5  # max chord deviation from the true arc, font units


def expand_vline(spec, width=STROKE_WIDTH):
    """Rectangle centered horizontally on x, extending y0 -> y1."""
    half = width / 2.0
    x = spec["x"]
    y0 = spec["y0"]
    y1 = spec["y1"]
    lo, hi = (y0, y1) if y0 <= y1 else (y1, y0)
    left = x - half
    right = x + half
    return [
        (left, lo),
        (right, lo),
        (right, hi),
        (left, hi),
    ]


def expand_hline(spec, width=STROKE_WIDTH):
    """Rectangle centered vertically on y, extending x0 -> x1."""
    half = width / 2.0
    y = spec["y"]
    x0 = spec["x0"]
    x1 = spec["x1"]
    lo, hi = (x0, x1) if x0 <= x1 else (x1, x0)
    bottom = y - half
    top = y + half
    return [
        (lo, bottom),
        (hi, bottom),
        (hi, top),
        (lo, top),
    ]


def expand_diag(spec, width=STROKE_WIDTH):
    """45-degree parallelogram with horizontal terminal edges (Newell DNA)."""
    top_y = spec["top_y"]
    top_x0 = spec["top_x0"]
    top_x1 = spec["top_x1"]
    bot_y = spec["bot_y"]
    bot_x0 = spec["bot_x0"]
    bot_x1 = spec["bot_x1"]

    if top_y == bot_y:
        raise ValueError(f"diag degenerate: top_y == bot_y == {top_y}")

    top_len = top_x1 - top_x0
    bot_len = bot_x1 - bot_x0
    if top_len != bot_len:
        raise ValueError(
            f"diag terminals must be parallel and equal length; "
            f"top={top_len}, bot={bot_len}"
        )

    dy = abs(top_y - bot_y)
    left_dx = abs(top_x0 - bot_x0)
    right_dx = abs(top_x1 - bot_x1)
    if left_dx != dy:
        raise ValueError(
            f"diag left side must be 45 degrees; |dx|={left_dx}, |dy|={dy}"
        )
    if right_dx != dy:
        raise ValueError(
            f"diag right side must be 45 degrees; |dx|={right_dx}, |dy|={dy}"
        )

    return [
        (top_x0, top_y),
        (top_x1, top_y),
        (bot_x1, bot_y),
        (bot_x0, bot_y),
    ]


def _validate_arc(spec):
    """Assert arc invariants (spec section 2). Raises ValueError."""
    r = spec.get("r")
    a0 = spec.get("a0")
    a1 = spec.get("a1")
    for name, v in (("r", r), ("a0", a0), ("a1", a1)):
        if v is None or not math.isfinite(v):
            raise ValueError(f"arc {name} must be finite; got {v!r}")
    # r must EXCEED stroke/2: r == stroke/2 collapses the inner radius
    # to zero — a solid pie sector, not an arc stroke (spec amendment
    # path would be required to allow it).
    if r <= STROKE_WIDTH / 2:
        raise ValueError(
            f"arc r={r} must be > stroke/2 ({STROKE_WIDTH / 2}); "
            "smaller radii collapse the annulus — draw rails instead"
        )
    raw = a1 - a0
    if not (0 < raw <= 360):
        raise ValueError(
            f"arc span must be counterclockwise a0 -> a1 within (0, 360]; "
            f"got a0={a0}, a1={a1}"
        )


def expand_arc(spec, width=STROKE_WIDTH):
    """Annulus-sector polygon for a perfect-circle arc stroke.

    spec: {type: "arc", cx, cy, r, a0, a1} — angles in degrees,
    counterclockwise, a0 -> a1. Returns a single closed contour
    (list of (x, y) tuples): outer boundary a0->a1, radial cut at a1,
    inner boundary a1->a0, radial cut at a0.

    Chord count: n = ceil(span_rad / (2 * acos(1 - SAGITTA / r))), the
    largest n whose worst-case chord sagitta stays <= SAGITTA. Minimum 2.
    """
    _validate_arc(spec)
    cx = spec["cx"]
    cy = spec["cy"]
    r = spec["r"]
    a0 = spec["a0"]
    a1 = spec["a1"]

    span = a1 - a0
    span_rad = math.radians(span)
    # chord count from the sagitta bound: sagitta of a chord subtending
    # angle theta is r * (1 - cos(theta/2)). Require <= SAGITTA.
    n = math.ceil(span_rad / (2 * math.acos(1 - SAGITTA / r)))
    n = max(n, 2)

    outer = []
    inner = []
    for i in range(n + 1):
        ang = math.radians(a0 + span * i / n)
        cos_a = math.cos(ang)
        sin_a = math.sin(ang)
        outer.append((cx + (r + _HALF) * cos_a, cy + (r + _HALF) * sin_a))
        inner.append((cx + (r - _HALF) * cos_a, cy + (r - _HALF) * sin_a))

    # single closed contour: outer a0->a1, cut, inner a1->a0, cut
    poly = outer + inner[::-1]
    # snap integral floats to ints for clean deterministic UFO output
    return [
        (int(p[0]) if float(p[0]).is_integer() else p[0],
         int(p[1]) if float(p[1]).is_integer() else p[1])
        for p in poly
    ]


_PRIMITIVE_EXPANDERS = {
    "vline": expand_vline,
    "hline": expand_hline,
    "diag": expand_diag,
    "arc": expand_arc,
}


def expand_primitive(spec, width=STROKE_WIDTH):
    """Dispatch on spec['type'] to the matching expander.

    width = stroke thickness for rails/diags (arcs derive thickness from
    their own r and the stroke constant).
    """
    try:
        kind = spec["type"]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"primitive spec missing 'type': {spec!r}") from exc
    try:
        expander = _PRIMITIVE_EXPANDERS[kind]
    except KeyError:
        raise ValueError(f"unknown primitive type {kind!r}; spec={spec!r}")
    return expander(spec, width)
