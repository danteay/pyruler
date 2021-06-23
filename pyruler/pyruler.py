"""Ruler definitions."""

from queue import Queue
from typing import (
    Any,
    AnyStr,
    Callable,
    Dict,
    List,
    NoReturn,
    Optional,
    Set,
    Tuple,
    Union,
)

from .errors import RuleError, RulerConfigError, RulerError, RuleSetConfigError


class Rule:
    """Base Rule definition."""

    _resolve: Callable
    _name: AnyStr

    def __init__(self, name: AnyStr, resolver: Callable):
        self._resolver = resolver
        self._name = name

    @property
    def name(self):
        """Return the name of the rule.

        :return AnyStr: Rule name
        """

        return self._name

    def execute(self, data: Any) -> bool:
        """Execute rule validation.

        :param data:
        """

        return self._resolver(data)

    def __hash__(self) -> int:
        """Generate hash representation.

        :return int: Has representation
        """

        return hash((self._name, self._resolver))


class RuleSet:
    """Rule Set definition to apply a set of rules to a context info."""

    _name: AnyStr
    _rules: Queue
    _rule_hashes: Set[int]

    def __init__(self, name: AnyStr):
        self._name = name
        self._rules = Queue()
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
            raise RuleSetConfigError(f"Rule '{rule.name}' was already configured in the RuleSet", )

        self._rules.put(rule)
        self._rule_hashes.add(rule.__hash__())

    def count_rules(self) -> int:
        """Count the total of rules configured on the set.

        :return int: Count of rules
        """

        return self._rules.qsize()

    def apply(self, data: Any, fail_fast: Optional[bool] = True) -> NoReturn:
        """Apply the configured rule set to a specific data.

        :param data: Data to be validated by the rule set
        :param fail_fast: flag to determine if the error will raise at first not True rule, or will execute all and
            collect all the rules that fails with the data before raise it.
        :raises RuleError: when the data is not complaint with some rule of the set
        """

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

        while not self._rules.empty():
            rule = self._rules.get()

            if not rule.execute(data):
                raise RuleError(f"Rule '{rule.name}' fail")

    def _apply(self, data: Any) -> NoReturn:
        """Apply the configured rule set to the data and collect all the rules
        that fail before raise an error.

        :param data: Data to be validated by the rule set
        :raises RuleError: when the data is not complaint with some rule of the set
        """

        errors = []

        while not self._rules.empty():
            rule = self._rules.get()

            if not rule.execute(data):
                errors.append(rule.name)

        if errors:
            raise RuleError(f"Rules '{str(errors)}' fail")

    def __hash__(self) -> int:
        """Generate hash representation.

        :return int: Has representation
        """

        return hash((self._name, self._rules))


class Ruler:
    """Compound ruler class."""

    _rule_sets: Dict[AnyStr, RuleSet]
    _rule_set_hashes: Set[int]

    def __init__(self):
        self._rule_sets = {}
        self._rule_set_hashes = set()

    def add_set(self, rule_set: RuleSet) -> NoReturn:
        """Add a new Rule set to the ruler.

        :param rule_set: configured rule set object
        :raises RulerConfigError: When the ruler detects that the provided rule_set was already configured
        """

        if rule_set.__hash__() in self._rule_set_hashes:
            raise RulerConfigError(f"RuleSet '{rule_set.name}' was already configured on the ruler", )

        self._rule_sets.update({rule_set.name: rule_set})
        self._rule_set_hashes.add(rule_set.__hash__())

    def count_sets(self) -> int:
        """Count the total of configured sets.

        :return int: Count of sets
        """

        return len(self._rule_sets.keys())

    def apply(
        self,
        sets: Union[AnyStr, Tuple, List[AnyStr], Set[AnyStr]],
        data: Any,
        fail_fast: Optional[bool] = True,
    ) -> NoReturn:
        """Apply specified rule set, all of the stored sets or a sub collection
        of the stored rule sets.

        :param sets: Rule sets to be applied
        :param data: Data to be validated by the rule sets
        :param fail_fast: Run on fail fast mode
        :raises RuleError: When some rule was not asserted successfully by the rule set
        :raises RulerError: When some set can't be applied
        """

        sets = self._process_set_names(sets)

        if isinstance(sets, set):
            self._apply_set(set_names=sets, data=data, fail_fast=fail_fast)
            return

        self._apply_one(set_name=sets, data=data, fail_fast=fail_fast)

    def _apply_set(
        self,
        set_names: Set[AnyStr],
        data: Any,
        fail_fast: Optional[bool] = True,
    ) -> NoReturn:
        """Apply configured rule sets to the provided data.

        :param set_names: List of set names
        :param data: Data to be validated by the rule sets
        :param fail_fast: Run on fail fast mode
        :raise RuleError: When some rule was not asserted successfully by the rule set
        :raise RulerError: When some set can't be applied
        """

        for set_name in set_names:
            self._apply_one(set_name, data, fail_fast)

    def _apply_one(self, set_name: AnyStr, data: Any, fail_fast: Optional[bool] = True) -> NoReturn:
        """Apply just one rule set to the data.

        :param set_name: Rule set name to be applied
        :param data: Data to be validated by the rule sets
        :param fail_fast: Run on fail fast mode
        :raise RuleError: When some rule was not asserted successfully by the rule set
        :raise RulerError: When some set can't be applied
        """

        rule_set = self._get_rule_set(set_name)
        rule_set.apply(data, fail_fast)

    def _get_rule_set(self, set_name: AnyStr) -> RuleSet:
        """Get the corresponding rule set by name.

        :param set_name: Rule set name.
        :raises RulerError: When the required rule set is not configured on the ruler
        """

        rule_set = self._rule_sets.get(set_name, None)

        if rule_set is None:
            raise RulerError(f"Not found RuleSet '{set_name}' on Ruler configuration", )

        return rule_set

    def _process_set_names(self, sets: Any) -> Union[AnyStr, Set[AnyStr]]:
        """Verify the set names that will be applied and format it.

        :param sets: Set name or List of set names.
        :return Union[AnyStr, Set[AnyStr]]: Formatted set names
        """

        if isinstance(sets, str) and sets.lower() == 'all':
            return set(self._rule_sets.keys())

        if isinstance(sets, (tuple, list)):
            return set(sets)

        return sets
