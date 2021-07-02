"""Implementation of simple rule."""

from typing import Any, AnyStr, Callable

from .errors import RuleConfigError


class Rule:
    """Definition for atomic operation that validates data.

    :param name: Name of the rule
    :param resolver: Callable function that receives exactly 1 param as the data that will be validated
    :param error: Custom exception that can be raised by the RuleSet in case the rule validation fails
    """

    _resolve: Callable
    _name: AnyStr
    _error: Exception

    def __init__(self, name: AnyStr, resolver: Callable = None, error: Exception = None):
        self._resolver = resolver
        self._name = name
        self._error = error

    @property
    def name(self):
        """Return the name of the rule.

        :return AnyStr: Rule name
        """

        return self._name

    @property
    def error(self):
        """Return the save custom error.

        :return Exception: Configured error
        """

        return self._error

    def execute(self, data: Any) -> bool:
        """Execute rule validation.

        :param data: Data to be validated by the Rule
        :raise RuleConfigError: When the resolver is not callable
        """

        if self._resolver is None or not callable(self._resolver):
            raise RuleConfigError(f"Rule '{self._name}' doesn't have a Callable resolver")

        return self._resolver(data)

    def __hash__(self) -> int:
        """Generate hash representation.

        :return int: Has representation
        """

        return hash((self._name, self._resolver))
