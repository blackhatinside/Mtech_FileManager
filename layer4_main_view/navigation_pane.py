# FileManager/layer4_main_view/navigation_pane.py

import tkinter as tk
from tkinter import ttk

class NavigationPane(ttk.Frame):
    def __init__(self, parent, address_bar, on_path_change=None):
        super().__init__(parent)
        self.bookmarks = {}  # Dictionary to store bookmarks (folder name -> path)
        self.address_bar = address_bar  # Reference to the address bar
        self.current_path = address_bar.current_path

        # Title and '+' button for Bookmarks
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=tk.X, padx=10, pady=5)

        title_label = ttk.Label(title_frame, text="Bookmarks")
        title_label.pack(side=tk.LEFT)

        self.add_button = ttk.Button(title_frame, text="+", width=2, command=self.add_bookmark)
        self.add_button.pack(side=tk.RIGHT)

        # Frame to hold the list of bookmarks
        self.bookmark_list_frame = ttk.Frame(self)
        self.bookmark_list_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        # Refresh bookmarks on initialization
        self.refresh_bookmarks()

    def add_bookmark(self):
        self.current_path = self.address_bar.get_current_path()  # Get the current path from address bar
        print("current_path: ", self.current_path)
        if self.current_path:
            folder_name = self.current_path.split("\\")[-1][:16]  # Get the last part of the path and crop to 16 characters
            if folder_name not in self.bookmarks:
                self.bookmarks[folder_name] = self.current_path
                self.refresh_bookmarks()
            else:
                print(f"Bookmark '{folder_name}' already exists.")

    def remove_bookmark(self, folder_name):
        if folder_name in self.bookmarks:
            del self.bookmarks[folder_name]
            self.refresh_bookmarks()

    def refresh_bookmarks(self):
        # Clear current bookmarks display
        for widget in self.bookmark_list_frame.winfo_children():
            widget.destroy()

        # Display the updated list of bookmarks
        for folder_name, path in self.bookmarks.items():
            bookmark_frame = ttk.Frame(self.bookmark_list_frame)
            bookmark_frame.pack(fill=tk.X, pady=2)

            bookmark_label = ttk.Label(bookmark_frame, text=folder_name)
            bookmark_label.pack(side=tk.LEFT, padx=5)

            remove_button = ttk.Button(bookmark_frame, text="X", width=2, command=lambda fn=folder_name: self.remove_bookmark(fn))
            remove_button.pack(side=tk.RIGHT, padx=5)

            # Bind double-click to navigate to the bookmarked path
            bookmark_label.bind("<Double-1>", lambda e, p=path: self.on_bookmark_selected(p))

    def on_bookmark_selected(self, path):
        print(f"Bookmark selected: {path}")
        self.address_bar.update_address(path)
        # Here, trigger the update of the main view as well
