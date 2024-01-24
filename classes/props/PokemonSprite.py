from .AnimatedSprite import AnimatedSprite


class PokemonSprite(AnimatedSprite):

	def __init__(self, texturePath, rows=1, columns=1,
				 pos=(0, 0, 0), scale=(1, 1, 1), color=(1, 1, 1, 1),
				 parent=None, frame=None, name="p_sprite",
				 wait_time=.1, missing_frames=0):
		AnimatedSprite.__init__(self, texturePath, rows, columns,
								pos, scale, parent, frame, name,
								missing_frames, wait_time)