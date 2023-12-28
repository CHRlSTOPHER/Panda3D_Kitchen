from .AnimatedSprite import AnimatedSprite


class PokemonSprite(AnimatedSprite):

	def __init__(self, texturePath, rows=1, columns=1, missing_frames=0,
				 wait_time=.1, pos=(0, 0, 0), scale=(1, 1, 1),
				 parent=None, frame=None, name="a_sprite"):
		AnimatedSprite.__init__(self, texturePath, rows, columns,
								missing_frames, wait_time, pos, scale,
								parent, frame, name)