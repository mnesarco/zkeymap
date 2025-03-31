# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

"""
ZKeymap: Internal implementation of builtin svg generator.
"""

from __future__ import annotations

import datetime
import html
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cached_property
from itertools import count
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Protocol

from zkeymap.api import (
    Alias,
    Behavior,
    CustomBx,
    HoldTapBx,
    HWKey,
    KeyPressBx,
    Layer,
    LayerActionBx,
    LayerTapBx,
    Layout,
    Modifiers,
    ModTapBx,
    MutedBx,
    TransparentBx,
    env,
)
from zkeymap.generators.utils import file_header_comment, path_with_suffix

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path


# All units are in millimeters (mm)

# Standard key size footprint
OUTER_KEYCAP_SIZE = (19, 19)

# Keycap border margin
KEYCAP_MARGIN = 0.7

# Keycap padding for text
KEYCAP_PADDING = 1.5

# Global document properties
DOC_FONT_SIZE = 8
DOC_MARGIN = 10

# +---------------------------------+
# | Svg Templates                   |
# +---------------------------------+

SVG_FILE = """
    <?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <!-- {comment} -->
    <svg
        width="{doc_width}mm"
        height="{doc_height}mm"
        viewBox="0 0 {doc_width} {doc_height}"
        version="1.1"
        id="svg1"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:svg="http://www.w3.org/2000/svg">
        <style>
            {stylesheet}
        </style>
        <g class="content">
            <rect x="0" y="0"
                width="{doc_width}" height="{doc_height}"
                class="background-box" />
            {layers}
        </g>
    </svg>
    """

CHERRY_SWITCH_POCKET = """
    <path transform="translate({x}, {y})" class="key-switch" id="{id}"
        d="M 0.999938,-0.799952 V 0 H 0 V 0.999939 H -0.799952 V 4.499983
        H 0 v 4.999695 h -0.799952 v 3.500045 H 0 v 0.999939 h 0.999938
        v 0.799951 h 3.500045 v -0.799951 h 4.999695 v 0.799951 h 3.50004
        v -0.799951 h 0.99994 v -0.999939 h 0.79995 V 9.499678 h -0.79995
        V 4.499983 h 0.79995 V 0.999939 h -0.79995 V 0 h -0.99994 V -0.799952
        H 9.499678 V 0 H 4.499983 v -0.799952 z" />
"""

# Auto id generator state
SVG_ID = defaultdict(count)


# Region/Item bounding box
class Rect(Protocol):
    """Duck type for geometry."""

    x: float
    y: float
    w: float
    h: float


@dataclass(kw_only=True)
class Display:
    """
    Keycap's Text values for each section.

    +------------------+
    | mods             |
    |                  |
    |       tap        |
    |                  |
    | behavior    hold |
    +------------------+

    """

    tap: str = ""
    hold: str = ""
    sticky: str = ""
    mods: str = ""
    behavior: str = ""


def next_id(prefix: str) -> str:
    """Automatic id generator with prefix."""

    def factory() -> str:
        return f"{prefix}{next(SVG_ID[prefix])}"

    return factory


def display_value(value: str | Alias) -> str:
    """Resolve display value from literal string or delegate to an Alias."""
    match value:
        case str():
            return value
        case Alias():
            return value.display
        case _:
            return "???"


def mods_display(mods: Modifiers) -> str:
    """Render modifiers looking for its aliases."""
    names = env.aliases.resolve_all(mods)
    return " ".join(display_value(name) for name in names)


def choose(*values: list[Any], options: Iterable) -> Any:
    """
    Selects an option based on the first truthy value.

    Iterates over the provided values and corresponding options.
    Returns the first option whose corresponding value is truthy.
    If no such value is found, returns None.

    :param values: Variable-length argument list of values.
    :param options: Iterable containing options corresponding to the values.
    :return: The option matching the first truthy value, or None if no truthy value is found.
    """
    for v, op in zip(values, options, strict=False):
        if v:
            return op
    return None


