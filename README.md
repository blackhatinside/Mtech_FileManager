We are going to build a File Manager Project in Python. Here is the File Structure and Project Description:

``` ProjectFileStructure
FileManager/
│
├── layer1_tab_bar/
│   ├── __init__.py
│   ├── tab_bar.py
│   └── tab_button.py
│
├── layer2_navigation/
│   ├── __init__.py
│   ├── navigation_buttons.py
│   ├── address_bar.py
│   └── search_bar.py
│
├── layer3_ribbon/
│   ├── __init__.py
│   ├── ribbon.py
│   └── file_operations.py
│
├── layer4_main_view/
│   ├── __init__.py
│   ├── navigation_pane.py
│   ├── main_view.py
│   └── bookmarks.py
│
└── main.py
```

````
SRS:

Layer 1:
    Tab bar
        Should show all the open tabs
        Should have a "add new tab" button
        Should be able to rename Tabs
        Tabs should have unique name and ID
Layer 2:
    Navigation buttons
        Forward
        Backward
        Previous Level Directory
        Home Directory
    Address Bar
        Should have a Text box showing current path address
        Ability to move across valid directories using just path address and error handling if path invalid
    Search Bar
        Search for Files/Folders dynamically in current directory and highlight them
Layer 3:
    Ribbon:
        Should contain buttons for file management tools like Cut, Copy, Paste, Delete, Rename and Sort current directory
Layer 4:
    Navigation pane on Left with Bookmarks
        Ability to add and remove Bookmarks
    Main View displaying all files and folders using file icon and directory icon.
        Ability to bookmark folders
        Ability to view files
        Ability to navigate through files and folders
        Ability to view the details of files and folders
```