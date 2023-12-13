"""
Defines a set space of the window and pushes the mouse back into it.
"""
import json

import mouse

from direct.gui.DirectGui import DirectButton

from classes.globals import Globals as G
from classes.props.PlaneModel import PlaneModel

JSON_SETTINGS = json.loads(open(G.SETTINGS_JSON).read())
LOCK_MOUSE_TASK = "lock_mouse_task"
MONITOR_RES = JSON_SETTINGS[G.MONITOR_RES]
PUSH = 10

WINDOW_LOCK_TEXTURE = "windows/mouse-lock.png"
POS = (.08, 0, .08)


class MouseWindowLock(DirectButton):

    def __init__(self):
        DirectButton.__init__(self, parent=base.a2dBottomLeft,
                              geom=PlaneModel(WINDOW_LOCK_TEXTURE),
                              scale=.07, pos=POS,
                              command=self.toggle_lock)
        self.initialiseoptions(MouseWindowLock)
        self.guis = [self]

        self.last_x = base.win.get_x_size() // 2
        self.last_y = base.win.get_y_size() // 2

        self.lock = JSON_SETTINGS[G.MOUSE_LOCK]
        self.toggle_lock()

    def lock_mouse(self, task):
        mouse_x, mouse_y = mouse.get_position()
        win_origin_x = base.win.get_properties().get_x_origin()
        win_origin_y = base.win.get_properties().get_y_origin()
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

    def toggle_lock(self):
        if not self.lock:
            taskMgr.remove(LOCK_MOUSE_TASK)
        else:
            taskMgr.add(self.lock_mouse, LOCK_MOUSE_TASK)

        self.lock = not self.lock

    def cleanup(self):
        taskMgr.remove(LOCK_MOUSE_TASK)