def display(behavior: Behavior) -> Display:  # noqa: PLR0911
    """Resolve display texts based on behavior."""
    match behavior:
        case KeyPressBx():
            return Display(
                tap=display_value(behavior.value),
                sticky=behavior.sticky,
                mods=mods_display(behavior.mods),
            )
        case HoldTapBx() | ModTapBx():
            dtap = display(behavior.tap)
            dhold = display(behavior.hold)
            return Display(
                tap=dtap.tap,
                hold=f"{dhold.mods}{dhold.tap}",
                mods=dtap.mods,
                sticky=behavior.sticky,
                behavior="mt" if isinstance(behavior, ModTapBx) else "ht",
            )
        case LayerTapBx():
            layer = env.layers.resolve(behavior.layer)
            dtap = display(behavior.tap)
            return Display(
                tap=dtap.tap,
                hold=layer.display or layer.name,
                behavior="lt",
            )
        case LayerActionBx():
            layer = env.layers.resolve(behavior.layer)
            bh = choose(
                behavior.sticky,
                behavior.absolute,
                behavior.toggle,
                True,  # noqa: FBT003
                options=("sl", "to", "tog", "mo"),
            )
            return Display(
                tap=layer.display or layer.name,
                sticky=behavior.sticky,
                behavior=bh,
            )
        case CustomBx():
            return Display(tap=behavior.raw)
        case TransparentBx():
            return Display(tap="▽")
        case MutedBx():
            return Display(tap="")
        case _:
            return Display(tap="???")


@dataclass
class SvgGroup:
    """Basic Svg Group."""

    content: str
    transform: str | None = None
    id: str = field(default_factory=next_id("g"), init=False)
    css_class: str | None = None

    def __repr__(self) -> str:
        """
        Return the SVG representation of this group element.

        :return str: The SVG representation of this group element.
        """
        transform = "" if not self.transform else f""" transform="{self.transform}" """
        css = "" if not self.css_class else f""" class="{html.escape(self.css_class)}" """
        return dedent(f"""<g id="{self.id}"{transform}{css}>{self.content}</g>""")


@dataclass
class SvgText:
    """Basic Svg Text."""

    content: str
    font_size: float = DOC_FONT_SIZE
    x: float = 0
    y: float = 0
    css_class: str = ""
    style: str = "text-align:left;text-anchor:start;"
    transform: str = ""

    @cached_property
    def w(self) -> float:  # noqa: D102
        lines = self.content.splitlines()
        if lines:
            return max(len(line) for line in lines) * self.font_size
        return 0

    @cached_property
    def h(self) -> float:  # noqa: D102
        lines = self.content.splitlines()
        return len(lines) * self.font_size

    def __repr__(self) -> str:
        """
        Return the SVG representation of this text element.

        :return str: The SVG representation of this text element.
        """
        x = f""" x="{self.x}" """ if self.x != 0 else ""
        transform = f""" transform="{self.transform}" """ if self.transform else ""
        return f"""
            <text {transform}
                y="{self.y + self.font_size}" {x}
                class="{self.css_class}"
                style="font-size:{self.font_size};{self.style};">
                <![CDATA[{self.content}]]>
            </text>
            """

    @cached_property
    def extent(self) -> tuple[float, float, float, float]:
        """Return (x, y, right, bottom)."""
        return self.x, self.y, self.right, self.bottom

    @cached_property
    def bottom(self) -> float:  # noqa: D102
        return self.y + self.h

    @cached_property
    def right(self) -> float:  # noqa: D102
        return self.x + self.w


@dataclass(kw_only=True)
class Options:
    """
    Generator options to customize output.

    switch: render switch outlines.
    outer: render outer outlines.
    cap: render Keycap.
    cherry_pocket: Render switch pockets using standard cherry shape.
    """

    switch: bool = False
    outer: bool = False
    cap: bool = True
    cherry_pocket: bool = False


