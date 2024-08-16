# FileManager/layer2_navigation/address_bar.py

import tkinter as tk
from tkinter import ttk, messagebox
import os


class AddressBar(ttk.Frame):
    def __init__(self, parent, initial_path, on_path_change=None):
        super().__init__(parent)
        self.current_path = initial_path
        self.on_path_change = on_path_change  # Callback for address bar changes

        # Create and pack the text box for showing and editing the current path
        self.path_var = tk.StringVar(value=self.current_path)
        self.path_entry = ttk.Entry(self, textvariable=self.path_var, width=75)
        self.path_entry.pack(padx=5, pady=5, fill=tk.X)
        
        # Bind the Enter key to trigger path change
        self.path_entry.bind("<Return>", self.change_directory)
    
    def change_directory(self, event):
        new_path = self.path_var.get()
        if os.path.isdir(new_path):
            self.current_path = new_path
            print(f"Changed directory to: {self.current_path}")
            if self.on_path_change:
                self.on_path_change(self.current_path)  # Notify callback about the path change
        else:
            messagebox.showerror("Invalid Path", "The path you entered does not exist or is not a directory.")

    def update_address(self, path):
        if self.path_var.get() != path:
            self.path_var.set(path)
