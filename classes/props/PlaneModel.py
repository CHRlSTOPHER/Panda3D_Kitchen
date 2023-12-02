"""
Creates a procedurally generated plane in a 3D space.
"""
from panda3d.core import loadPrcFileData, NodePath, SamplerState, TransparencyAttrib
from panda3d.core import GeomVertexArrayFormat, Geom, GeomVertexFormat
from panda3d.core import GeomVertexData, GeomVertexWriter, GeomTriangles, GeomNode

# make pixel art look more clear
loadPrcFileData("", "textures-power-2 0")


class PlaneModel(NodePath):

    def __init__(self, texturePath, rows=1, columns=1, name="plane_model"):
        self.texturePath = texturePath
        self.rows = rows
        self.columns = columns

        NodePath.__init__(self, self.generate_plane_model())
        self.set_name(name)

    def generate_plane_model(self):
        array = GeomVertexArrayFormat()

        array.add_column("vertex", 3, Geom.NTFloat32, Geom.CPoint)  # Vertices
        array.add_column("texcoord", 2, Geom.NTFloat32, Geom.CTexcoord)  # UV

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
        # Divide by column/row amount to narrow down the uv scale (origin is bottom left)
        vertex.add_data3(1, 0, 1)
        texcoord.add_data2(1 / self.columns, 1 / self.rows)

        vertex.add_data3(-1, 0, 1)
        texcoord.add_data2(0, 1 / self.rows)

        vertex.add_data3(1, 0, -1)
        texcoord.add_data2(1 / self.columns, 0)

        vertex.add_data3(-1, 0, -1)
        texcoord.add_data2(0, 0)