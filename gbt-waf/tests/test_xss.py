from rules.xss import detect_xss


def test_detect_xss():
    result = detect_xss("<script>alert('XSS')</script>")

    assert result is not None
    assert result["attack"] == "XSS"


def test_normal_text_is_not_xss():
    result = detect_xss("Merhaba dünya")

    assert result is None