# FileManager/layer2_navigation/navigation_buttons.py

import tkinter as tk
from tkinter import ttk, messagebox
import os

class NavigationButtons(ttk.Frame):
    def __init__(self, parent, navigation_manager):
        super().__init__(parent)
        self.navigation_manager = navigation_manager

        # Create buttons with tooltips
        self.back_button = self.create_button("<", self.go_backward, "Go back")
        self.forward_button = self.create_button(">", self.go_forward, "Go forward")
        self.up_button = self.create_button("↑", self.go_up_one_level, "Go up one level")
        self.home_button = self.create_button("⌂", self.go_home, "Go to home directory")

        # Initial button state update
        self.update_buttons_state()

    def create_button(self, text, command, tooltip):
        """Create a navigation button with tooltip"""
        btn = ttk.Button(self, text=text, command=command, width=2, padding=5)
        btn.pack(side=tk.LEFT, padx=2)
        self.create_tooltip(btn, tooltip)
        return btn

    def create_tooltip(self, widget, text):
        """Create tooltip for navigation buttons"""
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

    def go_backward(self):
        """Navigate to previous directory in history"""
        self.navigation_manager.go_back()
        self.update_buttons_state()

    def go_forward(self):
        """Navigate to next directory in history"""
        self.navigation_manager.go_forward()
        self.update_buttons_state()

    def go_up_one_level(self):
        """Navigate to parent directory"""
        current_path = self.navigation_manager.get_current_path()
        if current_path:
            parent_path = os.path.dirname(current_path)
            if os.path.exists(parent_path) and parent_path != current_path:
                self.navigation_manager.navigate_to(parent_path, 'nav_buttons')
        self.update_buttons_state()

    def go_home(self):
        """Navigate to home directory"""
        home_dir = os.path.expanduser("~")
        self.navigation_manager.navigate_to(home_dir, 'nav_buttons')
        self.update_buttons_state()

    def update_buttons_state(self):
        """Update the state of navigation buttons"""
        # Enable/disable back button
        self.back_button.config(
            state=tk.NORMAL if self.navigation_manager.can_go_back() else tk.DISABLED
        )

        # Enable/disable forward button
        self.forward_button.config(
            state=tk.NORMAL if self.navigation_manager.can_go_forward() else tk.DISABLED
        )

        # Enable/disable up button based on current path
        current_path = self.navigation_manager.get_current_path()
        if current_path:
            parent_path = os.path.dirname(current_path)
            # Enable up button if current path has a parent and is not at root
            self.up_button.config(
                state=tk.NORMAL if os.path.exists(parent_path) and
                                 parent_path != current_path else tk.DISABLED
            )
        else:
            self.up_button.config(state=tk.DISABLED)

        # Home button is always enabled
        self.home_button.config(state=tk.NORMAL)

        # Log current states for debugging
        self._log_button_states()

    def _log_button_states(self):
        """Log the current state of all navigation buttons"""
        states = {
            "Back": self.back_button.cget("state"),
            "Forward": self.forward_button.cget("state"),
            "Up": self.up_button.cget("state"),
            "Home": self.home_button.cget("state"),
        }
        print("Button States:", states)

    def handle_error(self, operation, error):
        """Central error handling for navigation operations"""
        error_msg = str(error)
        print(f"Error during {operation}: {error_msg}")
        messagebox.showerror(
            f"Navigation Error - {operation}",
            f"An error occurred while navigating:\n{error_msg}"
        )