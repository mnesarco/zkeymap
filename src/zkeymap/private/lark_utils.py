# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

from textwrap import dedent


def escaped(par: str, name: str) -> str:
    """
    Create a rule for an enclosed string with custom quotes and escape sequence.

    :param par: pair of quote chars ie "[]", "{}", "()", "<>", "||", ...
    :param name: name of the rule.
    """

    left, right = par
    name = name.upper()
    rule = rf"""
        _{name}_INNER: /.*?/
        _{name}_ESC_INNER: _{name}_INNER /(?<!\\)(\\\\)*?/

        {name}: "{left}" _{name}_ESC_INNER "{right}"
        """
    return dedent(rule).strip()
