from app import sanitize_input


def test_sanitize_input_empty():
    assert sanitize_input("") == ""
    assert sanitize_input(None) == ""


def test_sanitize_input_html():
    raw = "<script>alert(1)</script> healthy food"
    sanitized = sanitize_input(raw)
    assert "<script>" not in sanitized
    assert "alert(1)" in sanitized


def test_sanitize_input_brackets():
    raw = "chicken {and} rice > pasta"
    sanitized = sanitize_input(raw)
    assert "{" not in sanitized
    assert "}" not in sanitized
    assert ">" not in sanitized
    assert "chicken and rice  pasta" in sanitized


def test_sanitize_input_length_truncation():
    raw = "a" * 1000
    sanitized = sanitize_input(raw)
    assert len(sanitized) == 500
