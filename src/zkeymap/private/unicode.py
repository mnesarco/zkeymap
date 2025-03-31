# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

from zkeymap.private.data import Macro, Morph, mod
from zkeymap.private.lang import MetaMacro, meta_macro, morph


def uc_sequence(char: str | bytes | bytearray | int) -> str:
    """
    Convert an unicode character into a sequence of key presses of its hex code.
    """
    if not isinstance(char, int):
        char = ord(char)
    seq = hex(char)[2:]
    return " ".join(seq)


class UnicodeMacro:
    """
    Class to convert unicode chars into Macros.
    """

    def __init__(self, meta: MetaMacro) -> None:
        """
        Meta macro to create unicode macros.

        As each OS has its leading and trailing sequences for entering
        unicode chars from keyboard, one instance of this class must be
        created per case.

        :param MetaMacro meta: Operating system dependent sequencer for unicode.
        """
        self._meta = meta

    def __call__(self, *, name: str, char: str, shifted: str | None = None) -> Morph | Macro:
        """
        Create a Macro or Morph to enter a Unicode character with optional shifted variant.

        :param name: Name of the macro.
        :param char: Unicode character for the unshifted variant.
        :param shifted: Unicode character for the shifted variant, if applicable.
        :return: A Macro or a Morph combining both unshifted and shifted variants.
        """
        lower = self._meta(uc_sequence(char), name=f"{name}_lc")
        if not shifted:
            return lower
        upper = self._meta(uc_sequence(shifted), name=f"{name}_uc")
        return morph(f"<&{lower.name}> <&{upper.name}>", mod.LShift + mod.RShift, name=name)


uc_win_alt_plus = UnicodeMacro(
    meta_macro(
        before="<&macro_press &kp LALT> <&macro_tap &kp KP_PLUS>",
        after="<&macro_release &kp LALT>",
    ),
)

uc_linux_shift_ctrl_u = UnicodeMacro(
    meta_macro(
        before="<&macro_tap &kp LS(LC(U))>",
        after="<&macro_tap &kp ENTER>",
    ),
)


uc_mac_option = UnicodeMacro(
    meta_macro(
        before="<&macro_press &kp LALT>",
        after="<&macro_release &kp LALT>",
    ),
)
