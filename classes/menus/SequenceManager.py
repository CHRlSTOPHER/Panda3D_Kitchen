from direct.gui.DirectGui import DirectSlider, DirectFrame, DirectButton, DGG
from panda3d.core import TextNode

UPDATE_TASK = "update_slider_task"
SET_TIME_TASK = "set_time_task"
START_TIME = "00:00:00"
START_DURATION = "00000"


class SequenceManager(DirectSlider):

    def __init__(self, sequence):
        if not sequence.getDuration():
            return

        DirectSlider.__init__(self, pos=(0, 0, -.9),
                              range=(0, sequence.getDuration()),
                              value=0, pageSize=.1)
        self.initialiseoptions(SequenceManager)

        self.sequence = sequence
        self.duration = sequence.getDuration()
        self.time = 0
        self.pause = False
        self.manual_pause = False

        self.load_gui(sequence)
        taskMgr.doMethodLater(.01, self.update_slider, UPDATE_TASK)

    def load_gui(self, sequence):
        # Thumb is defined in the DirectSlider class.
        self.thumb.bind(DGG.B1PRESS, self.toggle_time)
        self.thumb.bind(DGG.B1RELEASE, self.toggle_time)

        self.seq_time = DirectFrame(text=START_TIME, parent=self,
                                    pos=(.35, 0, .12), scale=(.13, 1, .13),
                                    text_align=TextNode.ALeft)
        self.track_time = DirectFrame(text=START_DURATION, parent=self,
                                      pos=(-.8, 0, .12), scale=(.13, 1, .13),
                                      text_align=TextNode.ALeft)

        self.pause_button = DirectButton(text="||", parent=self,
                                         command=self.toggle_button,
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

    def toggle_time(self, value):
        self.pause = not self.pause
        if self.pause:
            # Pause Sequence. Start task that updates time by input.
            self.sequence.pause()
            taskMgr.doMethodLater(.01, self.set_slider_time, SET_TIME_TASK)
            taskMgr.remove(UPDATE_TASK)
        else:
            # Resume Sequence. Start task that updates time by time passed.
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
            self.update_visible_time(current_time)
            return task.again

    def set_slider_time(self, task): # manual user input
        self.sequence.setT(self['value'])
        self.update_visible_time(self['value'])
        return task.again

    def move_back(self):
        # The number below needs to be changed later.
        # It doesn't scale properly for longer animations.
        frame = self['value'] - (self.duration / 1500.0)
        self.set_time(frame)

    def move_forward(self):
        frame = self['value'] + (self.duration / 1500.0)
        self.set_time(frame)

    def set_time(self, frame):
        self['value'] = frame
        self.sequence.setT(frame)
        self.update_visible_time(frame)

    def update_visible_time(self, frame):
        minutes = int(frame / 60.0)
        seconds = int(frame % 60)
        milliseconds = int(frame / .01 % 100)

        new_time = ""
        for measure in [minutes, seconds, milliseconds]:
            if measure < 10:
                measure = f"0{measure}"
            new_time += f"{measure}:"

        self.seq_time['text'] = new_time[:8]
        self.track_time['text'] = str( round(self.sequence.getT(), 2) )