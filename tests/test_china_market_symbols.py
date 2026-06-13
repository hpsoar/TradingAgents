import pytest

from china_market.symbols import normalize_symbol


@pytest.mark.unit
def test_normalize_explicit_a_share_suffixes():
    assert normalize_symbol("600519.SH").canonical == "600519.SH"
    assert normalize_symbol("000001.SZ").canonical == "000001.SZ"


@pytest.mark.unit
def test_normalize_provider_prefixes():
    assert normalize_symbol("sh600519").canonical == "600519.SH"
    assert normalize_symbol("sz000001").canonical == "000001.SZ"
    assert normalize_symbol("sh.688001").canonical == "688001.SH"


@pytest.mark.unit
def test_infer_common_six_digit_a_share_codes():
    assert normalize_symbol("600519").canonical == "600519.SH"
    assert normalize_symbol("688001").canonical == "688001.SH"
    assert normalize_symbol("000001").canonical == "000001.SZ"
    assert normalize_symbol("300750").canonical == "300750.SZ"


@pytest.mark.unit
def test_reject_non_a_share_symbols():
    assert normalize_symbol("AAPL") is None
    assert normalize_symbol("TSLA") is None
    assert normalize_symbol("0700.HK") is None
    assert normalize_symbol("9988.HK") is None
    assert normalize_symbol("123456") is None
