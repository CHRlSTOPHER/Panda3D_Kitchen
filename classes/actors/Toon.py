"""
Loads a Toon from Toontown.
"""
from direct.actor.Actor import Actor
from panda3d.core import OmniBoundingVolume

from .AutoWalker import AutoWalker
from classes.globals import Globals as G, ToonGlobals as TG
from .ToonHead import ToonHead

ALPHA = (1,)

class Toon(Actor, ToonHead, AutoWalker):

    def __init__(self, parent, gender='m', toon_name="~Toon", lod=1000,
                 head='dss', torso='s', legs='s', bottom='shorts',
                 shirt_t=0, sleeve_t=0, bottom_t=0,
                 head_color=41, shirt_color=41, sleeve_color=41,
                 arm_color=41, glove_color=41, leg_color=41, bottom_color=41,
                 names=True):
        self.gender = gender
        self.toon_name = toon_name
        self.lod = lod

        self.head = head
        self.torso = torso
        self.legs = legs
        self.bottom = bottom

        self.shirt_t = shirt_t
        self.sleeve_t = sleeve_t
        self.bottom_t = bottom_t

        colors = TG.TOON_COLORS
        self.head_c = colors[head_color] + ALPHA
        self.shirt_c = colors[shirt_color] + ALPHA
        self.sleeve_c = colors[sleeve_color] + ALPHA
        self.arm_c = colors[arm_color] + ALPHA
        self.glove_c = colors[glove_color] + ALPHA
        self.leg_c = colors[leg_color] + ALPHA
        self.bottom_c = colors[bottom_color] + ALPHA

        self.names = names
        self.species = head[0]
        self.forehead = head[1]
        self.muzzle = head[2]
        self.toon_head = None

        self.assemble_toon()
        self.set_name(toon_name)
        self.reparent_to(parent)

    def assemble_toon(self, actor=None):
        Actor.__init__(self, actor)
        self.load_legs()
        self.load_toon_anims(self.legs, TG.LEGS)

        self.load_torso()
        self.load_toon_anims(self.torso, TG.TORSO, self.bottom)
        self.apply_clothing_colors()

        ToonHead.__init__(self, self, self.head, self.head_c, self.lod,
                          gender=self.gender)
        self.attach(TG.HEAD, TG.TORSO, TG.JOINT_HEAD)
        if self.names:
            self.name_body_parts()

        AutoWalker.__init__(self, self, speed=15, run_anim="run", run_div=2.0)
        self.set_blend(frameBlend=True)
        self.node().set_bounds(OmniBoundingVolume())
        self.node().set_final(1)
        self.set_scale(TG.SCALE[self.species])
        self.loop("neutral")

    def load_legs(self):
        model_string = G.CHAR_3 + TG.TOON_MODEL_FILE.format(
            self.legs, 'shorts', TG.LEGS, self.lod) + G.BAM
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

    def load_toon_anims(self, body_part_type, body_part, bottom='shorts'):
        anim_dict = {}
        for phase_file, anims in TG.ANIMS.items():
            for anim in anims:
                phase_path = f"phase_{phase_file}/models/char/"
                anim_file = f"""{TG.TOON_MODEL_FILE.format(
                    body_part_type, bottom, body_part, anim)}"""
                anim_dict[anim] = phase_path + anim_file + G.BAM
                # "tt_a_chr_dg{}_{}_{}_{}"

        self.load_anims(anim_dict, body_part)

    def name_body_parts(self):
        head_nodeifier = '~.get_part("head")'
        self.get_part(TG.HEAD).set_name(f"{self.toon_name}{head_nodeifier}")
        # l and r eye are defined in ToonHead
        self.left_eye.set_name(f"{self.toon_name}.left_eye")
        self.right_eye.set_name(f"{self.toon_name}.right_eye")

    def set_leg_color(self):
        color = self.leg_c
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
        else:
            bottom_tex = loader.load_texture(TG.SKIRT_TEX[bottom_tex_index])

        self.find(f'**/{TG.TORSO_BOTTOM}').set_texture(bottom_tex, 1)

    def apply_clothing_colors(self):
        self.find(f'**/{TG.TORSO_TOP}').set_color(self.shirt_c)
        self.find(f'**/{TG.SLEEVES}').set_color(self.sleeve_c)
        self.find(f'**/{TG.TORSO_BOTTOM}').set_color(self.bottom_c)

        arm_color, glove_color = [self.arm_c, self.glove_c]
        self.find(f'**/{TG.NECK}').set_color(arm_color)
        self.find(f'**/{TG.ARMS}').set_color(arm_color)
        self.find(f'**/{TG.GLOVES}').set_color(glove_color)

    def cleanup_actor(self):
        self.cleanup_walker()
        self.delete()