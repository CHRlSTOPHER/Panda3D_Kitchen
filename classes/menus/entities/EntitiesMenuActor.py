from direct.actor.Actor import Actor
from panda3d.core import OmniBoundingVolume
import random
import math

from classes.startup.DisplayRegions import swap_preview_region_in
from classes.settings.FileManagement import update_database_library


class EntitiesMenuActor():

    def __init__(self):
        self.anim_list = None
        self.actor = None
        self.rng_button = None
        self.last_anim = None

    def load_entity(self, directory):
        self.actor = Actor()
        self.actor.load_model(directory)
        if self.anim_list:
            # load anims and set the actor to the first frame of the first anim
            self.actor.load_anims(self.anim_list)
            first_anim = next(iter(self.anim_list))
            self.actor.pose(first_anim, 3)
        self.actor.reparent_to(base.preview_render)
        # get y2 and y1 for the distance formula
        y2 = self.actor.get_tight_bounds()[0][1]
        y1 = self.actor.get_tight_bounds()[1][1]
        distance = math.sqrt((y2 - y1) ** 2)
        self.actor.set_y(distance * 1.5)
        self.actor.node().set_bounds(OmniBoundingVolume())
        self.actor.node().set_final(1)

        if self.anim_list:
            self.actor.load_anims(self.anim_list)
            first_anim = next(iter(self.anim_list))
            self.actor.pose(first_anim, 3)

        self.rng_button.show()
        swap_preview_region_in(True)
        base.node_mover.set_node(self.actor)
        base.node_mover.set_clickability(False)

    def set_anims(self, anim_names, anim_dirs):
        self.anim_list = {}
        for i in range(0, len(anim_names)):
            self.anim_list[f"{anim_names[i]}"] = f"{anim_dirs[i]}"

    def randomize_anim(self):
        anim = self.last_anim
        if self.anim_list:
            # keep going until a new anim is picked -- rarely loops
            while anim == self.last_anim:
                anim, location = random.choice(list(self.anim_list.items()))
                anim_control = self.actor.get_anim_control(anim)
                frames = anim_control.get_num_frames()
                random_frame = random.choice([0, frames])
                self.actor.pose(anim, random_frame)

    def define_rng_button(self, button):
        self.rng_button = button
        self.rng_button['command'] = self.randomize_anim

    def save_item(self, item_name, item_location):
        save_data = {item_name: [item_location, self.anim_list]}
        update_database_library("Actor", save_data)

    def cleanup_entity(self):
        swap_preview_region_in(False)
        if self.actor:
            self.actor.cleanup()