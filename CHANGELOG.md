# Changelog

All notable changes to Tangent are documented here.

## [v0.1.0-alpha] — 2026-11-18

### Added
- Initial release: 25 uppercase letters (A–Z minus S), digits 0–9, and
  the punctuation set — 59 glyphs.
- The arc primitive: perfect-circle strokes only (annulus sectors with
  radial end cuts, sagitta-derived segmentation). No béziers, no
  ellipses — the compass, not the hand.
- Tangent arc-to-rail junctions (U, J, D bowls) — the signature gesture.
- Legibility regression harness from day one: pairwise ink-signature
  distinctness, bbox-vs-advance bounds, contour sanity, CI manifest gate.
- Static Regular only. S ships in v0.2 (the hero battle).
