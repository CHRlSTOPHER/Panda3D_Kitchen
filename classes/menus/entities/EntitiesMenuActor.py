from direct.actor.Actor import Actor
from panda3d.core import OmniBoundingVolume
import math

from classes.startup.DisplayRegions import swap_preview_region_in
from classes.settings.FileManagement import update_database_library


class EntitiesMenuActor():

    def __init__(self):
        self.anim_list = None
        self.actor = None

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

        swap_preview_region_in(True)
        base.node_mover.set_node(self.actor)
        base.node_mover.set_clickability(False)

    def set_anims(self, anim_names, anim_dirs):
        self.anim_list = {}
        for i in range(0, len(anim_names)):
            self.anim_list[f"{anim_names[i]}"] = f"{anim_dirs[i]}"

    def save_item(self, item_name, item_location):
        save_data = {item_name: [item_location, self.anim_list]}
        update_database_library("Actor", save_data)

    def cleanup_entity(self):
        swap_preview_region_in(False)
        if self.actor:
            self.actor.cleanup()