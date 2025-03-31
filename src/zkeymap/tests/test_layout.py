# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

# ruff: noqa: S101, PLR2004


def test_empty() -> None:
    """
    Test an empty layout.

    This test ensures that an empty layout has an empty row list.
    """
    from zkeymap.lang import Layout

    empty = Layout()

    assert empty.rows == []


def test_one_key() -> None:
    """
    Test the most basic case of a layout with one key.
    """
    from zkeymap.lang import HWKey, Layout, Row

    key = HWKey()
    layout = Layout() / Row(key)

    assert len(layout.rows) == 1
    assert len(layout.rows[0]) == 1
    assert layout.rows[0][0] is key


def test_repeat() -> None:
    """
    Test repeating a single row multiple times.

    This test creates a layout with a single row containing three keys.
    It uses the Repeat class to duplicate that row n times, where n is 3 in this case.
    The test verifies that the total number of rows is n+1 and that each row contains three keys.
    """

    from zkeymap.lang import HWKey, Layout, Repeat, Row

    n = 3

    layout = Layout() / (Row(HWKey(x=0), HWKey(x=1), HWKey(x=2)), Repeat(n=n))

    assert len(layout.rows) == n + 1
    for row in layout.rows:
        assert len(row) == 3


def test_mirror() -> None:
    """
    Test the Mirror class.

    This test creates a layout with a single row containing three keys
    followed by a Mirror object.
    The test verifies that the total number of keys is six and that the
    rightmost three keys are the same
    as the leftmost three keys, but mirrored.
    """
    from zkeymap.lang import HWKey, Layout, Mirror, Row

    pos = 9
    layout = Layout() / Row(HWKey(x=0), HWKey(x=1), HWKey(x=2), Mirror(x=pos))

    assert len(layout.rows) == 1
    assert len(layout.rows[0]) == 6
    for i, key in enumerate(reversed(layout.rows[0][:3])):
        mirrored_key = layout.rows[0][3 + i]
        assert mirrored_key.x == -(key.x + key.w) + pos
