#!/usr/bin/env python3
import os

import gi


gi.require_version("Gtk", "4.0")
from gi.repository import Gdk, Gtk


CSS_MAP = {
    "default": os.path.abspath(os.path.join("..", "brand_default.css")),
    "protan": os.path.abspath(os.path.join("..", "brand_protan.css")),
    "deutan": os.path.abspath(os.path.join("..", "brand_deutan.css")),
    "tritan": os.path.abspath(os.path.join("..", "brand_tritan.css")),
    "mono": os.path.abspath(os.path.join("..", "brand_mono.css")),
}

provider = None


def apply_css(path: str):
    global provider
    if provider is None:
        provider = Gtk.CssProvider()
    provider.load_from_path(path)
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )


class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="dev.brand.cvd.template")

    def do_activate(self, *args):
        apply_css(CSS_MAP["default"])
        win = Gtk.ApplicationWindow(application=self)
        win.set_title("Brand + CVD GTK4 Template")
        win.set_default_size(560, 340)

        header = Gtk.HeaderBar()
        win.set_titlebar(header)
        combo = Gtk.ComboBoxText()
        for k in CSS_MAP:
            combo.append_text(k)
        combo.set_active(0)
        combo.connect("changed", lambda w: apply_css(CSS_MAP[w.get_active_text()]))
        header.pack_end(combo)

        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
            margin_top=12,
            margin_bottom=12,
            margin_start=12,
            margin_end=12,
        )
        win.set_child(box)

        btn_primary = Gtk.Button(label="Primary")
        btn_primary.add_css_class("suggested-action")
        box.append(btn_primary)

        btn_secondary = Gtk.Button(label="Secondary")
        btn_secondary.add_css_class("secondary")
        box.append(btn_secondary)

        link = Gtk.Label()
        link.set_use_markup(True)
        link.set_markup(
            '<span underline="single"><a href="https://example.com">Example link</a></span>'
        )
        link.add_css_class("link")
        box.append(link)

        chip = Gtk.Label(label="Paused")
        chip.add_css_class("chip")
        chip.add_css_class("paused")
        box.append(chip)

        win.present()


if __name__ == "__main__":
    App().run(None)
