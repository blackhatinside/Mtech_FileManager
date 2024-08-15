# FileManager/layer2_navigation/navigation_buttons.py

import tkinter as tk
from tkinter import ttk
import os

class NavigationButtons(ttk.Frame):
    def __init__(self, parent, home_directory):
        super().__init__(parent)

        self.history = []  # List to keep track of visited directories
        self.current_index = -1  # To track the current position in the history
        self.home_directory = home_directory  # Set the home directory

        # Backward Button
        self.back_button = ttk.Button(self, text="<", command=self.go_backward, width=2, padding=5)
        self.back_button.pack(side=tk.LEFT)
        
        # Forward Button
        self.forward_button = ttk.Button(self, text=">", command=self.go_forward, width=2, padding=5)
        self.forward_button.pack(side=tk.LEFT)
        
        # Previous Level Directory Button
        self.up_button = ttk.Button(self, text="↑", command=self.go_up_one_level, width=2, padding=5)
        self.up_button.pack(side=tk.LEFT)
        
        # Home Directory Button
        self.home_button = ttk.Button(self, text="⌂", command=self.go_home, width=2, padding=5)
        self.home_button.pack(side=tk.LEFT)
        
        # Disable buttons initially
        self.update_buttons_state()

    def go_backward(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.navigate_to(self.history[self.current_index])
        self.update_buttons_state()

    def go_forward(self):
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            self.navigate_to(self.history[self.current_index])
        self.update_buttons_state()

    def go_up_one_level(self):
        current_path = self.history[self.current_index]
        parent_path = os.path.dirname(current_path)
        if os.path.exists(parent_path):
            self.add_to_history(parent_path)
            self.navigate_to(parent_path)
        self.update_buttons_state()

    def go_home(self):
        self.add_to_history(self.home_directory)
        self.navigate_to(self.home_directory)
        self.update_buttons_state()

    def add_to_history(self, path):
        # If navigating to a new path, truncate the forward history
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]
        self.history.append(path)
        self.current_index = len(self.history) - 1

    def navigate_to(self, path):
        print(f"Navigating to: {path}")
        # Code to update the displayed content according to the path
        # For now, we just print the path

    def update_buttons_state(self):
        # Disable/Enable Backward button
        if self.current_index > 0:
            self.back_button.config(state=tk.NORMAL)
        else:
            self.back_button.config(state=tk.DISABLED)

        # Disable/Enable Forward button
        if self.current_index < len(self.history) - 1:
            self.forward_button.config(state=tk.NORMAL)
        else:
            self.forward_button.config(state=tk.DISABLED)

        # Disable/Enable Up button
        current_path = self.history[self.current_index] if self.current_index >= 0 else None
        if current_path and os.path.dirname(current_path) != current_path:
            self.up_button.config(state=tk.NORMAL)
        else:
            self.up_button.config(state=tk.DISABLED)

        # Home button is always enabled
