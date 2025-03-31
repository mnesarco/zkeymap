# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

"""
ZKeymap: QMK generators implementations.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

from zkeymap.generators.utils import path_with_suffix

if TYPE_CHECKING:
    from pathlib import Path

    from zkeymap.api import HWKey, Layout


def key_to_qmk(key: HWKey) -> dict[str, Any]:
    """
    Convert a HWKey object to a dictionary that can be serialized to JSON.

    The keys in the returned dictionary are the keys expected by the QMK
    info.json file format. The values are extracted from the HWKey object.
    Any missing optional values are replaced with 0.

    :param key: The HWKey object to convert
    :return: A dictionary with the QMK info.json format
    """
    d = {k: (v or 0) for (k, v) in asdict(key).items() if k not in {"matrix", "gpio"}}
    if key.matrix:
        d["matrix"] = key.matrix
    if key.gpio:
        d["gpio"] = key.gpio
    return d


def info_json(layout: Layout, filename: str | Path) -> None:
    """
    Generate info.json file for the given layout.

    The file contains the layout definition in the QMK info.json format.
    """
    filename = path_with_suffix(filename, "_info.json")
    with filename.open("w") as out:
        keys = [key_to_qmk(k) for k in layout.keys]
        data = {
            "layouts": {
                f"LAYOUT_{layout.name}": {
                    "layout": keys,
                },
            },
        }
        json.dump(data, out, indent=4)
