from Actors import Actors
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