@dataclass
class KeyCap:
    """Keycap data to render."""

    layer: Layer
    behavior: Behavior
    key: HWKey
    options: Options = field(default_factory=Options)
    x: float = 0
    y: float = 0
    w: float = 1
    h: float = 1
    rx: float = 0
    ry: float = 0

    def __post_init__(self) -> None:
        """Set defaults at the scale defined by `OUTER_KEYCAP_SIZE`."""
        w_unit, h_unit = OUTER_KEYCAP_SIZE
        key = self.key
        self.x, self.y, self.w, self.h, self.rx, self.ry = (
            (key.x or 0) * w_unit,
            (key.y or 0) * h_unit,
            (key.w or 1) * w_unit,
            (key.h or 1) * h_unit,
            (key.rx or 0) * w_unit,
            (key.ry or 0) * h_unit,
        )

    def outer(self) -> str:
        """
        Return SVG code to render the outer outline of this keycap.

        The outer outline is the outline of the keycap,
        including spacing.
        """
        return f"""
            <rect
                x="0"
                y="0"
                width="{self.w}"
                height="{self.h}"
                class="key-outer"/>"""

    def switch_hole(self) -> str:
        """
        Return SVG code to render a switch hole at the center of this keycap.

        The switch hole is the hole for the physical switch.
        """
        w, h = 14, 14
        x, y = (self.w - w) / 2.0, (self.h - h) / 2.0
        keyid = f"key-switch-{self.layer.num}-{self.key.pos}"
        if self.options.cherry_pocket:
            return CHERRY_SWITCH_POCKET.format(
                x=x,
                y=y,
                id=keyid,
            )
        return f"""
            <rect
                id="{keyid}"
                x="{x}"
                y="{y}"
                width="{w}"
                height="{h}"
                rx="0.5"
                ry="0.5"
                class="key-switch"/>"""

    def keycap_size(self) -> tuple[float, float]:
        """
        Calculate the size of the keycap excluding the margins (spacing).

        :returns tuple[float, float]:
            A tuple representing the width and height of the keycap
            after subtracting the margins from the total dimensions.
        """
        return self.w - 2 * KEYCAP_MARGIN, self.h - 2 * KEYCAP_MARGIN

    def cap_border(self) -> str:
        """
        Return SVG code to render a keycap border around the keycap.

        The keycap border is the outer border of the keycap. It is drawn
        after applying the margins (spacing) to the keycap size.
        """
        border_radius = 1
        w, h = self.keycap_size()
        x, y = (self.w - w) / 2.0, (self.h - h) / 2.0
        return f"""
            <rect
                x="{x}"
                y="{y}"
                width="{w}"
                height="{h}"
                rx="{border_radius}"
                ry="{border_radius}"
                class="key-cap"/>"""

    def text(self) -> str:
        """
        Return SVG code to render text on the keycap.

        This method generates and returns the SVG elements that represent
        the various text components on a keycap based on the display settings.
        It includes the main tap text, modifier text, hold text, and behavior
        text, each positioned and styled appropriately.

        :returns str:
            The SVG string containing the text elements for the keycap.
        """
        if not self.options.cap:
            return ""

        font_size = OUTER_KEYCAP_SIZE[1] * 0.3
        mod_font_size = font_size * 0.6
        hold_font_size = mod_font_size
        behavior_font_size = mod_font_size
        font_baseline = 0.2  # Percent of font size
        display = self.display()
        return f"""
            <text x="{self.w / 2}" y="{(self.h - KEYCAP_MARGIN - KEYCAP_PADDING - font_size)}"
                class="key-tap-text"
                style="text-align:center;text-anchor:middle;font-size:{font_size};">
                <![CDATA[{display.tap}]]>
            </text>
            <text x="{KEYCAP_MARGIN + KEYCAP_PADDING}"
                y="{KEYCAP_MARGIN + KEYCAP_PADDING + mod_font_size}"
                class="key-mods-text"
                style="text-align:left;text-anchor:start;font-size:{mod_font_size};">
                <![CDATA[{display.mods}]]>
            </text>
            <text x="{self.w - KEYCAP_MARGIN - KEYCAP_PADDING}"
                y="{self.h - KEYCAP_MARGIN - KEYCAP_PADDING - hold_font_size * font_baseline}"
                class="key-hold-text"
                style="text-align:right;text-anchor:end;font-size:{hold_font_size};">
                <![CDATA[{display.hold}]]>
            </text>
            <text
                x="{KEYCAP_MARGIN + KEYCAP_PADDING}"
                y="{self.h - KEYCAP_MARGIN - KEYCAP_PADDING - behavior_font_size * font_baseline}"
                class="key-behavior-text"
                style="text-align:left;text-anchor:start;font-size:{behavior_font_size};">
                <![CDATA[{display.behavior}]]>
            </text>
            """

    def __repr__(self) -> str:
        """
        Return a string representation of the SVG elements for this key.

        The method constructs an SVG group element containing various SVG
        components based on the key's options and styling. These components
        include the outer outline, switch hole, keycap border, and text.
        The SVG group is positioned and optionally rotated according to the
        key's attributes, and is assigned a CSS class based on the key's
        behavior and position.

        :returns str:
            The SVG string representing the key.
        """
        shapes = []
        if self.options.outer:
            shapes.append(self.outer())
        if self.options.switch:
            shapes.append(self.switch_hole())
        if self.options.cap:
            shapes.append(self.cap_border())
        shapes.append(self.text())
        shapes = "".join(shapes)
        g = SvgGroup(shapes, f"translate({self.x}, {self.y})")
        if self.key.r:
            g = SvgGroup(g, f"rotate({self.key.r}, {self.rx}, {self.ry})")
        bh_name = type(self.behavior).__name__.lower().removesuffix("bx")
        g.css_class = f"key keypos-{self.key.pos} behavior-{bh_name}"
        return str(g)

    __str__ = __repr__

    def display(self) -> Display:
        """Return display values for this key."""
        return display(self.behavior)


