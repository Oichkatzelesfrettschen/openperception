#!/usr/bin/env python3
# GTK4 demo using brand CSS variants

import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk


def load_css(path: str):
    provider = Gtk.CssProvider()
    provider.load_from_path(path)
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )


class Demo(Gtk.Application):
    def __init__(self, css_path):
        super().__init__(application_id='dev.brand.cvd.demo')
        self.css_path = css_path

    def do_activate(self, *args):
        load_css(self.css_path)

        win = Gtk.ApplicationWindow(application=self)
        win.set_title("Brand + CVD GTK4 Demo")
        win.set_default_size(520, 260)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12, margin_top=12, margin_bottom=12, margin_start=12, margin_end=12)
        win.set_child(box)

        header = Gtk.Label(label="Accessible UI: links underlined, focus rings visible, redundant cues.")
        box.append(header)

        # Primary button (suggested-action)
        btn_primary = Gtk.Button(label="Primary")
        btn_primary.add_css_class('suggested-action')
        box.append(btn_primary)

        # Secondary button (custom class)
        btn_secondary = Gtk.Button(label="Secondary")
        btn_secondary.add_css_class('secondary')
        box.append(btn_secondary)

        # Link label (redundant underline)
        link_label = Gtk.Label()
        link_label.set_use_markup(True)
        link_label.set_markup('<span underline="single"><a href="https://example.com">Example link</a></span>')
        link_label.add_css_class('link')
        box.append(link_label)

        # Chip with hatch background for paused
        chip = Gtk.Label(label="Paused")
        chip.add_css_class('chip')
        chip.add_css_class('paused')
        box.append(chip)

        win.present()


if __name__ == '__main__':
    variant = (sys.argv[1] if len(sys.argv) > 1 else 'default').lower()
    css_map = {
        'default': 'gtk4/brand_default.css',
        'protan': 'gtk4/brand_protan.css',
        'deutan': 'gtk4/brand_deutan.css',
        'tritan': 'gtk4/brand_tritan.css',
        'mono': 'gtk4/brand_mono.css',
    }
    css_path = css_map.get(variant, css_map['default'])
    app = Demo(css_path)
    app.run(None)

