# FileManager/layer2_navigation/address_bar.py

import tkinter as tk
from tkinter import ttk, messagebox
import os

class AddressBar(ttk.Frame):
    def __init__(self, parent, navigation_manager, initial_path, on_path_change=None):
        super().__init__(parent)
        self.navigation_manager = navigation_manager
        self.current_path = initial_path
        self.on_path_change = on_path_change

        # Create and pack the text box
        self.path_var = tk.StringVar(value=self.current_path)
        self.path_entry = ttk.Entry(self, textvariable=self.path_var, width=75)
        self.path_entry.pack(padx=5, pady=5, fill=tk.X)

        # Bind Enter key and focus out events
        self.path_entry.bind("<Return>", self.on_path_change_event)
        self.path_entry.bind("<FocusOut>", self.on_focus_out)

    def on_path_change_event(self, event=None):
        new_path = self.path_var.get()
        if os.path.exists(new_path) and os.path.isdir(new_path):
            self.current_path = new_path
            if self.on_path_change:
                self.on_path_change(new_path)
        else:
            self.path_var.set(self.current_path)
            messagebox.showerror("Invalid Path", "The specified path does not exist or is not a directory.")

    def on_focus_out(self, event=None):
        # Reset to current path if invalid path entered
        if self.path_var.get() != self.current_path:
            self.path_var.set(self.current_path)

    def update_address(self, path):
        """Update address bar without triggering navigation"""
        if self.path_var.get() != path:
            self.path_var.set(path)
            self.current_path = path

    def get_current_path(self):
        return self.current_path