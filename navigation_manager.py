# FileManager/navigation_manager.py

import os
from tkinter import messagebox

class NavigationManager:
    def __init__(self):
        self.history = []
        self.current_index = -1
        self.max_history = 50  # Maximum history entries

        # Callbacks to be registered
        self.address_bar_callback = None
        self.main_view_callback = None
        self.navigation_buttons_callback = None

    def register_callbacks(self, address_bar_cb, main_view_cb, nav_buttons_cb):
        """Register callbacks for navigation events"""
        self.address_bar_callback = address_bar_cb
        self.main_view_callback = main_view_cb
        self.navigation_buttons_callback = nav_buttons_cb

    def navigate_to(self, path, source=None):
        """
        Central navigation method that coordinates all navigation actions
        source: Identifies which component initiated the navigation
        """
        try:
            # Validate path
            if not os.path.exists(path):
                raise FileNotFoundError(f"Path does not exist: {path}")
            if not os.path.isdir(path):
                raise NotADirectoryError(f"Path is not a directory: {path}")
            if not os.access(path, os.R_OK):
                raise PermissionError(f"Cannot access directory: {path}")

            # Add to history if it's a new path
            if not self.history or path != self.history[self.current_index]:
                # Truncate forward history if navigating from middle
                if self.current_index < len(self.history) - 1:
                    self.history = self.history[:self.current_index + 1]

                # Add new path
                self.history.append(path)
                self.current_index = len(self.history) - 1

                # Trim history if it exceeds max size
                if len(self.history) > self.max_history:
                    self.history = self.history[-self.max_history:]
                    self.current_index = len(self.history) - 1

            # Always update all components, regardless of source
            if self.address_bar_callback:
                self.address_bar_callback(path)
            if self.main_view_callback:
                self.main_view_callback(path)
            if self.navigation_buttons_callback:
                self.navigation_buttons_callback()

            return True

        except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
            print(f"Navigation error: {str(e)}")
            messagebox.showerror("Navigation Error", str(e))
            return False
        except Exception as e:
            print(f"Unexpected error during navigation: {str(e)}")
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")
            return False

    def can_go_back(self):
        return self.current_index > 0

    def can_go_forward(self):
        return self.current_index < len(self.history) - 1

    def go_back(self):
        if self.can_go_back():
            self.current_index -= 1
            self.navigate_to(self.history[self.current_index], 'nav_buttons')
            return True
        return False

    def go_forward(self):
        if self.can_go_forward():
            self.current_index += 1
            self.navigate_to(self.history[self.current_index], 'nav_buttons')
            return True
        return False

    def get_current_path(self):
        if self.history and self.current_index >= 0:
            return self.history[self.current_index]
        return None