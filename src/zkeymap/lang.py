# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

# ruff: noqa: F401

"""
ZKeymap: Lang.

Domain Specific Language for ZMK Keymap definitions.
"""

from zkeymap.private.data import (
    HWKey,
    mod,
)
from zkeymap.private.lang import (
    MetaMacro,
    alias,
    combo,
    if_layers,
    label,
    layer,
    macro,
    meta_macro,
    morph,
    tap_dance,
)
from zkeymap.private.layout import (
    Layout,
    Mirror,
    Repeat,
    Row,
)
from zkeymap.private.unicode import (
    uc_linux_shift_ctrl_u,
    uc_mac_option,
    uc_win_alt_plus,
)
