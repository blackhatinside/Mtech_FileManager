# FileManager/layer4_main_view/navigation_pane.py

import tkinter as tk
from tkinter import ttk, messagebox

class NavigationPane(ttk.Frame):
    def __init__(self, parent, address_bar, navigation_manager=None):
        super().__init__(parent)
        # Create a custom style for clickable labels
        self.style = ttk.Style()
        self.style.configure("Clickable.TLabel", foreground="blue", cursor="hand2")
        self.style.configure("ClickableHover.TLabel", foreground="dark blue", cursor="hand2")
        self.bookmarks = {}  # Dictionary to store bookmarks (folder name -> path)
        self.address_bar = address_bar  # Reference to the address bar
        self.navigation_manager = navigation_manager  # Reference to the navigation manager
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
        if self.current_path:
            folder_name = self.current_path.split("\\")[-1][:16]  # Get the last part of the path and crop to 16 characters
            if folder_name not in self.bookmarks:
                self.bookmarks[folder_name] = self.current_path
                self.refresh_bookmarks()
            else:
                messagebox.showinfo("Bookmark Exists", f"Bookmark '{folder_name}' already exists.")

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

            # Create a clickable label instead of button
            bookmark_label = ttk.Label(
                bookmark_frame,
                text=folder_name,
                style="Clickable.TLabel"
            )
            bookmark_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

            # Bind click and hover events
            bookmark_label.bind('<Button-1>', lambda e, p=path: self.navigate_to_bookmark(p))
            bookmark_label.bind('<Enter>', lambda e, label=bookmark_label:
                              label.configure(style="ClickableHover.TLabel"))
            bookmark_label.bind('<Leave>', lambda e, label=bookmark_label:
                              label.configure(style="Clickable.TLabel"))

            remove_button = ttk.Button(
                bookmark_frame,
                text="×",  # Using × instead of X for a cleaner look
                width=2,
                command=lambda fn=folder_name: self.remove_bookmark(fn)
            )
            remove_button.pack(side=tk.RIGHT, padx=5)

            # Add tooltip showing full path
            self.create_tooltip(bookmark_label, path)

    def navigate_to_bookmark(self, path):
        """Navigate to the bookmarked path using NavigationManager"""
        if self.navigation_manager:
            success = self.navigation_manager.navigate_to(path, source='bookmarks')
            if not success:
                messagebox.showerror(
                    "Navigation Error",
                    f"Could not navigate to:\n{path}\nThe path may no longer exist."
                )
        else:
            messagebox.showerror(
                "Navigation Error",
                "Navigation manager not initialized."
            )

    def create_tooltip(self, widget, text):
        """Create tooltip for bookmark buttons"""
        def show_tooltip(event):
            x = widget.winfo_rootx() + widget.winfo_width() + 5
            y = widget.winfo_rooty()

            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")

            label = ttk.Label(
                self.tooltip,
                text=text,
                background="#ffffe0",
                relief='solid',
                borderwidth=1
            )
            label.pack()

        def hide_tooltip(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()

        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)