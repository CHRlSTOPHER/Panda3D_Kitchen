ACTOR_DATA = """
class Actors():

    def __init__(self):
        pass
"""

DIALOGUE_DATA = """
class Dialogue():

    def __init__(self):
        pass
"""

MAIN_DATA = """from .Actors import Actors
from .Dialogue import Dialogue
from .Music import Music
from .ParticleEffects import ParticleEffects
from .Props import Props
from .Scenes import Scenes
from .Sounds import Sounds
from .TextBoxes import TextBoxes
from .Textures import Textures


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
        pass
"""

PARTICLE_DATA = """
class ParticleEffects():

    def __init__(self):
        pass
"""

PROP_DATA = """
class Props():

    def __init__(self):
        pass
"""

SCENE_DATA = """
class Scenes():

    def __init__(self):
        pass
"""

SOUND_DATA = """
class Sounds():

    def __init__(self):
        pass
"""

TEXTBOX_DATA = """
class TextBoxes():

    def __init__(self):
        pass
"""

TEXTURE_DATA = """
class Textures():

    def __init__(self):
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