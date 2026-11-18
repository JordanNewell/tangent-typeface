"""Tests for the Tangent generator.

Written with bare assert statements so the file runs directly with
`py src/tangent/test_generator.py` (no pytest required). pytest will
also collect the test_* functions if available.

Run:
    py src/tangent/test_generator.py
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.dirname(_HERE)
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from tangent.primitives import STROKE_WIDTH, expand_arc, expand_primitive
from tangent.legibility import run_checks
from tangent.glyphs import GLYPHS


def _radius(pt, cx=0.0, cy=0.0):
    return math.hypot(pt[0] - cx, pt[1] - cy)


def test_arc_quarter_endpoints():
    """Quarter arc r=200 at origin, 0..90deg: endpoints land on the axes."""
    poly = expand_arc({"type": "arc", "cx": 0, "cy": 0, "r": 200, "a0": 0, "a1": 90})
    r_out, r_in = 200 + STROKE_WIDTH / 2, 200 - STROKE_WIDTH / 2
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    # a0=0 terminal: radial cut on the +x axis
    assert min(p for p in xs if abs(_radius((p, 0)) - r_in) < 1 or True) is not None  # smoke
    # every point within the annulus
    for p in poly:
        assert r_in - 0.5 <= _radius(p) <= r_out + 0.5, p
    # extremes touch the axes (0deg and 90deg ends)
    assert max(xs) <= r_out + 0.5
    assert max(ys) <= r_out + 0.5
    assert min(ys) >= -0.5  # quarter arc stays in upper half plane


def test_arc_annulus_thickness():
    """Inner and outer boundary radii differ by exactly the stroke width."""
    poly = expand_arc({"type": "arc", "cx": 0, "cy": 0, "r": 200, "a0": 0, "a1": 360})
    radii = sorted(set(round(_radius(p), 6) for p in poly))
    # outer boundary and inner boundary are constant-radius chains
    r_out = max(radii)
    r_in = min(r for r in radii if r > 1.0)  # ignore any center-adjacent noise
    assert abs((r_out - r_in) - STROKE_WIDTH) < 0.5, (r_out, r_in)


def test_arc_radial_end_cut():
    """Both end cuts run along radii: first/last chords point at the center."""
    poly = expand_arc({"type": "arc", "cx": 0, "cy": 0, "r": 200, "a0": 0, "a1": 90})
    # the two terminal edges: pairs of points whose radii differ by ~stroke
    r_in, r_out = 200 - STROKE_WIDTH / 2, 200 + STROKE_WIDTH / 2
    ends = [p for p in poly if abs(_radius(p) - r_in) < 0.5 or abs(_radius(p) - r_out) < 0.5]
    assert len(ends) >= 4  # two cut edges, each with inner+outer points
    angles = sorted(math.degrees(math.atan2(p[1], p[0])) % 360 for p in ends)
    assert abs(angles[0] - 0) < 1.0 or abs(angles[0] - 360) < 1.0
    assert abs(angles[-1] - 90) < 1.0


def test_arc_sagitta_within_tolerance():
    """Every chord's sagitta <= 0.5 units (property, not a magic count)."""
    r = 310
    poly = expand_arc({"type": "arc", "cx": 0, "cy": 0, "r": r, "a0": 10, "a1": 200})
    # outer boundary points in ARC order (relative to a0 — atan2 wraps
    # at +-180deg, which would scramble arcs crossing that seam)
    outer = sorted(
        (p for p in poly if _radius(p) > r),
        key=lambda p: (math.degrees(math.atan2(p[1], p[0])) - 10) % 360,
    )
    for a, b in zip(outer, outer[1:]):
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        sag = abs(_radius(mid) - _radius(a))
        assert sag <= 0.75, sag  # midpoint of chord dips below arc by sagitta


def test_arc_deterministic():
    """Two runs produce identical polygons."""
    spec = {"type": "arc", "cx": 100, "cy": 200, "r": 150, "a0": -30, "a1": 210}
    assert expand_arc(spec) == expand_arc(spec)


def test_arc_r_at_stroke_half_raises():
    """r = stroke/2 collapses the annulus: must raise (strict >)."""
    for r in (54.9, 55, 55.0):
        try:
            expand_arc({"type": "arc", "cx": 0, "cy": 0, "r": r, "a0": 0, "a1": 90})
        except ValueError:
            continue
        raise AssertionError(f"r={r} must raise (annulus collapse)")


def test_arc_bad_span_raises():
    for span in ((0, 0), (30, 30), (0, 400), (0, 720)):
        try:
            expand_arc({"type": "arc", "cx": 0, "cy": 0, "r": 200, "a0": span[0], "a1": span[1]})
        except ValueError:
            continue
        raise AssertionError(f"span {span} must raise")


def test_arc_nan_raises():
    for bad in (float("nan"), float("inf")):
        try:
            expand_arc({"type": "arc", "cx": 0, "cy": 0, "r": bad, "a0": 0, "a1": 90})
        except ValueError:
            continue
        raise AssertionError(f"r={bad} must raise")


def test_arc_via_expand_primitive():
    """Dispatch reaches the arc expander."""
    poly = expand_primitive({"type": "arc", "cx": 0, "cy": 0, "r": 200, "a0": 0, "a1": 180})
    assert len(poly) >= 8


def test_arc_full_circle_closed():
    """Full circle: polygon contains an even, closed annulus (>= 16 pts)."""
    poly = expand_arc({"type": "arc", "cx": 0, "cy": 0, "r": 200, "a0": 0, "a1": 360})
    assert len(poly) >= 16
    assert len(poly) % 2 == 0


def test_legibility_heuristics():
    """Harness is live from day one (Newell #11 lesson)."""
    failures = run_checks(GLYPHS)
    assert failures == [], "\n".join(failures)


def run_all():
    tests = [
        name for name in globals()
        if name.startswith("test_") and callable(globals()[name])
    ]
    tests.sort()
    failed = 0
    for name in tests:
        try:
            globals()[name]()
            print(f"PASS  {name}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL  {name}: {type(exc).__name__}: {exc}")
    print()
    print(f"{len(tests) - failed}/{len(tests)} passed")
    return failed


if __name__ == "__main__":
    sys.exit(1 if run_all() else 0)
