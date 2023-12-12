"""
Actors will inherit this class to automatically transition between
animations like neutral and walk/run/etc..
Only 'neutral' and 'walk' animations are set by default.
"""
import json
import math

from classes.globals import Globals as G

json_settings = json.loads(open(G.SETTINGS_JSON).read())

ROTATION_REVERSE_START = 45
ROTATION_REVERSE_END = 225
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
        x1, y1, z1 = self.previous_pos
        x2, y2, z2 = self.actor.get_pos()

        magnitude = self.find_magnitude(x1, y1, z1, x2, y2, z2)
        direction = 1 # default to 1 if there is no movement.
        if magnitude != 1:
            direction = self.find_direction(x1, y1, z1, x2, y2, z2)

        # "With both direction and magnitude! OH YEAH!!!" -Vector.
        # https://www.youtube.com/watch?v=nw9QoYL_8tI
        playrate = direction * magnitude

        current_anim = self.actor.get_current_anim()
        if magnitude == 1.0 and current_anim != self.neutral_anim:
            self.loop(self.neutral_anim)
        elif magnitude >= self.run_threshold and current_anim != self.run_anim:
            if self.run_anim:
                self.loop(self.run_anim)
        elif (magnitude < self.run_threshold and current_anim != self.walk_anim
              and magnitude != 1):
            self.loop(self.walk_anim)

        if self.actor.get_current_anim() == self.run_anim:
            playrate /= self.run_div
        self.actor.set_play_rate(playrate, self.actor.get_current_anim())

    def find_direction(self, x1, y1, z1, x2, y2, z2):
        vector = (x2 - x1) + (y2 - y1) + (z2 - z1)
        if vector < 0:
            vector = -1
        else:
            vector = 1

        h = self.actor.get_h() % 360
        if h > ROTATION_REVERSE_START and h < ROTATION_REVERSE_END:
            vector *= -1

        return vector

    def find_magnitude(self, x1, y1, z1, x2, y2, z2):
        # the distance formula lmao
        magnitude = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
        if not magnitude:
            magnitude = 1 / self.speed

        return magnitude * self.speed

    def set_multiplier(self, speed):
        self.speed = speed