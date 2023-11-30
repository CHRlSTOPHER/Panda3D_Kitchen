"""
Prints various bits of information about the currently selected node.
"""
from dataclasses import dataclass
import re

from classes.globals import Globals as G

# Use this function to provide the necessary amount of args required for NodeDataPrinter.
def get_transform_data(node):
    string_data = [
        node.get_name()
    ]

    float_data = [
        node.get_x(), node.get_y(), node.get_z(),
        node.get_h(), node.get_p(), node.get_r(),
        node.get_sx(), node.get_sy(), node.get_sz(),
        base.camLens.get_fov()[0],
    ]
    rounded_data = [round(data, 2) for data in float_data]

    return string_data + rounded_data


@dataclass
class TransformFunctionPrinter():
    name: str
    x: float
    y: float
    z: float
    h: float
    p: float
    r: float
    sx: float
    sy: float
    sz: float
    fov: float

    def print_transform_func(self, index):
        unformatted_string = G.TRANSFORM_FUNCTION_STRINGS[index]
        class_attribute_dict = vars(self)

        required_arg_names = re.findall(G.FIND_ARGS_IN_CURLY_BRACES, unformatted_string)
        required_arg_dict = {}
        for key in required_arg_names:
            required_arg_dict[key] = class_attribute_dict[key]

        formatted_string = unformatted_string.format(**required_arg_dict)
        print(formatted_string)

    def update_transform_data(self, node):
        new_node_values = get_transform_data(node)
        class_attributes = [var for var in vars(self)]

        for index in range(0, len(class_attributes)):
            setattr(self, class_attributes[index], new_node_values[index])