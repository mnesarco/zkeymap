# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

"""
ZKeymap: ZMK Keymap Generators. Implementation details.
"""

from dataclasses import asdict
from itertools import chain
from pathlib import Path
from textwrap import dedent, indent

from zkeymap.api import (
    Alias,
    Behavior,
    CustomBx,
    HoldTapBx,
    HWKey,
    KeyPressBx,
    Layer,
    LayerActionBx,
    LayerTapBx,
    Layout,
    Modifiers,
    ModTapBx,
    MutedBx,
    TransparentBx,
    env,
)
from zkeymap.generators.utils import (
    file_header_comment,
    file_tag,
    path_with_suffix,
    table_output,
)

MOD_VARIANTS = {
    "LS": "MOD_LSFT",
    "RS": "MOD_RSFT",
    "LC": "MOD_LCTL",
    "RC": "MOD_RCTL",
    "LA": "MOD_LALT",
    "RA": "MOD_RALT",
    "LG": "MOD_LGUI",
    "RG": "MOD_RGUI",
}

DEFAULT_TRANSFORM = """
    #ifndef {file_tag}
    #define {file_tag}

    #include <dt-bindings/zmk/matrix_transform.h>

    / {{
        // {description}
        {label}: {node} {{
            compatible = "zmk,matrix-transform";
            columns = <{cols}>;
            rows = <{rows}>;
            map = <{map}
            >;
        }};
    }};

    #endif /* {file_tag} */
    """

KEY_H = "//                       w    h       x       y     rot      rx      ry"
KEY = "<&key_physical_attrs {w: >4} {h: >4} {x: >7} {y: >7} {r: >7} {rx: >7} {ry: >7}>"

PHYSICAL_LAYOUT = """
    #ifndef {file_tag}
    #define {file_tag}

    #include <physical_layouts.dtsi>

    / {{
        {label}: {node} {{
            compatible = "zmk,physical-layout";
            display-name = "{display}";
            keys {keys}
                ;
        }};
    }};

    #endif /* {file_tag} */
    """


KEYMAP = """
    #ifndef {file_tag}
    #define {file_tag}

    {layer_defs}
    {macros}
    {morphs}
    {combos}

    / {{
        keymap {{
            compatible = "zmk,keymap";
            {layers}
        }};
    }};

    #endif /* {file_tag} */
    """

MACRO = """
    / {{
        macros {{
            {name}: {name} {{
                compatible = "zmk,behavior-macro";
                #binding-cells = <0>;
                bindings = {bindings};
                {wait_ms}
                {tap_ms}
            }};
        }};
    }};
    """


MORPH = """
    / {{
        behaviors {{
            {name}: {name} {{
                compatible = "zmk,behavior-mod-morph";
                #binding-cells = <0>;
                bindings = {bindings};
                mods = {mods};
                {keep}
            }};
        }};
    }};
    """


COMBO = """
    / {{
        combos {{
            compatible = "zmk,combos";
            {name} {{
                key-positions = <{positions}>;
                bindings = <{bindings}>;
                {require_prior_idle}
                {timeout}
                {slow_release}
                {layers}
            }};
        }};
    }};
    """


LAYER = """
    {name} {{
        display-name = "{display}";
        bindings = <
        {bindings}
        >;
    }};

"""


def keymap(layout: Layout, filename: str | Path) -> None:
    """Generate keymap file."""
    filename = path_with_suffix(filename, "_keymap.dtsi")
    with filename.open("w") as out:
        out.write(file_header_comment())
        out.write(
            dedent(
                KEYMAP.format(
                    file_tag=file_tag(filename),
                    layer_defs=layer_defs(),
                    macros=macros(),
                    morphs=morphs(),
                    combos=combos(),
                    layers=render_layers(layout),
                ),
            ),
        )


def layer_macro_id(layer: Layer) -> str:
    """Return C/C++ Macro name for the layer."""
    return f"L_{layer.name.upper()}"


