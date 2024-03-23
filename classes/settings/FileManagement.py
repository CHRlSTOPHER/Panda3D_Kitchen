import tkinter as tk
from tkinter import filedialog

FILES_JSON = "json/files.json"

# Update the last project the user loaded in files.json.
def update_json_last_selected(folder_location, keyword):
    if folder_location == "":
        return # Don't replace the last project with an empty string.

    file = open(FILES_JSON, "r")
    line_data = file.readlines()
    lines = ""
    # update the last-project line to store the new project location.
    for line in line_data:
        if keyword in line:
            line = f'    "{keyword}": "{folder_location}"\n'
        lines += line

    # write the new line data to the file.
    file = open(FILES_JSON, "w")
    file.writelines(lines)
    file.close()

# Returns the full directory location and the location relative to resources.
def get_directory_and_resource_dir(initialdir=""):
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