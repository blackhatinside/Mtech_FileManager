# FileManager/main.py

import tkinter as tk
from tkinter import ttk
from layer1_tab_bar.tab_bar import TabBar
from layer2_navigation.navigation_buttons import NavigationButtons
from layer2_navigation.address_bar import AddressBar
from layer1_tab_bar.search_bar import SearchBar
from layer3_ribbon.ribbon import Ribbon
from layer4_main_view.navigation_pane import NavigationPane
from layer4_main_view.main_view import MainView

class FileManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Manager")
        self.geometry("1000x600")

        # Set the home directory
        self.home_directory = "C:\\Cyberkid\\MyProjects\\My_Python\\tkinter\\FileManager"

        # Create frames for different layers
        tab_frame = self.create_frame()
        separator1 = self.create_separator()  # between tab_frame and nav_frame

        nav_frame = self.create_frame()
        separator2 = self.create_separator()  # between nav_frame and ribbon_frame

        ribbon_frame = self.create_frame()
        separator3 = self.create_separator()

        content_frame = self.create_frame(fill=tk.BOTH, expand=True)

        # Initialize TabBar (Layer 1)
        self.tab_bar = TabBar(tab_frame)

        # Define a method to synchronize the address bar with navigation buttons
        def address_bar_changed(new_path):
            self.navigation_buttons.update_from_address_bar(new_path)
            # self.navigation_pane.update_from_address_bar(new_path)
            self.main_view.load_directory(new_path)  # Update the Main View

        def update_main_view(new_path):
            self.main_view.load_directory(new_path)

        # Initialize AddressBar (Layer 2) and NavigationButtons (Layer 2)
        self.address_bar = AddressBar(nav_frame, initial_path=self.home_directory, on_path_change=address_bar_changed)
        self.navigation_buttons = NavigationButtons(nav_frame, self.home_directory, self.address_bar.update_address, update_main_view)
        self.navigation_buttons.pack(side=tk.LEFT, fill=tk.X)
        self.address_bar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Initialize Search bar (Layer 2)
        self.search_bar = SearchBar(nav_frame)
        self.search_bar.pack(side=tk.RIGHT, padx=5, fill=tk.X)

        # Initialize Ribbon (Layer 3)
        self.ribbon = Ribbon(ribbon_frame)
        self.ribbon.pack(side=tk.TOP, fill=tk.X)

        # Initialize NavigationPane (Layer 4)
        self.navigation_pane = NavigationPane(content_frame, self.address_bar, on_path_change=address_bar_changed)
        self.navigation_pane.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=10, pady=5)

        # Initialize MainView (Layer 4)
        self.main_view = MainView(content_frame)
        self.main_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

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
