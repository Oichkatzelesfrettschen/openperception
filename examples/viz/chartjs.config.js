// Chart.js 4 config with color + non-color encodings
// Pick variant: 'default' | 'protan' | 'deutan' | 'tritan' | 'mono'

const TOKENS = require('../../tokens/color-tokens.json');

function makeDatasets(variant = 'default', data = []) {
  const t = TOKENS[variant] || TOKENS.default;
  const colors = t.viz.categorical;
  const dashes = t.viz.dashes;
  const markers = t.viz.markers; // pointStyle in Chart.js: 'circle', 'triangle', 'rect', 'rectRot', 'cross', 'star'

  return data.map((series, i) => ({
    label: series.label,
    data: series.values,
    borderColor: colors[i % colors.length],
    backgroundColor: colors[i % colors.length],
    borderDash: dashes[i % dashes.length],
    pointStyle: markers[i % markers.length],
    spanGaps: true,
  }));
}

module.exports = { makeDatasets };

