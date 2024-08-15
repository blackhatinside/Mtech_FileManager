# FileManager/main.py

import tkinter as tk
from layer1_tab_bar.tab_bar import TabBar
from layer2_navigation.navigation_buttons import NavigationButtons
from layer2_navigation.address_bar import AddressBar

class FileManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Manager")
        self.geometry("800x600")

        # Initialize and pack the TabBar (Layer 1)
        self.tab_bar = TabBar(self)
        self.tab_bar.pack(side=tk.TOP, fill=tk.X)

        # Set the home directory
        home_directory = "C:\\Cyberkid\\MyProjects\\My_Python\\tkinter\\FileManager"

        # Initialize and pack the NavigationButtons (Layer 2)
        self.navigation_buttons = NavigationButtons(self, home_directory)
        self.navigation_buttons.pack(side=tk.TOP, fill=tk.X)

        # Initialize and pack the AddressBar (Layer 2)
        self.address_bar = AddressBar(self, home_directory)
        self.address_bar.pack(side=tk.TOP, fill=tk.X)

if __name__ == "__main__":
    app = FileManagerApp()
    app.mainloop()