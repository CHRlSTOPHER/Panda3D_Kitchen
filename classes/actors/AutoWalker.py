import json
import math

from classes.globals import Globals as G

json_settings = json.loads(open(G.SETTINGS_JSON).read())
print(json_settings)


class AutoWalker():

    def __init__(self, actor, multiplier=13):
        self.actor = actor
        self.multiplier = multiplier
        self.previous_pos = actor.get_pos()
        self.previous_hpr = actor.get_hpr()
        self.walking = False
        if json_settings[G.AUTO_WALKER]:
            taskMgr.add(self.toggle_actor_anim_state, G.AUTO_WALKER_TASK)

    def toggle_actor_anim_state(self, task):
        # If actor has moved since last frame...
        if self.actor.get_pos() != self.previous_pos or self.actor.get_hpr() != self.previous_hpr:
            self.walk()
        else:
            self.neutral()

        # Figure out the playrate based
        self.direction_and_magnitude() # https://www.youtube.com/watch?v=nw9QoYL_8tI

        self.previous_pos = self.actor.get_pos()
        self.previous_hpr = self.actor.get_hpr()
        return task.again

    def walk(self):
        # If actor is not yet walking and is ONLY in the neutral animation.
        # (We don't want to interrupt other animations ex: slip-forward)
        if not self.walking and self.actor.get_current_anim() == "neutral":
            self.walking = True
            self.actor.loop("walk")

    def neutral(self):
        # If actor has JUST stopped walking and is ONLY in the walk animation.
        if self.walking and self.actor.get_current_anim() == "walk":
            self.walking = False
            self.actor.loop("neutral")

    # "With both direction and magnitude! OH YEAH!!!" -Vector
    def direction_and_magnitude(self):
        # the distance formula lmao (this is the magnitude / force of strength)
        x1, y1, z1 = self.previous_pos
        x2, y2, z2 = self.actor.get_pos()

        coords = (x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2
        distance = math.sqrt(coords)

        if not distance: distance = 1 / self.multiplier
        current_anim = self.actor.get_current_anim()
        self.actor.set_play_rate(distance * self.multiplier, current_anim)

        # then we have to figure out the direction. WIP

    def set_multiplier(self, multiplier):
        self.multiplier = multiplier