import importlib

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
        self.actors = Actors.Actors(self.master_editor)
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

