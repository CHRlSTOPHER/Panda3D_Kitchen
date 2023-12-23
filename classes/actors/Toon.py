"""
Loads a Toon from Toontown.
"""
from direct.actor.Actor import Actor
from panda3d.core import OmniBoundingVolume

from .AutoWalker import AutoWalker
from classes.globals import Globals as G, ToonGlobals as TG
from classes.globals.ToonColors import ToonColors
from classes.physics.Ragdoll import Ragdoll
from classes.physics.BulletTest import BulletTest
from .ToonHead import ToonHead

ALPHA = (1,)

ROOT = 0
PARENT = 1
# Parent joints should always be listed first.
JOINT_HIERARCHY = {
    # TG.HEAD: [], # might add dog options later...
    # TG.TORSO: [
    #
    #     '0def_spineB', '1def_cageA', '2def_cageB',
    #     '3def_left_shoulder', '4def_left_elbow', '5def_left_wrist',
    #     '3def_right_shoulder', '4def_right_elbow', '5def_right_wrist',
    #     '3def_head'
    # ],
    TG.LEGS: [
        '0joint_hips',

        '1def_left_hip', '2def_left_knee',
        '3def_left_ankle', '4def_left_ball',

        '1def_right_hip', '2def_right_knee',
        '3def_right_ankle', '4def_right_ball',
    ]
}


class Toon(Actor, ToonHead, AutoWalker, Ragdoll):

    def __init__(self, parent, gender='m', toon_name="~Toon", lod=1000,
                 head='dss', torso='s', legs='s', bottom='shorts',
                 shirt_t=0, sleeve_t=0, bottom_t=0,
                 head_color=ToonColors.WHITE,
                 shirt_color=ToonColors.WHITE, sleeve_color=ToonColors.WHITE,
                 arm_color=ToonColors.WHITE, glove_color=ToonColors.WHITE,
                 leg_color=ToonColors.WHITE, bottom_color=ToonColors.WHITE):
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

        self.head_c = head_color.value + ALPHA
        self.shirt_c = shirt_color.value + ALPHA
        self.sleeve_c = sleeve_color.value + ALPHA
        self.arm_c = arm_color.value + ALPHA
        self.glove_c = glove_color.value + ALPHA
        self.leg_c = leg_color.value + ALPHA
        self.bottom_c = bottom_color.value + ALPHA

        self.species = head[0]
        self.forehead = head[1]
        self.muzzle = head[2]
        self.toon_head = None
        self.joint_hierarchy = JOINT_HIERARCHY

        self.assemble_toon()
        self.set_name(toon_name)
        self.reparent_to(parent)

    def assemble_toon(self, actor=None):
        Actor.__init__(self, actor)
        self.load_legs()
        self.load_toon_anims(self.legs, TG.LEGS)

        self.load_torso()
        self.load_toon_anims(self.torso, TG.TORSO)
        self.apply_clothing_colors()

        ToonHead.__init__(self, self)
        self.attach(TG.HEAD, TG.TORSO, TG.JOINT_HEAD)
        self.name_body_parts()

        AutoWalker.__init__(self, self, speed=15, run_anim="run", run_div=2.0)
        self.set_blend(frameBlend=True)
        self.node().set_bounds(OmniBoundingVolume())
        self.node().set_final(1)
        self.set_scale(TG.SCALE[self.species])
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

    def load_toon_anims(self, body_part_type, body_part):
        anim_dict = {}
        for phase_file, anims in TG.ANIMS.items():
            for anim in anims:
                phase_path = f"phase_{phase_file}/models/char/"
                anim_file = f"""{TG.TOON_MODEL_FILE.format(
                    body_part_type, self.bottom, body_part, anim)}"""
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

    def load_ragdoll(self):
        Ragdoll.__init__(self, self, self.joint_hierarchy)

    def cleanup(self):
        self.cleanup_walker()