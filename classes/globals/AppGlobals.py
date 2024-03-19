ACTOR_DATA = """
class Actors():

    def __init__(self):
        print('loading actors')
    
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


class Main(DirectObject):

    def __init__(self):
        self.classes = []
        self.master_editor = MasterEditor(mouse_lock=False)
        self.load_project()
        self.accept('r', self.reload_modules)

    def load_project(self):
        self.actors = Actors.Actors()
        self.dialogue = Dialogue.Dialogue()
        self.music = Music.Music()
        self.particle_effects = ParticleEffects.ParticleEffects()
        self.props = Props.Props()
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

    def __init__(self):
        print('loading props')
    
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