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
def get_resource_and_filename(title="", initialdir="", multiple=False):
    root = tk.Tk()
    root.withdraw()  # Hide the tk box that pops up.
    if multiple:
        file_location = (filedialog.askopenfilenames(
                            title=title, initialdir=initialdir))
    else:
        file_location = filedialog.askopenfilename(
                            title=title, initialdir=initialdir)
    root.destroy()

    def get_resource_directory(file_location):
        # get the proper resource path from the file location
        add_folder = False
        resource_location = ""
        for folder in file_location.split("/"):
            if add_folder:
                resource_location += folder + "/"
            if folder == 'resources':
                add_folder = True

        return resource_location, folder

    if not multiple:
        resource_dir, file = get_resource_directory(file_location)
        item_name = file.split('.')[0]
        return item_name, resource_dir[:-1],

    items_names = []
    resource_directories = []
    for location in file_location:
        resource_dir, file = get_resource_directory(location)
        item_name = file.split('.')[0]
        resource_dir = resource_dir[:-1]
        items_names.append(item_name)
        resource_directories.append(resource_dir)

    return items_names, resource_directories

# Adds or replaces new items into the database libraries.
def update_database_library(mode, save_data, filename):
    library = f"/{mode}Library.py"
    filepath = G.DATABASE_DIRECTORY + library
    file = open(filepath, "r")
    line_data = file.readlines()

    duplicate = False
    new_lines = ""
    for line in line_data:
        # Check if item is already in library. If so, replace.
        if f'"{filename}"' in line:
            duplicate = True
            line = "    " + save_data
        new_lines += line

    # if no duplicate was found, add the item to the end of the list.
    if not duplicate:
        # remove the bracket
        new_lines = new_lines[:-1]
        new_lines += "    " + save_data + "}"

    # write the new line data to the file.
    file = open(filepath, "w")
    file.writelines(new_lines)
    file.close()