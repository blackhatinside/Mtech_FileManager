# FileManager/layer1_tab_bar/tab_bar.py

import tkinter as tk
from tkinter import ttk
from .tab_button import TabButton

class TabBar(ttk.Frame):
    MAX_TABS = 8  # Define the maximum number of tabs

    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side=tk.TOP, fill=tk.X)

        self.tabs_frame = tk.Frame(self)
        self.tabs_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Add New Tab Button
        self.add_tab_button = ttk.Button(self, text="+", command=self.add_new_tab, width=2, padding=5)
        self.add_tab_button.pack(side=tk.LEFT, padx=5)

        # Placeholder for storing tabs with unique IDs
        self.open_tabs = {}

        # Update the state of the add tab button
        self.update_add_tab_button_state()

    def add_new_tab(self):
        if len(self.open_tabs) < self.MAX_TABS:
            new_tab = TabButton(self.tabs_frame, self.remove_tab)
            new_tab.pack(side=tk.LEFT)
            self.open_tabs[new_tab.get_tab_id()] = new_tab
            self.update_add_tab_button_state()
        else:
            print("Add New Tab button clicked but maximum tabs reached.")

    def remove_tab(self, tab_id):
        print(f"Attempting to remove tab: {tab_id}. Current tab count: {len(self.open_tabs)}")
        if tab_id in self.open_tabs:
            self.open_tabs[tab_id].destroy()
            del self.open_tabs[tab_id]
            print(f"Tab removed: {tab_id}. Total tabs now: {len(self.open_tabs)}")
        else:
            print(f"Tab {tab_id} not found.")
        self.update_add_tab_button_state()
    
    def update_add_tab_button_state(self):
        """ Enable or disable the add tab button based on the number of open tabs """
        current_tab_count = len(self.open_tabs)
        if current_tab_count >= self.MAX_TABS:
            self.add_tab_button.config(state=tk.DISABLED)
            print(f"Maximum tabs reached. Add New Tab button is DISABLED.")
        else:
            self.add_tab_button.config(state=tk.NORMAL)
            print(f"Add New Tab button is ENABLED. Current tab count: {current_tab_count}")
