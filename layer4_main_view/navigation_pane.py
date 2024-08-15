# FileManager/layer4_main_view/navigation_pane.py

import tkinter as tk
from tkinter import ttk

class NavigationPane(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.bookmarks = []  # List to store bookmarks

        # Title and '+' button for Bookmarks
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=tk.X, padx=10, pady=5)

        title_label = ttk.Label(title_frame, text="Bookmarks")
        title_label.pack(side=tk.LEFT)

        add_button = ttk.Button(title_frame, text="+", width=2, command=self.add_bookmark)
        add_button.pack(side=tk.RIGHT)

        # Frame to hold the list of bookmarks
        self.bookmark_list_frame = ttk.Frame(self)
        self.bookmark_list_frame.pack(fill=tk.BOTH, expand=True, padx=10)

    def add_bookmark(self):
        # Placeholder for add bookmark functionality
        print("Add bookmark functionality will be implemented here")

    def remove_bookmark(self, bookmark):
        # Placeholder for remove bookmark functionality
        print(f"Remove bookmark functionality will be implemented for {bookmark}")

    def refresh_bookmarks(self):
        for widget in self.bookmark_list_frame.winfo_children():
            widget.destroy()

        for bookmark in self.bookmarks:
            bookmark_frame = ttk.Frame(self.bookmark_list_frame)
            bookmark_frame.pack(fill=tk.X, pady=2)

            bookmark_label = ttk.Label(bookmark_frame, text=bookmark)
            bookmark_label.pack(side=tk.LEFT, padx=5)

            remove_button = ttk.Button(bookmark_frame, text="-", width=2, 
                                       command=lambda b=bookmark: self.remove_bookmark(b))
            remove_button.pack(side=tk.RIGHT, padx=5)

# Usage in the main view
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Navigation Pane Test")
    root.geometry("300x400")

    nav_pane = NavigationPane(root)
    nav_pane.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
