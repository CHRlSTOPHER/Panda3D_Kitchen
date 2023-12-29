# The code below lets you load the py file directly in cmd/IDE.
# (You will still need to use a version of python that comes with Panda3D)
import os, sys
project_path = ""
for folder in os.getcwd().split("\\"):
    project_path += folder + "/"
    if folder == "Panda3D_Kitchen": break
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
from classes.editors.NodeSelector import NodeSelector
from classes.editors.MasterEditor import MasterEditor
from classes.globals import Globals as G
from classes.globals import ToonGlobals as TG
import Make_A_Toon_Globals as MT
from classes.globals.ToonColors import ToonColors as TC
from classes.props.PlaneModel import PlaneModel
from classes.props.AnimatedSprite import AnimatedSprite


class Make_A_Toon_Sad_GUI(DirectFrame): # Currently unused.

    def __init__(self):
        DirectFrame.__init__(self)
        self.initialiseoptions(Make_A_Toon_Sad_GUI)

    def limbs_page(self):
        limb_frame = DirectFrame(self.core, pos=(0, 0, -.7), scale=.9)
        for limb, pos in MT.LIMB_POS.items():
            for i in range(0, 3):  # make three copies
                geom = AnimatedSprite(G.APP_MAPS + f'sketch-{limb}{G.PNG}',
                                      rows=1, columns=4, wait_time=.2,
                                      scale=MT.LIMB_SCALE[limb], pos=pos[i],
                                      parent=limb_frame)
                geom.loop()
        for pos in MT.HEAD_POS:
            geom = AnimatedSprite(G.APP_MAPS + f'sketch-head{G.PNG}',
                                  rows=1, columns=4, wait_time=.2,
                                  scale=.1, pos=pos, parent=limb_frame)
            geom.loop()

        # DirectButton(limbs_frame)
        return limb_frame


class Make_A_Toon_Happy_GUI(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self)
        self.initialiseoptions(Make_A_Toon_Happy_GUI)

        self.edit_toon = False
        self.create_toon = False
        self.toon = None

        # Data to construct the display toon and the data that gets saved.
        self.gender = ['m', 'shorts']
        self.limbs = ['dss', 'm', 'm']
        self.colors = [41, 41, 41, 41, 41, 41, 41] # White = 41
        self.clothes = [0, 0, 0]
        self.name = "~Actors.snoopy"

        # Body type displays
        self.body_displays = []

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
        textures = [MT.FRAME_TEXTURE + ".jpg", MT.FRAME_TEXTURE + "_a.rgb"]
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
            self.gender = [self.gender[0], MT.BOTTOM_DICT[bottom]]
            self.load_toon()

        gender_frame = DirectFrame(self.core, pos=(.45, 0, .5))
        i = 0
        gender_textures = [[MT.LASHES_TEXTURE, new_gender],
                           [MT.BOTTOMS_TEXTURE, new_bottom]]
        for texture, command in gender_textures:
            geom = [PlaneModel(texture, 2, 2, frame=x) for x in range(0, 4)]
            DirectButton(gender_frame, geom=(geom[0], geom[1], geom[0]),
                         pos=MT.GENDER_POS[i], scale=.165,
                         frameVisibleScale=(0, 0), frameSize=(.8, -.8, .8, -.8),
                         command=command, extraArgs=['f'])
            DirectButton(gender_frame, geom=(geom[2], geom[3], geom[2]),
                         pos=MT.GENDER_POS[i + 1], scale=.165,
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
            meter = PlaneModel(MT.SPECIES_TEXTURE, rows=4, columns=4)
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
        limb_frame = DirectFrame(self.core, pos=(0, 0, -.75), scale=.9)
        i = 0
        for body in MT.BODY_SIZES:
            # I really don't know why but for some reason we need to
            # attach the actor to a node???
            # Otherwise when you try to move the position of the actor
            # directly in aspect2d it ignores stuff like pose and stop funcs...
            body_node = limb_frame.attach_new_node("body_node")
            hpr, scale = [(180, 0, 0), (.1, .1, .1)]
            body_node.set_pos_hpr_scale(*MT.BODY_POS[i], *hpr, *scale)

            # create a body display. 9 different limb types.
            body = Toon(parent=body_node, torso=body[0], legs=body[1])
            body.get_part(TG.HEAD).remove_node()
            body.find(f"**/{TG.NECK}").remove_node()
            # body.pose("neutral", 24)
            light_blue = (1, 1, 1, 1)
            body.set_color_scale(*light_blue)
            body.set_depth_write(True)
            body.set_depth_test(True)
            i += 1
            self.body_displays.append(body)

        return limb_frame

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


class Make_A_Toon(ShowBase, Make_A_Toon_Happy_GUI):

    def __init__(self):
        ShowBase.__init__(self)
        Make_A_Toon_Happy_GUI.__init__(self)
        base.disable_mouse()
        camera.set_pos_hpr(-3.5, 12.0, 3.0, -150.0, -4.0, 0.0)
        # MasterEditor()
        self.node_selector = NodeSelector()


Make_A_Toon().run()