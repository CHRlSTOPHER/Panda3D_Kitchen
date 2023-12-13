"""
Hover your mouse over a gui section on a specified side of the screen
to reveal gui that is hidden offscreen.
"""
from direct.gui.DirectGui import DirectFrame
from direct.gui import DirectGuiGlobals as DGG
from panda3d.core import TransparencyAttrib, LPoint3f

from classes.props.PlaneModel import PlaneModel

REVEAL_TASK = "reveal_task"
HIDE_TASK = "hide_task"
INCREMENT = 0.05


class RevealerGUI(DirectFrame):

    def __init__(self, icon_texture, icon_scale, icon_pos,
                 detection_texture, detection_rotation, detection_scale,
                 gui_hide_pos, parent):
        self.icon_texture = icon_texture
        self.icon_scale = icon_scale
        self.icon_pos = icon_pos
        self.icon_geom = None
        self.icon_alpha = 1

        self.detection_texture = detection_texture
        self.detection_rotation = detection_rotation
        self.detection_scale = detection_scale
        self.detection_alpha = .1

        self.gui_hide_pos = gui_hide_pos

        self.setup_icon_geom(parent)
        self.setup_detection_frame(parent)
        DirectFrame.__init__(self, parent=parent)

        self.set_pos(self.gui_hide_pos)
        self.guis = [self, self.detection_frame, self.icon_geom]

    def setup_icon_geom(self, parent):
        self.icon_geom = PlaneModel(self.icon_texture)
        self.icon_geom.reparent_to(parent)
        self.icon_geom.set_scale(self.icon_scale)
        self.icon_geom.set_pos(self.icon_pos)
        self.icon_geom.set_transparency(True)

    def setup_detection_frame(self, parent):
        self.detection_frame = DirectFrame(
                                    parent=parent,
                                    geom=PlaneModel(self.detection_texture),
                                    geom_scale=self.detection_scale,
                                    geom_hpr=(0, 0, self.detection_rotation),
                                    state=DGG.NORMAL
                                )
        self.detection_frame.bind(DGG.WITHIN, self.reveal_gui)
        self.detection_frame.bind(DGG.WITHOUT, self.hide_gui)
        self.detection_frame.set_transparency(TransparencyAttrib.MAlpha)
        self.detection_frame.set_alpha_scale(self.detection_alpha)

    def reveal_gui(self, bind_enter):
        taskMgr.remove(HIDE_TASK)
        taskMgr.add(self.reveal_gui_task, REVEAL_TASK)

    def reveal_gui_task(self, task):
        if not self.get_x() and not self.get_z():
            return task.done

        x = self.get_x()
        if x > 0: # check if x needs to move
            self.set_x(round(x - INCREMENT, 2))
        elif x < 0:
            self.set_x(round(x + INCREMENT, 2))

        z = self.get_z()
        if z > 0: # check if z needs to move
            self.set_z(round(z - INCREMENT, 2))
        elif z < 0:
            self.set_z(round(z + INCREMENT, 2))

        self.detection_alpha += INCREMENT * 1.8
        self.detection_frame.set_alpha_scale(self.detection_alpha)

        return task.again

    def hide_gui(self, bind_exit):
        taskMgr.remove(REVEAL_TASK)
        taskMgr.add(self.hide_gui_task, HIDE_TASK)

    def hide_gui_task(self, task):
        if self.get_pos() == self.gui_hide_pos:
            return task.done

        x = self.gui_hide_pos[0]
        if x > 0:
            self.set_x(round(self.get_x() + INCREMENT, 2))
        elif x < 0:
            self.set_x(round(self.get_x() - INCREMENT, 2))

        z = self.gui_hide_pos[2]
        if z > 0:
            self.set_z(round(self.get_z() + INCREMENT, 2))
        elif z < 0:
            self.set_z(round(self.get_z() - INCREMENT, 2))

        self.detection_alpha -= INCREMENT * 1.8
        self.detection_frame.set_alpha_scale(self.detection_alpha)

        return task.again

    def cleanup(self):
        taskMgr.remove(REVEAL_TASK)
        taskMgr.remove(HIDE_TASK)
        self.detection_frame.destroy()
        self.icon_geom.remove_node()
        self.destroy()