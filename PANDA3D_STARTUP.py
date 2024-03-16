"""
Make a new project. Load an existing project.
Move a project. Delete a project.
Start a side application like Make-a-Toon
"""
from direct.showbase.ShowBase import ShowBase


class Startup(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        base.disable_mouse()


project = Startup()
project.run()