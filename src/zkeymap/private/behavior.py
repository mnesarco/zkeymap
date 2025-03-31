# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .data import Alias, Modifiers


class Behavior:
    """Base class for all behaviors."""


@dataclass
class KeyPressBx(Behavior):
    """Key press behavior."""

    value: str | Alias
    mods: Modifiers | None = None
    sticky: bool = False


@dataclass
class HoldTapBx(Behavior):
    """Hold-tap behavior."""

    hold: Behavior
    tap: Behavior

    @property
    def sticky(self) -> bool:  # noqa: D102
        return getattr(self.tap, "sticky", False)


class ModTapBx(HoldTapBx):
    """Mod-Tap behavior."""


@dataclass
class LayerTapBx(Behavior):
    """Layer-Tap behavior."""

    layer: str
    tap: Behavior


@dataclass
class LayerActionBx(Behavior):
    """Layer-Action behavior."""

    layer: str
    sticky: bool = False
    absolute: bool = False
    toggle: bool = False


@dataclass
class CustomBx(Behavior):
    """Custom behavior. (Not translated, passed as it is)."""

    raw: str


class TransparentBx(Behavior):
    """Transparent behavior."""


class MutedBx(Behavior):
    """Muted/None behavior."""
