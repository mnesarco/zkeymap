# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

"""
zkeymap language implementation.
"""

# [...]     &kp
# [p:...]   &macro_press &kp
# [r:...]   &macro_release &kp
# [t:...]   &kt
# [...~]    &sk
# {_ _}     &mt
# (_ _)     &lt
# (_)       &mo
# (_ ~)     &sl
# (_ !)     &to
# (_ /)     &tog
# <_ ...>   alias
# _____     &trans
# xxxxx     &none

from __future__ import annotations

import re
from collections.abc import Iterator
from copy import copy
from dataclasses import asdict, dataclass
from functools import cached_property
from io import TextIOWrapper
from itertools import chain, count
from pathlib import Path
from textwrap import dedent as _dedent
from typing import Any, ClassVar, Protocol

from .utils import first

# Base mods aliases pattern
RE_MODS = re.compile(
    r"((?P<lr>[lr]?)(?P<mod>shift|ctrl|alt|gui|cmd|win|[scag⌘⎈⇧⎇])(?P<ilr>'?)(?P<keep>\*?))",
    re.UNICODE,
)

# mod alias to universal mod name translation table
MOD_ALIAS = {
    # - Shift
    "shift": "shift",
    "s": "shift",
    "⇧": "shift",
    # - Ctrl
    "ctrl": "ctrl",
    "c": "ctrl",
    "⎈": "ctrl",
    # - Alt
    "alt": "alt",
    "a": "alt",
    "⎇": "alt",
    # - Gui
    "gui": "gui",
    "g": "gui",
    "⌘": "gui",
    "cmd": "gui",
    "win": "gui",
}


class Mods:
    """
    Mods model: LSHIFT, RSHIFT, LCTL, RCTL, etc...
    """

    _all_mods = {
        "lshift",
        "rshift",
        "lctrl",
        "rctrl",
        "lalt",
        "ralt",
        "lgui",
        "rgui",
    }

    def __init__(self, source: str | None = None) -> None:
        """
        Create Mods from a string source.
        Example: source="lshift ralt"
        """
        self.lshift = self.rshift = 0
        self.lctrl = self.rctrl = 0
        self.lalt = self.ralt = 0
        self.lgui = self.rgui = 0
        if source:
            for it in RE_MODS.finditer(source):
                d = it.groupdict()
                side = "r" if d["lr"] == "r" or d["ilr"] == "'" else "l"
                mod = MOD_ALIAS.get(d["mod"])
                keep = 1 if d["keep"] else 0
                if mod:
                    setattr(self, f"{side}{mod}", 1 + keep)
        self.shift = self.lshift or self.rshift
        self.ctrl = self.lctrl or self.rctrl
        self.alt = self.lalt or self.ralt
        self.gui = self.lgui or self.rgui

    def __bool__(self) -> bool:
        return bool(self.shift or self.ctrl or self.alt or self.gui)

    def __repr__(self) -> str:
        if not bool(self):
            return ""
        mods = (
            name
            for (name, value) in vars(self).items()
            if value and name[0] in "rl"
        )
        return " ".join(mods)

    def fn(self, kp: str) -> str:
        """Apply the current mods to `kp` in functional style."""
        frames = []
        if self.lshift:
            frames.append("LSHIFT")
        if self.rshift:
            frames.append("RSHIFT")
        if self.lctrl:
            frames.append("LCTRL")
        if self.rctrl:
            frames.append("RCTRL")
        if self.lalt:
            frames.append("LALT")
        if self.ralt:
            frames.append("RALT")
        if self.lgui:
            frames.append("LGUI")
        if self.rgui:
            frames.append("RGUI")
        pars = len(frames) - 1
        if not kp:
            kp = frames[-1]
            frames = frames[:-1]
            pars = pars - 1
        paren = "(".join(f[0:2] for f in frames) + f"({kp})" + (")" * pars)
        if paren.startswith("("):
            return paren[1:-1]
        return paren

    def __add__(self, m: Mods) -> Mods:
        """Combine two mods"""
        mods = Mods()
        for name in (
            *Mods._all_mods,
            "shift",
            "ctrl",
            "alt",
            "gui",
        ):
            setattr(mods, name, max(getattr(self, name), getattr(m, name)))
        return mods

    @cached_property
    def key(self) -> str:
        mods = []
        for m in Mods._all_mods:
            if getattr(self, m, False):
                mods.append(m[0:2].upper())
        return "".join(sorted(mods))

    @cached_property
    def group(self) -> str:
        """Generate mods expression for morph mods"""
        key = self.key
        mods = []
        for side, mod in zip(key[::2], key[1::2], strict=False):
            match mod:
                case "S":
                    mods.append(f"MOD_{side}SFT")
                case "C":
                    mods.append(f"MOD_{side}CTL")
                case "A":
                    mods.append(f"MOD_{side}ALT")
                case "G":
                    mods.append(f"MOD_{side}GUI")
        return f"({'|'.join(mods)})"

    def __hash__(self) -> int:
        """Allow Mods to be used in dicts"""
        return hash(self.key)

    def __eq__(self, value: Mods) -> bool:
        return self.key == value.key


