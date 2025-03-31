# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

from .lark_utils import escaped

# Custom Quoted rules
EXPR_KP = escaped("[]", "EXPR_KP")
EXPR_HT = escaped("{}", "EXPR_HT")
EXPR_LT = escaped("()", "EXPR_LT")
EXPR_RAW = escaped("<>", "EXPR_RAW")

# Base Tokens
LITERAL = r"LITERAL: /[^<({[ \t\n\f\r]+/"
WORD = r"WORD: /\S+/"

# Main Keymap Grammar
keymap = f"""
    keymap: expr*

    ?expr: TRANSPARENT -> trans
         | NONE        -> muted
         | EXPR_KP     -> kp
         | EXPR_HT     -> ht
         | EXPR_LT     -> lt
         | EXPR_RAW    -> raw
         | LITERAL     -> lit

    kp_content: WORD+ [STICKY]
    ht_content: WORD+ [[SEP] WORD+]
    lt_content: WORD [([SEP] WORD+) | (STICKY | ABSOLUTE | TOGGLE)]

    {LITERAL}
    {EXPR_KP}
    {EXPR_HT}
    {EXPR_LT}
    {EXPR_RAW}
    {WORD}

    NONE: "xxxxx" | "🛇"
    TRANSPARENT: "_____" | "▿"
    STICKY: "~"
    SEP: "/"
    ABSOLUTE: "!"
    TOGGLE: "/"

    %import common.WS
    %ignore WS
    """
