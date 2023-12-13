import os, sys
# The code below lets you load the py file directly in cmd/IDE.
# (You will still need to use a version of python that comes with Panda3D)
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
        base.set_background_color(.1, .1, .1, 1)

        self.master_editor = MasterEditor()

        background = AnimatedSprite(SPRITE_TEX_PATH + "route-23.png")
        background.set_pos(3.5, .5, -5)
        scale_boost = 7
        background.set_scale(scale_boost, 1, scale_boost * 2.72)
        background.remove_node()

        self.setup_pokemon()

    def setup_pokemon(self):
        # Make Kanto Pokemon sprites. (151 Total)
        self.generate_sprites(0, 9, "00")
        self.generate_sprites(9, 99, "0")
        self.generate_sprites(99, 151, "")

        camera.set_pos_hpr(11.36, -8.12, -1.22, 38.38, -4.6, 0.0)

    def generate_sprites(self, start, end, dex_str):
        # For pokemon in a specified range-
        for i in range(start, end):
            # Pull their entry and generate a sprite.
            entry = KG.DEX_ENTRIES[i]
            texture_path = SPRITE_TEX_PATH + f"ani_bw_{dex_str}{i+1}.png"
            sprite = PokemonSprite(texture_path, columns=entry[0],
                                   wait_time=.1, scale=SPRITE_SCALE,
                                   parent=render, name=f"self.sprites[{i}]")
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