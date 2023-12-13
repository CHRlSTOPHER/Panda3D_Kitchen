"""
Takes a procedurally generated plane and applies a texture offset sequence.
(The texture uv position changes by a set amount each frame
to trick the eye into thinking movement is occurring)
"""
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from panda3d.core import TextureStage

from .PlaneModel import PlaneModel


class AnimatedSprite(PlaneModel):

	def __init__(self, texturePath, rows=1, columns=1, missing_frames=0,
				 wait_time=.1, scale=(1, 1, 1), parent=None, name="a_sprite"):
		PlaneModel.__init__(self, texturePath, rows, columns,
							scale, parent, name)
		self.missing_frames = missing_frames
		self.wait_time = wait_time
		self.uv_sequence = Sequence()

		# load the "animation" for the sprite. (a sequence of texture offsets)
		self.load_sprite_animation()

	def load_sprite_animation(self):
		# If there is only 1 frame, it is not a spreadsheet.
		if self.rows < 2 and self.columns < 2: return

		# multiply the columns by rows to get the max amount of frames
		# subtract by the missing frames on the bottom line to avoid blanks
		max_frames = (self.columns * self.rows) - self.missing_frames

		base_x_offset = 1.0 / self.columns
		base_y_offset = 1.0 / self.rows

		# make V negative to change the position of the UV from
		# the bottom left corner to the top left corner
		u = 0
		v = -base_y_offset
		x_limit = 0

		# set UV coordinate starting position
		self.set_tex_offset(TextureStage.get_default(), u, v)

		for frame in range(0, max_frames - 1):
			# if the U coordinate goes too far to the right, reset and go down.
			if x_limit > self.columns - 2:
				u = 0
				v -= base_y_offset
				x_limit = 0
			# otherwise, let the U coordinate move the offset to the right
			else:
				u += base_x_offset
				x_limit += 1

			# add a small pause between frames
			self.uv_sequence.append(Wait(self.wait_time))
			self.uv_sequence.append(Func(self.set_tex_offset,
										 TextureStage.get_default(), u, v))

	def cleanup(self):
		self.uv_sequence.finish()