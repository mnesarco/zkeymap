# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
from typing import NoReturn

logger = logging.getLogger("ZKeymap")


class ScopeInstantiationError(Exception):
    """Scope is not meant to be instantiated."""


class Scope:
    """Static namespace, allows to keep names isolated from outer scopes."""

    def __new__(cls) -> NoReturn:
        """
        Raises ScopeInstantiationError, as Scope is not meant to be instantiated.

        Scopes are used to isolate names from outer scopes.
        """
        raise ScopeInstantiationError
