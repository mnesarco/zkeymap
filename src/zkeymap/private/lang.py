# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

# ruff: noqa: F401
# ruff: noqa: D101 This is a private module
# ruff: noqa: N801 This DSL uses lowercase classes as keywords
# ruff: noqa: D105 __truediv__, __itruediv__, __add__, __iadd__ are used as DSL constructs

"""
ZKeymap: Lang.

Domain Specific Language for ZMK Keymap definitions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .data import Alias, Combo, Dance, Layer, Macro, Modifiers, Morph
from .keymap import parse_keymap
from .oracle import aliases, combos, dances, layers, macros, morphs

if TYPE_CHECKING:
    from .behavior import Behavior


@dataclass
class AliasBuilder:
    alias: Alias

    def __truediv__(self, value: str | label | Macro | Morph | Modifiers) -> AliasBuilder:
        match value:
            case label():
                self.alias.display_override = value
            case str() | Macro() | Morph():
                self.alias.content = value
            case Modifiers():
                self.alias.modifiers = value
            case _:
                msg = f"Unsupported parameter type {type(value)}"
                raise TypeError(msg)
        return self

    def __add__(self, value: Modifiers) -> AliasBuilder:
        self.alias.modifiers += value
        return self


class label(str):
    """Display text for a layers, alias, macros, etc..."""

    __slots__ = ()


class if_layers:
    """Conditional layers."""

    def __init__(self, *args: list[str]) -> None:
        """
        Construct an if_layers object.

        :param args: List of layer names that should be checked.
        :type args: list[str]
        :return: A conditional layer object.
        """
        self.layers: list[str] = [*args]


@dataclass
class LayerBuilder:
    """Language construct for defining layers."""

    layer: Layer

    def __truediv__(self, value: str | label | if_layers) -> LayerBuilder:
        match value:
            case if_layers():
                self.layer.if_layers = value.layers
            case label():
                self.layer.display = value
            case str():
                self.layer.behaviors = parse_keymap(value)
            case _:
                msg = f"Unsupported parameter type {type(value)}"
                raise TypeError(msg)
        return self


class LayerKeyword:
    """Language keyword for declaring layers."""

    def __truediv__(self, name: str) -> LayerBuilder:
        layer = layers.add(name)
        layer.display = name
        return LayerBuilder(layer)


class AliasKeyword:
    """Language keyword for declaring aliases."""

    def __truediv__(self, name: str | tuple[str]) -> AliasBuilder:
        return AliasBuilder(aliases.add(name))


def combo(
    bindings: str,
    key_positions: list[int],
    *,
    name: str | None = None,
    layers: list[str] | None = None,
    timeout_ms: int | None = None,
    require_prior_idle_ms: int | None = None,
    slow_release: int | None = None,
) -> Combo:
    """
    Declare a combo.

    :param bindings: Keymap string that defines the combo behavior.
    :param key_positions: List of key positions involved in the combo.
    :param name: Optional name for the combo.
    :param layers: Optional list of layers where the combo is active.
    :param timeout_ms: Optional timeout in milliseconds before the combo is cancelled.
    :param require_prior_idle_ms: Optional idle time in milliseconds required before the combo activates.
    :param slow_release: Optional flag for slow release behavior.
    :return: The declared combo.
    """
    combo = Combo(
        parse_keymap(bindings)[0],
        key_positions,
        name,
        layers,
        timeout_ms,
        require_prior_idle_ms,
        slow_release,
    )
    combos.add(combo)
    return combo


def macro(
    bindings: str,
    *,
    name: str | None = None,
    wait_ms: int | None = None,
    tap_ms: int | None = None,
) -> Macro:
    """
    Declare a macro.

    :param bindings: Keymap string that defines the macro behavior.
    :param name: Optional name of the macro.
    :param wait_ms: Optional wait timeout in milliseconds.
    :param tap_ms: Optional tap timeout in milliseconds.
    :return: The declared macro.
    """
    macro = Macro(name, parse_keymap(bindings), wait_ms, tap_ms)
    macros.add(macro)
    return macro


def tap_dance(
    bindings: str,
    name: str | None = None,
    tapping_term_ms: int | None = None,
) -> Dance:
    """
    Declare a tap dance.

    :param bindings: Keymap string that defines the tap dance behavior.
    :param name: Optional name of the tap dance.
    :param tapping_term_ms: Optional tapping term timeout in milliseconds.
    :return: The declared tap dance.
    """
    dance = Dance(name, parse_keymap(bindings), tapping_term_ms)
    dances.add(dance)
    return dance


def morph(
    bindings: str,
    mods: Modifiers,
    *,
    name: str | None = None,
    keep: Modifiers | None = None,
) -> Morph:
    """
    Declare a morph behavior.

    :param bindings: Keymap string that defines two behaviors for the morph.
    :param mods: Modifiers required for the morph behavior.
    :param keep: Optional modifiers to keep during the morph.
    :return: The declared morph.
    :raises ValueError: If the number of behaviors is not two or no modifiers are provided.
    """

    behaviors = parse_keymap(bindings)

    if (n := len(behaviors)) != 2:  # noqa: PLR2004
        msg = f"morph accepts exactly two behaviors but {n} were provided '{bindings}'"
        raise ValueError(msg)

    if not mods:
        msg = "morph requires at leas one modifier"
        raise ValueError(msg)

    morph = Morph(name, behaviors[0], behaviors[1], mods, keep)
    morphs.add(morph)
    return morph


@dataclass(kw_only=True)
class MetaMacro:
    """
    MetaMacro class represents a macro builder with optional pre- and post-processing behaviors.

    :param before: Optional list of behaviors to be executed before the macro.
    :param after: Optional list of behaviors to be executed after the macro.
    :param wait_ms: Optional wait timeout in milliseconds.
    :param tap_ms: Optional tap timeout in milliseconds.
    """

    before: list[Behavior] | None
    after: list[Behavior] | None
    wait_ms: int | None = None
    tap_ms: int | None = None

    def __call__(
        self,
        bindings: str,
        *,
        name: str | None = None,
        wait_ms: int | None = None,
        tap_ms: int | None = None,
    ) -> Macro:
        """
        Create and register a macro with optional pre- and post-processing behaviors.

        :param bindings: Keymap string defining the macro behavior.
        :param name: Optional name for the macro.
        :param wait_ms: Optional wait timeout in milliseconds. Defaults to the instance's wait_ms.
        :param tap_ms: Optional tap timeout in milliseconds. Defaults to the instance's tap_ms.
        :return: The registered Macro object.
        """

        if wait_ms is None:
            wait_ms = self.wait_ms
        if tap_ms is None:
            tap_ms = self.tap_ms
        behaviors = parse_keymap(bindings)
        if self.before:
            behaviors = [*self.before, *behaviors]
        if self.after:
            behaviors = [*behaviors, *self.after]
        macro = Macro(name, behaviors, wait_ms, tap_ms)
        macros.add(macro)
        return macro


def meta_macro(
    *,
    before: str | None,
    after: str | None,
    wait_ms: int | None = None,
    tap_ms: int | None = None,
) -> MetaMacro:
    """
    Create a MetaMacro object with optional pre- and post-processing behaviors.

    :param before: Optional keymap string defining behaviors to be executed before the macro.
    :param after: Optional keymap string defining behaviors to be executed after the macro.
    :param wait_ms: Optional wait timeout in milliseconds.
    :param tap_ms: Optional tap timeout in milliseconds.
    :return: A MetaMacro object.
    """
    before = parse_keymap(before)
    after = parse_keymap(after)
    return MetaMacro(before=before, after=after, wait_ms=wait_ms, tap_ms=tap_ms)


# Global language keywords

alias = AliasKeyword()
layer = LayerKeyword()
