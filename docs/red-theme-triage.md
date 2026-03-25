# Red Theme Triage

Date: 2026-03-22

## Verdict

Yes, the red theme is worth pursuing, but not as the default semantic color
system for `openperception`.

The right triage is:

- use red as atmosphere,
- use burgundy/mahogany as tertiary emphasis,
- keep non-red structure for primary interaction and accessibility,
- treat pure alert-red as a narrow warning/error signal rather than the whole
  brand.

## Why

The local red-theme corpus is strongest when it talks about:

- MATE and FreeBSD-adjacent "classy" desktops,
- burgundy, mahogany, maroon, oxblood, and wood-toned atmospheres,
- institutional and heritage palettes,
- wallpaper, chrome, and surface identity.

It is weakest when it drifts toward:

- pure red/black gamer aesthetics,
- red-only semantics,
- treating "red" as both atmosphere and warning at the same time,
- assuming a red-forward theme will remain separable for red-weak users.

That split matters. "Theme" and "semantic UI system" are not the same thing.

## Triage table

| Direction | Status | Why |
|---|---|---|
| Burgundy/mahogany document skin | Greenlight | Works as atmosphere and can stay accessible with cream/slate text pairing |
| Burgundy tertiary emphasis inside the experimental accessible pack | Greenlight | Already aligned with the indigo/mauve/burgundy work |
| Mahogany wallpaper + subdued chrome + neutral widgets | Greenlight | Preserves mood without overloading semantics |
| Institutional maroon surfaces with strong text contrast | Yellowlight | Viable, but needs careful contrast and not too many simultaneous accents |
| Pure red as primary CTA color everywhere | Redlight | Too likely to collide with warning semantics and CVD collapse |
| Red/black-only default UI | Redlight | High fatigue, weak nuance, poor accessibility headroom |

## Recommended role split

For `openperception`, the cleanest split is:

- Primary interaction: indigo or another non-red stable family
- Secondary interpretation/highlight: mauve
- Tertiary/high-gravity emphasis: burgundy
- Atmosphere layer: mahogany, wood, parchment, cream, brass, slate
- Warning/error lane: narrow, explicit, text-labeled red states only

This lets the project keep the emotional force of the red theme without making
the whole system fragile.

## Red-theme candidate palette

This is not proposed as the main app semantic stack. It is the best "theme
skin" direction from the current triage:

| Role | Hex | Use |
|---|---|---|
| mahogany-900 | `#241513` | shell/chrome depth |
| mahogany-700 | `#4A231D` | panels, window trim, dark cards |
| burgundy-700 | `#7A1628` | tertiary emphasis |
| oxblood-600 | `#A1344C` | callouts, focused accents |
| brass-500 | `#A67C52` | decorative contrast, highlights |
| cream-100 | `#F8F3EE` | surfaces and reading areas |
| slate-700 | `#374151` | text and neutral structure |

## Practical recommendation

Short term:

1. Keep the experimental indigo/mauve/burgundy pack as the accessibility-first
   lane.
2. Use the red theme as a skin layer for docs, wallpapers, or desktop-targeted
   theming.
3. Only promote burgundy into product UI where the meaning is also carried by
   text, icon, or pattern.

Medium term:

1. If a dedicated red theme is wanted, build it as a separate theme pack rather
   than replacing the default token source.
2. Pair it with a comparison example like the current accessible-pack demo, not
   as a silent production swap.

## Links to current work

- `papers/unified_color_scheme_scope_2026-03-22.md`
- `tokens/experimental-mauve-burgundy.json`
- `tokens/experimental-red-mahogany.json`
- `examples/ui/palette-compare.html`
