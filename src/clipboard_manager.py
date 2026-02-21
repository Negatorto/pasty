import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gdk, GObject

import json
import os

class ClipboardManager(GObject.Object):
    __gsignals__ = {
        'history-changed': (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.history = []
        data_dir = os.path.expanduser("~/.local/share/pasty")
        os.makedirs(data_dir, exist_ok=True)
        self.history_file = os.path.join(data_dir, "history.json")
        self.load_history()
        
        self.clipboard = Gdk.Display.get_default().get_clipboard()
        self.clipboard.connect('changed', self.on_clipboard_changed)
        
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except Exception as e:
                print(f"Error loading history: {e}")
                self.history = []

    def save_history(self):
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            print(f"Error saving history: {e}")

    def on_clipboard_changed(self, clipboard):
        clipboard.read_text_async(None, self.on_read_text_finish, None)

    def on_read_text_finish(self, clipboard, result, data):
        try:
            text = clipboard.read_text_finish(result)
            if text is not None and text.strip():
                self.add_to_history(text)
        except Exception as e:
            print(f"Error reading clipboard: {e}")

    def add_to_history(self, text):
        # Remove duplicate if it exists anywhere in the list
        if text in self.history:
            self.history.remove(text)
        
        # Add to top
        self.history.insert(0, text)
        print(f"Copied: {text[:20]}...")
        
        # Limit history size
        max_size = self.config_manager.get("history_size", 50)
        while len(self.history) > max_size:
            self.history.pop()
        
        self.save_history()
        self.emit('history-changed')

    def get_history(self):
        return self.history

    def delete_item(self, index):
        if 0 <= index < len(self.history):
            del self.history[index]
            self.save_history()
            self.emit('history-changed')