class Alias:
    """Core Alias model"""

    def __init__(self, alias: str) -> None:
        self.alias = alias
        self.mod: Mods | None = None
        self.normal: str | Macro | Unicode | Dance | RotEnc | None = None
        self.morph: dict[Mods, Macro] = {}

    def __repr__(self) -> str:
        return f"{self.alias!s} -> {self.normal!s} {self.morph}"

    def __str__(self) -> str:
        return str(self.normal)

    def __truediv__(
        self,
        value: str | Macro | Unicode | Dance | RotEnc | Mods,
    ) -> Alias:
        # Macros
        if isinstance(value, Macro):
            if self.normal and value.mods:
                self.morph[value.mods] = value
                if not value.name:
                    value.name = f"{self.alias}_{value.mods.key}"
                return self
            self.normal = value
            if not value.name:
                value.name = self.alias
            return self

        # Unicode
        if isinstance(value, Unicode):
            self.normal = Macro(value.normal, name=f"{value.name}_ucl")
            if value.shifted:
                self / Macro(
                    value.shifted,
                    mods="lshift rshift",
                    name=f"{value.name}_ucu",
                )
            return self

        # Simple alias
        if isinstance(value, str):
            self.normal = value
            return self

        # Other simple models
        if isinstance(value, Dance | RotEnc):
            self.normal = value
            if not value.name:
                value.name = self.alias
            return self

        # Mods
        if isinstance(value, Mods):
            self.mod = value
            return self

        msg = f"Unsupported type {type(value)}"
        raise TypeError(msg)

    @property
    def ismod(self) -> bool:
        return bool(self.mod)

    def resolve(self) -> list[str]:
        # Morph behavior
        if morph := first(self.morph):
            mods, macro = morph
            if macro.name.endswith("_ucu"):
                name = macro.name.removesuffix("_ucu")
            else:
                name = f"{macro.name}_{mods.key.lower()}"
            return [f"&{name}"]

        # Basic alias
        if isinstance(self.normal, str):
            out: list[str] = []
            for a in self.normal.split(" "):
                if isinstance(a, str):
                    out.append(a)
                else:
                    out.extend(a.resolve())
            return out

        # Macros
        if isinstance(self.normal, Macro):
            return [f"&{self.normal.name}"]

        # Tap Dance
        if isinstance(self.normal, Dance):
            return [f"&td_{self.alias}"]

        # Rotary encoder
        if isinstance(self.normal, RotEnc):
            return [f"&re_{self.alias}"]

        msg = f"Unsupported type {type(self.normal)}"
        raise TypeError(msg)


class AliasRegistry:
    """Alias container"""

    data: dict[str, Alias]

    def __init__(self):
        self.data = {}

    def __getitem__(self, symbol: str) -> str | Alias:
        symbol = symbol.strip()
        return self.data.get(symbol, symbol)

    def __truediv__(self, names: str | tuple) -> Alias:
        if isinstance(names, tuple | list):
            s, *more = names
        elif isinstance(names, str):
            s, more = names, []
        s = s.strip()
        alias = Alias(s)
        for k in chain([s], more):
            self.data[k.strip()] = alias
        return alias

    @property
    def morphs(self) -> Iterator[Alias]:
        return (a for a in alias.data.values() if a.morph)

    @property
    def macros(self) -> Iterator[Macro]:
        for a in alias.data.values():
            if isinstance(a.normal, Macro):
                yield a.normal
            if a.morph:
                yield from a.morph.values()

    @property
    def tap_dances(self) -> Iterator[Dance]:
        for a in alias.data.values():
            if isinstance(a.normal, Dance):
                yield a.normal

    @property
    def rot_encoders(self) -> Iterator[RotEnc]:
        for a in alias.data.values():
            if isinstance(a.normal, RotEnc):
                yield a.normal


