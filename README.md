# ZKeymap (WIP)

Python DSL for ZMK Keymaps definitions and files generation.

This tool can generate keymaps, transoforms and layouts in json and svg formats.

![](https://github.com/mnesarco/zkeymap/raw/main/docs/diagram1.png)

## Motivation

While I still prefer text-based layout definitions over graphical editors, devicetree syntax seems overly complicated. As a result, I created this small language to enable easy and pleasant keymap definitions for ZMK, eliminating the need for graphical editors.

## Big Note

You can use unicode chars directly as aliases, it looks good and works well but it is totally optional.
All aliases are user defined or can be overridden by the user.

## Usage

### 1. Install zkeymap

```bash
pip install zkeymap
```

### 2. Add a python file to your config directory, for example `mykeymap.py`

### 3. Write your keymap in zkeymap language, here is an example `splitkb.py`:

[](src/zkeymap/demo/splitkb.py)

### 4. Generate your devicetree files:

```bash
python3 mykeymap.py
```

That will generate four files as per the example:

| File | Content| Format |
|------|--------|--------|
splitkb_keymap.dtsi| Keymap, macros, dances, encoders| devicetree |
splitkb_transform.dtsi| zmk,matrix-transform | devicetree |
splitkb_layout.dtsi| zmk,physical-layout | devicetree |
splitkb_info.json | physical layout | QMK info.json |
splitkb_layout.svg | Graphical layout (built-in generator) | svg |
splitkb_drawer.svg | Graphical layout (keymap-drawer generator) | svg |
splitkb_switches_layout.svg | Graphical layout for switches holes | svg |

### 5. Then in your zmk keymap file remove the keymap node and include the generated file example:

```c
#include <behaviors.dtsi>
#include <dt-bindings/zmk/keys.h>
#include <dt-bindings/zmk/bt.h>
#include <dt-bindings/zmk/ext_power.h>
#include <dt-bindings/zmk/outputs.h>
#include <dt-bindings/zmk/matrix_transform.h>

// +------------------------------------+
// | Include the generated keymap here: |
// +------------------------------------+
#include "splitkb_keymap.dtsi"
#include "splitkb_transform.dtsi"
#include "splitkb_layout.dtsi"

/ {

    chosen {
        zmk,kscan = &kscan0;
        zmk,matrix-transform = &marz_split_3x6_4_transform;
        zmk,physical-layout = &marz_split_3x6_4;
    };

    kscan0: kscan {
        compatible = "zmk,kscan-gpio-matrix";
        label = "KSCAN";

        diode-direction = "col2row";
        wakeup-source;

        row-gpios
            = <&pro_micro 4 (GPIO_ACTIVE_HIGH | GPIO_PULL_DOWN)>
            , <&pro_micro 5 (GPIO_ACTIVE_HIGH | GPIO_PULL_DOWN)>
            , <&pro_micro 6 (GPIO_ACTIVE_HIGH | GPIO_PULL_DOWN)>
            , <&pro_micro 7 (GPIO_ACTIVE_HIGH | GPIO_PULL_DOWN)>
            ;

    };


};
```

### Commit and push your changes as usual to built the firmware.

## Basic language rules

Everything is based around aliases, you define an alias mapping any char
(even unicode chars) to ZML Keys or macros or whatever.

Depending on how you decorate the alias, it will be translated into a specific
behavior (&lt, &mo, &to, &kp, etc...)

### Aliases definitions

To define an alias just express it like this:

```python
alias / "alias" / "translation"
```

Example: define symbol `⌘` as an alias of `LGUI`:

```python
alias / "⌘" / "LGUI"
```

Then you can use `⌘` in the keymap as `[ ⌘ ]` it will be translated to `&kp LGUI`

### Key press (&kp, &sk)

Square brackets syntax `[ alias ]`.

Example:
Where `a` is an alias and `X` is the alias resolution

| syntax      | compiles to   | Notes                  |
|-------------|---------------|------------------------|
| [ a ]       | &kp X         | Simple case            |
| [ shift a ] | &kp LS(X)     | With shift mods        |
| [ ⎈ a ]     | &kp LC(X)     | With Ctrl mods         |
| [ r⇧ ⎈ a ]  | &kp RS(LC(X)) | With RShift+LCtrl mods |

For a sticky key variation, just add `~` at the end and
`&kp` will be changed to `&sk`

| syntax      | compiles to   | Notes                  |
|-------------|---------------|------------------------|
| [ lshift ~] | &sk LSHIFT    | One shot/sticky Shift  |


### Mod-Tap behavior (&mt)

Curly brackets syntax `{ mod alias }`.

Example:
Where `a` is an alias and `X` is the alias resolution.

| syntax      | compiles to   | Notes                  |
|-------------|---------------|------------------------|
| { shift a } | &mt LSHIFT X  | hold=lshift, tap=X     |
| { ⎈ a }     | &mt LCTRL X   | hold=lctrl, tap=X      |
| { r⇧ a }    | &mt RSHIFT X  | hold=rshift, tap=X     |


### Layer based behaviors (&lt, &mo, &sl, &to, &tog)

Parenthesis syntax `( layer alias )`.

Example:
Where `LAY` is a layer, `a` is an alias and `X` is the alias resolution.

| syntax      | compiles to   | Notes                  |
|-------------|---------------|------------------------|
| ( LAY )     | &mo LAY       | momentary layer        |
| ( LAY a )   | &lt LAY X     | layer tap LAY and X    |
| ( LAY / ~ )   | &lt LAY TILDE | layer tap LAY and ~    |
| ( LAY ~)    | &sl LAY       | sticky layer LAY. See the difference with previous  |
| ( LAY !)    | &to LAY       | absolute layer LAY        |
| ( LAY /)    | &tog LAY      | toggle layer LAY          |

### Raw ZMK stuff

Triangle brackets syntax `< whatever >`.

Content inside `<` and `>` is resolved to raw ZMK code.

Example:

| syntax       | compiles to   | Notes                  |
|--------------|---------------|------------------------|
| <A>          | A             | raw zmk code           |
| <&lt 1 A>    | &lt 1 A       | raw zmk code            |
| <&caps_word> | &caps_word    | raw zmk code            |
| <&kp LCTRL>  | &kp LCTRL     | raw zmk code            |


### Macros

Definitions of macros is done using aliases:

```python
alias / "hello" / macro("[shift h] e l l o")
```

Then it can be used in a layer:

```python
layer / "def" / r""" hello """
```

### Unicode

A special case for Unicode macros allows to define lower and upper variations:

```python

alias / "∴" / uc(name="t3p", char="∴", shifted="△")

layer / "def" / r""" [ ∴ ] """

```

In this case `[ ∴ ]` will be translated to `∴` on tap and to `△` on Shift tap.

## Status

This project is quite new and experimental, testers and contributors are welcome.

Key areas of contribution:

1. Documentation
2. Aliases for different languages/layouts.
3. Unit tests
4. Reporting bugs


## Common Unicode chars for keyboards

|  LEFT  | RIGHT   | UNICODE   | DESCRIPTION       |
| -------|---------|-----------|-------------------|
|  ⌘     |  r⌘     |  u2318    |  GUI/Command |
|  ⎈     |  r⎈     |  u2388    |  Ctrl |
|  ⇧     |  r⇧     |  u21E7    |  Shift |
|  ⎇     |  r⎇     |  u2387    |  Alt |
|  ⏎     |         |  u23CE    |  Enter |
|  ␣     |         |  u2423    |  Space |
|  ⌫     |         |  u232b    |  Backspace |
|  ←     |         |  u2190    |  Arrow Left |
|  ↑     |         |  u2191    |  Arrow Up |
|  →     |         |  u2192    |  Arrow Right |
|  ↓     |         |  u2193    |  Arrow Down |
|  ᛒ     |         |  u16D2    |  Bluetooth |
|  ⇪     |         |  u21EA    |  CapsLock |
|  🄰     |         | u1F130    | CapsLock |
|  ⎙     |         |  u2399    |  PrintScreen |
|  ⇄     |         |  u21C4    |  Tab |
|  ↖     |         |  u2196    |  Home |
|  ↘     |         |  u2198    |  End |
|  ⇞     |         |  u21DE    |  PgUp |
|  ⇟     |         |  u21DF    |  PgDn |
|  ↶     |         |  u21B6    |  Undo |
|  ↷     |         |  u21B7    |  Redo |
|  ✂     |         |  u2702    |  Cut |
|  ⿻     |         | u2FFb     | Copy |
|  ⧉     |         |  u29c9    |  Paste |
|  ⚙     |         |  u2699    |  Bootloader |

## Working examples

- https://github.com/mnesarco/zmk-config

## AI Usage

Codeium AI was used to generate docstrings and basic unit tests.