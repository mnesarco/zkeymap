# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

"""
Default key aliases.
"""

from zkeymap import alias, Mods, UnicodeSeq
from string import ascii_lowercase

# Modifiers

alias / ("lshift", "shift", "⇧") / "LSHIFT" / Mods("lshift")
alias / ("rshift", "r⇧") / "RSHIFT" / Mods("rshift")

alias / ("lctrl", "ctrl", "⎈") / "LCTRL" / Mods("lctrl")
alias / ("rctrl", "r⎈") / "RCTRL" / Mods("rctrl")

alias / ("lalt", "alt", "⎇" )/ "LALT" / Mods("lalt")
alias / ("ralt", "r⎇") / "RALT" / Mods("ralt")

alias / ("lgui", "gui", "⌘") / "LGUI" / Mods("lgui")
alias / ("rgui", "r⌘") / "RGUI" / Mods("rgui")

# Ascii Letters

for c in ascii_lowercase:
    alias / (c, c.upper()) / c.upper()

# Digits

for d in range(10):
    alias / str(d) / f"N{d}"

# Function keys

for d in range(1, 25):
    alias / f"f{d}" / f"F{d}"

# Power

alias / "sys_pwr" / "SYS_PWR"
alias / "k_pwr" / "K_PWR"
alias / "sys_sleep" / "SYS_SLEEP"
alias / "sys_wake" / "SYS_WAKE"

# Symbols (Standard US Keyboard)

alias / "!" / "EXCL"
alias / "@" / "AT"
alias / "#" / "HASH"
alias / "$" / "DOLLAR"
alias / "%" / "PRCNT"
alias / "^" / "CARET"
alias / "&" / "AMPS"
alias / "*" / "STAR"
alias / "(" / "LPAR"
alias / ")" / "RPAR"
alias / "-" / "MINUS"
alias / "_" / "UNDER"
alias / "=" / "EQL"
alias / "+" / "PLUS"
alias / "[" / "LBKT"
alias / "{" / "LBRC"
alias / "\\]" / "RBKT"
alias / "}" / "RBRC"
alias / "\\" / "BSLH"
alias / "|" / "PIPE"
alias / "N#" / "NUHS"
alias / "~" / "TILDE2"
alias / ";" / "SEMI"
alias / ":" / "COLON"
alias / "'" / "SQT"
alias / '"' / "DQT"
alias / "`" / "GRAVE"
alias / "grv" / "GRAVE"
alias / "G~" / "TILDE"
alias / "," / "COMMA"
alias / "<" / "LT"
alias / "." / "DOT"
alias / ">" / "GT"
alias / "/" / "SLASH"
alias / "?" / "QMARK"
alias / "\\2" / "NUBS"
alias / "|2" / "PIPE2"

# Control as white space

alias / ("ret", "enter", "⏎") / "RET"
alias / "esc" / "ESC"
alias / ("bspc", "⌫") / "BSPC"
alias / ("tab", "⇄") / "TAB"
alias / ("spc", "space", "␣") / "SPC"
alias / ("caps", "⇪", "🄰") / "CAPS"

alias / ("pscrn", "⎙") / "PSCRN"
alias / "slck" / "SLCK"
alias / "pause" / "PAUSE_BREAK"
alias / "ins" / "INS"
alias / "del" / "DEL"

# Navigation

alias / ("home", "↖") / "HOME"
alias / ("pgup", "⇞") / "PG_UP"
alias / ("end", "↘") / "END"
alias / ("pgdn", "⇟") / "PG_UP"
alias / ("right", "→") / "RIGHT"
alias / ("left", "←") / "LEFT"
alias / ("down", "↓") / "DOWN"
alias / ("up", "↑") / "UP"

# Keypad

alias / "nlck" / "KP_NLCK"
alias / "clear2" / "CLEAR2"
alias / "k/" / "KP_SLASH"
alias / "k*" / "KP_ASTERISK"
alias / "k-" / "KP_MINUS"
alias / "k+" / "KP_PLUS"
alias / "k." / "KP_DOT"
alias / "k=" / "KP_EQUAL"
alias / "k," / "KP_COMMA"
alias / ("kent", "kenter") / "KP_ENTER"

# Keypad Numbers

for d in range(10):
    alias / f"k{d}" / f"KP_N{d}"

# Undo/Redo

alias / ("redo", "↷") / "K_REDO"
alias / ("undo", "↶") / "K_UNDO"

# Clipboard

alias / ("cut", "✂") / "K_CUT"
alias / ("copy", "⿻") / "K_COPY"
alias / ("paste", "⧉") / "K_PASTE"

# Media

alias / ("vol_up", "vol+") / "K_VOL_UP"
alias / ("vol_dn", "vol-") / "K_VOL_DN"
alias / "mute" / "K_MUTE"

# Bluetooth

alias / ("btclr", "ᛒclr") / "&bt BT_CLR"
for d in range(6):
    alias / (f"bt{d}", f"ᛒ{d}") / f"&bt BT_SEL {d}"