class Macro:
    """Zmk Macro model"""

    names: ClassVar[set] = set()

    def __init__(
        self,
        bindings: str | list[Token],
        *,
        mods: str | None = None,
        name: str | None = None,
    ):
        self._name = None
        if name:
            self.name = name
        self.mods = Mods(mods)
        if isinstance(bindings, list):
            self.bindings = bindings
        else:
            self.bindings = list(tokenize(bindings))

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value.isidentifier():
            msg = f"Macro name '{value}' is not a valid identifier."
            raise DefinitionError(msg)

        if value and value in Macro.names:
            msg = f"Macro '{value}' was already defined."
            raise DefinitionError(msg)

        self._name = value
        Macro.names.add(value)

    def __repr__(self) -> str:
        if self.mods:
            return f"morph {self.mods!s} {str(self.bindings)}"
        return str(self.bindings)

    def render(self, writer: Writer) -> None:
        bindings = []
        kp = []
        for token in self.bindings:
            if isinstance(token, KeyPress):
                kp.append(token.zmk())
            else:
                if kp:
                    bindings.append(f"<&macro_tap {' '.join(kp)}>")
                bindings.append(f"<{token.zmk()}>")

        writer.ln(
            f"""
            / {{
                macros {{
                    {self.name}: {self.name} {{
                        compatible = "zmk,behavior-macro";
                        wait-ms = <0>;
                        tap-ms = <0>;
                        #binding-cells = <0>;
                        bindings = {", ".join(bindings)};
                    }};
                }};
            }};
            """,
            dedent=True,
        )

    @property
    def is_unicode(self) -> bool:
        if self.name and self.name.endswith("_ucl"):
            base = self.name.removesuffix("_ucl")
            return f"{base}_ucu" in Macro.names
        return False


class Dance:
    """Tap dance model"""

    def __init__(self, *bindings: list[str], name: str | None = None) -> None:
        self._name = None
        self.bindings = list(map(list, map(tokenize, bindings)))
        if name:
            self.name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if not name.isidentifier():
            msg = f"Invalid behavior name '{name}' (Dance)"
            raise ValueError(msg)

    def __repr__(self) -> str:
        return str(self.bindings)

    def render(self, writer: Writer) -> None:
        bindings = [f"<{token.zmk()}>" for token in self.bindings]
        writer.ln(
            f"""
            / {{
                behaviors {{
                    {self.name}: {self.name}_0 {{
                        compatible = "zmk,behavior-tap-dance";
                        #binding-cells = <0>;
                        tapping-term-ms = <200>;
                        bindings = {", ".join(bindings)};
                    }};
                }};
            }};
            """,
            dedent=True,
        )


class RotEnc:
    """Rotary encoder model"""

    def __init__(self, cw: str, ccw: str, name: str | None = None) -> None:
        self._name = None
        self.cw = list(tokenize(cw))
        self.ccw = list(tokenize(ccw))

        if name:
            self.name = name

        if len(self.cw) != 1 or len(self.ccw) != 1:
            msg = f"Rotary encoders accept only one behavior per side: cc=({cw}), ccw=({ccw})"
            raise ValueError(msg)

    def __repr__(self) -> str:
        return f"cw={self.cw!s} ccw={self.ccw!s}"

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if not name.isidentifier():
            msg = f"Invalid behavior name '{name}' (RotEnc)"
            raise ValueError(msg)

    def render(self, writer: Writer) -> None:
        cw = self.cw[0].zmk()
        ccw = self.ccw[0].zmk()
        writer.ln(
            f"""
            / {{
                behaviors {{
                    {self.name}: {self.name}_0 {{
                        compatible = "zmk,behavior-sensor-rotate";
                        #sensor-binding-cells = <0>;
                        bindings = <{cw}> <{ccw}>;
                    }};
                }};
            }};
            """,
            dedent=True,
        )


