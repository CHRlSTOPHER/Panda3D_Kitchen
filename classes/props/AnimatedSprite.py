from direct.interval.IntervalGlobal import Sequence, Func, Wait
from panda3d.core import loadPrcFileData, NodePath, SamplerState, TextureStage, TransparencyAttrib
from panda3d.core import GeomVertexArrayFormat, Geom, GeomVertexFormat
from panda3d.core import GeomVertexData, GeomVertexWriter, GeomTriangles, GeomNode

# make pixel art look more clear
loadPrcFileData("", "textures-power-2 0")

class AnimatedSprite(NodePath):

	def __init__(self, texturePath, rows=1, columns=1, missing_frames=0, wait_time=.1, name="a_sprite"):
		self.texturePath = texturePath
		self.rows = rows
		self.columns = columns
		self.missing_frames = missing_frames
		self.wait_time = wait_time
		self.uv_sequence = Sequence()

		NodePath.__init__(self, self.plane_model())
		self.set_name(name)

		# load the "animation" for the sprite. (this is just a sequence of texture offsets)
		self.load_sprite_animation()

	def plane_model(self):
		array = GeomVertexArrayFormat()

		array.add_column("vertex", 3, Geom.NTFloat32, Geom.CPoint) # Vertices
		array.add_column("texcoord", 2, Geom.NTFloat32, Geom.CTexcoord) # UV

		format = GeomVertexFormat()
		format.add_array(array)
		format = GeomVertexFormat.register_format(format)

		# Trivia: If the model changes frequently, Geom.UHDynamic can be used to not cache data
		vdata = GeomVertexData('name', format, Geom.UHStatic)
		vdata.set_num_rows(3)
		vertex = GeomVertexWriter(vdata, 'vertex')
		texcoord = GeomVertexWriter(vdata, 'texcoord')

		self.add_vertex_and_uv_coords(vertex, texcoord)

		# create GeomPrimitive object
		prim = GeomTriangles(Geom.UHStatic)
		prim.add_vertices(0, 1, 2)
		prim.add_vertices(1, 3, 2)

		# add the GeomVertexData & GeomPrimitive object to a GeomNode. Add the GeomNode to the scene.
		geom = Geom(vdata)
		geom.add_primitive(prim)
		node = GeomNode('gnode')
		node.add_geom(geom)
		plane_model = render.attach_new_node(node)

		texture = loader.load_texture(self.texturePath)
		plane_model.set_texture(texture, 1)
		# improve the texture rendering
		texture.set_magfilter(SamplerState.FT_nearest)
		plane_model.set_transparency(TransparencyAttrib.MDual)

		return plane_model

	def add_vertex_and_uv_coords(self, vertex, texcoord):
		# Divide by column/row amount to narrow down the uv scale to a single frame of the spreadsheet. (the bottom left one)
		vertex.add_data3(1, 0, 1)
		texcoord.add_data2(1/self.columns, 1/self.rows)

		vertex.add_data3(-1, 0, 1)
		texcoord.add_data2(0, 1/self.rows)

		vertex.add_data3(1, 0, -1)
		texcoord.add_data2(1/self.columns, 0)

		vertex.add_data3(-1, 0, -1)
		texcoord.add_data2(0, 0)

	def load_sprite_animation(self):
		# If there is only 1 frame, it is not a spreadsheet.
		if self.rows < 2 and self.columns < 2: return

		# multiply the columns by rows to get the max amount of frames
		# subtract by the missing frames on the bottom line to avoid blank sprites
		max_frames = (self.columns * self.rows) - self.missing_frames

		base_x_offset = 1.0 / self.columns
		base_y_offset = 1.0 / self.rows

		# we make V negative to change the position of the UV from bottom left corner to the top left corner
		u = 0
		v = -base_y_offset
		x_limit = 0

		# set UV coordinate starting position
		self.set_tex_offset(TextureStage.get_default(), u, v)

		for frame in range(0, max_frames - 1):
			# if the U coordinate goes too far to the right, reset and increment V down to the next column
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
			self.uv_sequence.append(Func(self.set_tex_offset, TextureStage.get_default(), u, v))

	def cleanup(self):
		self.uv_sequence.finish()
		self.remove_node()