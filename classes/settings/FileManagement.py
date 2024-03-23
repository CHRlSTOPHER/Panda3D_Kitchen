import tkinter as tk
from tkinter import filedialog

from classes.settings import Globals as G

FILES_JSON = "json/files.json"

# Store the last selected directory for a project into the json file
def update_json_last_selected(folder_location, keyword):

    if folder_location == "":
        return # Don't replace the last project with an empty string.

    file_name = FILES_JSON
    file = open(file_name, "r")
    line_data = file.readlines()
    new_lines = ""
    # update the last-project line to store the new project location.
    for line in line_data:
        if keyword in line:
            line = f'    "{keyword}": "{folder_location}"\n'
        new_lines += line

    # write the new line data to the file.
    file = open(FILES_JSON, "w")
    file.writelines(new_lines)
    file.close()

# Returns the directory relative to resources and the file name.
def get_resource_dir_and_file_name(initialdir=""):
    root = tk.Tk()
    root.withdraw()  # Hide the tk box that pops up.
    file_location = filedialog.askopenfilename(initialdir=initialdir)
    root.destroy()

    # get the proper resource path from the file location
    add_folder = False
    resource_location = ""
    for folder in file_location.split("/"):
        if add_folder:
            resource_location += folder + "/"
        if folder == 'resources':
            add_folder = True

    item_name = folder.split('.')[0]

    return (resource_location[:-1], item_name)

# Adds or replaces new items into the database libraries.
def update_database_library(mode, resource_dir, filename):
    library = f"/{mode}Library.py"
    filepath = G.DATABASE_DIRECTORY + library
    file = open(filepath, "r")
    line_data = file.readlines()

    item_addition = f'    "{filename}": "{resource_dir}",\n'

    duplicate = False
    new_lines = ""
    for line in line_data:
        # Check if item is already in library. If so, replace.
        if f'"{filename}"' in line:
            duplicate = True
            line = item_addition
        new_lines += line

    # if no duplicate was found, add the item to the end of the list.
    if not duplicate:
        # remove the bracket
        new_lines = new_lines[:-1]
        new_lines += item_addition + "}"

    # write the new line data to the file.
    file = open(filepath, "w")
    file.writelines(new_lines)
    file.close()