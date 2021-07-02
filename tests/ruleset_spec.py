"""RuleSet unit testing."""

from expects import be_a, equal, expect
from mamba import description, it

from pyruler import Rule, RuleSet

with description('Should test RuleSet configuration') as self:
    with it('checks add_rule method'):
        rule_set = RuleSet(name='set1')

        rule_set.add_rule(Rule(name='rule1', resolver=lambda x: True))
        rule_set.add_rule(Rule(name='rule2', resolver=lambda x: True))

        expect(rule_set.count_rules()).to(equal(2))

    with it('adds many rules from a list at ones'):
        rule_set = RuleSet(name='set1')

        rule_set.add_many([Rule(name='rule1', resolver=lambda x: True), Rule(name='rule2', resolver=lambda x: True)])

        expect(rule_set.count_rules()).to(equal(2))

    with it('checks error by adding many values with conflict for an existing rule'):
        rule_set = RuleSet(name='set1')
        rule = Rule(name='rule1', resolver=lambda x: True)

        rule_set.add_rule(rule)

        try:
            rule_set.add_many([rule, Rule(name='rule2', resolver=lambda x: True)])
            assert False
        except Exception as error:
            expect(error.args[0]).to(equal("Rule 'rule1' was already configured in the RuleSet"))

    with it('checks error by adding many values with duplicated rules'):
        rule_set = RuleSet(name='set1')
        rule = Rule(name='rule1', resolver=lambda x: True)

        try:
            rule_set.add_many([rule, rule])
            assert False
        except Exception as error:
            expect(error.args[0]).to(equal("Rule 'rule1' is duplicated on the given rules"))

    with it('checks for added rule names'):
        rule_set = RuleSet(name='set1')

        rule_set.add_many([Rule(name='rule1', resolver=lambda x: True), Rule(name='rule2', resolver=lambda x: True)])

        expect(rule_set.rule_names()).to(equal(['rule1', 'rule2']))

    with it('throws duplicated rule error'):
        rule_set = RuleSet(name='set1')
        rule = Rule(name='rule1', resolver=lambda x: True)

        try:
            rule_set.add_rule(rule)
            rule_set.add_rule(rule)
        except Exception as error:
            expect(error.args[0]).to(equal("Rule 'rule1' was already configured in the RuleSet"), )

    with it('throws fail_fast mode error'):
        rule_set = RuleSet(name='set1')

        rule_set.add_rule(Rule(name='rule1', resolver=lambda x: False))
        rule_set.add_rule(Rule(name='rule2', resolver=lambda x: False))

        try:
            rule_set.apply({}, fail_fast=True)
        except Exception as error:
            expect(error.args[0]).to(equal("Rule 'rule1' fail"))

    with it('throws error with fail_fast mode disabled'):
        rule_set = RuleSet(name='set1')

        rule_set.add_rule(Rule(name='rule1', resolver=lambda x: False))
        rule_set.add_rule(Rule(name='rule2', resolver=lambda x: False))

        try:
            rule_set.apply({}, fail_fast=False)
        except Exception as error:
            expect(error.args[0]).to(equal("Rules '['rule1', 'rule2']' fail"))

    with it('apply all rules successfully'):
        rule_set = RuleSet(name='set1')

        rule_set.add_rule(Rule(name='rule1', resolver=lambda x: True))
        rule_set.add_rule(Rule(name='rule2', resolver=lambda x: True))

        rule_set.apply({})

        assert True

    with it('apply rule set multiple times'):
        rule_set = RuleSet(name='set1')

        rule_set.add_rule(Rule(name='rule1', resolver=lambda x: True))
        rule_set.add_rule(Rule(name='rule2', resolver=lambda x: True))

        rule_set.apply({})
        rule_set.apply({})
        rule_set.apply({})

        assert True

    with it('raises error for not configured rules on RuleSet'):
        rule_set = RuleSet(name='set1')

        try:
            rule_set.apply({})
            assert False
        except Exception as error:
            expect(error.args[0]).to(equal("No rules configured on rule set set1"))

    with it('raises custom rule error'):
        rule_set = RuleSet(name='set1')

        rule_set.add_rule(Rule(name='rule1', resolver=lambda x: False, error=AssertionError('custom error')))

        try:
            rule_set.apply({})
            assert False
        except Exception as error:
            expect(error).to(be_a(AssertionError))
            expect(error.args[0]).to(equal('custom error'))
