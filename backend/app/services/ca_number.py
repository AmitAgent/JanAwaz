import re
from dataclasses import dataclass


class InvalidCANumber(ValueError):
    """The CA Number is not in an acceptable format for the DISCOM."""


@dataclass(frozen=True)
class CARule:
    pattern: re.Pattern[str]
    description: str


# Generic rule for now: letters and digits, 5 to 20 characters. Tighten per DISCOM here
# once the real formats are confirmed; nothing else in the code needs to change.
_GENERIC = CARule(re.compile(r"[A-Z0-9]{5,20}"), "5 to 20 letters or digits")
CA_RULES: dict[str, CARule] = {"SBPDCL": _GENERIC, "NBPDCL": _GENERIC}

_SEPARATORS = re.compile(r"[\s\-_/.]+")


def normalize_ca_number(discom: str, raw: str) -> str:
    """Return the canonical CA Number, or raise InvalidCANumber.

    Removes spaces and common separators and uppercases letters.
    """
    rule = CA_RULES.get(discom)
    if rule is None:
        raise InvalidCANumber(f"Unknown DISCOM: {discom!r}")
    value = _SEPARATORS.sub("", raw or "").upper()
    if not rule.pattern.fullmatch(value):
        raise InvalidCANumber(f"CA Number must be {rule.description}")
    return value
