import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Gio, GLib, GObject, Adw
import time

class HistoryWindow(Adw.Window):
    def __init__(self, clipboard_manager):
        super().__init__(title="Clipboard History")
        self.clipboard_manager = clipboard_manager
        self.set_default_size(320, 450)
        self.set_modal(True)
        self.set_resizable(False)  # Prevents tiling WMs from resizing

        # Main Layout: Toolbar View
        toolbar_view = Adw.ToolbarView()
        self.set_content(toolbar_view)

        # Header
        header = Adw.HeaderBar()
        toolbar_view.add_top_bar(header)
        
        # Settings Button
        settings_btn = Gtk.Button(icon_name="emblem-system-symbolic")
        settings_btn.set_tooltip_text("Settings")
        settings_btn.connect('clicked', self.on_settings_clicked)
        header.pack_end(settings_btn)

        # List Content
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.list_box.connect('row-activated', self.on_row_activated)
        self.list_box.add_css_class("boxed-list") # Adwaita style for lists
        
        # Wrap in ScrolledWindow
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(self.list_box)
        scrolled.set_vexpand(True)
        toolbar_view.set_content(scrolled)

        controller = Gtk.EventControllerKey()
        controller.connect('key-pressed', self.on_key_pressed)

        self.add_controller(controller)
        self.clipboard_manager.connect('history-changed', self.on_history_changed)
        self.refresh_list()

    def on_history_changed(self, manager):
        self.refresh_list()

    def refresh_list(self):
        # Clear existing
        while child := self.list_box.get_first_child():
            self.list_box.remove(child)

        history = self.clipboard_manager.get_history()
        
        for idx, item in enumerate(history):
            # Use horizontal Box for delete button + label
            row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            row_box.set_margin_top(8)
            row_box.set_margin_bottom(8)
            row_box.set_margin_start(12)
            row_box.set_margin_end(12)
            
            # Delete button
            del_btn = Gtk.Button(label="✕")
            del_btn.add_css_class("flat")
            del_btn.add_css_class("circular")
            del_btn.connect("clicked", self.on_delete_clicked, idx)
            row_box.append(del_btn)
            
            # Text label
            display_text = item.replace('\n', ' ').strip()
            if not display_text:
                display_text = "<Empty or Image>"
            
            label = Gtk.Label(label=display_text[:80], xalign=0, hexpand=True)
            label.set_ellipsize(3)
            row_box.append(label)
            
            self.list_box.append(row_box)

    def on_delete_clicked(self, button, index):
        self.clipboard_manager.delete_item(index)

    def on_row_activated(self, listbox, row):
        index = row.get_index()
        history = self.clipboard_manager.get_history()
        if 0 <= index < len(history):
            text = history[index]
            print(f"Selected item index: {index}")
            
            try:
                print(f"Setting clipboard to: {text}")
                # self.clipboard_manager.clipboard.set_text(text)
                self.clipboard_manager.clipboard.set(text)
            except Exception as e:
                print(f"Error setting clipboard: {e}")
            
            self.close()

    def on_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape:
            self.close()
            return True
        return False

    def on_settings_clicked(self, btn):
        from settings_window import SettingsWindow
        win = SettingsWindow(self)
        win.present()
