# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

from pathlib import Path
from .model import Layout, layout as main_layout, alias as g_aliases

class _Namespace:
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def __getattr__(self, name: str) -> str:
        return self.__dict__.get(name)


def build_drawer_config(config_path: str | Path) -> None:
    import yaml
    keys = {}
    mods = {}
    raw = {}

    for key, alias  in g_aliases.data.items():
        text = " ".join(alias.resolve())
        if (old := keys.get(text)) and len(old) < len(key):
            continue

        if "&" in text:
            raw[text] = key
        else:
            keys[text.removeprefix("KC_")] = key

        if alias.ismod:
            mod = text.lower()
            if mod.startswith("l") or mod.startswith("r"):
                mod = ("left_" if mod.startswith("l") else "right_") + mod[1:]
                mods[mod] = key

    cfg = {
        "parse_config": {
            "zmk_keycode_map": keys,
            "modifier_fn_map": mods,
            "raw_binding_map": raw
        }
    }
    with Path(config_path).open("w") as out:
        yaml.dump(cfg, out, default_style='"')

def build_layout_svg_drawer(
    *,
    svg_file: str,
    keymap_file: str,
    layout_json_file: str,
    config_file: str | None = None,
    layout: Layout | None = None,
) -> None:
    """
    Generate Svg Graphics using the external tool keymap_drawer if installed.

    This function calla an external library to render the SVG (keymap-drawer)
    So to make it work, the user needs to install it previously.

    ```
    pip install keymap-drawer
    ```
    """
    import sys

    try:
        from keymap_drawer import __main__ as kd, config as kd_config
    except ImportError:
        print("[ERROR] keymap_drawer is not installed.")
        sys.exit(-1)

    svg_file: Path = Path(svg_file)

    kmf = Path(keymap_file)
    if not kmf.exists():
        print(f"[ERROR] keymap file {keymap_file} not found")
        sys.exit(-2)

    lyf = Path(layout_json_file)
    if not lyf.exists():
        print(f"[ERROR] layout (json) file {layout_json_file} not found")
        sys.exit(-3)

    if config_file:
        config = Path(config_file)
        if not config.exists():
            print(f"[ERROR] config file {config_file} not found")
            sys.exit(-4)
    else:
        config = Path(str(svg_file.with_suffix("")) + "_config.yaml")
        build_drawer_config(config)

    import yaml

    if not layout:
        layout = main_layout

    yaml_file = svg_file.with_suffix(".yaml")

    # Generate the yaml file
    with kmf.open() as kmf_h:
        with yaml_file.open("w") as out:
            if config:
                with config.open() as config_h:
                    config_obj = kd_config.Config.parse_obj(
                        yaml.safe_load(config_h)
                    )
            else:
                config_obj = kd_config.Config()
            args = _Namespace(
                columns=layout.num_cols,
                zmk_keymap=kmf_h,
                output=out,
            )
            kd.parse(args, config_obj)

    if not yaml_file.exists():
        print(f"[ERROR] failed to parse keymap {keymap_file}")
        sys.exit(-5)

    # Generate svg file
    with yaml_file.open() as src:
        with svg_file.open("w") as out:
            args = _Namespace(
                keymap_yaml=src,
                qmk_info_json=str(lyf),
                output=out,
            )
            kd.draw(args, config_obj)
