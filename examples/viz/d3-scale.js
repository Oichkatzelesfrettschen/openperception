// D3 categorical scale with brand-first, CVD-aware tokens
// Usage: pass `variant` as 'default' | 'protan' | 'deutan' | 'tritan' | 'mono'

const TOKENS = require('../../tokens/color-tokens.json');

function d3BrandScale(d3, variant = 'default') {
  const t = TOKENS[variant] || TOKENS.default;
  const colors = t.viz.categorical;
  return d3.scaleOrdinal().range(colors);
}

// Example: apply non-color encodings for lines/markers
function seriesStyles(variant = 'default') {
  const t = TOKENS[variant] || TOKENS.default;
  return {
    dashes: t.viz.dashes,        // e.g., svg stroke-dasharray
    markers: t.viz.markers       // semantic, map to shapes per charting layer
  };
}

module.exports = { d3BrandScale, seriesStyles };

