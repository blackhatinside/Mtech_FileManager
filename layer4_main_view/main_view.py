# FileManager/layer4_main_view/main_view.py

import tkinter as tk
from tkinter import ttk
import os
import time


class MainView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Create the treeview for displaying files and folders
        self.tree = ttk.Treeview(self, columns=("Name", "Size", "Created on", "Type"), show="headings")
        
        # Define the headings
        self.tree.heading("Name", text="Name")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Created on", text="Created on")
        self.tree.heading("Type", text="Type")
        
        # Define column width
        self.tree.column("Name", width=200)
        self.tree.column("Size", width=100)
        self.tree.column("Created on", width=150)
        self.tree.column("Type", width=100)
        
        # Pack the treeview
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbars
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load initial directory
        self.load_directory("C:\\")  # This can be updated later to reflect the actual directory

    def load_directory(self, path):
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get the list of files and directories
        try:
            for entry in os.scandir(path):
                if entry.is_dir():
                    file_type = "Folder"
                else:
                    file_type = "File"
                
                size = entry.stat().st_size
                created_on = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry.stat().st_ctime))
                
                # Insert into the treeview
                self.tree.insert("", tk.END, values=(entry.name, size, created_on, file_type))
        except PermissionError:
            print(f"Permission denied: {path}")

