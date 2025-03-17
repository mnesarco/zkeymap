# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

import json
from collections.abc import Iterator
from pathlib import Path
from zkeymap.model import Layout
import re

LAYOUT_NAME = re.compile(r"(LAYOUT_)?(?P<name>.*)")


class JsonImportError(Exception):
    pass


def import_layout_json(filename: str | Path, *, name: str = "LAYOUT") -> Layout:
    """Import a layout by name if defined in the json file (QMK info.json schema)"""
    for layout in import_all_layouts_json(filename):
        if (m := LAYOUT_NAME.match(layout.name)) and m.group("name") == name:
            return layout
    msg = f"Layout {name} not found in {filename}"
    raise JsonImportError(msg)


def import_all_layouts_json(filename: str | Path) -> Iterator[Layout]:
    """Import all Layouts defined in the json file (QMK info.json schema)"""
    with Path(filename).open() as src:
        info = json.load(src)
        if layouts := info.get("layouts"):
            for name, data in layouts.items():
                yield Layout.from_dict(name, data)
