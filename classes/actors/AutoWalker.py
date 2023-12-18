"""
Actors will inherit this class to automatically transition between
animations like neutral and walk/run/etc..
Only 'neutral' and 'walk' animations are set by default.
"""
import json
import math

from panda3d.core import Vec3

from classes.globals import Globals as G

json_settings = json.loads(open(G.SETTINGS_JSON).read())
AUTO_WALKER_TASK = "auto_walker_task"


class AutoWalker():

    def __init__(self, actor, speed=13, neutral_anim="neutral",
                 walk_anim="walk",
                 run_anim=None, run_threshold=1.25, run_div=2.0):
        self.actor = actor
        self.speed = speed
        self.neutral_anim = neutral_anim
        self.walk_anim = walk_anim
        self.run_anim = run_anim
        self.run_threshold = run_threshold
        self.run_div = run_div

        self.previous_pos = actor.get_pos()
        self.previous_hpr = actor.get_hpr()
        if json_settings[G.AUTO_WALKER]:
            taskMgr.add(self.update_actor_anim_task, AUTO_WALKER_TASK)

    def update_actor_anim_task(self, task):
        self.update_actor_anim()

        self.previous_pos = self.actor.get_pos()
        self.previous_hpr = self.actor.get_hpr()
        return task.again

    def update_actor_anim(self):
        magnitude = self.find_magnitude()
        direction = 1 # 1 is the default value for no movement.
        if magnitude != 1:
            # big scale moves farther. small scale moves not as far.
            magnitude /= self.actor.get_sy()
            direction = self.find_direction()
        elif self.actor.get_hpr() != self.previous_hpr:
            magnitude = self.find_turn_rate()

        # "With both direction and magnitude! OH YEAH!!!" -Vector.
        # https://www.youtube.com/watch?v=nw9QoYL_8tI
        playrate = direction * magnitude

        self.check_anim_state(magnitude)

        if self.actor.get_current_anim() == self.run_anim:
            playrate /= self.run_div
        self.actor.set_play_rate(playrate, self.actor.get_current_anim())

    def find_direction(self): # Thanks to Ashy for being a bro :)
        forward_vector = Vec3(0, 1, 0)
        forward_vector = render.getRelativeVector(self.actor, forward_vector)
        velocity = self.actor.get_pos() - self.previous_pos
        direction = forward_vector.dot(velocity)
        if direction < 0:
            direction = -1
        else:
            direction = 1

        return direction

    def find_magnitude(self):
        # the distance formula lmao
        x1, y1, z1 = self.previous_pos
        x2, y2, z2 = self.actor.get_pos()
        magnitude = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
        if not magnitude:
            magnitude = 1 / self.speed

        return magnitude * self.speed

    def find_turn_rate(self):
        h1, p1, r1 = self.previous_hpr
        h2, p2, r2 = self.actor.get_hpr()
        magnitude = math.sqrt((h2 - h1) ** 2 + (p2 - p1) ** 2 + (r2 - r1) ** 2)
        return magnitude

    def check_anim_state(self, magnitude):
        current_anim = self.actor.get_current_anim()
        # check if actor stopped moving.
        if magnitude == 1.0 and current_anim != self.neutral_anim:
            self.loop(self.neutral_anim)
        # check if actor started moving while under run limit
        elif (magnitude < self.run_threshold
              and current_anim != self.walk_anim
              and magnitude != 1):
            self.loop(self.walk_anim)
        # check if actor started moving without a run anim (default to walking)
        elif (not self.run_anim
              and current_anim != self.walk_anim
              and magnitude != 1):
            self.loop(self.walk_anim)
        # check if actor started going over run speed limit
        elif (magnitude >= self.run_threshold
              and self.run_anim
              and current_anim != self.run_anim):
            self.loop(self.run_anim)

    def set_multiplier(self, speed):
        self.speed = speed