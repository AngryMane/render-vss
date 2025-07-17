#!/usr/bin/env python3
import os
from vss_tools.vspec.main import get_trees
from vss_tools.vspec.tree import VSSNode
import vss_tools.vspec.cli_options as clo
from vss_tools.vspec.model import (
    VSSDataBranch,
    VSSDataStruct,
    VSSDataSensor,
    VSSDataActuator,
    VSSDataAttribute,
    VSSDataProperty,
    get_all_model_fields,
)

import click
import shutil
from pathlib import Path
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from typing import List

from typing import Type, Callable

class Context:
    def __init__(self: 'Context') -> None:
        self.env: Environment = Environment(loader=FileSystemLoader('./templates'))
        self.sensor_header_template: Template = self.env.get_template('sensor_header.tmpl')
        self.sensor_impl_template: Template = self.env.get_template('sensor_impl.tmpl')
        self.path: List[str] = []
        self.output_dir_path: str = os.getcwd() + "/out"
        try:
            shutil.rmtree(self.output_dir_path)
        except Exception as _:
            pass
    
    def push_path(self: 'Context', name: str):
        self.path.append(name)

    def pop_path(self: 'Context'):
        self.path.pop(-1)

def visit_branch_node(context: Context, node: VSSNode, data: VSSDataBranch):
    for child in node.children:
        visit_node(context, child)

def visit_struct_node(context: Context, node: VSSNode, data: VSSDataStruct):
    print("Struct")
    pass

def visit_sensor_node(context: Context, node: VSSNode, data: VSSDataSensor):
    path = [context.output_dir_path]
    path.extend(context.path)
    output_dir: List[str] = "/".join(path[0:-1])
    output_header_file: str = "/".join(path) + ".h"
    output_impl_file: str = "/".join(path) + ".cpp"
    os.makedirs(output_dir, exist_ok=True)
    with open(output_header_file, 'x') as f:
        rendered: str = context.sensor_header_template.render(path="_".join(context.path), name=node.name)
        f.write(rendered)
    with open(output_impl_file, 'x') as f:
        rendered: str = context.sensor_impl_template.render(path="_".join(context.path), name=node.name)
        f.write(rendered)

def visit_actuator_node(context: Context, node: VSSNode, data: VSSDataActuator):
    print("Actuator")
    pass

def visit_attribute_node(context: Context, node: VSSNode, data: VSSDataAttribute):
    print("Attribute")
    pass

def visit_property_node(context: Context, node: VSSNode, data: VSSDataProperty):
    # this is only for struct 
    pass

def visit_node(context: Context, node: VSSNode):
    VISITOR_MAP: dict[Type, Callable] = {
        VSSDataBranch : visit_branch_node,
        VSSDataStruct : visit_struct_node,
        VSSDataSensor : visit_sensor_node,
        VSSDataActuator : visit_actuator_node,
        VSSDataAttribute : visit_attribute_node,
        VSSDataProperty : visit_property_node,
    }
    context.push_path(node.name)
    VISITOR_MAP[type(node.data)](context, node, node.data)
    context.pop_path()

@click.command()
@clo.vspec_opt
@clo.output_required_opt
@clo.include_dirs_opt
@clo.extended_attributes_opt
@clo.strict_opt
@clo.aborts_opt
@clo.expand_opt
@clo.overlays_opt
@clo.quantities_opt
@clo.units_opt
@clo.types_opt
@clo.types_output_opt
@clo.pretty_print_opt
@clo.extend_all_attributes_opt
def render(
    vspec: Path,
    output: Path,
    include_dirs: tuple[Path],
    extended_attributes: tuple[str],
    strict: bool,
    aborts: tuple[str],
    expand: bool,
    overlays: tuple[Path],
    quantities: tuple[Path],
    units: tuple[Path],
    types: tuple[Path],
    types_output: Path | None,
    pretty: bool,
    extend_all_attributes: bool,
):
    tree, datatype_tree = get_trees(
        vspec=vspec,
        include_dirs=include_dirs,
        aborts=aborts,
        strict=strict,
        extended_attributes=extended_attributes,
        quantities=quantities,
        units=units,
        types=types,
        overlays=overlays,
        expand=expand,
    )

    context: Context = Context()
    visit_node(context, tree)

if __name__ == "__main__":
    render()