def layer_defs() -> str:
    """Return macro definitions for all layers."""
    defs = []
    for _, layer in env.layers:
        defs.append(f"\n#define {layer_macro_id(layer)} {layer.num}")
    return indent("".join(defs), " " * 4)


def macros() -> str:
    """Return all macros devicetree."""
    from zkeymap.private.oracle import macros

    items = []
    for name, macro in macros:
        wait_ms = "" if macro.wait_ms is None else "wait-ms = <{macro.wait_ms}>;"
        tap_ms = "" if macro.tap_ms is None else "tap-ms = <{macro.tap_ms}>;"
        items.append(
            MACRO.format(
                name=name,
                wait_ms=wait_ms,
                tap_ms=tap_ms,
                bindings=f"<{bindings(macro.bindings)}>",
            ),
        )
    return "\n".join(items)


def morphs() -> str:
    """Return all mod-morphs devicetree."""
    from zkeymap.private.oracle import morphs

    items = []
    for name, morph in morphs:
        keep = "" if morph.keep is None else f"keep-mods = <{mod_union_expression(morph.keep)}>;"
        items.append(
            MORPH.format(
                name=name,
                keep=keep,
                bindings=f"<{bindings([morph.low])}>, <{bindings([morph.high])}>",
                mods=f"<{mod_union_expression(morph.mods)}>",
            ),
        )
    return "\n".join(items)


def combos() -> str:
    """Return all combos devicetree."""
    from zkeymap.private.oracle import combos, layers

    items = []
    for name, combo in combos:
        timeout = "" if combo.timeout_ms is None else f"timeout-ms = <{combo.timeout_ms}>;"
        slow_release = "" if combo.slow_release is None else "slow-release;"
        require_prior_idle = ""
        if combo.require_prior_idle_ms is not None:
            require_prior_idle = f"require-prior-idle-ms = <{combo.require_prior_idle_ms}>;"
        if_layers = ""
        if combo.layers:
            nums = [str(ly.num) for ly in layers.resolve_iter(combo.layers)]
            if_layers = "layers = <" + (" ".join(sorted(nums))) + ">;"
        positions = " ".join(map(str, sorted(combo.key_positions)))
        items.append(
            COMBO.format(
                name=name,
                positions=positions,
                timeout=timeout,
                require_prior_idle=require_prior_idle,
                bindings=bindings([combo.bindings]),
                layers=if_layers,
                slow_release=slow_release,
            ),
        )
    return "\n".join(items)


def resolve(value: str | Alias) -> str:
    """Return the actual output value from an alias or literal."""
    match value:
        case str():
            return value
        case Alias():
            return value.resolved()
        case _:
            msg = "This should never happen"
            raise AssertionError(msg)


def bindings(behaviors: list[Behavior]) -> str:  # noqa: C901, PLR0912
    """Translate model bindings to actual zmk devicetree syntax."""
    data = []
    for b in behaviors:
        match b:
            case KeyPressBx():
                data.append(mod_fn(b.mods, resolve(b.value), "&sk" if b.sticky else "&kp"))
            case CustomBx():
                data.append(b.raw)
            case MutedBx():
                data.append("&none")
            case TransparentBx():
                data.append("&trans")
            case ModTapBx():
                hold = mod_fn(b.hold.mods, resolve(b.hold.value), "")
                tap = mod_fn(b.tap.mods, resolve(b.tap.value), "")
                data.append(f"&mt {hold} {tap}")
            case HoldTapBx():
                data.append(f"&ht {resolve(b.hold.value)} {resolve(b.tap.value)}")
            case LayerTapBx():
                layer = layer_macro_id(env.layers.resolve(b.layer))
                data.append(f"&lt {layer} {resolve(b.tap.value)}")
            case LayerActionBx():
                layer = layer_macro_id(env.layers.resolve(b.layer))
                if b.toggle:
                    data.append(f"&tog {layer}")
                elif b.absolute:
                    data.append(f"&to {layer}")
                elif b.sticky:
                    data.append(f"&sl {layer}")
                else:
                    data.append(f"&mo {layer}")
            case _:
                msg = "This case should never happen"
                raise AssertionError(msg)
    return " ".join(data)