class Unicode:
    def __init__(
        self,
        seq: UnicodeSeq,
        normal: str,
        shifted: str | None = None,
        *,
        name: str | None = None,
    ):
        self.name = name
        self.normal = [
            *seq.head,
            *tokenize(self.char_to_keys(normal)),
            *seq.tail,
        ]
        if shifted:
            self.shifted = [
                *seq.head,
                *tokenize(self.char_to_keys(shifted)),
                *seq.tail,
            ]
        else:
            self.shifted = None

    def char_to_keys(self, char: str) -> str:
        keys = hex(ord(char)).removeprefix("0x")
        return " ".join(f"[{k}]" for k in keys)


class UnicodeSeq:
    def __init__(self, head: str, tail: str):
        self.head = list(tokenize(head))
        self.tail = list(tokenize(tail))

    def __call__(
        self, normal: str, shifted: str, *, name: str | None = None
    ) -> Unicode:
        return Unicode(self, normal, shifted, name=name)


class If:
    def __init__(self, *layers: list[str]):
        self.layers = list(layers)

    def __repr__(self) -> str:
        return str(self.layers)


@dataclass
class label:
    value: str


@dataclass
class Layer:
    name: str
    num: int
    keymap: str | None = None
    display: str | None = None
    condition: If | None = None

    def __truediv__(self, value: str | If | label) -> Layer:
        if isinstance(value, If):
            self.condition = value
            return self
        if isinstance(value, label):
            self.display = value.value
            return self
        if isinstance(value, str):
            self.keymap = value
            return self
        msg = f"unsupported type {type(value)}"
        raise ValueError(msg)

    @cached_property
    def tokens(self) -> list[Token]:
        return list(tokenize(self.keymap))

    @property
    def num_tokens(self) -> int:
        return len(self.tokens)


class LayerRegistry:
    data: dict[str, Layer]
    count: count
    first: Layer | None

    def __init__(self) -> None:
        self._analyzed = False
        self.data = {}
        self.count = count()
        self.first = None

    def __truediv__(self, value: str) -> Layer:
        if layer := self.data.get(value):
            return layer
        layer = self.data[value] = Layer(value, next(self.count))
        if self.first is None:
            self.first = layer
        return layer

    def __getitem__(self, value: str | int) -> Layer:
        if isinstance(value, int):
            return next(filter(lambda x: x.num == value, self.data.values()))
        return self.data[value]

    @property
    def num_layers(self) -> int:
        return len(self.data)

    @property
    def num_tokens(self) -> int:
        if self.num_layers == 0:
            return 0
        return len(self.first.tokens)

    def analyze(self):
        if self._analyzed:
            return

        if self.num_layers == 0:
            msg = "No Layers are defined"
            raise DefinitionError(msg)

        if self.num_tokens == 0:
            msg = f"Empty layer: {self.first.name}"
            raise DefinitionError(msg)

        num_tokens = self.num_tokens
        for l_name, layer in self.data.items():
            if layer.num_tokens != num_tokens:
                msg = (
                    f"Inconsistent layer definition: '{l_name}'. "
                    f"Required {num_tokens} tokens but only {layer.num_tokens} were defined."
                )
                raise DefinitionError(msg)

        if layout.is_empty():
            flat = [rc] * layer.num_tokens
            width = 5
            for row in (
                flat[i : i + width] for i in range(0, len(flat), width)
            ):
                layout / row

        self._analyzed = True

    def render_layer_defs(self, writer: Writer) -> None:
        for layer in self.data.values():
            writer.ln(f"#define L_{layer.name.upper()} {layer.num}")


class DefinitionError(Exception):
    pass


@dataclass
class timeout:
    ms: int


class positions:
    def __init__(self, *pos: tuple[int, ...]) -> None:
        self._pos = pos

    def __iter__(self) -> Iterator[int]:
        return iter(self._pos)


@dataclass
class Combo:
    name: str
    timeout: int | None = None
    positions: list[int] | None = None
    bindings: str | list[Token] | None = None

    def __truediv__(self, value: str | positions | timeout) -> Combo:
        if isinstance(value, str):
            self.bindings = list(tokenize(value))
            return self
        if isinstance(value, positions):
            self.positions = value
            return self
        if isinstance(value, timeout):
            self.timeout = value.ms
            return self


