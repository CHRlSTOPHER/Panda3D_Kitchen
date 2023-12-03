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

loadPrcFileData("", f"depth-bits {json_settings['bits']}")
loadPrcFileData("", f"framebuffer-multisample {json_settings['framebuffer-multisample']}")
loadPrcFileData("", f"multisamples {json_settings['multisamples']}")
loadPrcFileData("", f"win-size {json_settings['screen_resolution']}")
loadPrcFileData("", f"show-frame-rate-meter {json_settings['show_fps_meter']}")

# Shadow bin for drop shadows
cbm = CullBinManager.getGlobalPtr()
cbm.addBin('shadow', CullBinManager.BTBackToFront, 20)