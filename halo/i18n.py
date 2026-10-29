"""Translation of the interface.

The English text is the key: a string is looked up in ``lang/<code>.json`` and
falls back to the English text itself, so a missing or damaged translation file
can never leave the menu empty.  ``t()`` is called again every time the menu is
built, which is why switching the language needs no restart.

    from halo import i18n
    i18n.load("zh-CN")          # "auto" follows the Windows display language
    i18n.t("Preferences")       # -> "首选项"
    i18n.t("Show {name}", name="Razer")   # -> "显示 Razer"
"""

from __future__ import annotations

import json
import logging
import os
import sys
from typing import Dict, Optional

log = logging.getLogger("halo_battery")

DEFAULT = "en"
AUTO = "auto"

# code -> name in its own language, for the Language menu
LANGUAGES = {"en": "English", "zh-CN": "简体中文", "zh-TW": "繁體中文"}

# How many strings the last load() got: shown in Diagnostics
_lines = 0
_strings: Dict[str, str] = {}
_code = DEFAULT


def lang_dir() -> str:
    """The ``lang`` folder: next to the sources, next to the .exe when someone drops
    their own translations there, or inside PyInstaller's bundle."""
    if getattr(sys, "frozen", False):
        beside = os.path.join(os.path.dirname(sys.executable), "lang")
        if os.path.isdir(beside):
            return beside
        base = getattr(sys, "_MEIPASS", None) or os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "lang")


def available() -> Dict[str, str]:
    """The languages that can be shown: English plus every ``lang/*.json``."""
    found = {DEFAULT: LANGUAGES[DEFAULT]}
    try:
        names = sorted(os.listdir(lang_dir()))
    except OSError:
        return found
    for name in names:
        if name.lower().endswith(".json"):
            code = name[:-5]
            found[code] = LANGUAGES.get(code, code)
    return found


def system_language() -> str:
    """The Windows display language, when one of ours matches it."""
    if sys.platform != "win32":
        return DEFAULT
    try:
        import ctypes
        langid = int(ctypes.windll.kernel32.GetUserDefaultUILanguage())
    except Exception:
        return DEFAULT
    if (langid & 0x3FF) != 0x04:          # 0x04 = Chinese; anything else stays English
        return DEFAULT
    sub = (langid >> 10) & 0x3F           # 1 = Taiwan, 2 = PRC, 3 = Hong Kong
    if sub in (1, 3) and "zh-TW" in available():
        return "zh-TW"
    return "zh-CN" if "zh-CN" in available() else DEFAULT


def load(code: Optional[str] = None) -> str:
    """Read ``lang/<code>.json``.  Returns the language that is in use now."""
    global _code, _strings, _lines
    code = (code or AUTO).strip() if isinstance(code, str) else AUTO
    if code in ("", AUTO):
        code = system_language()
    if code not in available():
        code = DEFAULT
    strings: Dict[str, str] = {}
    if code != DEFAULT:
        path = os.path.join(lang_dir(), code + ".json")
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                strings = {k: v for k, v in data.items() if isinstance(v, str)}
            else:
                log.warning("i18n: %s is not a JSON object, using English", path)
                code = DEFAULT
        except OSError:
            log.info("i18n: %s is missing, using English", path)
            code = DEFAULT
        except ValueError as e:
            log.warning("i18n: %s is damaged (%s), using English", path, e)
            code = DEFAULT
    _code, _strings, _lines = code, strings, len(strings)
    return code


def current() -> str:
    return _code


def t(text: str, **kw) -> str:
    """The translation of ``text``, or ``text`` itself when there is none."""
    out = _strings.get(text)
    if out is None:
        out = text
    if not kw:
        return out
    try:
        return out.format(**kw)
    except (KeyError, IndexError, ValueError):
        try:
            return text.format(**kw)
        except (KeyError, IndexError, ValueError):
            return out


def date(d) -> str:
    """A date the way the language writes it: ``5 October 2026`` / ``2026年10月5日``."""
    if _code.startswith("zh"):
        return "%d年%d月%d日" % (d.year, d.month, d.day)
    return "{} {} {}".format(d.day, d.strftime("%B"), d.year)


def status() -> str:
    """One line for the diagnostics report."""
    if _code == DEFAULT:
        return "language: English (built in)"
    return "language: {} ({} strings from lang/{}.json)".format(_code, _lines, _code)
