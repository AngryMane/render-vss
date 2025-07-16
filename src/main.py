#!/usr/bin/env python3
from vss_tools.vspec.main import get_trees
from vss_tools.vspec.tree import VSSNode
import vss_tools.vspec.cli_options as clo

import click
import json
from pathlib import Path
from typing import Any

def get_data(node: VSSNode, with_extra_attributes: bool = True, extended_attributes: tuple[str, ...] = ()):
    data = node.data.as_dict(with_extra_attributes, extended_attributes=extended_attributes)
    if len(node.children) > 0:
        data["children"] = {}
    for child in node.children:
        data["children"][child.name] = get_data(child)
    return data

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
    indent = None
    if pretty:
        indent = 2

    signals_data = {tree.name: get_data(tree, extend_all_attributes, extended_attributes)}


if __name__ == "__main__":
    render()