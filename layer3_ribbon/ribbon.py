# FileManager/layer3_ribbon/ribbon.py

import tkinter as tk
from tkinter import ttk


class Ribbon(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Create buttons for file management tools
        self.cut_button = ttk.Button(self, text="Cut", width=0)
        self.copy_button = ttk.Button(self, text="Copy", width=0)
        self.paste_button = ttk.Button(self, text="Paste", width=0)
        self.delete_button = ttk.Button(self, text="Delete", width=0)
        self.rename_button = ttk.Button(self, text="Rename", width=0)
        self.sort_button = ttk.Button(self, text="Sort", width=0)
        
        # Pack the buttons in a horizontal row
        self.cut_button.pack(side=tk.LEFT, pady=5)
        self.copy_button.pack(side=tk.LEFT, pady=5)
        self.paste_button.pack(side=tk.LEFT, pady=5)
        self.delete_button.pack(side=tk.LEFT, pady=5)
        self.rename_button.pack(side=tk.LEFT, pady=5)
        self.sort_button.pack(side=tk.LEFT, pady=5)
