"""
Set a Node to move and rotate. Modify with keyboard inputs.
The rate at which you can effect them can also be influenced by keyboard inputs.
"""
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from panda3d.core import NodePath
import json

from classes.globals import Globals as G

KBS = json.loads(open(G.KEYBINDINGS_JSON).read())


class NodeMover(NodePath, DirectObject):

    def __init__(self, node=None):
        DirectObject.__init__(self)
        self.move_options = None
        self.move_speed = G.NM_BASE_MOVE_RATE
        self.turn_speed = G.NM_BASE_TURN_RATE
        self.allow_click = True
        self.allow_tasks = True

        # As a shortcut, press the assigned key below to set the camera as the node being moved by the node mover.
        self.accept(G.MIDDLE_MOUSE_BUTTON, self.set_node, extraArgs=[camera])
        self.set_node(node)
        self.listen_for_key_inputs()

    def set_node(self, node):
        if node and self.allow_click:
            NodePath.__init__(self, node)
            self.set_move_options()

            # Make a little sequence to show it was selected.
            og_color_scale = node.get_color_scale()
            node.set_color_scale(G.RED)
            Sequence(
                Func(self.change_clickability), Wait(.3),
                Func(node.set_color_scale, *og_color_scale), Func(self.change_clickability)
            ).start()

    def set_move_options(self):
        self.move_options = [
            [self.setY, self.get_move_speed, 1],
            [self.setY, self.get_move_speed, -1],
            [self.setX, self.get_move_speed, -1],
            [self.setX, self.get_move_speed, 1],
            [self.setZ, self.getZ, self.get_move_speed, 1],
            [self.setZ, self.getZ, self.get_move_speed, -1],

            [self.setP, self.getP, self.get_turn_speed, 1],
            [self.setP, self.getP, self.get_turn_speed, -1],
            [self.setH, self.getH, self.get_turn_speed, 1],
            [self.setH, self.getH, self.get_turn_speed, -1],
            [self.setR, self.getR, self.get_turn_speed, 1],
            [self.setR, self.getR, self.get_turn_speed, -1],
        ]

    def listen_for_key_inputs(self):
        index = 0
        # Add input detection for node transformations.
        for key in G.NM_TRANSFORM_INPUTS:
            self.accept(KBS[key], self.initiate_movement, extraArgs=[key, index])
            self.accept(KBS[key] + "-up", self.stop_move_task, extraArgs=[key])
            index += 1

        # Add input detection for speeds adjustments.
        for key, speed in G.NM_SPEEDS:
            self.accept(f"{KBS[key]}", self.change_speed, extraArgs=[speed])
            self.accept(f"{KBS[key]}-up", self.change_speed, extraArgs=[1])

    def initiate_movement(self, key, direction):
        taskMgr.add(self.move_task, f"move_{key}", extraArgs=[key, direction], appendTask=True)

    def move_task(self, key, index, task):
        if not self.move_options or not self.allow_tasks:
            return task.done

        move_option = self.move_options[index]
        set_transform = move_option[0]

        if set_transform == self.setX or set_transform == self.setY: # These transformations need relative movement.
            get_speed, direction = move_option[1], move_option[2]
            set_transform(self, get_speed() * direction)
        else:
            get_transform, get_speed, direction = move_option[1], move_option[2], move_option[3]
            set_transform(get_transform() + get_speed() * direction)

        return task.again

    def stop_move_task(self, key):
        taskMgr.remove(f"move_{key}")

    def change_speed(self, speed):
        self.move_speed = G.NM_BASE_MOVE_RATE / speed
        self.turn_speed = G.NM_BASE_TURN_RATE / speed

    def change_clickability(self):
        self.allow_click = not self.allow_click

    def get_move_speed(self):
        return self.move_speed

    def get_turn_speed(self):
        return self.turn_speed

    def cleanup(self):
        self.allow_tasks = False
        self.ignore_all()