# Config

alias / ("boot", "⚙") / "&bootloader"
alias / ("out_ble", "→ᛒ") / "&out OUT_BLE"
alias / ("out_usb", "→usb") / "&out OUT_USB"
alias / ("out_tog", "usb/ᛒ") / "&out OUT_TOG"

# Unicode sequences

UnicodeLinux = UnicodeSeq("<&macro_tap &kp LS(LC(U))>", "<&macro_tap &kp SPACE>")
UnicodeWindowsAlt = UnicodeSeq("<&macro_press &kp LALT>", "<&macro_release &kp LALT>")
UnicodeWindows = UnicodeSeq("<&macro_tap &kp RALT &kp U>", "<&macro_tap &kp RET>")
UnicodeMac = UnicodeWindowsAlt

"""
TODO: Add more aliases

/* Keyboard Execute */
#define K_EXECUTE (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_EXECUTE))
#define K_EXEC (K_EXECUTE)

/* Keyboard Help */
#define K_HELP (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_HELP))

/* Keyboard Menu */
#define K_MENU (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_MENU))

/* Keyboard Select */
#define K_SELECT (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_SELECT))

/* Keyboard Stop */
#define K_STOP (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_STOP))



/* Keyboard Find */
#define K_FIND (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_FIND))



/* Keyboard Locking Caps Lock */
#define LOCKING_CAPS (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_LOCKING_CAPS_LOCK))
#define LCAPS (LOCKING_CAPS)

/* Keyboard Locking Num Lock */
#define LOCKING_NUM (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_LOCKING_NUM_LOCK))
#define LNLCK (LOCKING_NUM)

/* Keyboard Locking Scroll Lock */
#define LOCKING_SCROLL (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_LOCKING_SCROLL_LOCK))
#define LSLCK (LOCKING_SCROLL)


/* Keypad = (Equal) AS/400 */
#define KP_EQUAL_AS400 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYPAD_EQUAL_SIGN))

/* Keyboard International 1 */
#define INTERNATIONAL_1 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_INTERNATIONAL1))
#define INT1 (INTERNATIONAL_1)
#define INT_RO (INTERNATIONAL_1)

/* Keyboard International 2 */
#define INTERNATIONAL_2 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_INTERNATIONAL2))
#define INT2 (INTERNATIONAL_2)
#define INT_KATAKANAHIRAGANA (INTERNATIONAL_2)
#define INT_KANA (INTERNATIONAL_2)

/* Keyboard International 3 */
#define INTERNATIONAL_3 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_INTERNATIONAL3))
#define INT3 (INTERNATIONAL_3)
#define INT_YEN (INTERNATIONAL_3)

/* Keyboard International 4 */
#define INTERNATIONAL_4 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_INTERNATIONAL4))
#define INT4 (INTERNATIONAL_4)
#define INT_HENKAN (INTERNATIONAL_4)

/* Keyboard International 5 */
#define INTERNATIONAL_5 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_INTERNATIONAL5))
#define INT5 (INTERNATIONAL_5)
#define INT_MUHENKAN (INTERNATIONAL_5)

/* Keyboard International 6 */
#define INTERNATIONAL_6 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_INTERNATIONAL6))
#define INT6 (INTERNATIONAL_6)
#define INT_KPJPCOMMA (INTERNATIONAL_6)

/* Keyboard International 7 */
#define INTERNATIONAL_7 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_INTERNATIONAL7))
#define INT7 (INTERNATIONAL_7)

/* Keyboard International 8 */
#define INTERNATIONAL_8 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_INTERNATIONAL8))
#define INT8 (INTERNATIONAL_8)

/* Keyboard International 9 */
#define INTERNATIONAL_9 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_INTERNATIONAL9))
#define INT9 (INTERNATIONAL_9)

/* Keyboard Language 1 */
#define LANGUAGE_1 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_LANG1))
#define LANG1 (LANGUAGE_1)
#define LANG_HANGEUL (LANGUAGE_1)

/* Keyboard Language 2 */
#define LANGUAGE_2 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_LANG2))
#define LANG2 (LANGUAGE_2)
#define LANG_HANJA (LANGUAGE_2)

/* Keyboard Language 3 */
#define LANGUAGE_3 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_LANG3))
#define LANG3 (LANGUAGE_3)
#define LANG_KATAKANA (LANGUAGE_3)

/* Keyboard Language 4 */
#define LANGUAGE_4 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_LANG4))
#define LANG4 (LANGUAGE_4)
#define LANG_HIRAGANA (LANGUAGE_4)

/* Keyboard Language 5 */
#define LANGUAGE_5 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_LANG5))
#define LANG5 (LANGUAGE_5)
#define LANG_ZENKAKUHANKAKU (LANGUAGE_5)

/* Keyboard Language 6 */
#define LANGUAGE_6 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_LANG6))
#define LANG6 (LANGUAGE_6)

/* Keyboard Language 7 */
#define LANGUAGE_7 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_LANG7))
#define LANG7 (LANGUAGE_7)

/* Keyboard Language 8 */
#define LANGUAGE_8 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_LANG8))
#define LANG8 (LANGUAGE_8)

/* Keyboard Language 9 */
#define LANGUAGE_9 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_LANG9))
#define LANG9 (LANGUAGE_9)

/* Keyboard Alternate Erase */
#define ALT_ERASE (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_ALTERNATE_ERASE))

/* Keyboard SysReq/Attention */
#define SYSREQ (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_SYSREQ_ATTENTION))
#define ATTENTION (SYSREQ)

/* Keyboard Cancel */
#define K_CANCEL (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_CANCEL))

/* Keyboard Clear */
#define CLEAR (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_CLEAR))

/* Keyboard Prior */
#define PRIOR (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_PRIOR))

/* Keyboard Return */
#define RETURN2 (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_RETURN))
#define RET2 (RETURN2)

/* Keyboard Separator */
#define SEPARATOR (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_SEPARATOR))

/* Keyboard Out */
#define OUT (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_OUT))

/* Keyboard Oper */
#define OPER (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_OPER))

/* Keyboard Clear/Again */
#define CLEAR_AGAIN (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_CLEAR_AGAIN))

/* Keyboard CrSel/Props */
#define CRSEL (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_CRSEL_PROPS))

/* Keyboard ExSel */
#define EXSEL (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_EXSEL))

/* Keyboard Currency Unit */
#define CURU                                                                                       \


/* Keypad ( (Left Parenthesis) */
#define KP_LEFT_PARENTHESIS (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYPAD_LEFT_PARENTHESIS))
#define KP_LPAR (KP_LEFT_PARENTHESIS)

/* Keypad ) (Right Parenthesis) */
#define KP_RIGHT_PARENTHESIS (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYPAD_RIGHT_PARENTHESIS))
#define KP_RPAR (KP_RIGHT_PARENTHESIS)

/* Keypad Space */
#define KSPC                                                                                       \


/* Keypad Clear */
#define KP_CLEAR (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYPAD_CLEAR))

/* Keyboard Left Control */
#define LEFT_CONTROL (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_LEFTCONTROL))
#define LCTRL (LEFT_CONTROL)


/* Keyboard Left Shift */
#define LEFT_SHIFT (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_LEFTSHIFT))
#define LSHIFT (LEFT_SHIFT)
#define LSHFT (LEFT_SHIFT)


/* Keyboard Left Alt */
#define LEFT_ALT (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_LEFTALT))
#define LALT (LEFT_ALT)

/* Keyboard Left GUI (Windows / Command / Meta) */
#define LEFT_GUI (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_LEFT_GUI))
#define LGUI (LEFT_GUI)
#define LEFT_WIN (LEFT_GUI)
#define LWIN (LEFT_GUI)
#define LEFT_COMMAND (LEFT_GUI)
#define LCMD (LEFT_GUI)
#define LEFT_META (LEFT_GUI)
#define LMETA (LEFT_GUI)

/* Keyboard Right Control */
#define RIGHT_CONTROL (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_RIGHTCONTROL))
#define RCTRL (RIGHT_CONTROL)


/* Keyboard Right Shift */
#define RIGHT_SHIFT (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_RIGHTSHIFT))
#define RSHIFT (RIGHT_SHIFT)
#define RSHFT (RIGHT_SHIFT)


/* Keyboard Right Alt */
#define RIGHT_ALT (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_RIGHTALT))
#define RALT (RIGHT_ALT)

/* Keyboard Right GUI (Windows / Command / Meta) */
#define RIGHT_GUI (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_RIGHT_GUI))
#define RGUI (RIGHT_GUI)
#define RIGHT_WIN (RIGHT_GUI)
#define RWIN (RIGHT_GUI)
#define RIGHT_COMMAND (RIGHT_GUI)
#define RCMD (RIGHT_GUI)
#define RIGHT_META (RIGHT_GUI)
#define RMETA (RIGHT_GUI)

/* Keyboard Play/Pause */
#define K_PLAY_PAUSE (ZMK_HID_USAGE(HID_USAGE_KEY, 0xE8))
#define K_PP (K_PLAY_PAUSE)

/* Keyboard Stop */
#define K_STOP2 (ZMK_HID_USAGE(HID_USAGE_KEY, 0xE9))

/* Keyboard Previous */
#define K_PREVIOUS (ZMK_HID_USAGE(HID_USAGE_KEY, 0xEA))
#define K_PREV (K_PREVIOUS)

/* Keyboard Next */
#define K_NEXT (ZMK_HID_USAGE(HID_USAGE_KEY, 0xEB))

/* Keyboard Eject */
#define K_EJECT (ZMK_HID_USAGE(HID_USAGE_KEY, 0xEC))

/* Keyboard Volume Up */
#define K_VOLUME_UP2 (ZMK_HID_USAGE(HID_USAGE_KEY, 0xED))
#define K_VOL_UP2 (K_VOLUME_UP2)

/* Keyboard Volume Down */
#define K_VOLUME_DOWN2 (ZMK_HID_USAGE(HID_USAGE_KEY, 0xEE))
#define K_VOL_DN2 (K_VOLUME_DOWN2)

/* Keyboard Mute */
#define K_MUTE2 (ZMK_HID_USAGE(HID_USAGE_KEY, 0xEF))

/* Keyboard WWW */
#define K_WWW (ZMK_HID_USAGE(HID_USAGE_KEY, 0xF0))

/* Keyboard Back */
#define K_BACK (ZMK_HID_USAGE(HID_USAGE_KEY, 0xF1))

/* Keyboard Forward */
#define K_FORWARD (ZMK_HID_USAGE(HID_USAGE_KEY, 0xF2))

/* Keyboard Stop */
#define K_STOP3 (ZMK_HID_USAGE(HID_USAGE_KEY, 0xF3))

/* Keyboard Find */
#define K_FIND2 (ZMK_HID_USAGE(HID_USAGE_KEY, 0xF4))

/* Keyboard Scroll Up */
#define K_SCROLL_UP (ZMK_HID_USAGE(HID_USAGE_KEY, 0xF5))

/* Keyboard Scroll Down */
#define K_SCROLL_DOWN (ZMK_HID_USAGE(HID_USAGE_KEY, 0xF6))

/* Keyboard Edit */
#define K_EDIT (ZMK_HID_USAGE(HID_USAGE_KEY, 0xF7))

/* Keyboard Sleep */
#define K_SLEEP (ZMK_HID_USAGE(HID_USAGE_KEY, 0xF8))

/* Keyboard Lock */
#define K_LOCK (ZMK_HID_USAGE(HID_USAGE_KEY, 0xF9))
#define K_SCREENSAVER (K_LOCK)
#define K_COFFEE (K_LOCK)

/* Keyboard Refresh */
#define K_REFRESH (ZMK_HID_USAGE(HID_USAGE_KEY, 0xFA))

/* Keyboard Calculator */
#define K_CALCULATOR (ZMK_HID_USAGE(HID_USAGE_KEY, 0xFB))
#define K_CALC (K_CALCULATOR)

/* Consumer Power */
#define C_POWER (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_POWER))
#define C_PWR (C_POWER)

/* Consumer Reset */
#define C_RESET (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_RESET))

/* Consumer Sleep */
#define C_SLEEP (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_SLEEP))

/* Consumer Sleep Mode */
#define C_SLEEP_MODE (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_SLEEP_MODE))

/* Consumer Menu */
#define C_MENU (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MENU))

/* Consumer Menu Pick */
#define C_MENU_PICK (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MENU_PICK))
#define C_MENU_SELECT (C_MENU_PICK)

/* Consumer Menu Up */
#define C_MENU_UP (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MENU_UP))

/* Consumer Menu Down */
#define C_MENU_DOWN (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MENU_DOWN))

/* Consumer Menu Left */
#define C_MENU_LEFT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MENU_LEFT))

/* Consumer Menu Right */
#define C_MENU_RIGHT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MENU_RIGHT))

/* Consumer Menu Escape */
#define C_MENU_ESCAPE (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MENU_ESCAPE))
#define C_MENU_ESC (C_MENU_ESCAPE)

/* Consumer Menu Value Increase */
#define C_MENU_INCREASE (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MENU_VALUE_INCREASE))
#define C_MENU_INC (C_MENU_INCREASE)

/* Consumer Menu Value Decrease */
#define C_MENU_DECREASE (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MENU_VALUE_DECREASE))
#define C_MENU_DEC (C_MENU_DECREASE)

/* Consumer Data On Screen */
#define C_DATA_ON_SCREEN (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_DATA_ON_SCREEN))

/* Consumer Closed Caption */
#define C_CAPTIONS (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_CLOSED_CAPTION))
#define C_SUBTITLES (C_CAPTIONS)

/* Consumer Snapshot */
#define C_SNAPSHOT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_SNAPSHOT))

/* Consumer Picture-in-Picture Toggle */
#define C_PIP (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_PICTURE_IN_PICTURE_TOGGLE))

/* Consumer Red Menu Button */
#define C_RED_BUTTON (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_RED_MENU_BUTTON))
#define C_RED (C_RED_BUTTON)

/* Consumer Green Menu Button */
#define C_GREEN_BUTTON (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_GREEN_MENU_BUTTON))
#define C_GREEN (C_GREEN_BUTTON)

/* Consumer Blue Menu Button */
#define C_BLUE_BUTTON (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_BLUE_MENU_BUTTON))
#define C_BLUE (C_BLUE_BUTTON)

/* Consumer Yellow Menu Button */
#define C_YELLOW_BUTTON (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_YELLOW_MENU_BUTTON))
#define C_YELLOW (C_YELLOW_BUTTON)

/* Consumer Aspect */
#define C_ASPECT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_ASPECT))

/* Consumer Display Brightness Increment */
#define C_BRIGHTNESS_INC                                                                           \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_DISPLAY_BRIGHTNESS_INCREMENT))
#define C_BRI_INC (C_BRIGHTNESS_INC)
#define C_BRI_UP (C_BRIGHTNESS_INC)

/* Consumer Display Brightness Decrement */
#define C_BRIGHTNESS_DEC                                                                           \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_DISPLAY_BRIGHTNESS_DECREMENT))
#define C_BRI_DEC (C_BRIGHTNESS_DEC)
#define C_BRI_DN (C_BRIGHTNESS_DEC)

/* Consumer Display Backlight Toggle */
#define C_BACKLIGHT_TOGGLE                                                                         \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_DISPLAY_BACKLIGHT_TOGGLE))
#define C_BKLT_TOG (C_BACKLIGHT_TOGGLE)

/* Consumer Display Set Brightness to Minimum */
#define C_BRIGHTNESS_MINIMUM                                                                       \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_DISPLAY_SET_BRIGHTNESS_TO_MINIMUM))
#define C_BRI_MIN (C_BRIGHTNESS_MINIMUM)

/* Consumer Display Set Brightness to Maximum */
#define C_BRIGHTNESS_MAXIMUM                                                                       \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_DISPLAY_SET_BRIGHTNESS_TO_MAXIMUM))
#define C_BRI_MAX (C_BRIGHTNESS_MAXIMUM)

/* Consumer Display Set Auto Brightness */
#define C_BRIGHTNESS_AUTO                                                                          \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_DISPLAY_SET_AUTO_BRIGHTNESS))
#define C_BRI_AUTO (C_BRIGHTNESS_AUTO)

/* Consumer Mode Step */
#define C_MEDIA_STEP (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MODE_STEP))
#define C_MODE_STEP (C_MEDIA_STEP)

/* Consumer Recall Last */
#define C_RECALL_LAST (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_RECALL_LAST))
#define C_CHAN_LAST (C_RECALL_LAST)

/* Consumer Media Select Computer */
#define C_MEDIA_COMPUTER                                                                           \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MEDIA_SELECT_COMPUTER))

/* Consumer Media Select TV */
#define C_MEDIA_TV (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MEDIA_SELECT_TV))

/* Consumer Media Select WWW */
#define C_MEDIA_WWW (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MEDIA_SELECT_WWW))

/* Consumer Media Select DVD */
#define C_MEDIA_DVD (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MEDIA_SELECT_DVD))

/* Consumer Media Select Telephone */
#define C_MEDIA_PHONE (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MEDIA_SELECT_TELEPHONE))

/* Consumer Media Select Program Guide */
#define C_MEDIA_GUIDE                                                                              \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MEDIA_SELECT_PROGRAM_GUIDE))

/* Consumer Media Select Video Phone */
#define C_MEDIA_VIDEOPHONE                                                                         \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MEDIA_SELECT_VIDEO_PHONE))

/* Consumer Media Select Games */
#define C_MEDIA_GAMES (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MEDIA_SELECT_GAMES))

/* Consumer Media Select Messages */
#define C_MEDIA_MESSAGES                                                                           \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MEDIA_SELECT_MESSAGES))

/* Consumer Media Select CD */
#define C_MEDIA_CD (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MEDIA_SELECT_CD))

/* Consumer Media Select VCR */
#define C_MEDIA_VCR (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MEDIA_SELECT_VCR))

/* Consumer Media Select Tuner */
#define C_MEDIA_TUNER (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MEDIA_SELECT_TUNER))

/* Consumer Quit */
#define C_QUIT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_QUIT))

/* Consumer Help */
#define C_HELP (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_HELP))

/* Consumer Media Select Tape */
#define C_MEDIA_TAPE (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MEDIA_SELECT_TAPE))

/* Consumer Media Select Cable */
#define C_MEDIA_CABLE (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MEDIA_SELECT_CABLE))

/* Consumer Media Select Satellite */
#define C_MEDIA_SATELLITE                                                                          \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MEDIA_SELECT_SATELLITE))

/* Consumer Media Select Home */
#define C_MEDIA_HOME (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MEDIA_SELECT_HOME))

/* Consumer Channel Increment */
#define C_CHANNEL_INC (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_CHANNEL_INCREMENT))
#define C_CHAN_INC (C_CHANNEL_INC)

/* Consumer Channel Decrement */
#define C_CHANNEL_DEC (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_CHANNEL_DECREMENT))
#define C_CHAN_DEC (C_CHANNEL_DEC)

/* Consumer VCR Plus */
#define C_MEDIA_VCR_PLUS (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_VCR_PLUS))

/* Consumer Play */
#define C_PLAY (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_PLAY))

/* Consumer Pause */
#define C_PAUSE (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_PAUSE))

/* Consumer Record */
#define C_RECORD (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_RECORD))
#define C_REC (C_RECORD)

/* Consumer Fast Forward */
#define C_FAST_FORWARD (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_FAST_FORWARD))
#define C_FF (C_FAST_FORWARD)

/* Consumer Rewind */
#define C_REWIND (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_REWIND))
#define C_RW (C_REWIND)

/* Consumer Scan Next Track */
#define C_NEXT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_SCAN_NEXT_TRACK))


/* Consumer Scan Previous Track */
#define C_PREVIOUS (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_SCAN_PREVIOUS_TRACK))
#define C_PREV (C_PREVIOUS)


/* Consumer Stop */
#define C_STOP (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_STOP))


/* Consumer Eject */
#define C_EJECT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_EJECT))


/* Consumer Random Play */
#define C_RANDOM_PLAY (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_RANDOM_PLAY))
#define C_SHUFFLE (C_RANDOM_PLAY)

/* Consumer Repeat */
#define C_REPEAT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_REPEAT))

/* Consumer Slow Tracking */
#define C_SLOW_TRACKING (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_SLOW_TRACKING))
#define C_SLOW2 (C_SLOW_TRACKING)

/* Consumer Stop/Eject */
#define C_STOP_EJECT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_STOP_EJECT))

/* Consumer Play/Pause */
#define C_PLAY_PAUSE (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_PLAY_PAUSE))
#define C_PP (C_PLAY_PAUSE)


/* Consumer Voice Command */
#define C_VOICE_COMMAND (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_VOICE_COMMAND))

/* Consumer Mute */
#define C_MUTE (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_MUTE))


/* Consumer Bass Boost */
#define C_BASS_BOOST (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_BASS_BOOST))

/* Consumer Volume Increment */
#define C_VOLUME_UP (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_VOLUME_INCREMENT))
#define C_VOL_UP (C_VOLUME_UP)


/* Consumer Volume Decrement */
#define C_VOLUME_DOWN (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_VOLUME_DECREMENT))
#define C_VOL_DN (C_VOLUME_DOWN)


/* Consumer Slow */
#define C_SLOW (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_SLOW))

/* Consumer Alternate Audio Increment */
#define C_ALTERNATE_AUDIO_INCREMENT                                                                \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_ALTERNATE_AUDIO_INCREMENT))
#define C_ALT_AUDIO_INC (C_ALTERNATE_AUDIO_INCREMENT)

/* Consumer AL Consumer Control Configuration */
#define C_AL_CCC                                                                                   \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_CONSUMER_CONTROL_CONFIGURATION))

/* Consumer AL Word Processor */
#define C_AL_WORD (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_WORD_PROCESSOR))

/* Consumer AL Text Editor */
#define C_AL_TEXT_EDITOR (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_TEXT_EDITOR))

/* Consumer AL Spreadsheet */
#define C_AL_SPREADSHEET (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_SPREADSHEET))
#define C_AL_SHEET (C_AL_SPREADSHEET)

/* Consumer AL Graphics Editor */
#define C_AL_GRAPHICS_EDITOR                                                                       \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_GRAPHICS_EDITOR))

/* Consumer AL Presentation App */
#define C_AL_PRESENTATION                                                                          \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_PRESENTATION_APP))

/* Consumer AL Database App */
#define C_AL_DATABASE (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_DATABASE_APP))
#define C_AL_DB (C_AL_DATABASE)

/* Consumer AL Email Reader */
#define C_AL_EMAIL (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_EMAIL_READER))
#define C_AL_MAIL (C_AL_EMAIL)

/* Consumer AL Newsreader */
#define C_AL_NEWS (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_NEWSREADER))

/* Consumer AL Voicemail */
#define C_AL_VOICEMAIL (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_VOICEMAIL))

/* Consumer AL Contacts/Address Book */
#define C_AL_CONTACTS                                                                              \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_CONTACTS_ADDRESS_BOOK))
#define C_AL_ADDRESS_BOOK (C_AL_CONTACTS)

/* Consumer AL Calendar/Schedule */
#define C_AL_CALENDAR (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_CALENDAR_SCHEDULE))
#define C_AL_CAL (C_AL_CALENDAR)

/* Consumer AL Task/Project Manager */
#define C_AL_TASK_MANAGER                                                                          \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_TASK_PROJECT_MANAGER))

/* Consumer AL Log/Journal/Timecard */
#define C_AL_JOURNAL (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_LOG_JOURNAL_TIMECARD))

/* Consumer AL Checkbook/Finance */
#define C_AL_FINANCE (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_CHECKBOOK_FINANCE))

/* Consumer AL Calculator */
#define C_AL_CALCULATOR (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_CALCULATOR))
#define C_AL_CALC (C_AL_CALCULATOR)

/* Consumer AL A/V Capture/Playback */
#define C_AL_AV_CAPTURE_PLAYBACK                                                                   \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_A_V_CAPTURE_PLAYBACK))

/* Consumer AL Local Machine Browser */
#define C_AL_MY_COMPUTER                                                                           \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_LOCAL_MACHINE_BROWSER))

/* Consumer AL Internet Browser */
#define C_AL_WWW (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_INTERNET_BROWSER))

/* Consumer AL Network Chat */
#define C_AL_NETWORK_CHAT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_NETWORK_CHAT))
#define C_AL_CHAT (C_AL_NETWORK_CHAT)

/* Consumer AL Logoff */
#define C_AL_LOGOFF (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_LOGOFF))

/* Consumer AL Terminal Lock/Screensaver */
#define C_AL_LOCK                                                                                  \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_TERMINAL_LOCK_SCREENSAVER))
#define C_AL_SCREENSAVER (C_AL_LOCK)
#define C_AL_COFFEE (C_AL_LOCK)

/* Consumer AL Control Panel */
#define C_AL_CONTROL_PANEL (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_CONTROL_PANEL))

/* Consumer AL Select Task/Application */
#define C_AL_SELECT_TASK                                                                           \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_SELECT_TASK_APPLICATION))

/* Consumer AL Next Task/Application */
#define C_AL_NEXT_TASK                                                                             \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_NEXT_TASK_APPLICATION))

/* Consumer AL Previous Task/Application */
#define C_AL_PREVIOUS_TASK                                                                         \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_PREVIOUS_TASK_APPLICATION))
#define C_AL_PREV_TASK (C_AL_PREVIOUS_TASK)

/* Consumer AL Integrated Help Center */
#define C_AL_HELP (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_INTEGRATED_HELP_CENTER))

/* Consumer AL Documents */
#define C_AL_DOCUMENTS (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_DOCUMENTS))
#define C_AL_DOCS (C_AL_DOCUMENTS)

/* Consumer AL Spell Check */
#define C_AL_SPELLCHECK (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_SPELL_CHECK))
#define C_AL_SPELL (C_AL_SPELLCHECK)

/* Consumer AL Keyboard Layout */
#define C_AL_KEYBOARD_LAYOUT                                                                       \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_KEYBOARD_LAYOUT))

/* Consumer AL Screen Saver */
#define C_AL_SCREEN_SAVER (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_SCREEN_SAVER))

/* Consumer AL File Browser */
#define C_AL_FILE_BROWSER (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_FILE_BROWSER))
#define C_AL_FILES (C_AL_FILE_BROWSER)

/* Consumer AL Image Browser */
#define C_AL_IMAGE_BROWSER (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_IMAGE_BROWSER))
#define C_AL_IMAGES (C_AL_IMAGE_BROWSER)

/* Consumer AL Audio Browser */
#define C_AL_AUDIO_BROWSER (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_AUDIO_BROWSER))
#define C_AL_AUDIO (C_AL_AUDIO_BROWSER)
#define C_AL_MUSIC (C_AL_AUDIO_BROWSER)

/* Consumer AL Movie Browser */
#define C_AL_MOVIE_BROWSER (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_MOVIE_BROWSER))
#define C_AL_MOVIES (C_AL_MOVIE_BROWSER)

/* Consumer AL Instant Messaging */
#define C_AL_INSTANT_MESSAGING                                                                     \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_INSTANT_MESSAGING))
#define C_AL_IM (C_AL_INSTANT_MESSAGING)

/* Consumer AL OEM Features/Tips/Tutorial Browser */
#define C_AL_OEM_FEATURES                                                                          \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AL_OEM_FEATURES_TIPS_TUTORIAL_BROWSER))
#define C_AL_TIPS (C_AL_OEM_FEATURES)
#define C_AL_TUTORIAL (C_AL_OEM_FEATURES)

/* Consumer AC New */
#define C_AC_NEW (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_NEW))

/* Consumer AC Open */
#define C_AC_OPEN (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_OPEN))

/* Consumer AC Close */
#define C_AC_CLOSE (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_CLOSE))

/* Consumer AC Exit */
#define C_AC_EXIT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_EXIT))

/* Consumer AC Save */
#define C_AC_SAVE (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_SAVE))

/* Consumer AC Print */
#define C_AC_PRINT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_PRINT))

/* Consumer AC Properties */
#define C_AC_PROPERTIES (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_PROPERTIES))
#define C_AC_PROPS (C_AC_PROPERTIES)

/* Consumer AC Undo */
#define C_AC_UNDO (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_UNDO))

/* Consumer AC Copy */
#define C_AC_COPY (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_COPY))

/* Consumer AC Cut */
#define C_AC_CUT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_CUT))

/* Consumer AC Paste */
#define C_AC_PASTE (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_PASTE))

/* Consumer AC Find */
#define C_AC_FIND (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_FIND))

/* Consumer AC Search */
#define C_AC_SEARCH (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_SEARCH))

/* Consumer AC Go To */
#define C_AC_GOTO (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_GO_TO))

/* Consumer AC Home */
#define C_AC_HOME (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_HOME))

/* Consumer AC Back */
#define C_AC_BACK (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_BACK))

/* Consumer AC Forward */
#define C_AC_FORWARD (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_FORWARD))

/* Consumer AC Stop */
#define C_AC_STOP (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_STOP))

/* Consumer AC Refresh */
#define C_AC_REFRESH (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_REFRESH))

/* Consumer AC Bookmarks */
#define C_AC_BOOKMARKS (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_BOOKMARKS))
#define C_AC_FAVORITES (C_AC_BOOKMARKS)
#define C_AC_FAVOURITES (C_AC_BOOKMARKS)

/* Consumer AC Zoom In */
#define C_AC_ZOOM_IN (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_ZOOM_IN))

/* Consumer AC Zoom Out */
#define C_AC_ZOOM_OUT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_ZOOM_OUT))

/* Consumer AC Zoom */
#define C_AC_ZOOM (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_ZOOM))

/* Consumer AC View Toggle */
#define C_AC_VIEW_TOGGLE (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_VIEW_TOGGLE))

/* Consumer AC Scroll Up */
#define C_AC_SCROLL_UP (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_SCROLL_UP))

/* Consumer AC Scroll Down */
#define C_AC_SCROLL_DOWN (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_SCROLL_DOWN))

/* Consumer AC Edit */
#define C_AC_EDIT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_EDIT))

/* Consumer AC Cancel */
#define C_AC_CANCEL (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_CANCEL))

/* Consumer AC Insert Mode */
#define C_AC_INSERT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_INSERT_MODE))
#define C_AC_INS (C_AC_INSERT)

/* Consumer AC Delete */
#define C_AC_DEL (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_DELETE))

/* Consumer AC Redo/Repeat */
#define C_AC_REDO (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_REDO_REPEAT))

/* Consumer AC Reply */
#define C_AC_REPLY (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_REPLY))

/* Consumer AC Forward Msg */
#define C_AC_FORWARD_MAIL (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_FORWARD_MSG))

/* Consumer AC Send */
#define C_AC_SEND (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_SEND))

/* Consumer AC Desktop Show All Windows */
#define C_AC_DESKTOP_SHOW_ALL_WINDOWS                                                              \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_DESKTOP_SHOW_ALL_WINDOWS))

/* Consumer AC Desktop Show All Applications */
#define C_AC_DESKTOP_SHOW_ALL_APPLICATIONS                                                         \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_AC_DESKTOP_SHOW_ALL_APPLICATIONS))

/* Consumer Keyboard Input Assist Previous */
#define C_KEYBOARD_INPUT_ASSIST_PREVIOUS                                                           \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_KEYBOARD_INPUT_ASSIST_PREVIOUS))
#define C_KBIA_PREV (C_KEYBOARD_INPUT_ASSIST_PREVIOUS)

/* Consumer Keyboard Input Assist Next */
#define C_KEYBOARD_INPUT_ASSIST_NEXT                                                               \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_KEYBOARD_INPUT_ASSIST_NEXT))
#define C_KBIA_NEXT (C_KEYBOARD_INPUT_ASSIST_NEXT)

/* Consumer Keyboard Input Assist Previous Group */
#define C_KEYBOARD_INPUT_ASSIST_PREVIOUS_GROUP                                                     \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_KEYBOARD_INPUT_ASSIST_PREVIOUS_GROUP))
#define C_KBIA_PREV_GRP (C_KEYBOARD_INPUT_ASSIST_PREVIOUS_GROUP)

/* Consumer Keyboard Input Assist Next Group */
#define C_KEYBOARD_INPUT_ASSIST_NEXT_GROUP                                                         \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_KEYBOARD_INPUT_ASSIST_NEXT_GROUP))
#define C_KBIA_NEXT_GRP (C_KEYBOARD_INPUT_ASSIST_NEXT_GROUP)

/* Consumer Keyboard Input Assist Accept */
#define C_KEYBOARD_INPUT_ASSIST_ACCEPT                                                             \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_KEYBOARD_INPUT_ASSIST_ACCEPT))
#define C_KBIA_ACCEPT (C_KEYBOARD_INPUT_ASSIST_ACCEPT)

/* Consumer Keyboard Input Assist Cancel */
#define C_KEYBOARD_INPUT_ASSIST_CANCEL                                                             \
    (ZMK_HID_USAGE(HID_USAGE_CONSUMER, HID_USAGE_CONSUMER_KEYBOARD_INPUT_ASSIST_CANCEL))
#define C_KBIA_CANCEL (C_KEYBOARD_INPUT_ASSIST_CANCEL)

/* Apple Globe key */
#define C_AC_NEXT_KEYBOARD_LAYOUT_SELECT (ZMK_HID_USAGE(HID_USAGE_CONSUMER, 0x029D))
#define GLOBE (C_AC_NEXT_KEYBOARD_LAYOUT_SELECT)

/* Keyboard Application (Context Menu) */
#define K_APPLICATION (ZMK_HID_USAGE(HID_USAGE_KEY, HID_USAGE_KEY_KEYBOARD_APPLICATION))
#define K_APP (K_APPLICATION)
#define K_CONTEXT_MENU (K_APPLICATION)
#define K_CMENU (K_APPLICATION)


"""
