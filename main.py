# FileManager/main.py

import tkinter as tk
from tkinter import ttk, messagebox
import os
from layer1_tab_bar.tab_bar import TabBar
from layer2_navigation.navigation_buttons import NavigationButtons
from layer2_navigation.address_bar import AddressBar
from layer1_tab_bar.search_bar import SearchBar
from layer3_ribbon.ribbon import Ribbon
from layer4_main_view.navigation_pane import NavigationPane
from layer4_main_view.main_view import MainView
from navigation_manager import NavigationManager

class FileManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Manager")
        self.geometry("1000x600")

        # Set the initial directory
        self.initial_directory = os.path.abspath(os.path.dirname(__file__))  # Start in the current directory

        # Initialize NavigationManager with initial path
        self.navigation_manager = NavigationManager()

        # Create frames for different layers
        tab_frame = self.create_frame()
        separator1 = self.create_separator()

        nav_frame = self.create_frame()
        separator2 = self.create_separator()

        ribbon_frame = self.create_frame()
        separator3 = self.create_separator()

        content_frame = self.create_frame(fill=tk.BOTH, expand=True)

        # Initialize TabBar (Layer 1)
        self.tab_bar = TabBar(tab_frame)

        # Initialize MainView (Layer 4) early since it's needed by SearchBar
        self.main_view = MainView(content_frame, self.navigation_manager)

        # Initialize AddressBar (Layer 2) and NavigationButtons (Layer 2)
        self.address_bar = AddressBar(
            nav_frame,
            self.navigation_manager,
            self.initial_directory,
            on_path_change=lambda path: self.navigation_manager.navigate_to(path, 'address_bar')
        )

        self.navigation_buttons = NavigationButtons(nav_frame, self.navigation_manager)
        self.navigation_buttons.pack(side=tk.LEFT, fill=tk.X)
        self.address_bar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Initialize Search bar (Layer 2)
        self.search_bar = SearchBar(nav_frame, main_view=self.main_view)
        self.search_bar.pack(side=tk.RIGHT, padx=5, fill=tk.X)

        # Initialize Ribbon (Layer 3)
        self.ribbon = Ribbon(ribbon_frame, main_view=self.main_view)
        self.ribbon.pack(side=tk.TOP, fill=tk.X)

        # Initialize NavigationPane (Layer 4)
        self.navigation_pane = NavigationPane(
            content_frame,
            self.address_bar,
            navigation_manager=self.navigation_manager  # Add this parameter
        )
        self.navigation_pane.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=10, pady=5)

        # Pack MainView
        self.main_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Register callbacks with NavigationManager
        self.navigation_manager.register_callbacks(
            self.address_bar.update_address,
            self.main_view.load_directory,
            self.navigation_buttons.update_buttons_state
        )

        # Initialize with the starting directory
        self.navigation_manager.navigate_to(self.initial_directory)

    def create_frame(self, side=tk.TOP, fill=tk.X, expand=False):
        frame = ttk.Frame(self)
        frame.pack(side=side, fill=fill, expand=expand)
        return frame

    def create_separator(self, side=tk.TOP, fill=tk.X, pady=5, orient='horizontal'):
        separator = ttk.Separator(self, orient=orient)
        separator.pack(side=side, fill=fill)
        return separator

if __name__ == "__main__":
    app = FileManagerApp()
    app.mainloop()