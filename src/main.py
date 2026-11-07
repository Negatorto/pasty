import os
import sys

# Default to X11 backend (XWayland) on GNOME Wayland so GTK4 can continuously
# monitor and set the clipboard even when the window is hidden in background.
os.environ.setdefault("GDK_BACKEND", "x11")

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gio, Adw, Gtk, Gdk

from config_manager import ConfigManager
from clipboard_manager import ClipboardManager
from history_window import HistoryWindow


class PastyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(
            application_id="io.github.negatorto.pasty",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs,
        )
        self.connect('startup', self.on_startup)
        self.connect('activate', self.on_activate)
        self.connect('command-line', self.on_command_line)
        self.win = None
        self.config_manager = None
        self.clipboard_manager = None

    def on_startup(self, app):
        self.hold()
        self._register_app_icon()
        self.config_manager = ConfigManager()
        self.clipboard_manager = ClipboardManager(self.config_manager)
        self.win = HistoryWindow(self.clipboard_manager)
        self.win.set_application(self)

    def _register_app_icon(self):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(project_root, "data", "pasty.png")
        if os.path.exists(icon_path):
            display = Gdk.Display.get_default()
            if display:
                icon_theme = Gtk.IconTheme.get_for_display(display)
                icon_theme.add_search_path(os.path.join(project_root, "data"))
                icon_theme.add_resource_path(os.path.join(project_root, "data"))


    def on_command_line(self, app, command_line):
        args = command_line.get_arguments()
        if "--silent" in args or "-s" in args:
            print("Pasty running in background (Silent Mode)")
            return 0

        self.activate()
        return 0

    def on_activate(self, app):
        if self.win:
            self.win.open_window()


if __name__ == "__main__":
    app = PastyApp()
    sys.exit(app.run(sys.argv))
