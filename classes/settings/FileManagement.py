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
            line = f'    "{keyword}": "{folder_location}",\n'
        lines += line

    # write the new line data to the file.
    file = open(FILES_JSON, "w")
    file.writelines(lines)
    file.close()