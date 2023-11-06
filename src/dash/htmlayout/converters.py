from typing import Any
from ast import literal_eval


def evaluate(string: str) -> Any:
    """
    Evaluate a string in an HTML attribute to Python.

    Args:
        string: text passed as an attribute.

    Returns:
        A Python literal.

    """
    return literal_eval(string)
