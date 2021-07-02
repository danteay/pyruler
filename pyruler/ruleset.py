"""Implementation of RuleSet policies."""

from typing import Any, AnyStr, Iterable, List, NoReturn, Optional, Set

from .errors import RuleError, RuleSetConfigError, RuleSetError
from .linked_list import LinkedList
from .rule import Rule


class RuleSet:
    """Rule Set definition to apply a set of rules to a context info.

    :param name: Identifier name of the rule set
    """

    _name: AnyStr
    _rules: LinkedList[Rule]
    _rule_hashes: Set[int]

    def __init__(self, name: AnyStr):
        self._name = name
        self._rules = LinkedList()
        self._rule_hashes = set()

    @property
    def name(self):
        """Get property value."""
        return self._name

    def add_rule(self, rule: Rule) -> NoReturn:
        """Add new role to the set.

        :param rule: New Rule object to be applied by the set
        :raises RuleSetConfigError: when the set detects that the provided rule was already added to the set
        """

        if rule.__hash__() in self._rule_hashes:
            raise RuleSetConfigError(f"Rule '{rule.name}' was already configured in the RuleSet")

        self._rules.add_last(rule)
        self._rule_hashes.add(rule.__hash__())

    def add_many(self, rules: Iterable[Rule]) -> None:
        """Add many rules at ones.

        :param rules: Iterable object of rules
        """

        hashes = set()

        for rule in rules:
            if rule.__hash__() in self._rule_hashes:
                raise RuleSetConfigError(f"Rule '{rule.name}' was already configured in the RuleSet")

            if rule.__hash__() in hashes:
                raise RuleSetConfigError(f"Rule '{rule.name}' is duplicated on the given rules")

            hashes.add(rule.__hash__())

        self._rules.add_many(rules)
        self._rule_hashes.update(hashes)

    def count_rules(self) -> int:
        """Count the total of rules configured on the set.

        :return int: Count of rules
        """

        return len(self._rules)

    def rule_names(self) -> List[AnyStr]:
        """Return a list with the names of all the configured rules of the set.

        :return List[AnyStr]: List of rule names
        """

        names = []

        for rule in self._rules:
            names.append(rule.name)

        return names

    def apply(self, data: Any, fail_fast: Optional[bool] = True) -> NoReturn:
        """Apply the configured rule set to a specific data.

        :param data: Data to be validated by the rule set
        :param fail_fast: flag to determine if the error will raise at first not True rule, or will execute all and
            collect all the rules that fails with the data before raise it.
        :raises RuleError: when the data is not complaint with some rule of the set
        """

        if self._rules.empty():
            raise RuleSetError(f'No rules configured on rule set {self._name}')

        if fail_fast:
            self._fail_fast_apply(data)
            return

        self._apply(data)

    def _fail_fast_apply(self, data: Any) -> NoReturn:
        """Apply the configured rule set to the data and raise and error with
        the first rule failure.

        :param data: Data to be validated by the rule set
        :raises RuleError: when the data is not complaint with some rule of the set
        """

        for rule in self._rules:
            if not rule.execute(data):
                if rule.error is not None:
                    raise rule.error

                raise RuleError(f"Rule '{rule.name}' fail")

    def _apply(self, data: Any) -> NoReturn:
        """Apply the configured rule set to the data and collect all the rules
        that fail before raise an error.

        :param data: Data to be validated by the rule set
        :raises RuleError: when the data is not complaint with some rule of the set
        """

        errors = []

        for rule in self._rules:
            if not rule.execute(data):
                errors.append(rule.name)

        if errors:
            raise RuleError(f"Rules '{str(errors)}' fail")

    def __hash__(self) -> int:
        """Generate hash representation.

        :return int: Has representation
        """

        return hash((self._name, self._rules))