class ComboRegistry:
    data: dict[str, Combo]

    def __init__(self) -> None:
        self.data = {}

    def __truediv__(self, value: str) -> Combo:
        combo = self.data[value] = Combo(value)
        return combo

    def __getitem__(self, value: str) -> Combo:
        return self.data[value]


def token(delim: str, name: str) -> str:
    """
    Create a pattern to match anything enclosed with delim, Also accepts escaped close delim.

    :param str delim: open and close delimiters like "[]", "{}", "<>", "()"
    :param str name: the name of the matching group
    :return str: the pattern
    """
    ESC = "\\"
    open, close = delim
    rpar = "\\)"
    return "".join((
        f"(?P<{name}>",
        ESC,
        open,
        f"(?:\\\\({close if close != ')' else rpar})|[^",
        "\\" if close == "]" else "",
        close,
        "]",
        ")+?",
        ESC,
        close,
        ")",
    ))


def resolve(symbol: str) -> str:
    return str(alias[symbol])


TOK_KP = token("[]", "kp")
TOK_MT = token("{}", "mt")
TOK_LT = token("()", "lt")
TOK_RAW = token("<>", "raw")
TOK_TRANS = r"(?P<trans>_{3,5})"
TOK_NONE = r"(?P<none>x{3,5})"
ALL_TOKENS = "|".join((TOK_KP, TOK_MT, TOK_LT, TOK_RAW, TOK_TRANS, TOK_NONE))
TOKENS = re.compile(ALL_TOKENS)


class Token(Protocol):
    def zmk(self) -> str: ...

    @property
    def label(self) -> str: ...

    @property
    def svg_label(self) -> str: ...

def tokenize(source: str) -> Iterator[Token]:
    for t in TOKENS.finditer(source):
        d = t.groupdict()
        if kp := d.get("kp"):
            yield KeyPress(kp.strip())
        elif mt := d.get("mt"):
            yield ModTap(mt.strip())
        elif lt := d.get("lt"):
            yield LayerTap(lt.strip())
        elif raw := d.get("raw"):
            yield Raw(raw.strip())
        elif d.get("trans"):
            yield Trans()
        elif d.get("none"):
            yield Disabled()
        else:
            msg = f"Invalid sequence: '{t.string}'"
            raise ValueError(msg)


@dataclass
class Trans:
    def zmk(self) -> str:
        return "&trans"

    @property
    def label(self) -> str:
        return ""

    @property
    def svg_label(self) -> str:
        return self.label

@dataclass
class Disabled:
    def zmk(self) -> str:
        return "&none"

    @property
    def label(self) -> str:
        return "XXX"

    @property
    def svg_label(self) -> str:
        return self.label

@dataclass
class KeyPress:
    source: str

    @cached_property
    def label(self) -> str:
        return self.source.removeprefix("[").removesuffix("]").strip().replace("\\]", "]")

    @cached_property
    def svg_label(self) -> str:
        return "".join(self.label.split())

    def zmk(self) -> str:
        out = []
        mods = Mods()
        content = self.source.removeprefix("[").removesuffix("]").strip()
        if not content:
            return "&trans"
        for src in content.split():
            dat = alias[src]
            if isinstance(dat, Alias):
                if dat.ismod:
                    mods = mods + dat.mod
                else:
                    out.append(" ".join(dat.resolve()))
            else:
                print(
                    f"[WARNING] '{dat}' is not an alias, it should be defined in ZMK or compilation will fail."
                )
                out.append(dat)

        pre = " ".join(out).split()
        kp = []
        for d in pre:
            if d.lower() in Mods._all_mods:
                mods = mods + Mods(d.lower())
            else:
                kp.append(d)

        base = " ".join(kp)
        if base.strip().startswith("&"):
            if mods:
                return mods.fn(base)
            return base

        if mods:
            return f"&kp {mods.fn(base)}"
        return f"&kp {base}"


@dataclass
class ModTap:
    source: str

    @cached_property
    def label(self) -> str:
        return self.source.removeprefix("{").removesuffix("}").strip()

    @cached_property
    def svg_label(self) -> str:
        return self.label

    def zmk(self) -> str:
        content = self.source.removeprefix("{").removesuffix("}")
        mod, _, tap = content.partition(" ")
        if mod and tap:
            return f"&mt {resolve(mod)} {resolve(tap)}"
        msg = (
            f"Invalid &mt syntax. Expected {{mod tap}} but found {self.source}"
        )
        raise SyntaxError(msg)


