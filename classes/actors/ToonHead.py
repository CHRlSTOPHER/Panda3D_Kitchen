"""
A collection of Toon Head classes.

Toon Exception Notes-

"""
from classes.globals import Globals as G
from classes.actors import ToonGlobals as TG

EXPRESSIONS = ["neutral", "sad", "angry", "laugh", "surprise", "smile"]
DOG_PARTS = {
    'dss': ["tt_a_chr_dgm_skirt_head_{}", "dogMM_Skirt-headMuzzles-{}"],
    'dls': ["tt_a_chr_dgm_shorts_head_{}", "dogMM_Shorts-headMuzzles-{}"],
    'dsl': ["tt_a_chr_dgs_shorts_head_{}", "dogSS_Shorts-headMuzzles-{}"],
    'dll': ["tt_a_chr_dgl_shorts_head_{}", "dogLL_Shorts-headMuzzles-{}"],
}
HEAD_NODE_PARTS = ['head-', 'head-front-', 'ears-', 'eyes-',
                     'joint_pupilL_', 'joint_pupilR_']
HEAD_COLOR_PARTS = ['head-', 'head-front-', 'ears-']
EYE_NODE_PARTS = ['**/joint_pupilL_', '**/joint_pupilR_', '**/eyes-']
ANIMATED_HEADS = ['d']


class ToonHead():

    def __init__(self, toon):
        self.toon = toon
        self.head = toon.head
        self.head_c = toon.head_c
        self.forehead = toon.forehead
        self.muzzle_size = TG.SIZE[toon.muzzle]
        self.lod = toon.lod
        self.species = toon.head[0]
        self.l_eye = None
        self.r_eye = None

        self.head_nodes = HEAD_NODE_PARTS
        self.head_color_nodes = HEAD_COLOR_PARTS
        self.eye_nodes = EYE_NODE_PARTS

        self.load_head_model()

    def load_head_model(self):
        if self.species in ANIMATED_HEADS:
            load_animated_head = self.get_animated_head_loader()[self.species]
            load_animated_head()
            return

        species = TG.SPECIES[self.species]
        head_path = f"{G.CHAR_3}{species}-heads-{self.lod}{G.BAM}"
        self.toon.load_model(head_path, TG.HEAD)

        head_collection = self.toon.get_part(TG.HEAD)
        head_children = head_collection.get_children()
        if len(head_children) == 1:
            head_collection = [child for child in head_children][0]

        # hide all head nodes.
        for node in head_collection.get_children():
            node.hide()

        # Some Toons have unique traits. examples:
        # rabbits only have one pair of eyes.
        # ducks don't have ears.
        # deers have antler and nose variations...
        define_head_features = self.get_head_features()[self.species]
        if define_head_features: define_head_features()

        forehead = TG.SIZE[self.head[1]]
        self.left_eye = self.toon.find(f"**/{self.eye_nodes[0]}{forehead}")
        self.right_eye = self.toon.find(f"**/{self.eye_nodes[1]}{forehead}")

        for node in self.head_nodes:
            self.toon.find(f"**/{node}{forehead}").show()

        for node in self.head_color_nodes:
            self.toon.find(f"**/{node}{forehead}").set_color(self.toon.head_c)

        self.toon.find(f'**/muzzle-{self.muzzle_size}-neutral').show()

    def change_muzzle(self, expression):
        if self.species == 'd':
            print("didn't code dog muzzle change yet :)")
            return

        for e in EXPRESSIONS:
            self.toon.find(f'**/muzzle-{self.muzzle_size}-{e}').hide()
        self.toon.find(f'**/muzzle-{self.muzzle_size}-{expression}').show()

    def load_dog_head(self):
        head_path = DOG_PARTS[self.head][0].format(self.lod)
        muzzle_path = DOG_PARTS[self.head][1].format(self.lod)

        self.toon.load_model(f'{G.CHAR_3}{head_path}{G.BAM}', TG.HEAD)
        self.toon.load_anims(self.load_dog_anims(), TG.HEAD)
        self.muzzle_model = loader.load_model(f'{G.CHAR_3}{muzzle_path}{G.BAM}')
        self.muzzle_model.reparent_to(self.toon.get_part(TG.HEAD))

        self.toon.control_joint(None, TG.HEAD, "def_left_pupil")
        self.toon.control_joint(None, TG.HEAD, "def_right_pupil")
        self.left_eye = self.toon.find("**/def_left_pupil")
        self.right_eye = self.toon.find("**/def_right_pupil")

        for node in ['head', 'head-front']:
            self.toon.find(f'**/{node}').set_color(self.head_c)

        for e in ["sad", "angry", "laugh", "surprise", "smile"]:
            self.muzzle_model.find(f'**/muzzle-{self.muzzle_size}-{e}').hide()

    def load_dog_anims(self):
        anim_dict = {}
        for phase_file, anims in TG.ANIMS.items():
            for anim in anims:
                phase_path = f"phase_{phase_file}/models/char/"
                anim_file = f"{DOG_PARTS[self.head][0].format(anim)}"
                anim_dict[anim] = phase_path + anim_file + G.BAM
                # "tt_a_chr_dg?_?_head_{}"

        return anim_dict

    def horse_head_features(self):
        self.head_color_nodes = ['head-', 'head-front-']

    def mouse_head_features(self):
        self.muzzle_size = 'short'
        self.toon.find('**/').show() # Mouse nose lol...

    def rabbit_head_features(self):
        self.head_nodes = ['head-', 'head-front-', 'ears-',
                           'joint_pupilL_', 'joint_pupilR_']
        self.eye_nodes = ['**/joint_pupilL_', '**/joint_pupilR_']
        self.toon.find(f"**/eyes").show()

        if self.forehead == 's':
            self.muzzle_size = 'short'
        else:
            self.muzzle_size = 'long'

    def duck_head_features(self):
        self.head_nodes = ['head-', 'head-front-', 'eyes-',
                           'joint_pupilL_', 'joint_pupilR_']
        self.head_color_nodes = ['head-', 'head-front-']

    def monkey_head_features(self):
        self.head_color_nodes = ['head-', 'head-front-']

    def deer_head_features(self):
        for node in self.head_nodes:
            self.toon.find(f"**/{node}short").show()
        self.toon.find(f'**/nose-{self.muzzle_size}').show()
        self.head_nodes = ["antler-"]

        for node in self.head_color_nodes:
            self.toon.find(f"**/{node}short").set_color(self.toon.head_c)
        self.head_color_nodes = []

    def get_head_features(self):
        return {
            'd': None,
            'c': None,
            'h': self.horse_head_features,
            'm': self.mouse_head_features,
            'r': self.rabbit_head_features,
            'f': self.duck_head_features,
            'p': self.monkey_head_features,
            'b': None,
            's': None,
            # ttr
            'a': None,
            'q': self.deer_head_features,
        }

    def get_animated_head_loader(self):
        return {
            'd': self.load_dog_head,
        }