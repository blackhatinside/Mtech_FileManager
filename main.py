# FileManager/main.py

import tkinter as tk
from tkinter import ttk
from layer1_tab_bar.tab_bar import TabBar
from layer2_navigation.navigation_buttons import NavigationButtons
from layer2_navigation.address_bar import AddressBar
from layer1_tab_bar.search_bar import SearchBar


class FileManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Manager")
        self.geometry("800x600")

        # Set the home directory
        home_directory = "C:\\Cyberkid\\MyProjects\\My_Python\\tkinter\\FileManager"

        # Create frames for different layers
        tab_frame = ttk.Frame(self)
        tab_frame.pack(side=tk.TOP, fill=tk.X)

        nav_frame = ttk.Frame(self)
        nav_frame.pack(side=tk.TOP, fill=tk.X)

        # Initialize TabBar (Layer 1), Address Bar (Layer 1), NavigationButtons (Layer 2)
        self.tab_bar = TabBar(tab_frame)

        # Initialize Navigation bar
        self.address_bar = AddressBar(nav_frame, initial_path=home_directory)
        self.navigation_buttons = NavigationButtons(nav_frame, home_directory, self.address_bar.update_address)

        self.navigation_buttons.pack(side=tk.LEFT, fill=tk.X)
        self.address_bar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Initialize Search bar
        self.search_bar = SearchBar(nav_frame)
        self.search_bar.pack(side=tk.RIGHT, padx=5, fill=tk.X)

if __name__ == "__main__":
    app = FileManagerApp()
    app.mainloop()
