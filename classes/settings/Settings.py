""" SETTINGS CONFIG, AN ESSENTIAL FILE FOR BASIC NEEDS """
import json

from panda3d.core import loadPrcFileData, CullBinManager

from classes.globals import Globals as G

# Change the directory to the project path in the settings
json_settings = json.loads(open(G.SETTINGS_JSON).read())
RESOURCES = json_settings['project-path'] + "resources/"

loadPrcFileData("", f"model-path {RESOURCES}")
loadPrcFileData("", f"window-title {G.WINDOW_TITLE}")
loadPrcFileData("", f"icon-filename {RESOURCES}windows/{G.ICON_FILENAME}")

loadPrcFileData("", f"depth-bits {G.BITS}")
loadPrcFileData("", f"framebuffer-multisample {json_settings[G.FRAMEBUFFER_MULTISAMPLE]}")
loadPrcFileData("", f"multisamples {json_settings[G.MULTISAMPLES]}")
loadPrcFileData("", f"win-size {json_settings[G.SCREEN_RES]}")
loadPrcFileData("", f"undecorated {json_settings[G.BORDERLESS]}")
loadPrcFileData("", f"show-frame-rate-meter {json_settings[G.FPS_METER]}")

# Shadow bin for drop shadows
cbm = CullBinManager.getGlobalPtr()
cbm.addBin('shadow', CullBinManager.BTBackToFront, 20)