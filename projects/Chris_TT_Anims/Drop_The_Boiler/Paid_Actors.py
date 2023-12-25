from enum import Enum

from classes.actors.BoilerBoss import BoilerBoss
from classes.actors.Toon import Toon
from classes.globals.ToonColors import ToonColors

TC = ToonColors


class Actors(Enum):

    # Toons
    pink = Toon(parent=render, gender='m',
                toon_name="~Actors.pink",
                head='dss', torso='s', legs='m', bottom='shorts',
                shirt_t=8, sleeve_t=8, bottom_t=7,
                head_color=TC.BRIGHT_RED,
                shirt_color=TC.BRIGHT_RED,
                sleeve_color=TC.BRIGHT_RED,
                arm_color=TC.BRIGHT_RED,
                glove_color=TC.WHITE,
                leg_color=TC.BRIGHT_RED,
                bottom_color=TC.BRIGHT_RED)

    # Suits / Boss Suits
    boiler = BoilerBoss(name="~Actors.boiler")