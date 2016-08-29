from ..plugin import kobato_format

def test_format():
    assert kobato_format("{0}", 1) == "1"
    assert kobato_format("{0} {1}", 1, 2) == "1 2"
    assert kobato_format("{1} {1}", 1, 2) == "2 2"
    assert kobato_format("{1} {0}", 1, 2) == "2 1"
    assert kobato_format("{1}", 1, 2) == "2"
    assert kobato_format("{0} {1}", 1, 2, 3) == "1 2"
    assert kobato_format("{0} {1} {...}", 1, 2, 3, 4, 5, 6) == "1 2 3 4 5 6"
    assert kobato_format("{...} {0} {1}", 1, 2, 3, 4, 5, 6) == "3 4 5 6 1 2"
    assert kobato_format("{...}", 1, 2, 3) == "1 2 3"
    assert kobato_format("{3}{2}{1}", 1, 2, 3, 4) == "432"
    assert kobato_format("text", 1, 2, 3, 4) == "text"
    assert kobato_format("text") == "text"

