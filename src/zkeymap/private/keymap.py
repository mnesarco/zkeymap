# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

from __future__ import annotations

from itertools import takewhile
from typing import TYPE_CHECKING

from .behavior import (
    Behavior,
    CustomBx,
    KeyPressBx,
    LayerActionBx,
    LayerTapBx,
    ModTapBx,
    MutedBx,
    TransparentBx,
)
from .oracle import aliases, is_modifier, resolve_modifiers
from .parser import Expr, HoldTap, KeymapParser, Kp, LayerAction, LayerTap, Muted, Raw, Trans

if TYPE_CHECKING:
    from collections.abc import Callable


def resolve_kp(kp: Kp) -> KeyPressBx:
    """
    Resolves a keypress expression into a KeyPressBx object with modifiers.

    :param kp: A keypress expression containing words and a sticky flag.
    :return KeyPressBx: An object representing the resolved keypress with modifiers.

    The function first resolves all aliases for the words in the keypress
    expression. It distinguishes between modifiers and keys, using the
    resolved modifiers to construct a KeyPressBx object. The sticky attribute
    is preserved from the input keypress expression. In cases where no valid
    key or modifier combination is found, a Raw object is returned containing
    the unresolved words.
    """
    names = aliases.resolve_all(kp.words)
    mods = list(takewhile(is_modifier, names))
    keys = names[len(mods) :]
    match (len(mods), len(keys)):
        case (1, 0):
            return KeyPressBx(mods[0], None, kp.sticky)
        case (n, 0) if n > 1:
            return KeyPressBx(mods[-1], resolve_modifiers(mods[:-1]), kp.sticky)
        case (0, 1):
            return KeyPressBx(keys[0], None, kp.sticky)
        case (_, 1):
            return KeyPressBx(keys[0], resolve_modifiers(mods), kp.sticky)
        case _:
            return Raw(" ".join(w for w in kp.words if w is not None))


def resolve_ht(ht: HoldTap) -> ModTapBx:
    """
    Resolves a hold-tap expression into a ModTapBx object.

    :param ht: A hold-tap expression with hold and tap components.
    :return ModTapBx: An object representing the resolved hold-tap with modifiers.
    """
    hold = resolve_kp(Kp(ht.hold))
    tap = resolve_kp(Kp(ht.tap))
    return ModTapBx(hold, tap)


def resolve_trans(_tr: Trans) -> TransparentBx:
    """
    Resolves a transparent keymap expression into a TransparentBx object.

    :param tr: A transparent keymap expression.
    :return TransparentBx: An object representing the resolved transparent keymap.
    """
    return TransparentBx()


def resolve_muted(_muted: Muted) -> MutedBx:
    """
    Resolves a muted keymap expression into a MutedBx object.

    :param mut: A muted keymap expression.
    :return MutedBx: An object representing the resolved muted keymap.
    """
    return MutedBx()


def resolve_lt(lt: LayerTap) -> LayerTapBx:
    """
    Resolves a layer-tap expression into a LayerTapBx object.

    :param lt: A layer-tap expression containing a layer and tap component.
    :return LayerTapBx: An object representing the resolved layer-tap behavior.
    """
    layer = lt.layer
    tap = resolve_kp(Kp(list(lt.tap)))
    return LayerTapBx(layer, tap)


def resolve_la(lt: LayerAction) -> LayerActionBx:
    """
    Resolves a layer-action expression into a LayerActionBx object.

    :param lt: A layer-action expression containing a layer and action.
    :return LayerActionBx: An object representing the resolved layer-action behavior.
    """
    layer = lt.layer
    return LayerActionBx(layer, lt.sticky, lt.absolute, lt.toggle)


def resolve_raw(raw: Raw) -> CustomBx:
    """
    Resolves a raw keymap expression into a CustomBx object.

    :param raw: A raw keymap expression containing a string.
    :return CustomBx: An object representing the resolved raw keymap.
    """
    return CustomBx(raw.value)


def parse_keymap(source: str) -> list[Behavior]:
    """
    Parses a keymap source string into a list of Behavior objects.

    :param source: A string representation of the keymap to be parsed.
    :return: A list of Behavior objects representing the parsed keymap.
    """
    return [dispatcher.get(type(expr))(expr) for expr in parser.parse(source)]


dispatcher: dict[type[Expr], Callable[[Expr], Behavior]] = {
    Kp: resolve_kp,
    HoldTap: resolve_ht,
    Trans: resolve_trans,
    Muted: resolve_muted,
    Raw: resolve_raw,
    LayerAction: resolve_la,
    LayerTap: resolve_lt,
}

parser = KeymapParser()
