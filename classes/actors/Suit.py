from direct.actor.Actor import Actor

from .AutoWalker import AutoWalker
from classes.globals import Globals as G
from . import SuitGlobals as SG


class Suit(Actor, AutoWalker):

    def __init__(self, suit_key, parent=None, skelecog=False, name="~Suit"):
        self.suits = []
        self.skelecog = skelecog
        self.suit_name = name
        if isinstance(suit_key, str):
            self.suit = SG.SUITS[suit_key]
        self.body = self.suit[0]
        self.dept = self.suit[1]
        self.head_type = self.suit[2]
        self.hand_color = self.suit[3]
        self.head_texture = self.suit[4]
        self.scale = self.suit[5]

        self.assemble_cog_parts(parent)
        self.set_name(self.suit_name)

    def assemble_cog_parts(self, parent, actor=None):
        Actor.__init__(self, actor)
        self.load_suit(parent)

        AutoWalker.__init__(self, self)
        self.load_animations()
        self.load_health_meter()
        self.load_shadow()
        self.special_attributes()
        self.loop("neutral")
        self.suits.append(self)

    def load_suit(self, parent):
        model_path = f"phase_3.5/models/char/suit{self.body}-mod.bam"
        self.load_model(model_path)
        self.set_scale(self.scale)
        self.set_blend(frameBlend=True)

        if not parent:
            self.reparent_to(render)
        else:
            self.reparent_to(parent)

        self.leg_tex = loader.load_texture(f"phase_3.5/maps/{self.dept}_leg.jpg")
        self.sleeve_tex = loader.load_texture(f"phase_3.5/maps/{self.dept}_sleeve.jpg")
        self.blazer_text = loader.load_texture(f"phase_3.5/maps/{self.dept}_blazer.jpg")
        self.find('**/legs').set_texture(self.leg_tex, 1)
        self.find('**/arms').set_texture(self.sleeve_tex, 1)
        self.find('**/torso').set_texture(self.blazer_text, 1)
        self.find('**/hands').set_color(self.hand_color)

        self.head = loader.load_model(f"phase_4/models/char/suit{self.body}-heads.bam").find(f'**/{self.head_type}')
        self.head.reparent_to(self.find('**/joint_head'))
        self.head.set_name(self.suit_name + f".find('**/{self.head_type}')")
        if self.head_texture:
            self.head.set_texture(loader.load_texture(self.head_texture), 1)

    def load_animations(self):
        anim_name_dict = SG.SUIT_ANIMS[self.body]
        anim_dict = {}
        for anim in anim_name_dict:
            num = anim_name_dict[anim]
            anim_dict[anim] = f'phase_{num}/models/char/suit{self.body}-{anim}.bam'
        self.load_anims(anim_dict)

    def load_health_meter(self):
        pass

    def load_shadow(self):
        pass

    def special_attributes(self):
        if self.dept == 's' and self.head_type == 'coldcaller':
            self.head.set_color(SG.CC_COLOR)

        if self.head_type == "flunky" and not self.head_texture:
            glasses = loader.loadModel('phase_4/models/char/suitC-heads.bam').find('**/glasses')
            glasses.reparentTo(self.head)

    def cleanup(self):
        taskMgr.remove(G.AUTO_WALKER_TASK)