# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

# ruff: noqa: F401
# ruff: noqa: N801

"""ZKeymap: Public API."""

from zkeymap.private.behavior import (
    Behavior,
    CustomBx,
    HoldTapBx,
    KeyPressBx,
    LayerActionBx,
    LayerTapBx,
    ModTapBx,
    MutedBx,
    TransparentBx,
)
from zkeymap.private.data import (
    Alias,
    Dance,
    HWKey,
    Layer,
    Macro,
    Modifiers,
    Morph,
    mod,
)
from zkeymap.private.errors import ParseError
from zkeymap.private.layout import (
    Layout,
    Mirror,
    Repeat,
    Row,
)
from zkeymap.private.unicode import UnicodeMacro
from zkeymap.private.utils import Scope, ScopeInstantiationError, logger


class env(Scope):
    """
    Namespace with all the global state artifacts.
    """

    from zkeymap.private.oracle import (
        aliases,
        combos,
        dances,
        layers,
        macros,
        morphs,
    )
