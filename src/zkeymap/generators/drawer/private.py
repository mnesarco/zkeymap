# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

"""
ZKeymap: keymap-drawer layout generator implementation.
"""

import sys
from pathlib import Path

from zkeymap.api import Layout, env, logger
from zkeymap.generators.svg.private import display
from zkeymap.generators.utils import path_with_suffix


def svg(layout: Layout, filename: str | Path, config_file: str | Path | None = None) -> None:
    """
    Generate an SVG file representing the keyboard layout using the keymap-drawer library.

    This function utilizes the keymap-drawer library to convert a given keyboard layout
    into an SVG format. It takes an optional configuration file to customize the rendering
    settings. If the configuration file is not provided or found, default settings are used.

    :param layout: The keyboard layout to render.
    :param filename: The path where the SVG file will be saved.
    :param config_file: Optional; the path to a YAML configuration file for rendering settings.
    """

    try:
        import yaml
        from keymap_drawer.config import Config, DrawConfig
        from keymap_drawer.draw import KeymapDrawer
        from keymap_drawer.keymap import ComboSpec, LayoutKey
        from keymap_drawer.physical_layout import QmkLayout

        from zkeymap.generators.qmk.private import key_to_qmk
    except ImportError:
        logger.error("keymap_drawer is not installed.")
        sys.exit(-1)

    config = None
    if config_file:
        config = Path(config_file)
        if not config.exists():
            logger.error(f"Config file {config_file} not found.")
            sys.exit(-4)

    if config:
        with config.open() as config_h:
            config_obj = Config.parse_obj(yaml.safe_load(config_h))
    else:
        config_obj = Config(draw_config=DrawConfig(dark_mode="auto"))

    svg_file: Path = path_with_suffix(filename, "_drawer.svg")

    # Generate a keymap_drawer.physical_layout.PhysicalLayout instance
    # using QmkLayout, since that is natively compatible with info.json-like `layout` contents

    physical_layout = QmkLayout(
        layouts={None: [key_to_qmk(k) for k in layout.keys]},
    ).generate(None, config_obj.draw_config.key_h)

    layers = {}
    for name, layer in env.layers:
        keys = []
        for key in layer.behaviors:
            dsp = display(key)
            if dsp.hold:
                keys.append({
                    "t": str(dsp.tap),
                    "h": str(dsp.hold),
                })
            else:
                keys.append(str(dsp.tap))
        layers[layer.display or name] = keys

    combos = []
    for _, combo in env.combos:
        dsp = display(combo.bindings)
        selected_layers = [ly.display or ly.name for ly in env.layers.resolve_iter(combo.layers)]
        combos.append(
            ComboSpec(
                key_positions=combo.key_positions,
                layers=selected_layers,
                key=LayoutKey(
                    tap=str(dsp.tap),
                    hold=str(dsp.hold),
                ),
            ),
        )

    with svg_file.open("w") as out:
        kd = KeymapDrawer(config_obj, out, layers=layers, layout=physical_layout, combos=combos)
        kd.print_board()
