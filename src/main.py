from history_window import HistoryWindow
from clipboard_manager import ClipboardManager
import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib

class PastyApp(Adw.Application):
    def __init__(self, silent_start=False, **kwargs):
        super().__init__(**kwargs)
        self.set_application_id("io.github.negatorto.pasty")
        self.connect('activate', self.on_activate)
        self.win = None
        self.silent_start = silent_start

    def on_activate(self, app):
        from config_manager import ConfigManager
        
        if not hasattr(self, 'hold_id'):
            self.hold_id = self.hold()

        if not hasattr(self, 'config_manager'):
            self.config_manager = ConfigManager()

        if not hasattr(self, 'clipboard_manager'):
            self.clipboard_manager = ClipboardManager(self.config_manager)

        if self.silent_start:
            print("(Silent Mode)")
            self.silent_start = False
            return

        if not self.win:
            self.win = HistoryWindow(self.clipboard_manager)
            self.win.set_application(app)
            self.win.connect('close-request', self.on_window_close)
            self.win.present()
        else:
            self.win.refresh_list()
            self.win.present()

    def on_window_close(self, win):
        self.win = None
        return False

if __name__ == "__main__":
    silent_mode = False
    if "--silent" in sys.argv:
        silent_mode = True
        sys.argv.remove("--silent")

    app = PastyApp(silent_start=silent_mode)
    app.run(sys.argv)