# Matplotlib categorical palette with line and marker styles
# Variant: 'default' | 'protan' | 'deutan' | 'tritan' | 'mono'

import json
from pathlib import Path
from cycler import cycler
import matplotlib.pyplot as plt

TOKENS = json.loads(Path(__file__).resolve().parents[2].joinpath('tokens/color-tokens.json').read_text())


def apply_brand_cycler(variant: str = 'default'):
    t = TOKENS.get(variant, TOKENS['default'])
    colors = t['viz']['categorical']
    markers = t['viz']['markers']
    dashes = t['viz']['dashes']

    # Map generic marker names to matplotlib markers
    marker_map = {
        'circle': 'o',
        'square': 's',
        'triangle': '^',
        'diamond': 'D',
    }
    mm = [marker_map.get(m, 'o') for m in markers]

    # Convert dash arrays to matplotlib (on, off) tuples
    ls = [ (0, tuple(d if d != 0 else 1 for d in dash)) if dash != [0,0] else 'solid' for dash in dashes ]

    plt.rcParams['axes.prop_cycle'] = cycler(color=colors) + cycler(marker=mm) + cycler(dashes=ls)


if __name__ == '__main__':
    apply_brand_cycler('default')
    import numpy as np
    x = np.linspace(0, 10, 100)
    for i in range(6):
        y = np.sin(x + i * 0.4)
        plt.plot(x, y, label=f'Series {i+1}')
    plt.legend()
    plt.title('Brand + CVD-aware styles')
    plt.show()

