# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

"""
ZKeymap: Split KB Demo.
"""

# Import base aliases
from zkeymap import keys, keys_la  # noqa: F401

# Import Language keywords and functions
from zkeymap.lang import (
    alias,
    combo,
    if_layers,
    label,
    layer,
    macro,
)

# Import unicode macros
from zkeymap.lang import (
    uc_linux_shift_ctrl_u as uc,
)

# Import or define a Physical layout
from zkeymap.layouts import marz_split_3x6_4

layout = marz_split_3x6_4.layout

# Add/Override aliases as needed
alias / "cw" / "&caps_word" / label("⇪")
alias / "zw" / "LC(LA(DOWN))"  # Windows Zoom (Linux Mint)
alias / "∴" / uc(name="t3p", char="∴", shifted="△")  # Fancy unicode chars

# Define macros
alias / "M1" / macro("[⇧ h] e l l o", name="hello")

# Define layers using Keymap DSL

layer / "def" / label("DEF") / r"""
    {⌘ esc} [ q ] [ w ] [ f ] [ p ] [ b ]      [ j ] [ l ] [ u ] [ y ] [ acut ]    [ñ]
    {⎇ tab} {⇧ a} [ r ] [ s ] [ t ] [ g ]      [ m ] [ n ] [ e ] [ i ] {⇧ o}        cw
    {⎈  \ } [ z ] [ x ] [ c ] [ d ] [ v ]      [ k ] [ h ] [ , ] [ . ] [ ; ]     [ ⏎ ]
          (num tab) (sym ⌫) (nav ␣) [⇧ ⎇]      [r⎇] (nav ␣) (sym ⌫) (adj del)
    """

layer / "num" / label("NUM") / r"""
    _____   [ * ] [ 7 ] [ 8 ] [ 9 ] [ / ]      [ / ] [ 7 ] [ 8 ] [ 9 ] [ * ] [ ∴ ]
    [ , ]   [ 0 ] [ 4 ] [ 5 ] [ 6 ] [ - ]      [ - ] [ 4 ] [ 5 ] [ 6 ] [ 0 ] [ , ]
    [ zw ]  [ . ] [ 1 ] [ 2 ] [ 3 ] [ + ]      [ + ] [ 1 ] [ 2 ] [ 3 ] [ . ] _____
                  _____ _____ _____ _____      _____ _____ _____ _____
    """

layer / "sym" / label("SYM1") / r"""
    [ | ]    [ ! ] [ " ] [ # ] [ $ ] [ % ]      [ & ] [ / ] [ [ ] [ \] ] [ = ] [ ? ]
    [ grv ]  [ * ] [ ' ] [ : ] [ _ ] [ - ]      [ - ] [ ( ] [ ) ] [ {  ] [ } ] _____
    [ diae ] [ @ ] [ ~ ] [ ^ ] [ = ] [ + ]      [ + ] [ ' ] [ < ] [ >  ] [ \ ] _____
                   (adj) _____ _____ _____      _____ _____ (num ~) _____
    """

layer / "nav" / label("NAV") / r"""
    _____ [ f1 ] [ f2 ] [ f3 ] [ f4 ] [ f5  ]     _____     [ pgup ] [  ↑  ] [ pgdn ] [  f10 ] [ f11 ]
    _____ [ ⇧  ] [ '  ] [ :  ] [ _  ] [ -   ]     [  home ] [   ←  ] [  ↓  ] [   →  ] [  end ] [ f12 ]
    _____ [ f6 ] [ f7 ] [ f8 ] [ f9 ] [ f10 ]     [ ⎈ home] [ ⎈ ←  ]  xxxxx  [ ⎈ →  ] [⎈ end ]  _____
                      _____ _____ _____ _____     _____ _____ _____ _____
    """

layer / "adj" / label("ADJ") / if_layers("num", "sym") / r"""
    [⚙]    _____     _____   _____ _____   M1       _____ _____ _____ _____ _____ [⚙]
    [ᛒclr] [ᛒ0]      [ᛒ1]    [ᛒ2]  [ᛒ3]  [ᛒ4]       [ᛒ4]  [ᛒ3]  [ᛒ2]  [ᛒ1]  [ᛒ0]  [ᛒclr]
    _____  [ nlck ]  [usb/ᛒ] _____ _____ _____      _____ _____ _____ _____ _____ _____
                     _____   _____ _____ _____      _____ _____ _____ _____
    """

# Define combos
combo(
    "[shift a]",
    key_positions=[5, 6],
    layers=["def", "sym"],
    name="test",
    timeout_ms=50,
    require_prior_idle_ms=100,
    slow_release=True,
)

# Generate files -------

# Zmk dtsi...
from zkeymap.generators import zmk  # noqa: E402

zmk.default_transform(layout, "splitkb")
zmk.physical_layout(layout, "splitkb")
zmk.keymap(layout, "splitkb")

# SVG files...
from zkeymap.generators import svg  # noqa: E402
from zkeymap.generators.svg.themes import dark  # noqa: E402

# For presentation using built-in generator
svg.layout(
    layout,
    "splitkb",
    stylesheet=dark,
    options=svg.Options(outer=True),
)

# For plate cut (Switches)
svg.layout(
    layout,
    "splitkb_switches",
    options=svg.Options(
        cap=False,
        switch=True,
        outer=False,
        cherry_pocket=True,
    ),
)

# For presentation using keymap-drawer
from zkeymap.generators import drawer  # noqa: E402

drawer.svg(layout, "splitkb")

# QMK info.json
from zkeymap.generators import qmk  # noqa: E402

qmk.info_json(layout, "splitkb")
