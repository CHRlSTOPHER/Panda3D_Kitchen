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
from direct.interval.IntervalGlobal import (Sequence, Func,
                                            LerpPosInterval)

from classes.actors.Toon import Toon
from classes.editors.MasterEditor import MasterEditor
from classes.editors.NodeMover import NodeMover
from classes.editors.NodeSelector import NodeSelector
from classes.gui.ButtonGrid import ButtonGrid
from classes.globals import Globals as G
from classes.globals import ToonGlobals as TG
from classes.globals.ToonColors import ToonColors as TC
from classes.props.PlaneModel import PlaneModel
from classes.props.Prop import Prop
import Make_A_Toon_Globals as MT


class Make_A_Toon_Happy_GUI(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self)
        self.initialiseoptions(Make_A_Toon_Happy_GUI)

        self.toon = None
        self.head_display = None

        # Data to construct the display toon and the data that gets saved.
        self.gender = ['m', 'shorts']
        self.limbs = ['dss', 'm', 'm']
        self.colors = [41, 41, 41, 41, 41, 41, 41] # White = 41
        self.clothes = [0, 0, 0]
        self.name = MT.BODY

        self.load_pages()
        self.pages = [
            # self.file_page,
            self.body_page,
            # self.color_page,
            # self.clothes_pages,
        ]
        # each function returns a direct frame.
        self.gui_sections = [
            self.options_gui(),
            self.gender_gui(),
            self.species_gui(),
            self.limbs_gui(),
            self.colors_gui(),
            self.clothes_gui(),
            self.name_gui()
        ]
        self.load_toon()
        self.update_heads_display('d') # default to dog head

    def load_pages(self):
        textures = [MT.FRAME_TEXTURE + ".jpg", MT.FRAME_TEXTURE + "_a.rgb"]
        self.body_page = DirectFrame(parent=base.a2dLeftCenter,
                                     geom=PlaneModel(textures),
                                     frameVisibleScale=(0, 0),
                                     pos=MT.GUI_INTERVALS[MT.BODY])

    def options_gui(self):
        return []

    def gender_gui(self):
        def update_lashes(gender):
            self.toon.lashes.show()
            if gender == 'm':
                self.toon.lashes.hide()

        def update_gender(gender):
            self.gender = [gender, self.gender[1]]
            update_lashes(gender)

        def update_bottom(bottom):
            self.gender = [self.gender[0], MT.BOTTOM_DICT[bottom]]
            self.load_toon()

        gender_frame = DirectFrame(self.body_page, pos=(.45, 0, .5))

        i = 0
        for texture, command in [[MT.LASHES_TEXTURE, update_gender],
                                 [MT.BOTTOMS_TEXTURE, update_bottom]]:
            geom = [PlaneModel(texture, 2, 2, frame=f) for f in range(0, 4)]
            scale, fvs, frame_size = [.165, (0, 0), (.8, -.8, .8, -.8)]
            DirectButton(gender_frame, geom=(geom[0], geom[1], geom[0]),
                         pos=MT.GENDER_POS[i], scale=scale,
                         frameVisibleScale=fvs, frameSize=frame_size,
                         command=command, extraArgs=['f'])
            DirectButton(gender_frame, geom=(geom[2], geom[3], geom[2]),
                         pos=MT.GENDER_POS[i + 1], scale=scale,
                         frameVisibleScale=fvs, frameSize=frame_size,
                         command=command, extraArgs=['m'])
            i += 2

        return gender_frame

    def species_gui(self):
        def update_species(species):
            self.limbs[0] = f"{species}{self.limbs[0][1]}{self.limbs[0][2]}"
            self.update_heads_display(species) # change the head display
            self.load_toon()

        species_frame = ButtonGrid(
            parent=self.body_page, pos=(-.5, 0, .5), scale=.9,
            texture=MT.SPECIES_TEXTURE, rows=4, columns=4,
            db_scale=.115, collection=TG.SPECIES,
            command=update_species, extra_arg="key",
            base_x=-.25, base_z=.25, x_increment=.25, z_increment=.25)

        return species_frame

    def update_heads_display(self, species):
        def update_head(head_size):
            self.limbs = [self.limbs[0][0] + head_size,
                          self.limbs[1], self.limbs[2]]
            self.load_toon()

        if self.head_display:
            self.head_display.destroy()

        species_name = TG.SPECIES[species]

        collection = MT.HEAD_DISPLAYS
        rows, columns = [2, 2]
        if species == 'm' or species == 'r':
            collection = MT.HEAD_DISPLAYS[:2]
            rows, columns = [1, 2]

        self.head_display = ButtonGrid(
            parent=self.body_page, pos=(.05, 0.0, -.33), scale=1,
            texture=f"{G.APP_MAPS}{species_name}-heads.png",
            rows=rows, columns=columns, db_scale=.12,
            collection=collection, command=update_head, extra_arg=None,
            base_x=.25, base_z=.25, x_increment=.275, z_increment=.25,
            x_regression=-.125, fvs=(0, 0))

    def limbs_gui(self):
        def updates_limbs(limb_type):
            self.limbs = [self.limbs[0], limb_type[0], limb_type[1]]
            self.load_toon()

        limb_frame = DirectFrame(self.body_page, pos=(0, 0, -.75), scale=.9)
        i = 0
        for limbs in MT.BODY_SIZES:
            geom = PlaneModel(MT.LIMB_TEXTURE, rows=1, columns=9)
            geom.set_frame(i)
            pos = tuple(sum(x) for x in zip(MT.BODY_POS[i], (0, 0, .2)))
            DirectButton(limb_frame, pos=pos, scale=(1.35, 1, 1.9),
                         geom=geom, geom_scale=(.1125, 12, .12),
                         frameSize=(.11, -.11, .11, -.11),
                         frameVisibleScale=(0, 0),
                         command=updates_limbs, extraArgs=[limbs])
            i += 1
            # Toon Head code is in update_heads_display.
        return limb_frame

    def colors_gui(self):
        return []

    def clothes_gui(self):
        return []

    def name_gui(self):
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
            glove_color=color[3], leg_color=color[4], bottom_color=color[5],
            names=False
        )


