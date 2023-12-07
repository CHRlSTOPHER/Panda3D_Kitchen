import json
import math

from classes.globals import Globals as G

json_settings = json.loads(open(G.SETTINGS_JSON).read())
print(json_settings)

H_REVERSE_START = 45
H_REVERSE_END = 225
AUTO_WALKER_TASK = "auto_walker_task"


class AutoWalker():

    def __init__(self, actor, speed=13, run_anim="run", run_threshold=1.5):
        self.actor = actor
        self.speed = speed
        self.run_anim = run_anim
        self.run_threshold = run_threshold

        self.previous_pos = actor.get_pos()
        self.previous_hpr = actor.get_hpr()
        self.walking = False
        if json_settings[G.AUTO_WALKER]:
            taskMgr.add(self.toggle_actor_anim_state, AUTO_WALKER_TASK)

    def toggle_actor_anim_state(self, task):
        if (self.actor.get_pos() != self.previous_pos or
                self.actor.get_hpr() != self.previous_hpr):
            self.move_anim()
        else:
            self.neutral_anim()

        self.update_playrate()

        self.previous_pos = self.actor.get_pos()
        self.previous_hpr = self.actor.get_hpr()
        return task.again

    def move_anim(self):
        if not self.walking and self.actor.get_current_anim() == "neutral":
            self.walking = True
            self.actor.loop("walk")

    def neutral_anim(self):
        if not self.walking:
            return

        for anim in G.AUTOWALKER_MOVE_ANIMS: # check for movement animations
            if self.actor.get_current_anim() == anim:
                self.walking = False
                self.actor.loop("neutral")

    def update_playrate(self):
        x1, y1, z1 = self.previous_pos
        x2, y2, z2 = self.actor.get_pos()

        magnitude = self.find_magnitude(x1, y1, z1, x2, y2, z2)
        direction = 1 # default to 1 if there is no movement.
        if magnitude != 1:
            direction = self.find_direction(x1, y1, z1, x2, y2, z2)

        # "With both direction and magnitude! OH YEAH!!!" -Vector.
        # https://www.youtube.com/watch?v=nw9QoYL_8tI
        playrate = direction * magnitude
        self.actor.set_play_rate(playrate, self.actor.get_current_anim())

    def find_direction(self, x1, y1, z1, x2, y2, z2):
        vector = (x2 - x1) + (y2 - y1) + (z2 - z1)
        if vector < 0:
            vector = -1
        else:
            vector = 1

        h = self.actor.get_h() % 360
        if h > H_REVERSE_START and h < H_REVERSE_END:
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