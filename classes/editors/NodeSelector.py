"""
Hover your mouse over a node. Press left mouse button to select it.
Detect nodes using a collision ray. Move collision ray around with the mouse.
"""
from panda3d.core import (CollisionTraverser, CollisionRay, CollisionNode,
                          GeomNode, CollisionHandlerQueue)
from direct.showbase.DirectObject import DirectObject

from classes.globals import Globals as G


class NodeSelector(DirectObject):

    def __init__(self, node_mover=None):
        DirectObject.__init__(self)

        self.mouse_ray = None
        self.collision_handler = None
        self.node_mover = node_mover

        self.add_coll_ray_to_traverser()
        self.accept(G.LEFT_MOUSE_BUTTON, self.select_node)
        taskMgr.add(self.sync_ray_with_mouse_pos, G.RAY_MOUSE_TASK)

    def select_node(self):
        base.cTrav.traverse(render)
        if self.node_mover and self.collision_handler.get_num_entries() > 0:
            node = self.get_node_from_handler()
            self.node_mover.set_node(node)

    def get_node_from_handler(self):
        self.collision_handler.sort_entries()
        node = self.collision_handler.getEntry(0).get_into_node_path()
        if node == render or node.is_hidden():
            return None # Do NOT allow render or hidden nodes to be selected.

        # the special flag lets you pick nodes that aren't reparented to render
        while True:
            if (node.get_parent() == render or
                node.get_name()[0] == G.SPECIAL_NODE_IFIER_FLAG):
                break
            node = node.get_parent()

        return node

    def add_coll_ray_to_traverser(self):
        self.mouse_ray = CollisionRay()
        self.mouse_ray.set_direction(0, 1, 0)
        self.ray_collision_node = CollisionNode("mouse_ray")
        self.ray_collision_node.add_solid(self.mouse_ray)
        self.ray_collision_node.set_from_collide_mask(
            GeomNode.get_default_collide_mask())

        self.ray_node = camera.attach_new_node(self.ray_collision_node)
        self.collision_handler = CollisionHandlerQueue()

        if not base.cTrav:
            base.cTrav = CollisionTraverser("coll_traverser")
            base.cTrav.addCollider(self.ray_node, self.collision_handler)

    def sync_ray_with_mouse_pos(self, task):
        if base.mouseWatcherNode.hasMouse():
            mouse = base.mouseWatcherNode.getMouse()
            self.mouse_ray.set_from_lens(base.camNode, mouse.x, mouse.y)

        return task.again

    def cleanup(self):
        taskMgr.remove(G.RAY_MOUSE_TASK)
        self.ignore_all()