class Make_A_Toon(ShowBase, Make_A_Toon_Happy_GUI):

    def __init__(self):
        ShowBase.__init__(self)
        Make_A_Toon_Happy_GUI.__init__(self)
        self.selection_allowed = True

        base.disable_mouse()
        camera.set_pos_hpr(*MT.CAM_INTERVALS[MT.BODY])

        self.node_selector = NodeSelector(self)
        self.bucket = Prop(MT.BUCKET_MODEL, parent=render, name=MT.BUCKET,
                           pos=(0.72, -6.06, 0.0), hpr=(96.91, 0.0, 0.0))
        self.closet = Prop(MT.WARDROBE_MODEL, parent=render, name=MT.WARDROBE,
                           pos=(8.62, -3.77, -2.55), hpr=(-128.96, 0.0, 0.0))
        # self.node_mover = NodeMover(self.bucket)
        self.editor = MasterEditor(rot_cam=False, mouse_lock=False)
        self.body_page.hide()

    def set_node(self, node):
        if not self.selection_allowed or not node.name in MT.CAM_INTERVALS:
            return

        new_pos_hpr = MT.CAM_INTERVALS[node.name]
        if new_pos_hpr == (camera.get_pos(), camera.get_hpr()):
            return # the interval end point is our current position. Abort.

        self.load_gui_transition_sequence(node, new_pos_hpr)
        self.gui_sequence.start()

    def load_gui_transition_sequence(self, node, new_pos_hpr):
        self.gui_sequence = Sequence()
        self.gui_sequence.append(Func(self.toggle_selection_allowed))

        if node.name == MT.WARDROBE:
            turn = MT.WARDROBE_CAM_TURN
            interval = camera.posHprInterval(1, *turn, blendType='easeInOut')
            self.gui_sequence.append(interval)

        self.gui_sequence.append(camera.posHprInterval(1.7, *new_pos_hpr,
                                                 blendType='easeInOut'))
        self.gui_sequence.append(Func(self.toggle_selection_allowed))
        self.gui_sequence.start()

    def toggle_selection_allowed(self):
        self.selection_allowed = not self.selection_allowed

Make_A_Toon().run()