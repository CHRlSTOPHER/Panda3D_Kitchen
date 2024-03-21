""" SETTINGS CONFIG, AN ESSENTIAL FILE FOR BASIC NEEDS """
import json

from panda3d.core import loadPrcFileData, CullBinManager

from classes.settings import Globals as G

# Change the directory to the project path in the settings
JSON_SETTINGS = json.loads(open(G.SETTINGS_JSON).read())
RESOURCES = JSON_SETTINGS['project-path'] + "resources/"

loadPrcFileData("", f"model-path {RESOURCES}")
loadPrcFileData("", f"window-title {G.WINDOW_TITLE}")
loadPrcFileData("", f"icon-filename {RESOURCES}editor/{G.ICON_FILENAME}")

loadPrcFileData("", f"depth-bits {G.BITS}")
loadPrcFileData("", "framebuffer-multisample"
                    f"{JSON_SETTINGS[G.FRAMEBUFFER_MULTISAMPLE]}")
loadPrcFileData("", f"multisamples {JSON_SETTINGS[G.MULTISAMPLES]}")
if JSON_SETTINGS[G.FULL_SCREEN]:
    loadPrcFileData("", "fullscreen #t")
loadPrcFileData("", f"win-size {JSON_SETTINGS[G.WINDOW_SIZE]}")
loadPrcFileData("", f"undecorated {JSON_SETTINGS[G.BORDERLESS]}")
loadPrcFileData("", f"show-frame-rate-meter {JSON_SETTINGS[G.FPS_METER]}")
loadPrcFileData("", "win-fixed-size 1")

# Shadow bin for drop shadows
cbm = CullBinManager.getGlobalPtr()
cbm.addBin('shadow', CullBinManager.BTBackToFront, 20)