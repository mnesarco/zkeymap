# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

# ruff: noqa: S101

from zkeymap.private.parser import KeymapParser, Kp

parser = KeymapParser()


def test_keypress() -> None:
    """
    Tests that a single keypress is parsed correctly.
    """

    data = "[ A ]"
    result = parser.parse(data)
    assert len(result) == 1
    assert isinstance(result[0], Kp)
    assert result[0].words == ["A"]
    assert result[0].sticky is False


def test_keypress_sticky() -> None:
    """
    Tests that a single keypress with sticky modifier is parsed correctly.
    """

    data = "[ A ~]"
    result = parser.parse(data)
    assert len(result) == 1
    assert isinstance(result[0], Kp)
    assert result[0].words == ["A"]
    assert result[0].sticky is True
