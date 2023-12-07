# This code lets you load this file directly in cmd/IDE instead of bat file.
# (You will still need to use a version of python that comes with Panda3D)
import os, sys

current_path = os.getcwd()
project_path = ""
for folder in current_path.split("\\"):
    project_path += folder + "/"
    if folder == "Panda3D_Kitchen":
        break

sys.path.append(project_path)
os.chdir(project_path)

"""
Loads the OG 151 Pokémon as sprites.
Organizes them in a vertically rectangular shape.
"""
from classes.settings import Settings

from direct.showbase.ShowBase import ShowBase

from classes.actors.Suit import Suit
from classes.actors.Toon import Toon
from classes.camera.OrbitalCamera import OrbitalCamera
from classes.camera.FovScrollWheel import FovScrollWheel
from classes.editors.MasterEditor import MasterEditor
from classes.props.AnimatedSprite import AnimatedSprite
from classes.props.PokemonSprite import PokemonSprite
from classes.globals import Globals as G
import KantoGlobals as KG

SPRITE_TEX_PATH = "pokemon/sprites/"
SPRITE_SCALE = .5
X_LIMIT = 8


class KantoDex(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.x_pos = 0
        self.z_pos = 0
        self.shadows = []
        self.sprites = []

        self.accept(G.ESCAPE, exit)
        base.disable_mouse()
        base.set_background_color(.1, .1, .1, 1)
        base.camLens.set_fov(56.0)

        self.node_editor = MasterEditor()
        self.orb_cam = OrbitalCamera()
        self.fov_wheel = FovScrollWheel()

        background = AnimatedSprite(SPRITE_TEX_PATH + "route-23.png")
        background.set_pos(3.5, .5, -5)
        scale_boost = 7
        background.set_scale(scale_boost, 1, scale_boost * 2.72)
        background.remove_node()

        # self.setup_pokemon()
        # self.setup_cogs()
        self.setup_toons()

    def setup_pokemon(self):
        # Make Kanto Pokemon sprites. (151 Total)
        self.generate_sprites(0, 9, "00")
        self.generate_sprites(9, 99, "0")
        self.generate_sprites(99, 151, "")

        for sprite in self.sprites:
            sprite.set_scale(SPRITE_SCALE)

        camera.set_pos_hpr(11.36, -8.12, -1.22, 38.38, -4.6, 0.0)

    def setup_cogs(self):
        self.flunky = Suit("f", render, suit_name="~self.flunky")
        self.pusher = Suit("p", render, suit_name="~self.pusher")
        self.yesman = Suit("ym", render, suit_name="~self.yesman")
        self.micro = Suit("mm", render, suit_name="~self.micro")
        self.sizer = Suit("ds", render, suit_name="~self.sizer")
        self.hunter = Suit("hh", render, suit_name="~self.hunter")
        self.raider = Suit("cr", render, suit_name="~self.raider")
        self.cheese = Suit("tbc", render, suit_name="~self.cheese")

        self.flunky.set_pos_hpr(27.4, 4.3, 0.0, -92.29, 0.0, 0.0)
        self.pusher.set_pos_hpr(28.79, 6.68, 0.0, -127.06, 0.0, 0.0)
        self.yesman.set_pos_hpr(26.58, 6.27, 0.0, -103.71, 0.0, 0.0)
        self.micro.set_pos_hpr(29.5, 2.18, 0.0, -57.17, 0.0, 0.0)
        self.sizer.set_pos_hpr(26.55, 2.07, 0.0, -80.77, 0.0, 0.0)
        self.hunter.set_pos_hpr(25.72, 0.74, 0.0, -61.55, 0.0, 0.0)
        self.raider.set_pos_hpr(23.56, 8.52, 0.0, -116.73, 0.0, 0.0)
        self.cheese.set_pos_hpr(23.2, 4.39, 0.0, -92.45, 0.0, 0.0)

        camera.set_pos_hpr(34.85, 3.96, 1.59, 88.92, 20.85, 0.0)

    def setup_toons(self):
        self.pink = Toon(parent=render, gender='m',
                         toon_name="~self.pink",
                         head='pss', head_c=2,
                         torso='s', shirt_t=8, shirt_c=2,
                         sleeve_t=8, sleeve_c=2, arm_c=2, glove_c=0,
                         legs='m', leg_c=2,
                         bottom='shorts', bottom_t=7, bottom_c=2)

        camera.set_pos_hpr(3.46, 5.78, 1.38, 148.5, -4.36, 0.0)

    def generate_sprites(self, start, end, dex_str):
        # For pokemon in a specified range-
        for i in range(start, end):
            # Pull their entry and generate a sprite.
            entry = KG.DEX_ENTRIES[i]
            texture_path = SPRITE_TEX_PATH + f"ani_bw_{dex_str}{i+1}.png"
            sprite = PokemonSprite(texture_path, columns=entry[0],
                                   wait_time=.1, name=f"self.sprites[{i}]")
            sprite.uv_sequence.loop()
            sprite.set_pos(self.x_pos, 0, self.z_pos)
            self.setup_sprite_shadow(i, entry, sprite, dex_str)

            # Update the position for the next sprite if applicable.
            self.x_pos += 1
            if self.x_pos == X_LIMIT:
                self.x_pos = 0
                self.z_pos += -1

            self.sprites.append(sprite)

    # Make a copy of the sprite as a shadow.
    def setup_sprite_shadow(self, i, entry, sprite, num):
        sprite_shadow = AnimatedSprite(
            SPRITE_TEX_PATH + f"ani_bw_{num}{i+1}.png",
            columns=entry[0], wait_time=.1)
        sprite_shadow.reparent_to(sprite)
        sprite_shadow.set_y(.2)
        sprite_shadow.set_scale(SPRITE_SCALE * 2)
        sprite_shadow.set_color(0, 0, 0, 1)
        sprite_shadow.set_alpha_scale(0.5)
        self.shadows.append(sprite_shadow)


app = KantoDex()
app.run()