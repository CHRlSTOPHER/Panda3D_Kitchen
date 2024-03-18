ACTOR_DATA = """
class Actors():

    def __init__(self):
        print('loading actors')
"""

DIALOGUE_DATA = """
class Dialogue():

    def __init__(self):
        print('loading dialogue')
"""

MAIN_DATA = """from Actors import Actors
from Dialogue import Dialogue
from Music import Music
from ParticleEffects import ParticleEffects
from Props import Props
from Scenes import Scenes
from Sounds import Sounds
from TextBoxes import TextBoxes
from Textures import Textures


class Main():

    def __init__(self):
        self.load_project()

    def load_project(self):
        self.actors = Actors()
        self.dialogue = Dialogue()
        self.music = Music()
        self.particle_effects = ParticleEffects()
        self.props = Props()
        self.scenes = Scenes()
        self.sounds = Sounds()
        self.text_boxes = TextBoxes()
        self.textures = Textures()
"""

MUSIC_DATA = """
class Music():

    def __init__(self):
        print('loading music')
"""

PARTICLE_DATA = """
class ParticleEffects():

    def __init__(self):
        print('loading particle effects')
"""

PROP_DATA = """
class Props():

    def __init__(self):
        print('loading props')
"""

SCENE_DATA = """
class Scenes():

    def __init__(self):
        print('loading scenes')
"""

SOUND_DATA = """
class Sounds():

    def __init__(self):
        print('loading sounds')
"""

TEXTBOX_DATA = """
class TextBoxes():

    def __init__(self):
        print('loading text boxes')
"""

TEXTURE_DATA = """
class Textures():

    def __init__(self):
        print('loading textures')
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