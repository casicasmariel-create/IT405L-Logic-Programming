import contextlib
import io

from is_sorted import is_sorted


def test_sorted_values_include_empty_singleton_and_duplicates():
    for values in ([], [11], [-5, -1, -1, 8], [3, 3, 3]):
        result = is_sorted(values)
        assert result is True
        assert type(result) is bool


def test_any_decrease_makes_the_entire_sequence_unsorted():
    for values in ([2, 9, 6, 12], [7, 2], [9, 4, 9]):
        result = is_sorted(list(values))
        assert result is False
        assert type(result) is bool


def test_input_is_preserved_and_function_is_silent():
    values = [1, 2, 2, 4]
    original = values.copy()
    output = io.StringIO()

    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
        is_sorted(values)

    assert values == original
    assert output.getvalue() == ""
