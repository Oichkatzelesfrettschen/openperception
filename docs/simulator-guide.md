# CVD Simulator (SVG) Guide

Use the included SVG color-matrix filters to preview content under simulated color vision deficiencies.

Files:
- `examples/simulator/index.html` — toggles between none, protanopia, deuteranopia, tritanopia, and achromatopsia

Notes:
- The page applies `filter: url(#<filterId>)` to a container. Browser support for SVG filters on HTML elements is generally good in Chromium/Firefox.
- The matrices are common approximations; always verify with user testing when possible.
- This complements, not replaces, proper redundant encodings (shapes, dashes, patterns, direct labels).

Try it:
- Open `examples/simulator/index.html` in a browser.

