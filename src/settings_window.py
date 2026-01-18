import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw
import os

class SettingsWindow(Adw.PreferencesWindow):
    def __init__(self, parent):
        super().__init__(modal=True, transient_for=parent)
        self.set_title("Pasty Settings")
        self.set_default_size(500, 400)
        
        # General Page
        page = Adw.PreferencesPage()
        page.set_title("General")
        page.set_icon_name("emblem-system-symbolic")
        self.add(page)

        # Shortcut Group
        group_shortcut = Adw.PreferencesGroup()
        group_shortcut.set_title("Global Shortcut")
        group_shortcut.set_description("Configure a custom shortcut in GNOME Settings.")
        page.add(group_shortcut)

        # Instructions Row
        row_info = Adw.ActionRow()
        row_info.set_title("How to set shortcut")
        row_info.set_subtitle("Go to Settings > Keyboard > View and Customize Shortcuts > Custom Shortcuts.\nAdd a new shortcut running the 'pasty.sh' script.")
        group_shortcut.add(row_info)

        # History Group
        group_hist = Adw.PreferencesGroup()
        group_hist.set_title("Clipboard History")
        page.add(group_hist)
        
        # History Size Row
        row_size = Adw.ActionRow()
        row_size.set_title("History Size")
        row_size.set_subtitle("Number of items to keep (Max)")
        group_hist.add(row_size)

        spin = Gtk.SpinButton.new_with_range(10, 500, 10)
        spin.set_valign(Gtk.Align.CENTER)
        
        # Load current value
        current_size = parent.clipboard_manager.config_manager.get("history_size", 50)
        spin.set_value(current_size)
        
        # Save on change
        spin.connect("value-changed", self.on_size_changed, parent.clipboard_manager.config_manager)
        
        row_size.add_suffix(spin)

        # About Group
        group_about = Adw.PreferencesGroup()
        group_about.set_title("About")
        page.add(group_about)

        # Author Row
        row_author = Adw.ActionRow()
        row_author.set_title("Developed by")
        row_author.set_subtitle("Alessio Saponaro")
        row_author.set_icon_name("avatar-default-symbolic")
        group_about.add(row_author)

        # GitHub Row
        row_github = Adw.ActionRow()
        row_github.set_title("GitHub")
        row_github.set_subtitle("github.com/Negatorto")
        row_github.set_icon_name("web-browser-symbolic")
        group_about.add(row_github)

        # Email Row
        row_email = Adw.ActionRow()
        row_email.set_title("Contact")
        row_email.set_subtitle("alessio.s.87@gmail.com")
        row_email.set_icon_name("mail-unread-symbolic")
        group_about.add(row_email)

    def on_size_changed(self, spin, config_manager):
        value = int(spin.get_value())
        config_manager.set("history_size", value)