def size(items: list[Rect]) -> tuple[int, int]:
    """Calculate the total size of items."""
    if not items:
        return 0, 0
    top = float("inf")
    bottom = float("-inf")
    left = float("inf")
    right = float("-inf")
    for c in items:
        top = min(top, c.y)
        bottom = max(bottom, c.y + c.h)
        left = min(left, c.x)
        right = max(right, c.x + c.w)
    return right - left, bottom - top


@dataclass
class SvgItem:
    """Svg content block with boundaries."""

    content: str
    x: float = 0
    y: float = 0
    w: float = 0
    h: float = 0

    def __repr__(self) -> str:
        """
        Return the content of the svg item.

        This method is used to generate the SVG text representation of the
        SvgItem object. The content of the SvgItem is returned as a string,
        which is the SVG code for the item itself.

        :return str:
            The SVG content of the item.
        """
        return self.content

    __str__ = __repr__


@dataclass
class SvgContentColumn:
    """Cumulative Svg vertical content."""

    content: list[Rect] = field(default_factory=list)
    x: float = 0
    y: float = 0
    w: float = 0
    h: float = 0
    spacing: float = 0
    margins: tuple[float, float, float, float] = (10, 10, 10, 10)

    def __iadd__(self, content: Rect) -> SvgContentColumn:  # noqa: PYI034
        """
        Add the given content to the content column.

        The given content is appended to the column and the column's
        boundaries are updated accordingly. The content is assumed to be
        a vertical block of SVG content.

        The content is cumulatively added to the column, meaning that
        the column's boundaries are the minimum of the content's boundaries
        and the column's current boundaries.

        :param content: The content to be added to the column.
        :return: The same column, for chaining.
        """
        self.content.append(content)
        return self

    def space(self, height: float) -> SvgContentColumn:
        """
        Add vertical spacing to the content column.

        The given height is added to the content column as an empty SVG item
        with a width of 1 and a height of the given value. The purpose of this
        method is to add vertical spacing between items in the column.

        :param height: The height of the vertical spacing.
        """
        self.content.append(SvgItem("", w=1, h=height))
        return self

    def approx_size(self) -> tuple[float, float]:
        """
        Approximate size of the content column.

        The returned size is an approximation because it doesn't take into
        account the size of the SVG elements that will be generated for each
        item in the column. The size is calculated by adding up the heights of
        all the items in the column, plus the spacing between them, and then
        adding the margins.

        :return: A tuple of the approximate width and height of the content
            column.
        """
        m_top, m_right, m_bottom, m_left = self.margins
        w = self.x + m_left + m_right
        h = self.y + m_top + m_bottom
        for item in self.content:
            h += item.h + self.spacing
            w = max(w, item.x + item.w + m_left)
        h += m_bottom
        w += m_right
        return w, h

    def render(self) -> tuple[str, float, float]:
        """
        Render the SVG content column.

        This method generates an SVG representation of the content column,
        positioning each item with the specified margins and spacing. The items are
        wrapped in SVG groups with transformations applied to position them
        correctly. The method returns a tuple containing the generated SVG content
        as a string, and the final width and height of the rendered column.

        :return: A tuple with the SVG content as a string, and the width and height
                of the rendered column.
        """
        m_top, m_right, m_bottom, m_left = self.margins
        h = self.y + m_top
        x = self.x + m_left
        self.w = self.x + m_left + m_right
        self.h = self.y + m_top + m_bottom
        groups = []
        for item in self.content:
            groups.append(str(SvgGroup(str(item), transform=f"translate({x}, {h})")))
            h += item.h + self.spacing
            self.w = max(self.w, item.x + item.w + m_left)
        self.h = h + m_bottom
        self.w += m_right
        return "\n".join(groups), self.w, self.h


def render_keycaps(items: Iterable[KeyCap]) -> SvgItem:
    """
    Render an SVG item from a sequence of KeyCap items.

    This function takes a sequence of KeyCap items and renders them as a single
    SVG item. The SVG item is a group containing the SVG elements for each
    keycap. The width and height of the returned SVG item is the maximum width
    and height of the keycaps, respectively.

    :param items: A sequence of KeyCap items to render.
    :return: A single SVG item containing the rendered keycaps.
    """
    body = "\n".join(str(c) for c in items)
    width, height = size(items)
    return SvgItem(body, w=width, h=height)