def resolve_layer(name: str) -> Layer | None:
    try:
        return layer[name]
    except KeyError:
        msg = f"Layer not found: {name}"
        raise ValueError(msg)


@dataclass
class LayerTap:
    source: str

    @cached_property
    def label(self) -> str:
        return self.source.removeprefix("(").removesuffix(")").strip()

    @cached_property
    def svg_label(self) -> str:
        return self.label

    def zmk(self) -> str:
        content = self.source.removeprefix("(").removesuffix(")").strip()
        layer, _, tap = (p.strip() for p in content.partition(" "))

        # Sticky Layer &sl
        if layer.endswith("~"):
            layer = layer.removesuffix("~")
            return f"&sl L_{resolve_layer(layer).name.upper()}"

        # To Layer &to
        if layer.endswith("!"):
            layer = layer.removesuffix("!").strip()
            return f"&to L_{resolve_layer(layer).name.upper()}"

        # Toggle Layer &tog
        if layer.endswith("/"):
            layer = layer.removesuffix("/").strip()
            return f"&tog L_{resolve_layer(layer).name.upper()}"

        # Layer Tap &lt
        if layer and tap:
            return f"&lt L_{resolve_layer(layer).name.upper()} {resolve(tap)}"

        # Momentary Layer &mo
        if layer:
            return f"&mo L_{resolve_layer(layer).name.upper()}"


@dataclass
class Raw:
    source: str

    @cached_property
    def label(self) -> str:
        return self.source.removeprefix("<").removesuffix(">").strip()

    @cached_property
    def svg_label(self) -> str:
        return self.label

    def zmk(self) -> str:
        content = self.source.removeprefix("<").removesuffix(">").strip()
        return resolve(content)


class CCode:
    def __init__(self) -> None:
        self.code = []

    def __truediv__(self, code: str) -> CCode:
        self.code.append(_dedent(code))

    def __repr__(self) -> str:
        return "\n".join(self.code)


@dataclass(kw_only=True)
class rc:
    row: int = -1
    col: int = -1
    x: float = 0
    y: float = 0
    w: float | None = None
    h: float | None = None
    r: float | None = None
    rx: float | None = None
    ry: float | None = None

    matrix: list[int] | None = None
    label: str | None = None

    def __post_init__(self):
        if self.matrix is not None:
            self.row, self.col = self.matrix

    def map(self) -> str:
        return f"RC({self.row},{self.col})"

    def cell(self, label: str) -> dict[str, str | int | float | bool | None]:
        d = {k: v for (k, v) in asdict(self).items() if v is not None}
        d["label"] = label
        d["matrix"] = [self.row, self.col]
        if "row" in d:
            del d["row"]
        if "col" in d:
            del d["col"]
        return d

    @property
    def size(self) -> tuple[float, float]:
        return self.w or 1, self.h or 1


@dataclass(kw_only=True)
class transform:
    label: str = "default_transform"
    node: str = "keymap_transform_0"


