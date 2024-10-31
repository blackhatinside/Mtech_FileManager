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
        self.tree.column("Name", width=300)
        self.tree.column("Size", width=50)
        self.tree.column("Created on", width=100)
        self.tree.column("Type", width=50)

        # Pack the treeview
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add scrollbars
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Initialize current path
        self.current_path = ""

        # Load initial directory
        self.load_directory("C:\\")  # This can be updated later to reflect the actual directory

        # Bind single and double click events
        self.tree.bind("<ButtonRelease-1>", self.on_item_click)
        self.tree.bind("<Double-1>", self.on_item_double_click)

    def load_directory(self, path):
        self.current_path = path  # Update current path
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get the list of files and directories
        entries = []
        try:
            for entry in os.scandir(path):
                if entry.is_dir():
                    file_type = "Folder"
                else:
                    file_type = "File"

                size = entry.stat().st_size
                created_on = entry.stat().st_ctime
                entries.append((entry.name, size, created_on, file_type))

            # Sort entries: Folders first, then Files, sorted by created_on (descending)
            entries.sort(key=lambda x: (x[3], -x[2]))  # Sorting by type and creation time

            # Insert into the treeview
            for entry in entries:
                created_on = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(entry[2]))
                self.tree.insert("", tk.END, values=(entry[0], entry[1], created_on, entry[3]))

        except PermissionError:
            print(f"Permission denied: {path}")

    def on_item_click(self, event):
        item = self.tree.selection()
        if item:
            item_values = self.tree.item(item[0], 'values')
            print(f"Selected: {item_values}")

    def on_item_double_click(self, event):
        item = self.tree.selection()
        if item:
            item_values = self.tree.item(item[0], 'values')
            if item_values[3] == "Folder":
                selected_path = os.path.join(self.current_path, item_values[0])
                if os.path.isdir(selected_path):
                    self.load_directory(selected_path)
                    print(f"Opened folder: {selected_path}")
