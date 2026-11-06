import json
import os
import time

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gdk, GObject, GLib


class ClipboardManager(GObject.Object):
    __gsignals__ = {
        'history-changed': (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.history = []
        self._save_timeout_id = None
        self._last_clipboard_text = None
        self._is_reading = False

        data_dir = os.path.expanduser("~/.local/share/pasty")
        os.makedirs(data_dir, exist_ok=True)
        self.history_file = os.path.join(data_dir, "history.json")
        self.load_history()

        self.clipboard = Gdk.Display.get_default().get_clipboard()
        self.clipboard.connect('changed', self.on_clipboard_changed)

        # Read current clipboard immediately on startup and monitor periodically
        # as a fallback for Wayland/XWayland bridge transitions.
        GLib.idle_add(self.check_clipboard)
        GLib.timeout_add(1000, self._poll_clipboard)

    def _normalize_item(self, item):
        if isinstance(item, str):
            return {
                "text": item,
                "pinned": False,
                "timestamp": time.time(),
            }
        if isinstance(item, dict) and isinstance(item.get("text"), str):
            return {
                "text": item["text"],
                "pinned": bool(item.get("pinned", False)),
                "timestamp": float(item.get("timestamp", time.time())),
            }
        return None

    def _sort_history(self):
        # Keep pinned items at the top while preserving relative order
        pinned = [item for item in self.history if item.get("pinned", False)]
        unpinned = [item for item in self.history if not item.get("pinned", False)]
        self.history = pinned + unpinned

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    raw_history = json.load(f)
                if isinstance(raw_history, list):
                    normalized = []
                    for item in raw_history:
                        norm = self._normalize_item(item)
                        if norm and norm["text"].strip():
                            normalized.append(norm)
                    self.history = normalized
                    self._sort_history()
            except Exception as e:
                print(f"Error loading history: {e}")
                self.history = []

    def save_history(self):
        if self._save_timeout_id is not None:
            GLib.source_remove(self._save_timeout_id)
        self._save_timeout_id = GLib.timeout_add(500, self._do_save_history)

    def _do_save_history(self):
        self._save_timeout_id = None
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving history: {e}")
        return False

    def check_clipboard(self):
        if not self._is_reading:
            self._is_reading = True
            self.clipboard.read_text_async(None, self.on_read_text_finish, None)
        return False

    def _poll_clipboard(self):
        self.check_clipboard()
        return True

    def on_clipboard_changed(self, clipboard):
        self.check_clipboard()

    def on_read_text_finish(self, clipboard, result, data):
        self._is_reading = False
        try:
            text = clipboard.read_text_finish(result)
            if text is not None and text.strip():
                if text != self._last_clipboard_text:
                    self._last_clipboard_text = text
                    self.add_to_history(text)
        except GLib.Error:
            # Clipboard currently holds non-text data (e.g. image/files) or is empty
            pass
        except Exception as e:
            print(f"Error reading clipboard: {e}")

    def copy_to_clipboard(self, text):
        if not text:
            return
        self._last_clipboard_text = text
        try:
            val = GObject.Value(GObject.TYPE_STRING, text)
            provider = Gdk.ContentProvider.new_for_value(val)
            self.clipboard.set_content(provider)
        except Exception:
            try:
                self.clipboard.set(text)
            except Exception as e:
                print(f"Error setting clipboard: {e}")

        self.add_to_history(text)

    def add_to_history(self, text):
        if not text or not text.strip():
            return

        was_pinned = False
        existing_idx = None
        for idx, item in enumerate(self.history):
            if item["text"] == text:
                was_pinned = item.get("pinned", False)
                existing_idx = idx
                break

        if existing_idx is not None:
            del self.history[existing_idx]

        new_item = {
            "text": text,
            "pinned": was_pinned,
            "timestamp": time.time(),
        }

        self.history.insert(0, new_item)
        self._sort_history()
        self.enforce_size_limit()

    def enforce_size_limit(self):
        max_size = self.config_manager.get("history_size", 50)
        pinned = [item for item in self.history if item.get("pinned", False)]
        unpinned = [item for item in self.history if not item.get("pinned", False)]

        if len(unpinned) > max_size:
            unpinned = unpinned[:max_size]

        self.history = pinned + unpinned
        self.save_history()
        self.emit('history-changed')

    def get_history(self):
        return self.history

    def toggle_pin(self, index):
        if 0 <= index < len(self.history):
            self.history[index]["pinned"] = not self.history[index].get("pinned", False)
            self._sort_history()
            self.save_history()
            self.emit('history-changed')

    def delete_item(self, index):
        if 0 <= index < len(self.history):
            del self.history[index]
            self.save_history()
            self.emit('history-changed')

    def clear_unpinned(self):
        self.history = [item for item in self.history if item.get("pinned", False)]
        self.save_history()
        self.emit('history-changed')

