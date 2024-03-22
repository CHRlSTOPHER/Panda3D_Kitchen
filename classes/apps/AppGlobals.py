ACTOR_DATA = """
class Actors():

    def __init__(self, _render, editor):
        print('loading actors')
        self.render = _render
        self.editor = editor
    
    def cleanup(self):
        pass
"""

DIALOGUE_DATA = """
class Dialogue():

    def __init__(self):
        print('loading dialogue')
    
    def cleanup(self):
        pass
"""

MAIN_DATA = """import importlib

from direct.showbase.DirectObject import DirectObject
from panda3d.core import Camera, NodePath, MouseWatcher

from classes.editors.MasterEditor import MasterEditor

import Actors
import Dialogue
import Music
import ParticleEffects
import Props
import Scenes
import Sounds
import TextBoxes
import Textures

module_list = [Actors, Dialogue, Music, ParticleEffects, Props,
              Scenes, Sounds, TextBoxes, Textures]
DISPLAY_REGION = [.1616, .8283, .1616, .8283]


class Main(DirectObject):

    def __init__(self):
        self.classes = []
        self.make_display_region()

        self.editor = MasterEditor([camera, self.camera], self.mouse_watcher,
                                   self.region, self.render)

        self.load_project()
        self.accept('r', self.reload_modules)

    def make_display_region(self):
        self.region = base.win.makeDisplayRegion(*DISPLAY_REGION)

        camera_node = Camera('MainCam')
        self.camera = NodePath(camera_node)
        self.region.setCamera(self.camera)

        self.render = NodePath('render2')  # the string parameter is important
        self.camera.reparent_to(self.render)

        self.mouse_watcher = MouseWatcher()
        base.mouseWatcher.get_parent().attach_new_node(self.mouse_watcher)
        self.mouse_watcher.set_display_region(self.region)

        # Fix display region aspect ratio. Otherwise, it warps terribly.
        aspect_ratio = base.get_aspect_ratio()
        self.camera.node().get_lens().set_aspect_ratio(aspect_ratio)

    def load_project(self):
        self.actors = Actors.Actors(self.render, self.editor)
        self.dialogue = Dialogue.Dialogue()
        self.music = Music.Music()
        self.particle_effects = ParticleEffects.ParticleEffects()
        self.props = Props.Props(self.render, self.editor)
        self.scenes = Scenes.Scenes()
        self.sounds = Sounds.Sounds()
        self.text_boxes = TextBoxes.TextBoxes()
        self.textures = Textures.Textures()
        self.classes = [
            self.actors, self.dialogue, self.music, self.particle_effects,
            self.props, self.scenes, self.sounds, self.text_boxes, self.textures
        ]

    def reload_modules(self):
        for _class in self.classes:
            _class.cleanup()
        for module in module_list:
            importlib.reload(module)
        self.load_project()
"""

MUSIC_DATA = """
class Music():

    def __init__(self):
        print('loading music')
    
    def cleanup(self):
        pass
"""

PARTICLE_DATA = """
class ParticleEffects():

    def __init__(self):
        print('loading particle effects')

    def cleanup(self):
        pass
"""

PROP_DATA = """
class Props():

    def __init__(self, _render, editor):
        print('loading props')
        self.render = _render
        self.editor = editor

        # temporary test prop
        env = loader.load_model('environment.egg')
        env.reparent_to(self.render)

        panda = loader.load_model('panda.egg')
        panda.reparent_to(self.render)
    
    def cleanup(self):
        pass
"""

SCENE_DATA = """
class Scenes():

    def __init__(self):
        print('loading scenes')
    
    def cleanup(self):
        pass
"""

SOUND_DATA = """
class Sounds():

    def __init__(self):
        print('loading sounds')
    
    def cleanup(self):
        pass
"""

TEXTBOX_DATA = """
class TextBoxes():

    def __init__(self):
        print('loading text boxes')
    
    def cleanup(self):
        pass
"""

TEXTURE_DATA = """
class Textures():

    def __init__(self):
        print('loading textures')
    
    def cleanup(self):
        pass
"""

FILE_DATA = {
    "Actors": ACTOR_DATA,
    "Dialogue": DIALOGUE_DATA,
    "Main": MAIN_DATA,
    "Music": MUSIC_DATA,
    "ParticleEffects": PARTICLE_DATA,
    "Props": PROP_DATA,
    "Scenes": SCENE_DATA,
    "Sounds": SOUND_DATA,
    "TextBoxes": TEXTBOX_DATA,
    "Textures": TEXTURE_DATA
}