# FileManager/layer3_ribbon/ribbon.py

import tkinter as tk
from tkinter import ttk, messagebox
import os
import shutil
from tkinter import simpledialog

class Ribbon(ttk.Frame):
    def __init__(self, parent, main_view=None):
        super().__init__(parent)
        self.main_view = main_view
        self.clipboard = None  # Store path of copied/cut item

        # Create buttons with proper error handling
        self.buttons = {
            "New": self.new_item,
            "Cut": self.cut_item,
            "Copy": self.copy_item,
            "Paste": self.paste_item,
            "Delete": self.delete_item,
            "Rename": self.rename_item,
            "Sort": self.sort_items
        }

        for text, command in self.buttons.items():
            btn = ttk.Button(self, text=text, width=10, command=command)
            btn.pack(side=tk.LEFT, padx=2, pady=5)

    def handle_error(self, operation, error):
        """Central error handling for file operations"""
        error_msg = str(error)
        print(f"Error during {operation}: {error_msg}")
        messagebox.showerror(
            f"Error - {operation}",
            f"An error occurred while {operation.lower()}:\n{error_msg}"
        )

    def new_item(self):
        """Create new file or folder"""
        if not self.main_view:
            return

        # Ask user what to create
        item_type = messagebox.askquestion("New Item",
                                         "Do you want to create a folder?\n"
                                         "Yes - Create Folder\n"
                                         "No - Create File")

        # Get name for new item
        if item_type == 'yes':
            name = simpledialog.askstring("New Folder", "Enter folder name:")
            if name:
                try:
                    new_path = os.path.join(self.main_view.current_path, name)
                    os.makedirs(new_path)
                    self.main_view.load_directory(self.main_view.current_path)
                except Exception as e:
                    self.handle_error("Create Folder", e)
        else:
            name = simpledialog.askstring("New File", "Enter file name:")
            if name:
                try:
                    new_path = os.path.join(self.main_view.current_path, name)
                    with open(new_path, 'w') as f:
                        pass  # Create empty file
                    self.main_view.load_directory(self.main_view.current_path)
                except Exception as e:
                    self.handle_error("Create File", e)

    def cut_item(self):
        """Cut selected item"""
        if not self.main_view:
            return

        selected = self.main_view.tree.selection()
        if not selected:
            messagebox.showwarning("Cut", "Please select an item to cut")
            return

        try:
            item = selected[0]
            values = self.main_view.tree.item(item)['values']
            self.clipboard = {
                'action': 'cut',
                'path': os.path.join(self.main_view.current_path, values[0])
            }
        except Exception as e:
            self.handle_error("Cut", e)

    def copy_item(self):
        """Copy selected item"""
        if not self.main_view:
            return

        selected = self.main_view.tree.selection()
        if not selected:
            messagebox.showwarning("Copy", "Please select an item to copy")
            return

        try:
            item = selected[0]
            values = self.main_view.tree.item(item)['values']
            self.clipboard = {
                'action': 'copy',
                'path': os.path.join(self.main_view.current_path, values[0])
            }
        except Exception as e:
            self.handle_error("Copy", e)

    def paste_item(self):
        """Paste item from clipboard"""
        if not self.main_view or not self.clipboard:
            return

        try:
            source_path = self.clipboard['path']
            if not os.path.exists(source_path):
                messagebox.showerror("Paste", "Source item no longer exists")
                return

            filename = os.path.basename(source_path)
            dest_path = os.path.join(self.main_view.current_path, filename)

            # Handle name conflicts
            counter = 1
            while os.path.exists(dest_path):
                base, ext = os.path.splitext(filename)
                dest_path = os.path.join(self.main_view.current_path,
                                       f"{base} ({counter}){ext}")
                counter += 1

            if self.clipboard['action'] == 'cut':
                shutil.move(source_path, dest_path)
            else:  # copy
                if os.path.isdir(source_path):
                    shutil.copytree(source_path, dest_path)
                else:
                    shutil.copy2(source_path, dest_path)

            self.main_view.load_directory(self.main_view.current_path)
            if self.clipboard['action'] == 'cut':
                self.clipboard = None

        except Exception as e:
            self.handle_error("Paste", e)

    def delete_item(self):
        """Delete selected item"""
        if not self.main_view:
            return

        selected = self.main_view.tree.selection()
        if not selected:
            messagebox.showwarning("Delete", "Please select an item to delete")
            return

        try:
            if not messagebox.askyesno("Confirm Delete",
                                     "Are you sure you want to delete the selected items?"):
                return

            for item in selected:
                values = self.main_view.tree.item(item)['values']
                path = os.path.join(self.main_view.current_path, values[0])

                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)

            self.main_view.load_directory(self.main_view.current_path)

        except Exception as e:
            self.handle_error("Delete", e)

    def rename_item(self):
        """Rename selected item"""
        if not self.main_view:
            return

        selected = self.main_view.tree.selection()
        if not selected:
            messagebox.showwarning("Rename", "Please select an item to rename")
            return

        try:
            item = selected[0]
            values = self.main_view.tree.item(item)['values']
            old_name = values[0]
            old_path = os.path.join(self.main_view.current_path, old_name)

            new_name = simpledialog.askstring("Rename",
                                            "Enter new name:",
                                            initialvalue=old_name)
            if new_name and new_name != old_name:
                new_path = os.path.join(self.main_view.current_path, new_name)
                os.rename(old_path, new_path)
                self.main_view.load_directory(self.main_view.current_path)

        except Exception as e:
            self.handle_error("Rename", e)

    def sort_items(self):
        """Sort items in the current view"""
        if not self.main_view:
            return

        # Create popup menu for sort options
        popup = tk.Menu(self, tearoff=0)

        def sort_by(column, reverse=False):
            items = [(self.main_view.tree.set(item, column), item)
                    for item in self.main_view.tree.get_children('')]

            # Sort items
            items.sort(reverse=reverse)

            # Rearrange items in sorted positions
            for index, (_, item) in enumerate(items):
                self.main_view.tree.move(item, '', index)

        popup.add_command(label="Name (A to Z)",
                         command=lambda: sort_by("Name", False))
        popup.add_command(label="Name (Z to A)",
                         command=lambda: sort_by("Name", True))
        popup.add_command(label="Size (Smallest first)",
                         command=lambda: sort_by("Size", False))
        popup.add_command(label="Size (Largest first)",
                         command=lambda: sort_by("Size", True))
        popup.add_command(label="Date (Oldest first)",
                         command=lambda: sort_by("Created on", False))
        popup.add_command(label="Date (Newest first)",
                         command=lambda: sort_by("Created on", True))

        # Display popup menu
        try:
            popup.tk_popup(self.winfo_pointerx(), self.winfo_pointery())
        finally:
            popup.grab_release()