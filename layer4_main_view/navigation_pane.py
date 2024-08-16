# FileManager/layer4_main_view/navigation_pane.py

import tkinter as tk
from tkinter import ttk

class NavigationPane(ttk.Frame):
    def __init__(self, parent, address_bar):
        super().__init__(parent)
        self.bookmarks = []  # List to store bookmarks (paths)
        self.address_bar = address_bar  # Reference to the address bar

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
        current_path = self.address_bar.get_current_path()  # Get the current path from address bar
        if current_path:
            if current_path not in self.bookmarks:
                self.bookmarks.append(current_path)
                self.refresh_bookmarks()
            else:
                print(f"Bookmark '{current_path}' already exists.")

    def remove_bookmark(self, bookmark):
        if bookmark in self.bookmarks:
            self.bookmarks.remove(bookmark)
            self.refresh_bookmarks()

    def refresh_bookmarks(self):
        # Clear current bookmarks display
        for widget in self.bookmark_list_frame.winfo_children():
            widget.destroy()

        # Display the updated list of bookmarks
        for bookmark in self.bookmarks:
            bookmark_frame = ttk.Frame(self.bookmark_list_frame)
            bookmark_frame.pack(fill=tk.X, pady=2)

            bookmark_label = ttk.Label(bookmark_frame, text=bookmark)
            bookmark_label.pack(side=tk.LEFT, padx=5)

            remove_button = ttk.Button(bookmark_frame, text="X", width=2, command=lambda b=bookmark: self.remove_bookmark(b))
            remove_button.pack(side=tk.RIGHT, padx=5)

            # Bind double-click to navigate to the bookmarked path
            bookmark_label.bind("<Double-1>", lambda e, b=bookmark: self.on_bookmark_selected(b))

    def on_bookmark_selected(self, path):
        print(f"Bookmark selected: {path}")
        # Implement navigation to the selected path

# Usage in the main view
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Navigation Pane Test")
    root.geometry("300x400")

    # Dummy address bar for testing
    class DummyAddressBar:
        def get_current_path(self):
            return "C:\\path\\to\\current\\directory"  # Example path

    address_bar = DummyAddressBar()
    nav_pane = NavigationPane(root, address_bar=address_bar)
    nav_pane.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