def render_title(layout: Layout) -> SvgText:
    """
    Return an SVGText item containing the name of the given layout.

    The returned item is a text element with the name of the layout as its
    content. The font size is slightly larger than the default font size,
    and the text is centered horizontally.

    :param layout: The layout object
    :return: A new SvgText item containing the name of the layout
    """
    return SvgText(
        f"Layout: {layout.name}",
        css_class="layout-name",
        font_size=DOC_FONT_SIZE * 1.1,
    )


def render_subtitle(layout: Layout) -> SvgText:
    """
    Return an SVGText item containing the display property of the given layout.

    The returned item is a text element with the display property of the
    layout as its content. The font size is slightly smaller than the default
    font size, and the text is centered horizontally.

    :param layout: The layout object
    :return: A new SvgText item containing the display property of the layout
    """
    return SvgText(
        f"{layout.display}\n\n",
        css_class="layout-display",
        font_size=DOC_FONT_SIZE * 0.7,
    )


def render_layer_title(layer: Layer) -> SvgText:
    """
    Return an SVGText item containing the title of the given layer.

    The returned item is a text element with the title of the layer as its
    content. The font size is the default font size, and the text is centered
    horizontally. If the layer has one or more conditional layers, the title
    will include the list of conditional layers. The item is assigned a CSS class
    of "layer-title layer-<layer.num>-title".

    :param Layer layer: The layer object
    :return: A new SvgText item containing the title of the layer
    """
    conditional = f"Conditional on ({', '.join(layer.if_layers)})" if layer.if_layers else ""
    return SvgText(
        f"Layer: {layer.display} ({layer.num}) {conditional}",
        font_size=DOC_FONT_SIZE,
        css_class=f"layer-title layer-{layer.num}-title",
    )


def render_centered_text(text: str, width: float, css_class: str, font_size: float) -> SvgText:
    """
    Return an SvgText item containing the given text, centered horizontally.

    The returned item is a text element with the given text as its content,
    centered horizontally by applying a CSS transformation to move the text
    half the given width to the right. The text is assigned a CSS class of
    the given css_class, and the font size is set to the given font_size.

    :param str text: The text to be rendered
    :param float width: The width of the text element
    :param str css_class: The CSS class to assign to the text element
    :param float font_size: The font size of the text element
    :return: A new SvgText item containing the rendered text
    """
    return SvgText(
        text,
        css_class=f"{css_class}",
        style="transform-box:fill-box;text-align:center;text-anchor:middle;",
        font_size=font_size,
        transform=f"translate({width / 2}, 0)",
    )


def layout(
    layout: Layout,
    filename: str | Path,
    options: Options | None = None,
    stylesheet: str | None = None,
    layers: list[str] | None = None,
) -> None:
    """
    Render svg file.

    :param Layout layout: Selected layout
    :param str | Path filename: output file path
    :param Options | None options: customization options, defaults to None
    :param str | None stylesheet: custom css, defaults to None
    :param list[str] | None layers: included layers, all if not specified, defaults to None
    """
    if stylesheet is None:
        from .themes import light as stylesheet

    if options is None:
        options = Options()

    selected_layers = (item for item in env.layers if layers is None or item[0] in layers)

    filename = path_with_suffix(filename, "_layout.svg")
    with filename.open("w") as out:
        content = SvgContentColumn(spacing=2, margins=[DOC_MARGIN] * 4)
        content += render_title(layout)
        content += render_subtitle(layout)
        content.space(10)
        for _name, layer in selected_layers:
            content += render_layer_title(layer)
            content.space(10)
            items = zip(layer.behaviors, layout.keys, strict=False)
            caps = [KeyCap(layer, b, k, options) for (b, k) in items]
            content += render_keycaps(caps)
            content.space(10)

            # If no caps, generate only one layer
            if not options.cap:
                break

        size_w, _ = content.approx_size()
        content.space(10)

        content += render_centered_text(
            "Generated by zkeymap.",
            width=size_w,
            css_class="zkeymap-notice",
            font_size=DOC_FONT_SIZE * 0.7,
        )

        content += render_centered_text(
            str(datetime.datetime.now().isoformat(" ")),  # noqa: DTZ005
            width=size_w,
            css_class="generated-date",
            font_size=DOC_FONT_SIZE * 0.7,
        )

        all_content, doc_width, doc_height = content.render()

        out.write(
            SVG_FILE.format(
                comment=file_header_comment(""),
                doc_width=doc_width,
                doc_height=doc_height,
                layers=all_content,
                stylesheet=stylesheet,
            ).strip(),
        )
