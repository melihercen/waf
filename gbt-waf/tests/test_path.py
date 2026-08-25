from rules.path import detect_path


def test_detect_path():
    result=detect_path("/etc/passwd")

    assert result is not None
    assert result["attack"]=="PATH TRAVERSAL"

def test_normal_text_is_not_path():
    result = detect_path("Merhaba dünya")

    assert result is None