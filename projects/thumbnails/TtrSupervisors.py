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

from direct.interval.IntervalGlobal import (Track, ActorInterval, Wait,
                                            Sequence, Func, Parallel)
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Fog

from classes.editors.MasterEditor import MasterEditor
from classes.globals import Globals as G
from classes.actors.Suit import Suit
from classes.editors.MasterEditor import MasterEditor


class Thumbnail(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        base.disable_mouse()
        camera.set_pos_hpr(11.09, 3.66, 4.51, -245.42, 3.84, -4.0)
        base.camLens.set_fov(52.0)

        self.load_actors()
        self.load_scene()
        sequence = self.load_animation()
        sequence.start()

        self.editor = MasterEditor(rot_cam=True, mouse_lock=False,
                                   sequence=sequence)

    def load_old_actors(self):
        self.bp = Suit('cp', render)
        self.lc = Suit('lc', render)
        self.ma = Suit('ma', render)
        self.ff = Suit('ff', render)

        self.bp.set_pos_hpr(5.88, -0.33, 0.0, 0.0, 0.0, 0.0)
        self.bp.head.find('**/ttr_m_ene_bossbotClubPresident').set_pos_hpr(
            0.0, 0.0, 0.0, -49.23, -9.0, -6.0)
        self.ma.set_pos_hpr(0.71, -0.96, 0.0, -23.25, 0.0, 0.0)
        self.ma.head.find('**/ttr_m_ene_cashbotAuditor').set_pos_hpr(
            0.0, 0.0, 0.0, -44.25, -12.75, -12.0)
        self.ff.set_pos_hpr(-1.78, 0.53, 0.0, -27.75, 0.0, 0.0)
        self.ff.head.find('**/ttr_m_ene_sellbotForeman').set_pos_hpr(
            0.0, 0.0, 0.0, -49.5, -16.5, -1.5)
        self.lc.set_pos_hpr(-4.89, 1.69, 0.0, -43.5, 0.0, 0.0)
        self.lc.head.find('**/ttr_m_ene_lawbotClerk').set_pos_hpr(
            0.0, 0.0, 0.0, -51.5, -21.32, 0.0)

    def load_actors(self):
        f_pose = 0
        m_pose = 0
        l_pose = 0
        c_pose = 0

        self.ff = Suit('ff', render, suit_name='~self.ff', model=2)
        self.ff.get_ttr_manager_anims()

        self.ma = Suit('ma', render, suit_name='~self.ma', model=2)
        self.ma.get_ttr_manager_anims()

        self.lc = Suit('lc', render, suit_name='~self.lc', model=2)
        self.lc.get_ttr_manager_anims()

        self.cp = Suit('cp', render, suit_name='~self.cp', model=2)
        self.cp.get_ttr_manager_anims()

    def load_scene(self):
        room = loader.load_model("phase_5/models/cogdominium/ttr_m_ara_cbr_barrelRoom.bam")
        room.reparent_to(render)

        myFog = Fog("Barrel Room Fog")
        myFog.setColor(.05, .025, .025)
        myFog.setExpDensity(.01)
        render.setFog(myFog)

        room.set_pos_hpr(-4.21, -2.42, -5.63, -95.27, -4.33, 2.25)
        room.set_pos_hpr(-4.21, -2.42, -5.63, -95.27, 0, 0)

    def load_animation(self):
        base.camLens.set_fov(85.0)
        self.ff.set_pos_hpr(12.93, -3.76, -5.62, 149.45, 0.0, 0.0)
        self.lc.set_pos_hpr(2.65, -7.47, -5.63, -57.75, 0.0, 0.0)
        self.ma.set_pos_hpr(-7.79, -3.62, -5.64, 76.75, 0.0, 0.0)
        self.cp.set_pos_hpr(-21.45, -4.62, -5.71, 1.73, 0.0, 0.0)

        actor_track = Track(
            (0, ActorInterval(self.ff, 'chop-chop')),
            (2.5, ActorInterval(self.lc, 'shhh')),
            (4.0, ActorInterval(self.ma, 'promoting', endTime=4)),
            (8.0, ActorInterval(self.cp, 'jump', endTime=4.5)),
            (12.5, Wait(0))
        )
        camera_sequence = Sequence(
            Func(camera.set_pos_hpr, 11.86, -8.28, 1.98, -12.95, -12.8, 5.0),
            Wait(1),
            Func(camera.set_pos_hpr, 12.03, -9.6, -2.39, -7.58, 23.56, 5.0),
            Wait(.8),
            Func(camera.set_pos_hpr, 11.86, -8.28, 1.98, -12.95, -12.8, 5.0),
            Wait(.25),
            camera.posHprInterval(.5, (4.72, -4.85, 1.27),
                                    (141.17, 11.44, 5.0),blendType='easeIn'),
            Wait(.5),
            camera.posHprInterval(.5, (7.68, -1.94, -1.3),
                                    (145.51, 14.01, 5.0),blendType='easeInOut'),
            Wait(.6),
            Func(camera.set_pos_hpr, -10.59, -3.04, 0.62, 274.22, -12.8, 5.0),
            Wait(2.0),
            camera.posHprInterval(.5, (-15.22, -3.06, 1.9),
                                    (271.53, -15.74, 5.0), blendType='easeInOut'),
        )

        return Parallel(actor_track, camera_sequence)


Thumbnail().run()