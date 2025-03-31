# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

# ruff: noqa: F401

"""
Corn like split but 3x6_4.
"""

from zkeymap.lang import HWKey, Layout, Mirror, Repeat, Row

layout = Layout(
    name="marz_split_3x6_4",
    display="Corn like split but 3x6_4",
)

layout / (
    Row(
        # 6 keys (Left side)
        HWKey(y=0.75, matrix=[0,0]),
        HWKey(x=1, y=0.75, matrix=[0,1]),
        HWKey(x=2, y=0.25, matrix=[0,2]),
        HWKey(x=3, matrix=[0,3]),
        HWKey(x=4, y=0.35, matrix=[0,4]),
        HWKey(x=5, y=0.45, matrix=[0,5]),
        # Mirror the previous keys into the Right side
        Mirror(x=17, col_offset=6),
    ),
    Repeat(n=2),  # Repeat the previous row 2 times
    Row(
        # Thumb cluster (Left side)
        HWKey(x=3.90, y=3.5, r=10, rx=3.90, ry=3.5, matrix=[3,2]),
        HWKey(x=5.00, y=3.7, r=15, rx=5.00, ry=3.7, matrix=[3,3]),
        HWKey(x=6.05, y=4.0, r=20, rx=6.05, ry=4.0, matrix=[3,4]),
        HWKey(x=7.10, y=4.4, r=25, rx=7.10, ry=4.4, matrix=[3,5]),
        # Mirror the previous keys into the Right size
        Mirror(x=17, col_offset=6),
    ),
)
