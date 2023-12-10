"""
Toon from Toontown. WIP
"""
from direct.actor.Actor import Actor

from .AutoWalker import AutoWalker
from classes.globals import Globals as G
from . import ToonGlobals as TG

COLORS = TG.COLORS


class Toon(Actor, AutoWalker):

    def __init__(self, parent, gender='m', toon_name="~Toon",
                 head='dss', head_c=0,
                 torso='s', shirt_t=0, shirt_c=0,
                 sleeve_t=0, sleeve_c=0, arm_c=0, glove_c=0,
                 legs='s', leg_c=0, bottom='shorts', bottom_t=0, bottom_c=0):
        self.lod = 1000
        self.gender = gender
        self.toon_name = toon_name
        self.species = head[0]

        self.head = head
        self.head_c = head_c
        self.forehead = head[1]
        self.cheeks = head[2]

        self.torso = torso
        self.shirt_t = shirt_t
        self.shirt_c = shirt_c
        self.sleeve_t = sleeve_t
        self.sleeve_c = sleeve_c
        self.arm_c = arm_c
        self.glove_c = glove_c

        self.legs = legs
        self.leg_c = leg_c
        self.bottom = bottom
        self.bottom_t = bottom_t
        self.bottom_c = bottom_c

        self.assemble_toon()
        self.set_name(toon_name)
        self.reparent_to(parent)

    def assemble_toon(self, actor=None):
        Actor.__init__(self, actor)
        self.load_legs()
        self.load_torso()
        self.load_head()
        self.load_toon_anims(self.legs, TG.LEGS)
        self.load_toon_anims(self.torso, TG.TORSO)
        # self.load_toon_anims(self.head, TG.HEAD)
        self.loop("neutral")

    def load_legs(self):
        model_string = G.CHAR_3 + TG.TOON_MODEL_FILE.format(
            self.legs, self.bottom, TG.LEGS, self.lod) + G.BAM
        self.load_model(model_string, TG.LEGS)
        self.set_leg_color()
        self.hide_shoes()

    def load_torso(self):
        model_string = G.CHAR_3 + TG.TOON_MODEL_FILE.format(
            self.torso, self.bottom, TG.TORSO, self.lod) + G.BAM
        self.load_model(model_string, TG.TORSO)
        self.attach(TG.TORSO, TG.LEGS, TG.JOINT_HIPS)
        self.set_shirt_textures(self.shirt_t, self.sleeve_t)
        self.set_bottom_texture(self.bottom_t)

        arm_color, glove_color = [COLORS[self.arm_c], COLORS[self.glove_c]]
        self.find(f'**/{TG.NECK}').set_color(arm_color + (1,))
        self.find(f'**/{TG.ARMS}').set_color(arm_color + (1,))
        self.find(f'**/{TG.GLOVES}').set_color(glove_color + (1,))

    def load_head(self):
        pass

    def load_toon_anims(self, body_part_type, body_part):
        anim_dict = {}
        for phase_file, anims in TG.ANIMS.items():
            for anim in anims:
                anim_dict[anim] = G.CHAR_3 + TG.TOON_MODEL_FILE.format(
                    body_part_type, self.bottom, body_part, anim) + G.BAM
                    # "tt_a_chr_dg{}_{}_{}_{}"

        self.load_anims(anim_dict, body_part)

    def set_leg_color(self):
        color = TG.COLORS[self.leg_c] + (1,)
        for part in TG.LEG_PARTS:  # color legs
            self.find(f'**/{part}').set_color(color)

    def hide_shoes(self):
        for part in TG.SHOE_PARTS:
            self.find(f'**/{part}').hide()

    def set_shirt_textures(self, shirt_tex_index, sleeves_tex_index):
        shirt_tex = loader.load_texture(TG.SHIRTS_TEX[shirt_tex_index])
        self.find(f'**/{TG.TORSO_TOP}').set_texture(shirt_tex, 1)
        sleeve_tex = loader.load_texture(TG.SLEEVES_TEX[sleeves_tex_index])
        self.find(f'**/{TG.SLEEVES}').set_texture(sleeve_tex, 1)

    def set_bottom_texture(self, bottom_tex_index):
        if self.bottom == TG.SHORTS:
            bottom_tex = loader.load_texture(TG.SHORTS_TEX[bottom_tex_index])
        elif self.bottom == TG.SKIRT:
            bottom_tex = loader.load_texture(TG.SKIRT_TEX[bottom_tex_index])

        self.find(f'**/{TG.TORSO_BOTTOM}').set_texture(bottom_tex, 1)