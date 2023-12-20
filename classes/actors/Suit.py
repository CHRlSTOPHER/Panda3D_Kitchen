"""
A Cog Actor. You can either pass a string through calling a suit key
from SuitGlobals's SUIT dict or pass your own custom cog list in.
"""
from direct.actor.Actor import Actor
from panda3d.core import OmniBoundingVolume

from .AutoWalker import AutoWalker
from classes.globals import Globals as G, SuitGlobals as SG


class Suit(Actor, AutoWalker):

    def __init__(self, suit, parent, skelecog=False, suit_name="~Suit"):
        self.suit = suit
        if isinstance(suit, str): # check if cog is NOT custom.
            suit = SG.SUITS[suit]
        self.suit_parent = parent

        self.skelecog = skelecog
        self.suit_name = suit_name
        self.suits = []

        self.body = suit[0]
        self.dept = suit[1]
        self.head_type = suit[2]
        self.hand_color = suit[3]
        self.head_texture = suit[4]
        self.scale = suit[5]

        # for flunky.
        self.left_eye = None
        self.right_eye = None
        self.glasses = None

        self.assemble_suit()

    def assemble_suit(self, actor=None):
        Actor.__init__(self, actor)
        self.load_suit()
        AutoWalker.__init__(self, self, speed=SG.AUTO_WALKER_SPEED)
        self.load_animations()
        self.load_health_meter()
        self.load_shadow()
        self.special_attributes()

        self.set_scale(self.scale)
        self.set_blend(frameBlend=True)
        self.node().set_bounds(OmniBoundingVolume())
        self.node().set_final(1)
        self.loop("neutral")
        self.reparent_to(self.suit_parent)
        self.set_name(self.suit_name)

        self.suits.append(self)

    def load_suit(self):
        # Load suit model.
        suit_model_path = G.CHAR_3_5 + f"suit{self.body}-mod" + G.BAM
        self.load_model(suit_model_path)
        self.find('**/hands').set_color(self.hand_color)

        # Load suit textures.
        for cloth, body_part in SG.COG_CLOTHING:
            suit_cloth_path = G.MAPS_3_5 + f"{self.dept}_{cloth}" + G.JPG
            clothing_texture = loader.load_texture(suit_cloth_path)
            self.find(f"**/{body_part}").set_texture(clothing_texture, 1)

        # Load head and apply a name flag.
        head_path = SG.HEAD_MODEL_PATH.format(self.body)
        self.head = loader.load_model(head_path).find(f'**/{self.head_type}')
        self.head.reparent_to(self.find('**/joint_head'))
        self.head.set_name(self.suit_name + f".find('**/{self.head_type}')")

        if self.head_texture:
            head_texture_path = G.MAPS_4 + SG.HEADS[self.suit] + G.JPG
            self.head.set_texture(loader.load_texture(head_texture_path), 1)

        for texture in self.head.find_all_textures():
            # This fixes face blur. 16 (power of 2) makes it nice and clean.
            texture.set_anisotropic_degree(16)

    def load_animations(self):
        anim_path_dict = SG.SUIT_ANIMS[self.body]
        anim_dict = {}
        for anim, phase_number in anim_path_dict.items():
            anim_path = SG.ANIM_PATH
            anim_dict[anim] = anim_path.format(phase_number, self.body, anim)
        self.load_anims(anim_dict)

    def load_health_meter(self):
        pass

    def load_shadow(self):
        pass

    def special_attributes(self):
        # Cold Caller head.
        if self.dept == 's' and self.head_type == 'coldcaller':
            self.head.set_color(SG.CC_COLOR)

        # Flunky glasses
        if self.head_type == "flunky" and not self.head_texture:
            head_path = SG.HEAD_MODEL_PATH.format(self.body)
            self.glasses = loader.load_model(head_path).find(SG.GLASSES)
            self.glasses.reparentTo(self.head)
            self.glasses.set_name(f"{self.suit_name}.glasses")

        # Has separate eye nodes.
        if (self.head_type == 'flunky' and not self.head_texture
        or self.head_type in SG.ALL_SEEING_HEADS):
            self.left_eye = self.head.find(SG.LEFT_EYE)
            self.right_eye = self.head.find(SG.RIGHT_EYE)
            self.left_eye.set_name(f"{self.suit_name}.left_eye")
            self.right_eye.set_name(f"{self.suit_name}.right_eye")

    def cleanup(self):
        self.cleanup_walker()