# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

from __future__ import annotations

from dataclasses import dataclass
from itertools import takewhile
from typing import TYPE_CHECKING, TypeVar

from lark import Lark, Token, Transformer

from . import grammars

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable


class Expr:
    """Base class for all expressions."""


@dataclass
class Kp(Expr):
    """
    A keypress expression.

    Syntax: `[ alias+ ]` or `[ alias+ ~ ]`
    """

    words: list[str]
    sticky: bool = False


@dataclass
class HoldTap(Expr):
    """
    A hold-tap expression.

    Syntax: `{ hold tap }` or `{ hold / tap }`
    """

    hold: list[str]
    tap: list[str]


@dataclass
class LayerTap(Expr):
    """
    A layer tap expression.

    Syntax:
        `( layer tap )` or `( layer / tap )`
    """

    layer: str
    tap: list[str]


@dataclass
class LayerAction(Expr):
    """
    A layer action expression.

    Syntax:
           `( layer ~ )`
        or `( layer ! )`
        or `( layer / )`
        or `( layer )`
    """

    layer: str
    sticky: bool = False
    absolute: bool = False
    toggle: bool = False


@dataclass
class Raw(Expr):
    """
    A raw expression.

    Syntax: `< raw >`
    """

    value: str


@dataclass
class Trans(Expr):
    """
    A transparent expression.

    Syntax: `_____`
    """


@dataclass
class Muted(Expr):
    """
    A muted expression.

    Syntax: `xxxxx`
    """


class KeymapParser(Transformer):
    """Parser for the keymap grammar."""

    def __init__(self, visit_tokens: bool = True) -> None:
        super().__init__(visit_tokens)
        self._parser = Lark(
            grammars.keymap,
            start=[
                "keymap",
                "ht_content",
                "kp_content",
                "lt_content",
            ],
        )

    def kp(self, items: list[Token]) -> Kp:
        tokens = self._parser.parse(items[0][1:-1], start="kp_content").children
        return Kp(tokens[:-1], tokens[-1] == "~")

    def ht(self, items: list[Token]) -> HoldTap:
        tokens = self._parser.parse(items[0][1:-1], start="ht_content").children
        hold, tap = list_partition(lambda t: t is None or t.type == "SEP", tokens)
        if len(hold) == len(tokens):
            hold, tap = tokens[:-1], tokens[-1]
        return HoldTap(hold, tap)

    def lt(self, items: list[Token]) -> LayerTap | LayerAction:
        tokens = self._parser.parse(items[0][1:-1], start="lt_content").children
        if (last := tokens[-1]) and (type_ := last.type) in ("STICKY", "ABSOLUTE", "TOGGLE"):
            return LayerAction(
                tokens[0],
                sticky=type_ == "STICKY",
                absolute=type_ == "ABSOLUTE",
                toggle=type_ == "TOGGLE",
            )
        if tokens[-1] is None:
            return LayerAction(tokens[0])
        return LayerTap(tokens[0], [t for t in tokens[1:] if t and t.type != "SEP"])

    def raw(self, items: list[Token]) -> Raw:
        return Raw(items[0][1:-1])

    def lit(self, items: list[Token]) -> Kp:
        return Kp([items[0]])

    def trans(self, _items) -> Trans:
        return Trans()

    def muted(self, _items) -> Muted:
        return Muted()

    keymap = list

    def parse(self, code: str) -> list[Expr]:
        tree = self._parser.parse(code, start="keymap")
        return self.transform(tree)


T = TypeVar("T")


def list_partition(predicaste: Callable[[T], bool], data: Iterable[T]) -> tuple[list[T], list[T]]:
    """
    Partition a list into two parts based on a predicate.

    The first part (`left`) contains all elements of the iterable that do not
    satisfy the predicate. The second part (`right`) contains the rest of the
    elements.

    :param predicaste: A callable that takes an element of the iterable as its
                       argument and returns True if the element should be in
                       the right partition.
    :param data: The iterable to partition.
    :return: A tuple of two lists: `left` and `right`.
    """
    it = iter(data)
    left = list(takewhile(lambda t: not predicaste(t), it))
    right = list(it)
    return left, right
