# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from itertools import chain, count
from typing import TypeAlias, TypeVar

from .data import HWKey

T = TypeVar("T")


class Row:
    """Represents a row of keys."""

    def __init__(self, *items: list[RowItem]) -> None:
        """Initialize the Row object with the given items."""
        keys = []
        for item in items:
            match item:
                case HWKey():
                    keys.append(item)
                case Mirror():
                    keys.extend(item(keys))
                case other:
                    msg = f"Invalid type: {type(other)}"
                    raise TypeError(msg)

        self.keys: list[HWKey] = keys


@dataclass
class Mirror:
    """Represents a mirror of keys."""

    x: int = 0
    col_offset: int = 0
    row_offset: int = 0

    def __call__(self, keys: list[HWKey]) -> list[HWKey]:
        """Mirror the keys."""
        r_keys = [HWKey(**asdict(k)) for k in keys]
        self.mirror_x(r_keys, self.x, self.row_offset, self.col_offset)
        return list(reversed(r_keys))

    def mirror_x(
        self,
        keys: list[HWKey],
        x: int,
        row_offset: int,
        col_offset: int,
    ) -> None:
        """Mirror the keys."""
        if not keys:
            return
        x0 = x
        kmats = [k.matrix[1] for k in keys if k.matrix]
        maxcol = max(kmats) if kmats else 0
        for k in keys:
            k.x = -k.x - k.w + x0
            if k.r is not None:
                k.r = -k.r
                k.rx = -(k.rx or 0) + x0
                k.ry = k.ry or 0

            if k.matrix:
                r, c = k.matrix
                k.matrix = [r + row_offset, maxcol - c + col_offset]


@dataclass
class Repeat:
    """Represents a repeat of rows."""

    n: int = 1
    col_offset: int = 0
    row_offset: int = 1
    x_offset: int = 0
    y_offset: int = 1

    def __call__(self, rows: list[list[HWKey]]) -> list[list[HWKey]]:
        """
        Repeat the given rows n times, applying the given offsets to the position of each key.

        :param rows: A list of lists of HWKey objects to repeat.
        :return: Extended list of HWKey objects.
        """
        if not rows:
            return []

        x_offset = self.x_offset
        y_offset = self.y_offset
        row_offset = self.row_offset
        col_offset = self.col_offset
        prev = [HWKey(**asdict(k)) for k in rows[-1]]
        n_rows = []
        for _iter in range(self.n):
            new = []
            for k in prev:
                nk = HWKey(
                    x=k.x + x_offset,
                    y=k.y + y_offset,
                )
                if k.matrix:
                    r, c = k.matrix
                    nk.matrix = (r + row_offset, c + col_offset)
                new.append(nk)
            prev = new
            n_rows.append(new)
        return n_rows


RowItem: TypeAlias = HWKey | Mirror
LayoutItem: TypeAlias = Row | Repeat


@dataclass(kw_only=True)
class Layout:
    """Represents a physical layout of keys."""

    name: str | None = None
    display: str | None = None
    rows: list[list[HWKey]] = field(init=False, default_factory=list)
    positions: list[list[int]] = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        """Set defaults if not set."""
        if not self.name:
            self.name = "layout"
        if not self.display:
            self.display = self.name

    def __truediv__(self, items: list[LayoutItem]) -> None:
        """
        Adds the given items to this layout.

        :param items: A list of LayoutItems to add to the layout.
        :return: This layout.
        """
        if isinstance(items, Row):
            items = [items]
        rows: list[list[HWKey]] = []
        for item in items:
            match item:
                case Row():
                    rows.append(item.keys)
                case Repeat():
                    rows.extend(item(rows))
                case other:
                    msg = f"Unsupported type: {type(other)}"
                    raise TypeError(msg)
        self.rows: list[list[HWKey]] = rows

        positions = []
        p = count()
        for row in rows:
            p_keys = []
            for key in row:
                key.pos = next(p)
                p_keys.append(key.pos)
            positions.append(p_keys)
        self.positions = positions

        return self

    def apply(self, data: list[T]) -> list[list[T]]:
        """
        Apply the layout to the given data.

        The given data is expected to be a one-dimensional list or other iterable.
        The function returns a two-dimensional list of lists, where each inner list
        represents a row of the layout, and contains the elements of the given data
        in the same order.

        :param data: A one-dimensional list or other iterable of data to be applied
                     to the layout.
        :return: A two-dimensional list of lists, where each inner list represents
                 a row of the layout, and contains the elements of the given data
                 in the same order.
        """
        item = iter(data)
        return [[next(item) for _k in row] for row in self.rows]

    @property
    def keys(self) -> list[HWKey]:
        """
        Returns a one-dimensional list of all the keys in the layout.

        :return: A one-dimensional list of all the keys in the layout.
        """
        return list(chain.from_iterable(self.rows))
