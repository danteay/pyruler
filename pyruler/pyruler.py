"""Ruler definitions."""

from typing import (
    Any,
    AnyStr,
    Dict,
    Iterable,
    List,
    NoReturn,
    Optional,
    Set,
    Tuple,
    Union,
)

from .errors import RulerConfigError, RulerError
from .ruleset import RuleSet


class Ruler:
    """Store RuleSet objects to be applied over a given data. This class can apply one single stored RuleSet,
    a list of of some of the configured RuleSet objects or all of them.
    """

    _rule_sets: Dict[AnyStr, RuleSet]
    _rule_set_hashes: Set[int]

    def __init__(self):
        self._rule_sets = dict()
        self._rule_set_hashes = set()

    def add_set(self, rule_set: RuleSet) -> NoReturn:
        """Add a new Rule set to the ruler.

        :param rule_set: configured rule set object
        :raises RulerConfigError: When the ruler detects that the provided rule_set was already configured
        """

        if rule_set.__hash__() in self._rule_set_hashes:
            raise RulerConfigError(f"RuleSet '{rule_set.name}' was already configured on the ruler")

        self._rule_sets.update({rule_set.name: rule_set})
        self._rule_set_hashes.add(rule_set.__hash__())

    def add_many(self, rule_sets: Iterable[RuleSet]) -> NoReturn:
        """Add many RuleSet objects at ones.

        :param rule_sets: Iterable object of rule sets to be added
        """

        hashes = set()
        new_sets = dict()

        for rule_set in rule_sets:
            if rule_set.__hash__() in self._rule_set_hashes:
                raise RulerConfigError(f"RuleSet '{rule_set.name}' was already configured on the ruler")

            if rule_set.__hash__() in hashes:
                raise RulerConfigError(f"RuleSet '{rule_set.name}' is duplicated on the given rule sets")

            new_sets.update({rule_set.name: rule_set})
            hashes.add(rule_set.__hash__())

        self._rule_sets.update(new_sets)
        self._rule_set_hashes.update(hashes)

    def count_sets(self) -> int:
        """Count the total of configured sets.

        :return int: Count of sets
        """

        return len(self._rule_sets.keys())

    def rule_set_names(self) -> List[AnyStr]:
        """Return a list of all configured RuleSet objects in the ruler.

        :return: List of rule set names
        """

        return list(self._rule_sets.keys())

    def apply(
        self,
        data: Any,
        sets: Optional[Union[AnyStr, Tuple, List[AnyStr], Set[AnyStr]]] = None,
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

        if sets is None:
            sets = set(self._rule_sets.keys())

        sets = self._process_set_names(sets)

        if isinstance(sets, set):
            self._apply_set(set_names=sets, data=data, fail_fast=fail_fast)
            return

        self._apply_one(set_name=sets, data=data, fail_fast=fail_fast)

    def _apply_set(
        self,
        data: Any,
        set_names: Set[AnyStr],
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
            raise RulerError(f"Not found RuleSet '{set_name}' on Ruler configuration")

        return rule_set

    @staticmethod
    def _process_set_names(sets: Union[AnyStr, Tuple, List[AnyStr], Set[AnyStr]]) -> Union[AnyStr, Set[AnyStr]]:
        """Verify the set names that will be applied and format it.

        :param sets: RuleSet name or List of RuleSet names.
        :return Union[AnyStr, Set[AnyStr]]: Formatted set names
        """

        if isinstance(sets, (tuple, list)):
            return set(sets)

        return sets
