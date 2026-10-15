from app.services.money import fmt_inr, parse_amounts


def test_amount_parsing():
    assert parse_amounts("₹18 lakh") == [1800000]
    assert parse_amounts("₹18,00,000 (INR)") == [1800000]
    assert parse_amounts("₹20L and ₹200 crore") == [2000000, 2000000000]


def test_format_inr():
    assert fmt_inr(1800000) == "₹18,00,000"
    assert fmt_inr(900000) == "₹9,00,000"
