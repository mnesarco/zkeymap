# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

# ruff: noqa: N801 Some lowercase named classes are used as keywords.

"""
ZKeymap: Data structures.
"""

from __future__ import annotations

from dataclasses import asdict, astuple, dataclass, fields
from itertools import count
from typing import TYPE_CHECKING, Generic, TypeVar

from .utils import Scope, logger

if TYPE_CHECKING:
    from collections.abc import Iterator

    from .behavior import Behavior

T = TypeVar("T")


class AliasRegistry:
    """Container for all aliases."""

    def __init__(self) -> None:  # noqa: D107
        self._data: dict[str, Alias] = {}

    def resolve(self, name: str) -> Alias | str:
        """
        Resolve a key name to its corresponding alias.

        If the key is not an alias, it will be returned as is, but a warning will be printed.

        :param name: The key name to resolve.
        :return: The resolved alias or the original name if not an alias.
        """
        value = self._data.get(name)
        if not value:
            logger.warning(
                f"Literal '{name}' is not an alias, it must be defined by the firmware.",
            )
            return name
        return value

    def resolve_all(self, names: list[str]) -> list[Alias | str]:
        """
        Resolve all key names to their corresponding aliases.

        If any of the keys is not an alias, it will be returned as is, with a warning.

        :param names: A list of key names to resolve.
        :return: A list of resolved aliases or the original key names if not an alias.
        """
        if not names:
            return []
        return [self.resolve(name) for name in names]

    def add(self, name: str | tuple[str]) -> Alias:
        """
        Add a new alias to the registry.

        This method creates an alias with the given name(s) and stores it in the registry.
        If a single string is provided, it is treated as a tuple with one element.

        :param name: A string or tuple of strings representing the alias name(s).
        :return: The created Alias object.
        """
        if isinstance(name, str):
            name = (name,)
        alias = Alias(name=name[-1])
        for branch in name:
            self._data[branch] = alias
        return alias

    def __iter__(self) -> Iterator[tuple[str, Alias]]:
        """
        Iterate over the aliases in the registry.

        Yields tuples of (alias_name, alias_object).
        """
        return iter(self._data.items())


class LayerRegistry:
    """
    Container for all layers.
    """

    def __init__(self) -> None:  # noqa: D107
        self._data: dict[str, Layer] = {}

    def resolve_iter(self, names: list[str]) -> Iterator[Layer]:
        """
        Iterate over the layers in the registry with the given names.

        Yields the Layer objects which have a name in the given list of names.
        """
        yield from (layer for layer in self._data.values() if layer.name in names)

    def resolve(self, name: str) -> Layer | None:
        """
        Resolve a layer name to its corresponding Layer object.

        :param name: The name of the layer to resolve.
        :return: The resolved Layer object or None if not found.
        """
        return self._data.get(name)

    def add(self, name: str) -> Layer:
        """
        Add a new layer to the registry.

        This method creates a Layer object with the given name and assigns it a unique
        number based on the current size of the registry. The new Layer is then stored
        in the registry and returned.

        :param name: The name of the layer to be added.
        :return: The created Layer object.
        """
        layer = Layer(name=name, num=len(self._data))
        self._data[name] = layer
        return layer

    def __iter__(self) -> Iterator[tuple[str, Layer]]:
        """
        Iterate over the layers in the registry.

        Yields tuples of (layer_name, layer_object).
        """
        return iter(self._data.items())


class BasicRegistry(Generic[T]):
    """
    Container for all items of type T.
    """

    def __init__(self, prefix: str) -> None:
        """
        Initialize a BasicRegistry instance.

        :param prefix: A string prefix to be used for item names.
        """
        self._prefix = prefix
        self._data: dict[str, T] = {}
        self._seq = count()

    def add(self, item: T) -> None:
        """
        Add a new item to the registry.

        If the item has no name, assigns it one with the prefix and next sequence number.
        Then, stores the item in the registry with the assigned name.

        :param item: The item to be added.
        """
        if not item.name:
            item.name = f"{self._prefix}_{next(self._seq)}"
        self._data[item.name] = item

    def __iter__(self) -> Iterator[tuple[str, T]]:
        """
        Iterate over the items in the registry.

        Yields tuples of (item_name, item_object).
        """
        return iter(self._data.items())


