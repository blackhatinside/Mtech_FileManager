# FileManager/layer1_tab_bar/search_bar.py

import tkinter as tk
from tkinter import ttk

class SearchBar(ttk.Frame):
    def __init__(self, parent, main_view=None):
        super().__init__(parent, style='TFrame')
        self.main_view = main_view
        self.search_var = tk.StringVar()
        self.after_id = None  # For search delay

        # Create search box with placeholder
        self.search_box = ttk.Entry(self, textvariable=self.search_var, width=25)
        self.search_box.insert(0, "Search...")
        self.search_box.pack(side=tk.LEFT, padx=5, fill=tk.X)

        # Create search button container for better alignment
        button_frame = ttk.Frame(self)
        button_frame.pack(side=tk.LEFT, padx=2)

        # Add search button with simple text instead of emoji
        # self.search_button = ttk.Button(button_frame, text="Search", width=6,
        #                               command=self.perform_search)
        # self.search_button.pack(side=tk.LEFT)

        # Add clear button with simple text instead of emoji
        self.clear_button = ttk.Button(button_frame, text="X", width=2,
                                     command=self.clear_search)
        self.clear_button.pack(side=tk.LEFT, padx=2)

        # Configure tooltip for search box
        self.create_tooltip(self.search_box,
                          "Type to search files and folders\nResults update as you type")

        # Bind events
        self.search_box.bind("<FocusIn>", self.clear_default_text)
        self.search_box.bind("<FocusOut>", self.restore_default_text)
        self.search_box.bind("<KeyRelease>", self.on_search_change)
        self.search_box.bind("<Return>", lambda e: self.perform_search())
        self.search_var.trace('w', self.update_clear_button_state)

        # Initial state of clear button
        self.update_clear_button_state()

    def create_tooltip(self, widget, text):
        """Create tooltip for widgets"""
        def show_tooltip(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 20

            # Creates a toplevel window
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")

            label = ttk.Label(self.tooltip, text=text, background="#ffffe0",
                            relief='solid', borderwidth=1)
            label.pack()

        def hide_tooltip(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()

        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)

    def clear_default_text(self, event):
        """Clear placeholder text on focus"""
        if self.search_var.get().lower() == "search...":
            self.search_var.set("")
            self.search_box.config(foreground='black')

    def restore_default_text(self, event):
        """Restore placeholder text if empty"""
        if not self.search_var.get():
            self.search_var.set("Search...")
            self.search_box.config(foreground='gray')

    def clear_search(self):
        """Clear search and reset view"""
        self.search_var.set("")
        if self.main_view and hasattr(self.main_view, 'tree'):
            # Clear all highlights
            tree = self.main_view.tree
            for item in tree.get_children():
                tree.item(item, tags=())
            tree.tag_configure('match', background='white')
            tree.tag_configure('nomatch', background='white')

    def update_clear_button_state(self, *args):
        """Update clear button state based on search content"""
        if self.search_var.get() and self.search_var.get().lower() != "search...":
            self.clear_button.state(['!disabled'])
        else:
            self.clear_button.state(['disabled'])

    def perform_search(self):
        """Execute the search operation"""
        if not self.main_view:
            return

        search_term = self.search_var.get().lower()
        if search_term and search_term != "search...":
            self.highlight_matches(search_term)
            # Update UI to show search is active
            # self.search_button.config(text="Search", state='disabled')
            # self.after(500, lambda: self.search_button.config(state='normal'))

    def highlight_matches(self, search_term):
        """Highlight items in the main view that match the search term"""
        if not self.main_view or not hasattr(self.main_view, 'tree'):
            return

        tree = self.main_view.tree
        match_count = 0

        # Clear previous tags
        for item in tree.get_children():
            tree.item(item, tags=())

        # Search and highlight
        for item in tree.get_children():
            values = tree.item(item)['values']
            if any(search_term in str(value).lower() for value in values):
                tree.item(item, tags=('match',))
                match_count += 1
            else:
                tree.item(item, tags=('nomatch',))

        # Configure tags with smooth transition
        tree.tag_configure('match', background='light yellow')
        tree.tag_configure('nomatch', background='white')

        # Print match count (could be shown in UI)
        print(f"Found {match_count} matches for '{search_term}'")

    def on_search_change(self, event):
        """Delayed search as user types"""
        # Cancel previous delayed search if any
        if self.after_id:
            self.after_cancel(self.after_id)

        # Schedule new search with delay
        current_text = self.search_var.get().lower()
        if current_text and current_text != "search...":
            self.after_id = self.after(300, self.perform_search)  # Reduced delay to 300ms
        else:
            # Clear highlights if search is empty
            self.clear_search()