# FileManager/layer4_main_view/navigation_pane.py

import tkinter as tk
from tkinter import ttk


class NavigationPane(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Set the title for the Navigation Pane
        self.title_label = ttk.Label(self, text="Bookmarks", font=("Helvetica", 12, "bold"))
        self.title_label.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=5)
        
        # Create a Listbox to hold the bookmarks
        self.bookmark_listbox = tk.Listbox(self, height=20)
        self.bookmark_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add some sample bookmarks (This will be updated with actual bookmarks later)
        sample_bookmarks = ["C:\\Users\\Public", "C:\\Program Files", "C:\\Windows"]
        for bookmark in sample_bookmarks:
            self.bookmark_listbox.insert(tk.END, bookmark)

        # Add scrollbars to the Listbox
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.bookmark_listbox.yview)
        self.bookmark_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