class Layout:
    def __init__(
        self, name: str | None = None, *, description: str | None = None
    ):
        self.rows: list[list[rc]] = []
        self.num_cols: int = 0
        self.transform: transform = transform()
        self.name = name or "LAYOUT"
        self.description = description

    @classmethod
    def from_dict(cls, name: str, source: dict[str, Any]) -> Layout:
        inst = Layout(name)
        data = source.get("layout")
        if not data:
            data = source.get(name).get("layout")
        row = []
        last_x = 0

        def sortkey(a: dict) -> tuple[float,float]:
            return a.get("y", 0), a.get("x", 0)

        for j in sorted(data, key=sortkey):
            cell = rc(**j)
            w, h = cell.size
            if cell.x <= last_x + w / 2.0 and row:
                inst / row
                row = []
            row.append(cell)
            last_x = cell.x
        if row:
            inst / row
        return inst

    def __itruediv__(self, replace: Layout | str | Path) -> Layout:
        if isinstance(replace, str | Path):
            return self.import_json(replace)

        if not isinstance(replace, Layout):
            raise TypeError

        self.rows = replace.rows
        self.num_cols = replace.num_cols
        self.transform = replace.transform
        return layout

    def __truediv__(self, value: list[rc] | str | transform) -> Layout:
        if isinstance(value, list | tuple):
            self._add_row(value)
            return self
        if isinstance(value, transform):
            self.transform = transform
            return self
        if isinstance(value, str):
            self.name = f"LAYOUT_{value}"
            return self

    def _add_row(self, row: list[rc]) -> None:
        self.num_cols = max(self.num_cols, len(row))
        num_row = len(self.rows)
        num_col = 0 if row[0] is rc or row[0] is None else max(row[0].col, 0)
        current_row = []
        for item in row:
            if item is None:
                num_col = num_col + 1
                continue
            if item is rc:
                item = rc()
            if item.row < 0:
                item.row = num_row
            num_row = item.row
            if item.col < 0:
                item.col = num_col
            num_col = item.col + 1
            current_row.append(item)
        self.rows.append(current_row)

    @property
    def num_rows(self) -> int:
        return len(self.rows)

    def maps(self) -> Iterator[str]:
        return map(rc.map, chain.from_iterable(self.rows))

    def render_keymap(self, writer: Writer) -> None:
        write = writer
        write.ln(
            """
                 / {
                    keymap {
                        compatible = "zmk,keymap";""",
            dedent=True,
        )
        for lay in layer.data.values():
            write.ln()
            write.ln(f"        {lay.name} {{")
            if lay.display:
                write.ln(f'            display-name = "{lay.display}";')
            write.ln("            bindings = <")
            self.render((t.zmk() for t in lay.tokens), writer, indent=16)
            write.ln("            >;")
            if encoders := [f"<&td_{d}>" for d in alias.rot_encoders]:
                write.ln("     base {")
                write.ln(f"         sensor-bindings = {', '.join(encoders)};")
                write.ln("     };")
            write.ln("        };")
        write.ln()
        write.ln("    };")
        write.ln("};")

    def render_transform(self, writer: Writer) -> None:
        write = writer
        write.ln(
            f"""
            {self.transform.label}: {self.transform.node} {{
                compatible = "zmk,matrix-transform";
                columns = <{self.num_cols}>;
                rows = <{self.num_rows}>;
                map = <
                """,
            dedent=True,
        )
        self.render(self.maps(), write, indent=8)
        write.ln(
            """
                    >;
                };
                """,
            dedent=True,
        )

    def render(
        self,
        data: Iterator[str],
        writer: Writer,
        indent: int = 12,
        spacing: int = 2,
    ) -> None:
        write = writer
        widths = [0] * self.num_cols
        cells = [[None] * self.num_cols for i in range(self.num_rows)]
        for irow, row in enumerate(self.rows):
            offset = (self.num_cols - len(row)) // 2
            for icol, _rc in enumerate(row):
                code = next(data)
                icol_offset = icol + offset
                cells[irow][icol_offset] = code
                widths[icol_offset] = max(widths[icol_offset], len(code))

        for irow, row in enumerate(cells):
            write(" " * indent)
            for icol, code in enumerate(row):
                if code:
                    write(code.ljust(widths[icol] + spacing))
                else:
                    write(" " * (widths[icol] + spacing))
            write.ln()

    def is_empty(self) -> bool:
        return self.num_cols == 0

    def cells(self) -> Iterator[rc]:
        return chain.from_iterable(self.rows)

    def duplicate_row(self, *, y_offset: float = 1):
        if not self.rows:
            msg = "Invalid source row to copy, layout is empty."
            raise ValueError(msg)

        new_row = [copy(cell) for cell in self.rows[-1]]
        for cell in new_row:
            cell.y = cell.y + y_offset
            cell.row = cell.row + 1
        self / new_row


class Writer:
    def __init__(self, out: TextIOWrapper):
        self.out = out

    def __call__(self, *args, dedent: bool = False):
        if dedent:
            for text in args:
                self.out.write(_dedent(text))
        else:
            for text in args:
                self.out.write(text)

    def ln(self, *args, dedent: bool = False):
        self(*args, dedent=dedent)
        self("\n")


# Globals

layout = Layout()
ccode = CCode()
devicetree = CCode()
alias = AliasRegistry()
layer = LayerRegistry()
combo = ComboRegistry()
