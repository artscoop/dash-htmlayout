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


def evaluate_var(name: str) -> Any:
    """
    Get a local variable from its name.

    Args:
        name: local variable name. Must start with "data_".

    Returns:
        The content of the variable with the name passed as an argument.

    Raises:
        KeyError: when you give a non-existing name.
        ValueError: if the variable name does not start with data_.
    """
    if name.startswith("data_"):
        return locals()[name]
    else:
        raise ValueError("Only var names starting with data_ are allowed.")