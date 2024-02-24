import os, sys

from panda3d.core import PerspectiveLens
from direct.interval.IntervalGlobal import (Sequence, Parallel, Wait, Func,
                                            LerpFunc)

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
from classes.globals import Globals as G
from classes.actors.Toon import Toon
from classes.editors.MasterEditor import MasterEditor
from classes.props.Prop import Prop


class Main(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        base.disable_mouse()

        # self.editor = MasterEditor(rot_cam=False, mouse_lock=False)
        base.setBackgroundColor(1, 0, 0, 1)

        self.load_actors()
        self.load_scene()
        self.load_animation()

    def load_actors(self):
        # c for color lol
        c = 25
        t = 8
        self.toon = Toon(render, 'f', "~self.toon", 1000,
                         'rll', 'l', 'l', 'skirt',
                         t, t, 7, c, 41, 41, c, 41, c, 41, True)
        self.toon.set_pos(-0.25, 1, -2.5)
        self.toon.set_h(0)
        eyes = loader.load_texture(
            "phase_3/maps/eyes.jpg",
            "phase_3/maps/eyes_a.rgb",
        )
        self.toon.find('**/eyes').set_texture(eyes, 1)
        shirt_texture = loader.load_texture(
            "phase_4/maps/ttr_t_chr_avt_shirt_golfing04.jpg")
        sleeve_texture = loader.load_texture(
            "phase_4/maps/ttr_t_chr_avt_shirtSleeve_golfing04.jpg")
        dress_texture = loader.load_texture(
            "phase_4/maps/ttr_t_chr_avt_skirt_fishingMax.jpg")
        self.toon.disable_autowalker()
        self.toon.find('**/').show()

        #self.toon.find('**/eyes').set_texture(surprise_texture, 1)
        self.toon.find('**/torso-top').set_texture(shirt_texture, 1)
        self.toon.find('**/sleeves').set_texture(sleeve_texture, 1)
        self.toon.find('**/torso-bot').set_texture(dress_texture, 1)

        bow = loader.load_model(
            "phase_4/models/accessories/tt_m_chr_avt_acc_hat_ribbon.bam"
        )
        texture = loader.load_texture(
            "phase_4/maps/ttr_t_chr_avt_acc_hat_ribbonSeafoam.jpg")
        bow.set_texture(texture, 1)
        bow.set_pos_hpr(0.01, -0.09, 0.27, 179.83, -19.5, 3.17)
        bow.set_scale(.33)
        bow.set_name('~bow')
        bow.reparent_to(self.toon.get_part("head"))

    def load_scene(self):
        base.camLens.set_fov(60)
        camera.setPos(0, 16.0, 2.0)
        camera.lookAt(0, 0, 0.75)

        bg = render.attach_new_node("bg")
        self.foreground = Prop('phase_3.5/models/modules/TT_A1.bam', parent=bg,
                          pos=(12.5, -20, -5.5), hpr=(180, 0, 0))
        backgroundL = Prop('phase_3.5/models/modules/TT_A1.bam', parent=bg,
                          pos=(-12.5, -25, -5), hpr=(180, 0, 0))
        self.backgroundR = backgroundL.copyTo(bg)
        self.backgroundR.setPos(25, -25, -5)
        backgroundLL = Prop('phase_3.5/models/modules/TT_A1.bam', parent=bg,
                           pos=(34.64, -7.9, -5.0), hpr=(-110, 0, 0))
        street_pos = [(-40, -25, -5.5), (-20, -25, -5.5), (0, -25, -5.5)]
        for pos in street_pos:
            Prop('phase_3.5/models/modules/street_modules.bam',
                 parent=render,
                 pos=pos, color=(0.9, 0.6, 0.4, 1),
                 child='street_sidewalk_40x40')

        doors = Prop('phase_4/models/modules/doors.bam', parent=render,
                     pos=(0, -16.75, -5.5), hpr=(180, 0, 0),
                     scale=(1.5, 1.5, 2.0), color=(1.0, 0.8, 0, 1),
                     child='door_single_square_ur_door')

    def load_animation(self):
        d = .5
        Sequence(
            Wait(3),
            Parallel(
                camera.posHprInterval(
                    d, (-0.23, 3.36, 1.25), (180.0, 6.78, 0.0),
                    blendType='easeInOut'),
                LerpFunc(base.camLens.set_fov, fromData=60.0, toData=85.0,
                         duration=d, blendType='noBlend'),
                Sequence(Wait(.4), Func(self.surprise))
            ),
            Wait(2.0),

            Parallel(
                Func(self.brow_raise),
                self.toon.get_part("head").posHprInterval(
                    d, (0.0, 0.0, 0.0), (39.23, 3.75, 3.75),
                    blendType='easeInOut'),
                Sequence(
                    Wait(2.3),
                    self.foreground.posHprInterval(1.0, (12.5, -20.0, -5.5),
                                      (180.0, 63.0, 0.0),
                                      blendType='easeIn'),
                ),
                LerpFunc(base.camLens.set_fov, fromData=85.0, toData=85.0,
                         duration=.5, blendType='noBlend'),
                camera.posHprInterval(.5, (-0.78, 2.57, 1.32),
                                        (198.66, 4.81, 6.75),
                                        blendType='easeInOut'),
            )
        ).start()

    def surprise(self):
        surprise_texture = loader.load_texture(
            G.MAPS_3 + "eyesSurprised.jpg",
            G.MAPS_3 + "eyesSurprised_a.rgb")
        self.toon.find('**/eyes').set_texture(surprise_texture, 1)
        self.toon.lashes.hide()

    def brow_raise(self):
        brow_raise_c = loader.load_texture(G.MAPS_3 + "brow-raise-closed.png")
        brow_raise = loader.load_texture(G.MAPS_3 + "brow-raise.png")
        closed_lashes = loader.load_model(
            G.CHAR_3 + "rabbit-lashes.bam").find("**/closed-long")

        self.toon.find('**/eyes').set_texture(brow_raise_c, 1)
        Sequence(
            Func(self.toon.right_eye.hide),
            Func(self.toon.left_eye.hide),
            Func(closed_lashes.reparent_to, self.toon.get_part("head")),
            Wait(.1),
            Func(self.toon.find('**/eyes').set_texture, brow_raise, 1),
            Func(self.toon.right_eye.show),
            Func(self.toon.left_eye.show),
            Func(self.toon.lashes.show),
            Func(closed_lashes.hide),
        ).start()


Main = Main()
Main.run()