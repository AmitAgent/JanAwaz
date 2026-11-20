import pytest

from app.services.ca_number import InvalidCANumber, normalize_ca_number


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("123456789", "123456789"),
        (" 1234 5678-9 ", "123456789"),
        ("ab-12345", "AB12345"),
        ("1234/56789", "123456789"),
    ],
)
def test_normalizes_spaces_separators_and_case(raw, expected):
    assert normalize_ca_number("SBPDCL", raw) == expected


@pytest.mark.parametrize("raw", ["", "   ", "1234", "12 34", "x" * 21, "12345$67", "१२३४५६"])
def test_rejects_invalid_values(raw):
    with pytest.raises(InvalidCANumber):
        normalize_ca_number("NBPDCL", raw)


def test_rejects_unknown_discom():
    with pytest.raises(InvalidCANumber):
        normalize_ca_number("OTHER", "123456789")
