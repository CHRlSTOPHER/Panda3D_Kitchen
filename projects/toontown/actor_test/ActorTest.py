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
Tests functionality of actors.
"""
from classes.settings import Settings

from direct.showbase.ShowBase import ShowBase

from classes.actors.Suit import Suit
from classes.actors.Toon import Toon
from classes.editors.MasterEditor import MasterEditor
from classes.globals import Globals as G


class ActorTest(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.accept(G.ESCAPE, exit)
        self.master_editor = MasterEditor()

        # self.setup_cogs()
        self.setup_toons()

    def setup_cogs(self):
        self.flunky = Suit("f", render, suit_name="~self.flunky")
        self.penny = Suit("pp", render, suit_name="~self.penny")
        self.cheese = Suit("tbc", render, suit_name="~self.cheese")

        camera.set_pos_hpr(30.71, 3.51, 4.33, 76.28, -0.54, 0.0)

    def setup_toons(self):
        self.dog = Toon(parent=render, gender='m',
                         toon_name="~self.dog",
                         head='dss', head_c=2,
                         torso='s', shirt_t=8, shirt_c=2,
                         sleeve_t=8, sleeve_c=2, arm_c=2, glove_c=0,
                         legs='m', leg_c=2,
                         bottom='shorts', bottom_t=7, bottom_c=2)

        self.cat = Toon(parent=render, gender='m',
                         toon_name="~self.cat",
                         head='css', head_c=2,
                         torso='s', shirt_t=8, shirt_c=2,
                         sleeve_t=8, sleeve_c=2, arm_c=2, glove_c=0,
                         legs='m', leg_c=2,
                         bottom='shorts', bottom_t=7, bottom_c=2)

        self.horse = Toon(parent=render, gender='m',
                         toon_name="~self.horse",
                         head='hss', head_c=2,
                         torso='s', shirt_t=8, shirt_c=2,
                         sleeve_t=8, sleeve_c=2, arm_c=2, glove_c=0,
                         legs='m', leg_c=2,
                         bottom='shorts', bottom_t=7, bottom_c=2)

        self.mouse = Toon(parent=render, gender='m',
                         toon_name="~self.mouse",
                         head='mss', head_c=2,
                         torso='s', shirt_t=8, shirt_c=2,
                         sleeve_t=8, sleeve_c=2, arm_c=2, glove_c=0,
                         legs='m', leg_c=2,
                         bottom='shorts', bottom_t=7, bottom_c=2)

        self.rabbit = Toon(parent=render, gender='m',
                         toon_name="~self.rabbit",
                         head='rss', head_c=2,
                         torso='s', shirt_t=8, shirt_c=2,
                         sleeve_t=8, sleeve_c=2, arm_c=2, glove_c=0,
                         legs='m', leg_c=2,
                         bottom='shorts', bottom_t=7, bottom_c=2)

        self.duck = Toon(parent=render, gender='m',
                         toon_name="~self.duck",
                         head='fss', head_c=2,
                         torso='s', shirt_t=8, shirt_c=2,
                         sleeve_t=8, sleeve_c=2, arm_c=2, glove_c=0,
                         legs='m', leg_c=2,
                         bottom='shorts', bottom_t=7, bottom_c=2)

        self.monkey = Toon(parent=render, gender='m',
                         toon_name="~self.monkey",
                         head='pss', head_c=2,
                         torso='s', shirt_t=8, shirt_c=2,
                         sleeve_t=8, sleeve_c=2, arm_c=2, glove_c=0,
                         legs='m', leg_c=2,
                         bottom='shorts', bottom_t=7, bottom_c=2)

        self.bear = Toon(parent=render, gender='m',
                         toon_name="~self.bear",
                         head='bss', head_c=2,
                         torso='s', shirt_t=8, shirt_c=2,
                         sleeve_t=8, sleeve_c=2, arm_c=2, glove_c=0,
                         legs='m', leg_c=2,
                         bottom='shorts', bottom_t=7, bottom_c=2)

        self.pig = Toon(parent=render, gender='m',
                         toon_name="~self.pig",
                         head='sss', head_c=2,
                         torso='s', shirt_t=8, shirt_c=2,
                         sleeve_t=8, sleeve_c=2, arm_c=2, glove_c=0,
                         legs='m', leg_c=2,
                         bottom='shorts', bottom_t=7, bottom_c=2)

        self.croc = Toon(parent=render, gender='m',
                         toon_name="~self.croc",
                         head='ass', head_c=2,
                         torso='s', shirt_t=8, shirt_c=2,
                         sleeve_t=8, sleeve_c=2, arm_c=2, glove_c=0,
                         legs='m', leg_c=2,
                         bottom='shorts', bottom_t=7, bottom_c=2)

        self.deer = Toon(parent=render, gender='m',
                         toon_name="~self.dear",
                         head='qss', head_c=2,
                         torso='s', shirt_t=8, shirt_c=2,
                         sleeve_t=8, sleeve_c=2, arm_c=2, glove_c=0,
                         legs='m', leg_c=2,
                         bottom='shorts', bottom_t=7, bottom_c=2)

        self.deer.change_muzzle('smile')

        toons = [self.dog, self.cat, self.horse, self.mouse, self.rabbit,
                 self.duck, self.monkey, self.bear, self.pig,
                 self.croc, self.deer]
        x = 0
        for toon in toons:
            toon.set_x(x)
            x += 3.5

        camera.set_pos_hpr(-4.56, 4.14, 4.65, 227.25, -16.24, 0.0)


app = ActorTest()
app.run()