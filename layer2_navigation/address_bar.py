# FileManager/layer2_navigation/address_bar.py

import tkinter as tk
from tkinter import ttk, messagebox
import os

class AddressBar(ttk.Frame):
    def __init__(self, parent, initial_path):
        super().__init__(parent)
        self.current_path = initial_path

        # Create and pack the text box for showing and editing the current path
        self.path_var = tk.StringVar(value=self.current_path)
        self.path_entry = ttk.Entry(self, textvariable=self.path_var)
        self.path_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # Bind the Enter key to trigger path change
        self.path_entry.bind("<Return>", self.change_directory)
    
    def change_directory(self, event):
        new_path = self.path_var.get()
        if os.path.isdir(new_path):
            self.current_path = new_path
            print(f"Changed directory to: {self.current_path}")
            # Update the content of the application based on the new directory
            # For now, we just print the new path
        else:
            messagebox.showerror("Invalid Path", "The path you entered does not exist or is not a directory.")