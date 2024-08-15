# FileManager/layer1_tab_bar/search_bar.py

import tkinter as tk
from tkinter import ttk

class SearchBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style='TFrame')
        
        self.search_var = tk.StringVar()
        
        # Create the search box (Entry widget)
        self.search_box = ttk.Entry(self, textvariable=self.search_var)
        self.search_box.insert(0, "Search...")
        self.search_box.pack(side=tk.RIGHT, padx=10, fill=tk.X, expand=True)
        
        # Bind focus event to clear default text
        self.search_box.bind("<FocusIn>", self.clear_default_text)
        self.search_box.bind("<FocusOut>", self.restore_default_text)
    
    def clear_default_text(self, event):
        if self.search_box.get() == "Search...":
            self.search_box.delete(0, tk.END)
            self.search_box.config(foreground='black')
            print("Search field clicked.")
    
    def restore_default_text(self, event):
        if self.search_box.get() == "":
            self.search_box.insert(0, "Search...")
            self.search_box.config(foreground='grey')
