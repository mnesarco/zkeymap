# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

from __future__ import annotations
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K")

def first(d: dict[K, T]) -> tuple[K,T]:
    """Return the first tuple from a dictionary if any"""
    try:
        return next(iter(d.items()))
    except StopIteration:
        return None

