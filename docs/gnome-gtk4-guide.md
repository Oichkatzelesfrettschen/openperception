# GNOME/GTK4 + libadwaita Guide (Brand + CVD)

This guide shows how to apply the brand palette in GTK4/libadwaita apps with accessible defaults and CVD-aware variants.

Files:
- `gtk4/brand_default.css` (and `_protan`, `_deutan`, `_tritan`, `_mono`)
- `gtk4/demo.py` — loads the CSS provider and shows a sample UI

## Approach
- Use application-level CSS via `Gtk.CssProvider` instead of patching system theme
- Map brand colors to Adwaita color roles: `accent_bg_color`, `accent_color`, `link_color`, `borders`, etc.
- Redundant cues: underlines for links, focus ring outlines, icons/labels for success/error, hatch backgrounds for paused/disabled

## Usage

- Load a CSS file at startup:

```python
provider = Gtk.CssProvider()
provider.load_from_path('gtk4/brand_default.css')
Gtk.StyleContext.add_provider_for_display(
    Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
```

- To switch CVD variant, load the corresponding CSS: `brand_protan.css`, `brand_deutan.css`, `brand_tritan.css`, or `brand_mono.css`.

## Notes
- libadwaita provides `.suggested-action` and `.destructive-action` classes; keep icons and labels so users don’t rely on color only.
- Ensure buttons and interactive controls have visible focus rings; do not rely solely on color changes.
- For monochrome environments, additional patterns and icons signal state; link underlines should always be visible.

## Testing
- Test light/dark modes and high contrast in GNOME
- Verify focus visibility by keyboard navigation (Tab/Shift+Tab)
- Simulate CVD by comparing protan/deutan/tritan CSS variants

