# FileManager/layer4_main_view/main_view.py

import tkinter as tk
from tkinter import ttk, messagebox
import os
import time

class MainView(ttk.Frame):
    def __init__(self, parent, navigation_manager):
        super().__init__(parent)
        self.navigation_manager = navigation_manager
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

        # Bind single and double click events
        self.tree.bind("<ButtonRelease-1>", self.on_item_click)
        self.tree.bind("<Double-1>", self.on_item_double_click)

    def format_size(self, size):
        """Format file size into human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    def load_directory(self, path):
        """Load the contents of a directory into the treeview"""
        try:
            self.current_path = path
            # Clear the treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Get the list of files and directories
            entries = []
            for entry in os.scandir(path):
                try:
                    if entry.is_dir():
                        file_type = "Folder"
                    else:
                        file_type = "File"

                    stats = entry.stat()
                    size = stats.st_size
                    created_on = stats.st_ctime
                    entries.append((entry.name, size, created_on, file_type))
                except (PermissionError, OSError) as e:
                    print(f"Error accessing {entry.path}: {str(e)}")
                    continue

            # Sort entries: Folders first, then Files, sorted alphabetically
            entries.sort(key=lambda x: (x[3] != "Folder", x[0].lower()))

            # Insert into the treeview
            for entry in entries:
                created_on = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(entry[2]))
                size_formatted = self.format_size(entry[1]) if entry[3] == "File" else ""
                self.tree.insert("", tk.END, values=(entry[0], size_formatted, created_on, entry[3]))

        except PermissionError as e:
            messagebox.showerror("Access Denied", f"Cannot access {path}\nPermission denied.")
        except FileNotFoundError:
            messagebox.showerror("Path Not Found", f"The path {path} does not exist.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading {path}\n{str(e)}")

    def on_item_click(self, event):
        """Handle single click on an item"""
        selection = self.tree.selection()
        if selection:
            item_values = self.tree.item(selection[0])['values']
            print(f"Selected: {item_values}")

    def on_item_double_click(self, event):
        """Handle double click on an item"""
        selection = self.tree.selection()
        if not selection:
            return

        item = selection[0]
        values = self.tree.item(item)['values']

        if not values:
            return

        if values[3] == "Folder":
            selected_path = os.path.join(self.current_path, values[0])
            try:
                if os.path.exists(selected_path) and os.path.isdir(selected_path):
                    print(f"Navigating to: {selected_path}")
                    # Update: Call load_directory after navigation
                    if self.navigation_manager.navigate_to(selected_path, 'main_view'):
                        self.load_directory(selected_path)
                else:
                    messagebox.showerror("Error", "Selected folder no longer exists.")
            except Exception as e:
                messagebox.showerror("Navigation Error", f"Could not open folder: {str(e)}")
        elif values[3] == "File":
            try:
                selected_path = os.path.join(self.current_path, values[0])
                os.startfile(selected_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")