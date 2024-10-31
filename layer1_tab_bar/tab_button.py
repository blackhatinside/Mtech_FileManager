# FileManager/layer1_tab_bar/tab_button.py

import tkinter as tk
from tkinter import ttk, simpledialog
import uuid  # for generating unique Tab IDs

class TabButton(ttk.Frame):
    def __init__(self, parent, remove_callback):
        super().__init__(parent)

        # Generate unique Tab ID
        self.tab_id = uuid.uuid4()
        self.remove_callback = remove_callback

        # Set initial tab label
        self.label_text = tk.StringVar(value="New Tab")

        # Label for the tab
        self.label = ttk.Label(self, textvariable=self.label_text)
        self.label.pack(side=tk.LEFT)

        # Close button
        close_button = ttk.Button(self, text="x", command=self.close_tab, width=2, padding=5)
        close_button.pack(side=tk.LEFT)

        # Bind double-click event to the label for renaming
        self.label.bind("<Double-1>", self.rename_tab)

    def close_tab(self):
        print(f"Closing tab: {self.tab_id}")
        self.remove_callback(self.tab_id)  # Notify the parent to remove the tab
        self.destroy()

    def rename_tab(self, event):
        old_name = self.label_text.get()
        print(f"Attempting to rename tab {self.tab_id} from {old_name}.")

        # Open a dialog box to get a new tab name
        new_name = simpledialog.askstring("Rename Tab", "Enter new tab name:", initialvalue=old_name)
        if new_name:
            self.label_text.set(new_name)
            print(f"Renamed tab from {old_name} to {new_name}.")

    def get_tab_id(self):
        """ Returns the unique Tab ID """
        return self.tab_id
