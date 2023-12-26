# The code below lets you load the py file directly in cmd/IDE.
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
from classes.settings import Settings

'''
An application that lets you create new Toons and save them.
Or you can load an existing Toon and edit it!
'''
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton

from classes.actors.Toon import Toon
from classes.globals import Globals as G
from classes.globals import ToonGlobals as TG
from classes.globals.ToonColors import ToonColors as TC
from classes.props.PlaneModel import PlaneModel
from classes.editors.MasterEditor import MasterEditor

FRAME_TEXTURE = G.MAPS_3 + "tt_t_gui_ups_panelBg"
LASHES_TEXTURE = G.APP_MAPS + "lashes-buttons" + G.PNG
BOTTOMS_TEXTURE = G.APP_MAPS + "bottoms-buttons" + G.PNG
SPECIES_TEXTURE = G.APP_MAPS + "toon-species-buttons" + G.JPG
GXZ = .165
GENDER_POS = [(-GXZ, 0, GXZ), (GXZ, 0, GXZ), (-GXZ, 0, -GXZ), (GXZ, 0, -GXZ)]
BOTTOM_DICT = {'m': "shorts", "f": "skirt"}


class Make_A_Toon_GUI(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self)
        self.initialiseoptions(Make_A_Toon_GUI)

        self.edit_toon = False
        self.create_toon = False
        self.toon = None

        self.gender = ['m', 'shorts']
        self.limbs = ['dss', 'm', 'm']
        self.colors = [41, 41, 41, 41, 41, 41, 41] # White = 41
        self.clothes = [0, 0, 0]
        self.name = ""

        self.load_main_frame()

        # each function returns a list of gui.
        self.pages = [
            self.options_page(),
            self.gender_gui(),
            self.species_gui(),
            self.limbs_page(),
            self.colors_page(),
            self.clothes_page(),
            self.name_page()
        ]
        self.load_toon()
        # self.show_page(0)

    def load_main_frame(self):
        textures = [FRAME_TEXTURE + ".jpg", FRAME_TEXTURE + "_a.rgb"]
        self.core = DirectFrame(parent=base.a2dLeftCenter,
                                 geom=PlaneModel(textures),
                                 frameVisibleScale=(0, 0), pos=(1.0, 0, 0))

    def options_page(self):
        return []

    def gender_gui(self):
        def new_gender(gender):
            self.gender = [gender, self.gender[1]]
            if gender == 'f':
                self.toon.lashes.show()
            else:
                self.toon.lashes.hide()

        def new_bottom(bottom):
            self.gender = [self.gender[0], BOTTOM_DICT[bottom]]
            self.load_toon()

        gender_frame = DirectFrame(self.core, pos=(.45, 0, .5))
        i = 0
        trans = [[LASHES_TEXTURE, new_gender], [BOTTOMS_TEXTURE, new_bottom]]
        for texture, command in trans:
            geom = [PlaneModel(texture, 2, 2, frame=x) for x in range(0, 4)]
            DirectButton(gender_frame, geom=(geom[0], geom[1], geom[0]),
                         pos=GENDER_POS[i], scale=.165,
                         frameVisibleScale=(0, 0), frameSize=(.8, -.8, .8, -.8),
                         command=command, extraArgs=['f'])
            DirectButton(gender_frame, geom=(geom[2], geom[3], geom[2]),
                         pos=GENDER_POS[i + 1], scale=.165,
                         frameVisibleScale=(0, 0), frameSize=(.8, -.8, .8, -.8),
                         command=command, extraArgs=['m'])
            i += 2

        return gender_frame

    def species_gui(self):
        def change_species(species):
            self.limbs[0] = f"{species}{self.limbs[0][1]}{self.limbs[0][2]}"
            self.load_toon()

        species_frame = DirectFrame(self.core, pos=(-.5, 0, .5), scale=.9)
        x_value, z_value = [.25, .25]
        x, z = [-x_value, z_value]
        x_add, z_add = [x_value, z_value]
        uv_frame = 0
        for species, name in TG.SPECIES.items():
            meter = PlaneModel(SPECIES_TEXTURE, rows=4, columns=4)
            meter.set_frame(uv_frame)
            DirectButton(species_frame, geom=meter, pos=(x, 0, z), scale=.115,
                         command=change_species, extraArgs=[species])
            uv_frame += 1
            if x > x_add: # Reset x back to the far left and move down.
                x = -x_add
                z -= z_add
            else:
                x += x_add # Move next GUI to the right.

        return species_frame

    def limbs_page(self):
        return []

    def colors_page(self):
        return []

    def clothes_page(self):
        return []

    def name_page(self):
        return []

    def load_toon(self):
        if self.toon:
            self.toon.cleanup_actor()
        limbs, color, cloth = [self.limbs, self.colors, self.clothes]
        lashes, bottom = [self.gender[0], self.gender[1]]
        self.toon = Toon(
            render, lashes, toon_name=self.name, lod=1000,
            head=limbs[0], torso=limbs[1], legs=limbs[2], bottom=bottom,
            shirt_t=cloth[0], sleeve_t=cloth[1], bottom_t=cloth[2],
            head_color=color[0], shirt_color=color[1], sleeve_color=color[2],
            glove_color=color[3], leg_color=color[4], bottom_color=color[5]
        )

    def show_page(self, index):
        for page in self.pages:
            for gui_node in page:
                gui_node.hide() # hide all gui

        for gui_node in self.pages[index]:
            gui_node.show() # show desired page gui


class Make_A_Toon(ShowBase, Make_A_Toon_GUI):

    def __init__(self):
        ShowBase.__init__(self)
        Make_A_Toon_GUI.__init__(self)
        base.disable_mouse()
        camera.set_pos_hpr(-3.5, 12.0, 3.0, -150.0, -4.0, 0.0)
        self.master_editor = MasterEditor(nt_printer=False)


Make_A_Toon().run()