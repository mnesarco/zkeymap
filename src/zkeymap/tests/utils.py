# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

from random import randint

MAX_UNICODE = 0x10FFFF


def rand_string(min_len: int = 0, max_len: int = 10, exclude: str = "") -> str:
    """
    Return a random string with random length between min_len and max_len.

    The string will contain random characters in the range of valid Unicode
    code points (i.e. 1 to 0x10FFFF). If any of the characters in the string
    are in the exclude string, they are excluded from the output.

    :param min_len: Minimum length of the generated string
    :param max_len: Maximum length of the generated string
    :param exclude: String of characters to exclude from the output
    :return: Random string
    """
    length = randint(min_len, max_len)  # noqa: S311
    chars = (chr(randint(1, MAX_UNICODE)) for _ in range(length))  # noqa: S311
    return "".join(c for c in chars if c not in exclude)
