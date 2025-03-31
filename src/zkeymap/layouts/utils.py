# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

"""
ZKeymap: Layout utilities.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING

from zkeymap.private.data import HWKey
from zkeymap.private.layout import Layout, Row

if TYPE_CHECKING:
    from collections.abc import Iterator

# QMK info.json layouts are named like LAYOUT_<name>
_LAYOUT_NAME = re.compile(r"(LAYOUT_)?(?P<name>.*)")


class JsonImportError(Exception):
    """Error importing json file."""


def import_layout_json(filename: str | Path, *, name: str = "LAYOUT") -> Layout:
    """Import a layout by name if defined in the json file (QMK info.json schema)."""
    for layout in import_all_layouts_json(filename):
        if (m := _LAYOUT_NAME.match(layout.name)) and m.group("name") == name:
            return layout
    msg = f"Layout {name} not found in {filename}"
    raise JsonImportError(msg)


def import_all_layouts_json(filename: str | Path) -> Iterator[Layout]:
    """Import all Layouts defined in the json file (QMK info.json schema)."""
    with Path(filename).open() as src:
        info = json.load(src)
        if layouts := info.get("layouts"):
            for name, data in layouts.items():
                layout = Layout(name=name.removeprefix("LAYOUT_"))
                keys = [
                    HWKey(
                        x=float(k.get("x", 0)),
                        y=float(k.get("y", 0)),
                        w=float(k.get("w", 1)),
                        h=float(k.get("h", 1)),
                        rx=float(k.get("rx", 0)),
                        ry=float(k.get("ry", 0)),
                        r=float(k.get("r", 0)),
                        matrix=k.get("matrix"),
                        gpio=k.get("gpio"),
                    )
                    for k in data.get("layout", [])
                ]
                rows = []
                row = []
                for k in keys:
                    if not row:
                        row.append(k)
                        continue
                    if row[-1].x > k.x - k.w / 2:
                        rows.append(row)
                        row = [k]
                    else:
                        row.append(k)
                if row:
                    rows.append(row)
                layout / [Row(*r) for r in rows]
                yield layout