@dataclass(kw_only=True)
class Modifiers:
    """Standard 8 Keyboard modifiers."""

    lshift: bool = False
    rshift: bool = False
    lctrl: bool = False
    rctrl: bool = False
    lalt: bool = False
    ralt: bool = False
    lgui: bool = False
    rgui: bool = False

    def __add__(self, mods: Modifiers) -> Modifiers:
        """
        Combine two Modifiers instances.

        The returned Modifiers instance contains all the modifiers set in either of the
        two operands. If a modifier is set in both operands, the result will have it set
        as well.

        :param mods: The other Modifiers instance to combine with.
        :return: A new Modifiers instance with the combined modifiers.
        """
        flags = asdict(self)
        if mods:
            flags.update((k, v) for (k, v) in asdict(mods).items() if v)
        return Modifiers(**flags)

    def __iadd__(self, mods: Modifiers) -> Modifiers:  # noqa: PYI034
        """
        In-place combine two Modifiers instances.

        The result of this operation is that this Modifiers instance contains all the
        modifiers set in either of the two operands. If a modifier is set in any of
        operands, the result will have it set as well.

        :param mods: The other Modifiers instance to combine with.
        :return: Self.
        """
        self.__dict__.update((k, v) for (k, v) in asdict(mods).items() if v)
        return self

    def __bool__(self) -> bool:
        """
        Return True if any of the modifiers are set.

        :return: If any modifiers are set.
        """
        return any(astuple(self))

    def __iter__(self) -> Iterator[str]:
        """
        Iterate over the names of the modifiers that are set in this instance.

        Yields the names of the modifiers that are set in this instance as strings.
        """
        for field in fields(self):
            if getattr(self, field.name, False):
                yield field.name


class mod(Scope):
    """Namespace with all the modifiers as constants."""

    # fmt: off
    LShift = Shift = Modifiers(lshift=True)
    RShift =         Modifiers(rshift=True)
    LCtrl  = Ctrl =  Modifiers(lctrl=True)
    RCtrl  =         Modifiers(rctrl=True)
    LAlt   = Alt =   Modifiers(lalt=True)
    RAlt   = AltGr = Modifiers(ralt=True)
    LGui   = Gui =   Modifiers(lgui=True)
    RGui   =         Modifiers(rgui=True)
    # fmt: on


@dataclass
class Morph:
    """Morphing between two behaviors based on modifiers."""

    name: str
    low: Behavior
    high: Behavior
    mods: Modifiers
    keep: Modifiers | None = None


@dataclass
class Macro:
    """Macro behavior."""

    name: str
    bindings: list[Behavior]
    wait_ms: int | None = None
    tap_ms: int | None = None


@dataclass
class Dance:
    """Tap dance behavior."""

    name: str
    bindings: list[Behavior]
    tapping_term_ms: int | None = None


@dataclass
class Combo:
    """Combo behavior."""

    bindings: Behavior
    key_positions: list[int]
    name: str | None = None
    layers: list[str] | None = None
    timeout_ms: int | None = None
    require_prior_idle_ms: int | None = None
    slow_release: bool | None = None


@dataclass
class Alias:
    """
    Alias object. This is the core of the keymap.

    Aliases are resolved to behaviors and then translated to specific firmware macros.
    """

    name: str | None = None
    content: str | Morph | Macro | None = None
    modifiers: Modifiers | None = None
    display_override: str | None = None

    @property
    def display(self) -> str:
        """
        Display name of the alias.

        If an override is provided, that will be returned, otherwise the alias name.
        """
        if display := self.display_override:
            return display
        return self.name

    def resolved(self) -> str:
        """
        Resolve the alias content to a string.

        If the alias content is a string, it is returned as is. If it is a Morph, it is
        resolved to a string of the form "&name". If it is a Macro, it is resolved to a
        string of the form "&name". If it is any other type of content, an empty string is
        returned.

        :return: The resolved content as a string.
        """
        match self.content:
            case str():
                return self.content
            case Morph():
                return f"&{self.content.name}"
            case Macro():
                return f"&{self.content.name}"
            case _:
                return ""


@dataclass
class Layer:
    """Layer data structure."""

    name: str
    num: int
    display: str | None = None
    behaviors: list[Behavior] | None = None
    if_layers: list[str] | None = None


@dataclass
class HWKey:
    """Hardware key data structure."""

    x: float = 0
    y: float = 0
    w: float = 1
    h: float = 1
    r: float = None
    rx: float = None
    ry: float = None
    matrix: tuple[int, int] | None = None
    gpio: int | None = None

    @property
    def pos(self) -> int:
        """
        The position of the key on a layout.

        If the key is part of a layout, this is the position of the key in the layout.
        Otherwise, it is None.
        """
        return getattr(self, "_pos", None)

    @pos.setter
    def pos(self, p: int) -> None:
        self._pos = p
