import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from i18n import _


class SettingsWindow(Adw.PreferencesWindow):
    def __init__(self, parent):
        super().__init__(modal=True, transient_for=parent)
        self.set_title(_("settings_title"))
        self.set_default_size(500, 460)

        # General Page
        page = Adw.PreferencesPage()
        page.set_title(_("page_general"))
        page.set_icon_name("emblem-system-symbolic")
        self.add(page)

        # Shortcut Group
        group_shortcut = Adw.PreferencesGroup()
        group_shortcut.set_title(_("group_shortcuts"))
        group_shortcut.set_description(_("group_shortcuts_desc"))
        page.add(group_shortcut)

        row_info = Adw.ActionRow()
        row_info.set_title(_("row_global_shortcut_title"))
        row_info.set_subtitle(_("row_global_shortcut_sub"))
        group_shortcut.add(row_info)

        row_keys = Adw.ActionRow()
        row_keys.set_title(_("row_inapp_shortcuts_title"))
        row_keys.set_subtitle(_("row_inapp_shortcuts_sub"))
        group_shortcut.add(row_keys)

        # History Group
        group_hist = Adw.PreferencesGroup()
        group_hist.set_title(_("group_history"))
        page.add(group_hist)

        row_size = Adw.ActionRow()
        row_size.set_title(_("row_history_size_title"))
        row_size.set_subtitle(_("row_history_size_sub"))
        group_hist.add(row_size)

        spin = Gtk.SpinButton.new_with_range(10, 500, 10)
        spin.set_valign(Gtk.Align.CENTER)

        current_size = parent.clipboard_manager.config_manager.get("history_size", 50)
        spin.set_value(current_size)
        spin.connect("value-changed", self.on_size_changed, parent.clipboard_manager.config_manager)
        row_size.add_suffix(spin)

        # About Group
        group_about = Adw.PreferencesGroup()
        group_about.set_title(_("group_about"))
        page.add(group_about)

        row_author = Adw.ActionRow()
        row_author.set_title(_("row_developer"))
        row_author.set_subtitle("Alessio Saponaro")
        row_author.set_icon_name("avatar-default-symbolic")
        group_about.add(row_author)

        row_github = Adw.ActionRow()
        row_github.set_title(_("row_github"))
        row_github.set_subtitle("github.com/Negatorto")
        row_github.set_icon_name("web-browser-symbolic")
        group_about.add(row_github)

        row_email = Adw.ActionRow()
        row_email.set_title(_("row_contact"))
        row_email.set_subtitle("alessio.s.87@gmail.com")
        row_email.set_icon_name("mail-unread-symbolic")
        group_about.add(row_email)

    def on_size_changed(self, spin, config_manager):
        value = int(spin.get_value())
        config_manager.set("history_size", value)

        parent = self.get_transient_for()
        if parent and hasattr(parent, 'clipboard_manager'):
            parent.clipboard_manager.enforce_size_limit()



