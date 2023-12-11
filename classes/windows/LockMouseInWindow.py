"""
Defines a set space of the window and pushes the mouse back into it.
"""
import json

import mouse

from classes.globals import Globals as G

JSON_SETTINGS = json.loads(open(G.SETTINGS_JSON).read())
LOCK_MOUSE_TASK = "lock_mouse_task"
MONITOR_RES = JSON_SETTINGS[G.MONITOR_RES]
PUSH = 10


class LockMouseInWindow():

    def __init__(self):
        self.last_x = base.win.get_x_size() // 2
        self.last_y = base.win.get_y_size() // 2
        taskMgr.add(self.lock_mouse, LOCK_MOUSE_TASK)

    def lock_mouse(self, task):
        mouse_x, mouse_y = mouse.get_position()
        win_origin_x = base.win.getProperties().getXOrigin()
        win_origin_y = base.win.getProperties().getYOrigin()
        win_size_x, win_size_y = [base.win.get_x_size(), base.win.get_y_size()]

        x_barriers = [win_origin_x, win_origin_x + win_size_x]
        y_barriers = [win_origin_y, win_origin_y + win_size_y]

        if mouse_x < x_barriers[0]:
            mouse.move(self.last_x + PUSH, self.last_y, absolute=True)
        elif mouse_x > x_barriers[1]:
            mouse.move(self.last_x - PUSH, self.last_y, absolute=True)
        else:
            self.last_x = mouse_x

        if mouse_y < y_barriers[0]:
            mouse.move(self.last_x, self.last_y + PUSH, absolute=True)
        elif mouse_y > y_barriers[1]:
            mouse.move(self.last_x, self.last_y - PUSH, absolute=True)
        else:
            self.last_y = mouse_y

        return task.cont

    def cleanup(self):
        taskMgr.remove(LOCK_MOUSE_TASK)