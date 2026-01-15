# GTK4 Builder Template (Brand + CVD)

This is a minimal GTK4 Python application wired to brand CSS variants with a runtime switcher.

## Run
- `python3 app.py` (defaults to `default` variant)

## Features
- Headerbar with a Variant selector (default, protan, deutan, tritan, mono)
- Applies `gtk4/brand_<variant>.css` at runtime using `Gtk.CssProvider`
- Buttons show primary/secondary styles; link label underlined; paused chip with hatch

## GNOME Builder
- Open this folder in Builder, set run command to `python3 app.py`
- Optionally add a flatpak manifest for packaging later

