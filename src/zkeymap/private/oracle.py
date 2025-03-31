# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

"""
ZKeymap: Oracle.

The all-seeing oracle. This module has access to all of the language state.
"""

from __future__ import annotations

from .data import (
    Alias,
    AliasRegistry,
    BasicRegistry,
    Combo,
    Dance,
    LayerRegistry,
    Macro,
    Modifiers,
    Morph,
)
from .proxy import proxy

# fmt: off
DEFAULT_MODIFIERS = [
     "shift",  "ctrl",  "alt",  "gui",
    "lshift", "lctrl", "lalt", "lgui",
    "rshift", "rctrl", "ralt", "rgui",
]
# fmt: on


def is_modifier(token: str | Alias) -> bool:
    """
    Check if a token is a modifier.

    This function takes either a string that will be resolved to an alias or an
    Alias object. If the token is a modifier then it returns True, otherwise it
    returns False.

    :param token: string or Alias
    :return: bool
    """
    if isinstance(token, str):
        token = aliases.resolve(token)
    return isinstance(token, Alias) and token.modifiers


def resolve_modifiers(mods: list[str | Alias]) -> Modifiers:
    """
    Resolve modifiers from a list of str or Alias.

    This function takes a list of tokens and resolves them to Modifiers. It
    resolves each token to an Alias and sums up all the modifiers found. If a
    token is not a modifier then it is ignored.

    :param mods: list of str or Alias
    :return: Modifiers
    """
    mod = Modifiers()
    for m in mods:
        alias = aliases.resolve(m) if isinstance(m, str) else m
        if isinstance(alias, Alias) and alias.modifiers:
            mod += alias.modifiers
    return mod


def is_layer(name: str) -> bool:
    """
    Check if a name corresponds to an existing layer.

    This function determines whether a given layer name exists within the
    LayerRegistry. It returns True if the layer is found, otherwise it
    returns False.

    :param name: The name of the layer to check.
    :return: True if the layer exists, False otherwise.
    """
    return layers.resolve(name) is not None


# Global language state.
# The following global objects are proxies of the actual registries.
# All keymap parsing and generation logic refers to these proxy objects.
# For advanced use cases or test cases, wrapped objects ca be replaced using
# the `__itruediv__` operator. ie. `aliases /= AliasRegistry()`

aliases = proxy(AliasRegistry())
layers = proxy(LayerRegistry())
macros: BasicRegistry[Macro] = proxy(BasicRegistry(prefix="macro"))
dances: BasicRegistry[Dance] = proxy(BasicRegistry(prefix="dance"))
morphs: BasicRegistry[Morph] = proxy(BasicRegistry(prefix="morph"))
combos: BasicRegistry[Combo] = proxy(BasicRegistry(prefix="combo"))
