from .AnimatedSprite import AnimatedSprite


class PokemonSprite(AnimatedSprite):

	def __init__(self, texturePath, rows=1, columns=1, missing_frames=0,
				 wait_time=.1, scale=(1, 1, 1), parent=None, name="a_sprite"):
		AnimatedSprite.__init__(self, texturePath, rows, columns,
								missing_frames, wait_time, scale, parent, name)