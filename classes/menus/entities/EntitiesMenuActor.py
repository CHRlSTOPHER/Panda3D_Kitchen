from direct.actor.Actor import Actor
from panda3d.core import OmniBoundingVolume

from classes.startup.DisplayRegions import swap_preview_region_in


class EntitiesMenuActor():

    def __init__(self):
        self.anim_list = None
        self.actor = None

    def load_entity(self, directory):
        self.actor = Actor()
        self.actor.load_model(directory)
        self.actor.reparent_to(base.preview_render)
        self.actor.node().set_bounds(OmniBoundingVolume())
        self.actor.node().set_final(1)
        self.actor.set_y(5)
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
            self.anim_list[anim_names[i]] = anim_dirs[i]

    def cleanup_entity(self):
        swap_preview_region_in(False)
        if self.actor:
            self.actor.cleanup()