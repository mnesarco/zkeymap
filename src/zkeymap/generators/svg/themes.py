# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

"""
ZKeymap: Basic css theming for SVG Outputs.
"""

light = """

    .background-box {
        fill: #ffffff;
    }

    .content {
        fill: #000000;
    }

    .key-cap {
        stroke: #0080ff;
        stroke-width: 0.1;
        fill: #fafafa;
    }

    .behavior-muted .key-cap {
        stroke: #ff0000;
        stroke-width: 0.1;
        stroke-dasharray: 0.3, 0.3;
        stroke-dashoffset: 0;
        fill: #fefefe;
        opacity: 0.6;

    }

    .key-switch {
        stroke: #000000;
        stroke-width: 0.1;
        fill: none;
    }

    .key-outer {
        stroke: #dedede;
        stroke-width: 0.1;
        stroke-dasharray: 0.3, 0.3;
        stroke-dashoffset: 0;
        fill: none;
        opacity: 0.5;
    }

    .key-hold-text {
        fill: #ff0000;
        opacity: 0.5;
    }

    .key-mods-text {
        fill: #000080;
        opacity: 0.5;
    }

    .key-tap-text {
        fill: #0070ff;
    }

    .key-behavior-text {
        fill: #c0c0c0;
        opacity: 0.5;
    }

    .zkeymap-notice, .generated-date {
        opacity: 0.5;
    }

"""


dark = """

    .background-box {
        fill: #4d4d4d;
    }

    .content {
        fill: #e6e6e6;
    }

    .key-cap {
        stroke: #ffffff;
        stroke-width: 0.1;
        fill: ##afc6e9;
    }

    .behavior-muted .key-cap {
        stroke: #ff0000;
        stroke-width: 0.1;
        stroke-dasharray: 0.3, 0.3;
        stroke-dashoffset: 0;
        fill: #fefefe;
        opacity: 0.6;

    }

    .key-switch {
        stroke: #ffffff;
        stroke-width: 0.1;
        fill: none;
    }

    .key-outer {
        stroke: #dedede;
        stroke-width: 0.1;
        stroke-dasharray: 0.3, 0.3;
        stroke-dashoffset: 0;
        fill: none;
        opacity: 0.5;
    }

    .key-hold-text {
        fill: #ff0000;
        opacity: 0.5;
    }

    .key-mods-text {
        fill: #000080;
        opacity: 0.5;
    }

    .key-tap-text {
        fill: #0070ff;
    }

    .key-behavior-text {
        fill: #c0c0c0;
        opacity: 0.9;
    }

    .zkeymap-notice, .generated-date {
        opacity: 0.5;
    }

"""
