from rules.sqli import detect_sqli


def test_detect_sqli():
    result = detect_sqli("' OR 1=1 --")

    assert result is not None
    assert result["attack"] == "SQLI"


def test_normal_text_is_not_sqli():
    result = detect_sqli("Merhaba dünya")

    assert result is None