"""
Creates a procedurally generated plane in a 3D space.
"""
from panda3d.core import NodePath, SamplerState, TransparencyAttrib
from panda3d.core import GeomVertexArrayFormat, Geom, GeomVertexFormat
from panda3d.core import (GeomVertexData, GeomVertexWriter, GeomTriangles,
                          GeomNode)


class PlaneModel(NodePath):

    def __init__(self, texturePath, rows=1, columns=1, scale=(1, 1, 1),
                 parent=None, name="plane_model"):
        self.texturePath = texturePath
        self.rows = rows
        self.columns = columns
        self.node_parent = parent

        NodePath.__init__(self, self.generate_plane_model())
        self.apply_texture()
        self.set_scale(scale)
        self.set_name(name)

    def generate_plane_model(self):
        array = GeomVertexArrayFormat()

        array.add_column("vertex", 3, Geom.NTFloat32, Geom.CPoint)  # Vertices
        array.add_column("normal", 3, Geom.NTFloat32, Geom.CPoint)  # Normal
        array.add_column("color", 4, Geom.NTFloat32, Geom.CTexcoord)  # Color
        array.add_column("texcoord", 2, Geom.NTFloat32, Geom.CTexcoord)  # UV

        format = GeomVertexFormat()
        format.add_array(array)
        format = GeomVertexFormat.register_format(format)

        # Trivia: If the model changes frequently, Geom.UHDynamic can be used to not cache data
        vdata = GeomVertexData('name', format, Geom.UHStatic)
        vdata.set_num_rows(4)
        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')
        texcoord = GeomVertexWriter(vdata, 'texcoord')

        self.add_vertex_and_uv_coords(vertex, texcoord, normal, color)

        prim = GeomTriangles(Geom.UHStatic)
        prim.add_vertices(0, 1, 2)
        prim.add_vertices(1, 3, 2)

        # add the GeomVertexData & GeomPrimitive object to a GeomNode.
        # Return the GeomNode as NodePath's __init__ arg.
        geom = Geom(vdata)
        geom.add_primitive(prim)
        node = GeomNode('gnode')
        node.add_geom(geom)
        if self.node_parent:
            node = self.node_parent.attach_new_node(node)

        return node

    def add_vertex_and_uv_coords(self, vertex, texcoord, normal, color):
        # Divide by column/row to narrow the uv scale (origin is bottom left)
        vertex.add_data3(1, 0, 1)
        normal.add_data3(0, 0, 1)
        color.add_data4(1, 1, 1, 1)
        texcoord.add_data2(1 / self.columns, 1 / self.rows)

        vertex.add_data3(-1, 0, 1)
        normal.add_data3(0, 0, 1)
        color.add_data4(1, 1, 1, 1)
        texcoord.add_data2(0, 1 / self.rows)

        vertex.add_data3(1, 0, -1)
        normal.add_data3(0, 0, 1)
        color.add_data4(1, 1, 1, 1)
        texcoord.add_data2(1 / self.columns, 0)

        vertex.add_data3(-1, 0, -1)
        normal.add_data3(0, 0, 1)
        color.add_data4(1, 1, 1, 1)
        texcoord.add_data2(0, 0)

    def apply_texture(self):
        if isinstance(self.texturePath, list):
            texture = loader.load_texture(self.texturePath[0],
                                          self.texturePath[1])
        else:
            texture = loader.load_texture(self.texturePath)
        self.set_texture(texture, 1)
        # improve the texture rendering
        texture.set_magfilter(SamplerState.FT_nearest)
        self.set_transparency(TransparencyAttrib.MDual)