def mod_fn(mods: Modifiers, kp: str, behavior: str) -> str:
    """Apply modifiers as functions to the `kp` and prefix the behavior if required."""
    stack = []
    if mods:
        stack = [mod[0:2].upper() + "(" for mod in mods]
    data = ("".join(stack) + kp + (")" * len(stack))).strip()

    if data.startswith("&") or not behavior:
        return data

    return f"{behavior} {data}"


def mod_union_expression(mods: Modifiers) -> str:
    """
    Combine modifier names into a single string expression.

    This function takes a `Modifiers` object and translates each modifier into
    its corresponding variant name using the `MOD_VARIANTS` dictionary. It then
    combines these variant names into a single string expression separated by
    the '|' character, enclosed in parentheses.

    :param mods: A `Modifiers` instance containing the modifiers to be combined.
    :return: A string expression representing the combined modifier variants.
    """
    names = (MOD_VARIANTS.get(m[0:2].upper()) for m in mods)
    return f"({'|'.join(names)})"


def render_layers(layout: Layout) -> str:
    """Render all defined layers to devicetree."""
    all_layers = []
    for _name, layer in env.layers:
        table = layout.apply(layer.behaviors)
        table_str = table_output(
            table,
            render=lambda b, *_: bindings([b]),
            just=str.ljust,
            indent=12,
            sep="  ",
        )
        all_layers.append(
            dedent(
                LAYER.format(
                    name=layer.name,
                    display=layer.display,
                    bindings=table_str.content,
                ),
            ),
        )
    return indent("\n\n".join(all_layers), " " * 12)


def to_centi_units(d: dict) -> dict:
    """Transform values to centi-units."""
    for k, v in d.items():
        match v:
            case None:
                d[k] = 0
            case int() | float():
                if v >= 0:
                    d[k] = round(v * 100, 0)
                else:
                    d[k] = f"({round(v * 100, 0)})"
            case _:
                pass
    return d


def physical_layout(layout: Layout, filename: str | Path) -> None:
    """Generate physical layout file in devicetree."""
    filename = path_with_suffix(filename, "_layout.dtsi")
    with filename.open("w") as out:
        out.write(file_header_comment())
        keys = (KEY.format(**to_centi_units(asdict(k))) for k in chain.from_iterable(layout.rows))
        keys_fmt = "\n= " + ("\n, ".join(keys))
        out.write(
            dedent(
                PHYSICAL_LAYOUT.format(
                    file_tag=file_tag(filename),
                    label=layout.name,
                    node=layout.name,
                    display=layout.display,
                    keys=KEY_H + indent(keys_fmt, " " * 16),
                ),
            ),
        )


def rc(key: HWKey, row: int, col: int) -> str:
    """Return RC macro cell for the key."""
    if key.matrix:
        return f"RC({key.matrix[0]}, {key.matrix[1]})"
    return f"RC({row},{col})"


def default_transform(
    layout: Layout,
    filename: str | Path,
    *,
    name: str | None = None,
) -> None:
    """Generate default transform for the layout in devicetree."""
    filename = path_with_suffix(filename, "_transform.dtsi")
    with filename.open("w") as out:
        out.write(file_header_comment())
        table = table_output(layout.rows, render=rc, indent=12)
        out.write(
            dedent(
                DEFAULT_TRANSFORM.format(
                    file_tag=file_tag(filename),
                    label= name or f"{layout.name}_transform",
                    node= name or f"{layout.name}_transform",
                    description=layout.display,
                    cols=table.columns,
                    rows=table.rows,
                    map=table.content,
                ),
            ),
        )
