import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class SettingsWindow(Adw.PreferencesWindow):
    def __init__(self, parent):
        super().__init__(modal=True, transient_for=parent)
        self.set_title("Impostazioni Pasty")
        self.set_default_size(500, 460)

        # General Page
        page = Adw.PreferencesPage()
        page.set_title("Generale")
        page.set_icon_name("emblem-system-symbolic")
        self.add(page)

        # Shortcut Group
        group_shortcut = Adw.PreferencesGroup()
        group_shortcut.set_title("Scorciatoie da Tastiera")
        group_shortcut.set_description("Naviga rapidamente come con Win+V su Windows.")
        page.add(group_shortcut)

        row_info = Adw.ActionRow()
        row_info.set_title("Scorciatoia Globale (Super+V)")
        row_info.set_subtitle(
            "Vai in Impostazioni > Tastiera > Scorciatoie personalizzate.\n"
            "Aggiungi una scorciatoia che esegue lo script 'pasty.sh'."
        )
        group_shortcut.add(row_info)

        row_keys = Adw.ActionRow()
        row_keys.set_title("Comandi rapidi nella finestra")
        row_keys.set_subtitle(
            "• Digita per cercare istantaneamente\n"
            "• Frecce Su/Giù + Invio (o Alt+1..9) per copiare\n"
            "• Ctrl+P per fissare/rimuovere un appunto • Canc per eliminare"
        )
        group_shortcut.add(row_keys)

        # History Group
        group_hist = Adw.PreferencesGroup()
        group_hist.set_title("Cronologia Appunti")
        page.add(group_hist)

        row_size = Adw.ActionRow()
        row_size.set_title("Dimensione Cronologia")
        row_size.set_subtitle("Numero massimo di appunti non fissati da mantenere")
        group_hist.add(row_size)

        spin = Gtk.SpinButton.new_with_range(10, 500, 10)
        spin.set_valign(Gtk.Align.CENTER)

        current_size = parent.clipboard_manager.config_manager.get("history_size", 50)
        spin.set_value(current_size)
        spin.connect("value-changed", self.on_size_changed, parent.clipboard_manager.config_manager)
        row_size.add_suffix(spin)

        # About Group
        group_about = Adw.PreferencesGroup()
        group_about.set_title("Informazioni")
        page.add(group_about)

        row_author = Adw.ActionRow()
        row_author.set_title("Sviluppato da")
        row_author.set_subtitle("Alessio Saponaro")
        row_author.set_icon_name("avatar-default-symbolic")
        group_about.add(row_author)

        row_github = Adw.ActionRow()
        row_github.set_title("GitHub")
        row_github.set_subtitle("github.com/Negatorto")
        row_github.set_icon_name("web-browser-symbolic")
        group_about.add(row_github)

        row_email = Adw.ActionRow()
        row_email.set_title("Contatto")
        row_email.set_subtitle("alessio.s.87@gmail.com")
        row_email.set_icon_name("mail-unread-symbolic")
        group_about.add(row_email)

    def on_size_changed(self, spin, config_manager):
        value = int(spin.get_value())
        config_manager.set("history_size", value)

        parent = self.get_transient_for()
        if parent and hasattr(parent, 'clipboard_manager'):
            parent.clipboard_manager.enforce_size_limit()


