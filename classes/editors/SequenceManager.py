from direct.interval.IntervalGlobal import Sequence
from direct.gui.DirectGui import DirectSlider, DirectButton, DGG

UPDATE_TASK = "update_slider_task"
SET_TIME_TASK = "set_time_task"


class SequenceManager(DirectSlider):

    def __init__(self, sequence):
        if sequence.getDuration() == 0:
            return

        DirectSlider.__init__(self,
            range=(0, sequence.getDuration()), pos=(0, 0, -.9),
            value=0, pageSize=.1,
        )
        self.initialiseoptions(SequenceManager)

        self.pause_button = DirectButton(text="||",
                                         command=self.toggle_button,
                                         parent=self,
                                         pos=(0, 0, .119),
                                         scale=(.24, 1, .127))
        self.back_button = DirectButton(text="<", parent=self,
                                        command=self.move_back,
                                        pos=(-.145, 0, .12),
                                        scale=(.24, 1, .205))
        self.forward_button = DirectButton(text=">", parent=self,
                                           command=self.move_forward,
                                           pos=(.145, 0, .12),
                                           scale=(.24, 1, .205))

        self.sequence = sequence
        self.duration = sequence.getDuration()
        self.time = 0
        self.pause = False
        self.manual_pause = False

        self.thumb.bind(DGG.B1PRESS, self.toggle_time)
        self.thumb.bind(DGG.B1RELEASE, self.toggle_time)

        taskMgr.doMethodLater(.01, self.update_slider, UPDATE_TASK)

    def toggle_time(self, value):
        self.pause = not self.pause
        if self.pause:
            # Pause Sequence, Start task that updates time by input
            self.sequence.pause()
            taskMgr.doMethodLater(.01, self.set_slider_time, SET_TIME_TASK)
            taskMgr.remove(UPDATE_TASK)
        else:
            # Resume Sequence, Start task that updates time by time passed
            if not self.manual_pause:
                self.sequence.resume()
                taskMgr.doMethodLater(.01, self.update_slider, UPDATE_TASK)
                taskMgr.remove(SET_TIME_TASK)

    def toggle_button(self): # toogle pause button
        self.manual_pause = not self.manual_pause
        if self.manual_pause:
            self.sequence.pause()
        else:
            self.sequence.resume()
            taskMgr.doMethodLater(.01, self.update_slider, UPDATE_TASK)
            taskMgr.remove(SET_TIME_TASK)

    def update_slider(self, task): # automatic time passage
        if not self.manual_pause: # check if user pressed pause button
            current_time = self.sequence.getT()
            self['value'] = current_time
            return task.again

    def set_slider_time(self, task): # manual user input
        self.sequence.setT(self['value'])
        return task.again

    def move_back(self):
        frame = self['value'] - (self.duration / 1000.0)
        self.set_time(frame)

    def move_forward(self):
        frame = self['value'] + (self.duration / 1000.0)
        self.set_time(frame)

    def set_time(self, frame):
        self['value'] = frame
        self.sequence.setT(frame)
