import time
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, GLib, Adw, Pango


class HistoryWindow(Adw.Window):
    def __init__(self, clipboard_manager):
        super().__init__(title="Pasty")
        self.clipboard_manager = clipboard_manager
        self.set_default_size(380, 520)
        self.set_resizable(False)
        self.set_hide_on_close(True)

        self._filtered_indices = []
        self._only_pinned = False

        self._apply_custom_css()

        # Main Layout: Toolbar View
        toolbar_view = Adw.ToolbarView()
        self.set_content(toolbar_view)

        # Header Bar
        header = Adw.HeaderBar()
        self.window_title = Adw.WindowTitle(title="Pasty", subtitle="Cronologia appunti")
        header.set_title_widget(self.window_title)

        # Filter Pinned Toggle Button (Start)
        self.pin_filter_btn = Gtk.ToggleButton()
        self._set_button_icon_or_label(self.pin_filter_btn, "view-pin-symbolic", "📌")
        self.pin_filter_btn.set_tooltip_text("Mostra solo elementi fissati")
        self.pin_filter_btn.connect("toggled", self.on_pin_filter_toggled)
        header.pack_start(self.pin_filter_btn)

        # Settings Button (End)
        settings_btn = Gtk.Button(icon_name="emblem-system-symbolic")
        settings_btn.set_tooltip_text("Impostazioni")
        settings_btn.connect('clicked', self.on_settings_clicked)
        header.pack_end(settings_btn)

        # Clear All Button (End)
        self.clear_btn = Gtk.Button(icon_name="user-trash-symbolic")
        self.clear_btn.set_tooltip_text("Cancella cronologia (mantiene i fissati)")
        self.clear_btn.connect('clicked', self.on_clear_clicked)
        header.pack_end(self.clear_btn)

        toolbar_view.add_top_bar(header)

        # Search Bar Area
        search_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        search_box.set_margin_start(12)
        search_box.set_margin_end(12)
        search_box.set_margin_top(6)
        search_box.set_margin_bottom(6)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Cerca negli appunti... (digita per filtrare)")
        self.search_entry.set_hexpand(True)
        self.search_entry.connect("search-changed", self.on_search_changed)
        search_box.append(self.search_entry)

        toolbar_view.add_top_bar(search_box)

        # Stack for List vs Empty State
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_vexpand(True)

        # List Content
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.list_box.set_activate_on_single_click(True)
        self.list_box.connect('row-activated', self.on_row_activated)
        self.list_box.add_css_class("boxed-list")
        self.list_box.set_margin_start(12)
        self.list_box.set_margin_end(12)
        self.list_box.set_margin_top(6)
        self.list_box.set_margin_bottom(12)
        self.list_box.set_valign(Gtk.Align.START)

        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scrolled.set_child(self.list_box)
        self.scrolled.set_vexpand(True)
        self.stack.add_named(self.scrolled, "list")

        # Empty State
        self.empty_status = Adw.StatusPage()
        self.empty_status.set_icon_name("edit-paste-symbolic")
        self.empty_status.set_title("Nessun elemento")
        self.empty_status.set_description("Copia del testo con Ctrl+C per salvarlo qui.")
        self.stack.add_named(self.empty_status, "empty")

        toolbar_view.set_content(self.stack)

        # Capture-phase key controller for seamless keyboard navigation
        controller = Gtk.EventControllerKey()
        controller.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        controller.connect('key-pressed', self.on_key_pressed)
        self.add_controller(controller)

        self.connect('close-request', self.on_close_request)
        self.clipboard_manager.connect('history-changed', self.on_history_changed)
        self.refresh_list()

    def _apply_custom_css(self):
        css_provider = Gtk.CssProvider()
        css = """
        .pasty-meta {
            font-size: 0.78em;
            opacity: 0.65;
        }
        .pasty-shortcut {
            font-size: 0.72em;
            padding: 1px 6px;
            border-radius: 6px;
            background: alpha(currentColor, 0.08);
            opacity: 0.75;
        }
        .pasty-pin-active {
            color: @accent_color;
        }
        .pasty-preview {
            font-size: 0.95em;
        }
        """
        css_provider.load_from_data(css.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def _set_button_icon_or_label(self, button, icon_name, fallback_label):
        display = Gdk.Display.get_default()
        if display:
            theme = Gtk.IconTheme.get_for_display(display)
            if theme.has_icon(icon_name):
                button.set_icon_name(icon_name)
                return
        button.set_label(fallback_label)

    def _format_relative_time(self, timestamp):
        if not timestamp:
            return ""
        diff = max(0, int(time.time() - timestamp))
        if diff < 45:
            return "Adesso"
        if diff < 3600:
            return f"{diff // 60}m fa"
        if diff < 86400:
            return f"{diff // 3600}h fa"
        days = diff // 86400
        if days == 1:
            return "Ieri"
        return f"{days}g fa"

    def open_window(self):
        self.search_entry.set_text("")
        self.refresh_list()
        self.present()
        self.search_entry.grab_focus()
        first_row = self.list_box.get_row_at_index(0)
        if first_row:
            self.list_box.select_row(first_row)

    def on_close_request(self, win):
        self.set_visible(False)
        return True

    def on_history_changed(self, manager):
        self.refresh_list()

    def on_pin_filter_toggled(self, btn):
        self._only_pinned = btn.get_active()
        self.refresh_list()

    def on_search_changed(self, entry):
        self.refresh_list()

    def on_clear_clicked(self, btn):
        self.clipboard_manager.clear_unpinned()

    def refresh_list(self):
        while child := self.list_box.get_first_child():
            self.list_box.remove(child)

        history = self.clipboard_manager.get_history()
        query = self.search_entry.get_text().strip().lower()

        total_count = len(history)
        pinned_count = sum(1 for item in history if item.get("pinned", False))
        unpinned_count = total_count - pinned_count

        if total_count == 0:
            self.window_title.set_subtitle("Cronologia vuota")
        elif pinned_count > 0:
            self.window_title.set_subtitle(f"{total_count} elementi • {pinned_count} fissati")
        else:
            self.window_title.set_subtitle(f"{total_count} elementi")

        self.clear_btn.set_sensitive(unpinned_count > 0)

        self._filtered_indices = []
        for idx, item in enumerate(history):
            if self._only_pinned and not item.get("pinned", False):
                continue
            if query and query not in item.get("text", "").lower():
                continue
            self._filtered_indices.append(idx)

        if not self._filtered_indices:
            if query:
                self.empty_status.set_title("Nessun risultato")
                self.empty_status.set_description(f"Nessun appunto contiene \"{self.search_entry.get_text().strip()}\".")
            elif self._only_pinned:
                self.empty_status.set_title("Nessun elemento fissato")
                self.empty_status.set_description("Usa l'icona 📌 su un appunto per fissarlo in alto.")
            else:
                self.empty_status.set_title("Cronologia vuota")
                self.empty_status.set_description("Copia del testo con Ctrl+C per ritrovarlo qui.")
            self.stack.set_visible_child_name("empty")
            return

        self.stack.set_visible_child_name("list")

        for visible_pos, orig_idx in enumerate(self._filtered_indices):
            item = history[orig_idx]
            text = item.get("text", "")
            is_pinned = item.get("pinned", False)
            timestamp = item.get("timestamp", 0)

            card_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            card_box.set_margin_top(8)
            card_box.set_margin_bottom(8)
            card_box.set_margin_start(12)
            card_box.set_margin_end(8)

            # Top Metadata + Action Row
            top_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

            time_str = self._format_relative_time(timestamp)
            if is_pinned:
                meta_text = f"📌 Fissato • {time_str}" if time_str else "📌 Fissato"
            else:
                meta_text = time_str

            meta_label = Gtk.Label(label=meta_text, xalign=0, hexpand=True)
            meta_label.add_css_class("pasty-meta")
            top_row.append(meta_label)

            if visible_pos < 9:
                shortcut_lbl = Gtk.Label(label=f"Alt+{visible_pos + 1}")
                shortcut_lbl.add_css_class("pasty-shortcut")
                shortcut_lbl.set_valign(Gtk.Align.CENTER)
                top_row.append(shortcut_lbl)

            # Pin Button
            pin_btn = Gtk.Button()
            self._set_button_icon_or_label(pin_btn, "view-pin-symbolic", "📌")
            pin_btn.add_css_class("flat")
            pin_btn.add_css_class("circular")
            if is_pinned:
                pin_btn.add_css_class("pasty-pin-active")
                pin_btn.set_tooltip_text("Rimuovi dai fissati (Ctrl+P)")
            else:
                pin_btn.set_tooltip_text("Fissa in alto (Ctrl+P)")
            pin_btn.connect("clicked", self.on_pin_clicked, orig_idx)
            top_row.append(pin_btn)

            # Delete Button
            del_btn = Gtk.Button(icon_name="window-close-symbolic")
            del_btn.add_css_class("flat")
            del_btn.add_css_class("circular")
            del_btn.set_tooltip_text("Elimina (Canc)")
            del_btn.connect("clicked", self.on_delete_clicked, orig_idx)
            top_row.append(del_btn)

            card_box.append(top_row)

            # Multi-line text preview (up to 3 lines like Windows 11 Win+V)
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            preview_text = "\n".join(lines[:3]) if lines else "<Vuoto>"
            if len(preview_text) > 240:
                preview_text = preview_text[:240] + "…"

            label = Gtk.Label(label=preview_text, xalign=0, hexpand=True)
            label.set_lines(3)
            label.set_wrap(True)
            label.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
            label.set_ellipsize(Pango.EllipsizeMode.END)
            label.add_css_class("pasty-preview")
            card_box.append(label)

            row = Gtk.ListBoxRow()
            row.set_child(card_box)
            row.set_tooltip_text(text[:1000])
            self.list_box.append(row)

        first_row = self.list_box.get_row_at_index(0)
        if first_row:
            self.list_box.select_row(first_row)

    def on_pin_clicked(self, button, orig_idx):
        self.clipboard_manager.toggle_pin(orig_idx)

    def on_delete_clicked(self, button, orig_idx):
        self.clipboard_manager.delete_item(orig_idx)

    def _activate_visible_row(self, visible_index):
        if 0 <= visible_index < len(self._filtered_indices):
            orig_idx = self._filtered_indices[visible_index]
            history = self.clipboard_manager.get_history()
            if 0 <= orig_idx < len(history):
                text = history[orig_idx]["text"]
                self.clipboard_manager.copy_to_clipboard(text)
                self.set_visible(False)

    def on_row_activated(self, listbox, row):
        if row is not None:
            self._activate_visible_row(row.get_index())

    def _move_selection(self, delta):
        count = len(self._filtered_indices)
        if count == 0:
            return
        selected = self.list_box.get_selected_row()
        current_idx = selected.get_index() if selected else 0
        new_idx = max(0, min(count - 1, current_idx + delta))
        new_row = self.list_box.get_row_at_index(new_idx)
        if new_row:
            self.list_box.select_row(new_row)
            # Scroll row into view if needed
            adj = self.scrolled.get_vadjustment()
            if adj:
                alloc = new_row.get_allocation()
                if alloc.height > 0:
                    top = alloc.y
                    bottom = alloc.y + alloc.height
                    page_top = adj.get_value()
                    page_bottom = page_top + adj.get_page_size()
                    if top < page_top:
                        adj.set_value(top)
                    elif bottom > page_bottom:
                        adj.set_value(bottom - adj.get_page_size())

    def on_key_pressed(self, controller, keyval, keycode, state):
        modifiers = state & Gtk.accelerator_get_default_mod_mask()

        if keyval == Gdk.KEY_Escape:
            if self.search_entry.get_text():
                self.search_entry.set_text("")
            else:
                self.set_visible(False)
            return True

        if keyval == Gdk.KEY_Down:
            self._move_selection(1)
            return True

        if keyval == Gdk.KEY_Up:
            self._move_selection(-1)
            return True

        if keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            selected = self.list_box.get_selected_row()
            if selected:
                self._activate_visible_row(selected.get_index())
            return True

        # Alt+1 .. Alt+9 quick selection
        if modifiers == Gdk.ModifierType.ALT_MASK and Gdk.KEY_1 <= keyval <= Gdk.KEY_9:
            idx = keyval - Gdk.KEY_1
            self._activate_visible_row(idx)
            return True

        # Ctrl+P to pin/unpin selected item
        if modifiers == Gdk.ModifierType.CONTROL_MASK and keyval in (Gdk.KEY_p, Gdk.KEY_P):
            selected = self.list_box.get_selected_row()
            if selected and 0 <= selected.get_index() < len(self._filtered_indices):
                orig_idx = self._filtered_indices[selected.get_index()]
                self.clipboard_manager.toggle_pin(orig_idx)
            return True

        # Delete item when pressing Delete (if search entry is empty) or Ctrl+Delete
        if keyval == Gdk.KEY_Delete and (
            not self.search_entry.get_text() or modifiers == Gdk.ModifierType.CONTROL_MASK
        ):
            selected = self.list_box.get_selected_row()
            if selected and 0 <= selected.get_index() < len(self._filtered_indices):
                vis_idx = selected.get_index()
                orig_idx = self._filtered_indices[vis_idx]
                self.clipboard_manager.delete_item(orig_idx)
                # Keep selection near the deleted item
                next_idx = min(vis_idx, len(self._filtered_indices) - 1)
                if next_idx >= 0:
                    row = self.list_box.get_row_at_index(next_idx)
                    if row:
                        self.list_box.select_row(row)
                return True

        return False

    def on_settings_clicked(self, btn):
        from settings_window import SettingsWindow
        win = SettingsWindow(self)
        win.present()

