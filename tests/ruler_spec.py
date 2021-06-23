"""Testing ruler core."""

from expects import equal, expect
from mamba import description, it

from pyruler import Rule, Ruler, RuleSet

with description('Should test Rule configuration') as self:
    with it('checks Rule name and execution'):
        rule = Rule(name='test-rule', resolver=lambda x: True)

        expect(rule.name).to(equal('test-rule'))
        expect(rule.execute({'some': 1})).to(equal(True))

    with it('not callable resolver error'):
        rule = Rule(name='test-rule', resolver=None)

        try:
            _ = rule.execute({})
        except Exception as err:
            expect(err.args[0]).to(equal("'NoneType' object is not callable"))

with description('Should test RuleSet configuration') as self:
    with it('checks add_rule method'):
        rule_set = RuleSet(name='set1')

        rule_set.add_rule(Rule(name='rule1', resolver=lambda x: True))
        rule_set.add_rule(Rule(name='rule2', resolver=lambda x: True))

        expect(rule_set.count_rules()).to(equal(2))

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

with description('Should test Ruler configuration') as self:
    with it('creates ruler instance'):
        ruler = Ruler()
        ruler.add_set(RuleSet(name='set1'))
        ruler.add_set(RuleSet(name='set2'))

        expect(ruler.count_sets()).to(equal(2))

    with it('throws duplicated RuleSet error'):
        ruler = Ruler()
        rule_set = RuleSet(name='set1')

        try:
            ruler.add_set(rule_set)
            ruler.add_set(rule_set)
        except Exception as error:
            expect(error.args[0]).to(equal("RuleSet 'set1' was already configured on the ruler"), )

    with it('executes one rule_set'):
        ruler = Ruler()
        rule_set = RuleSet(name='set1')

        rule_set.add_rule(Rule(name='rule1', resolver=lambda x: True))
        rule_set.add_rule(Rule(name='rule2', resolver=lambda x: True))

        ruler.add_set(rule_set)
        ruler.add_set(RuleSet(name='set2'))

        ruler.apply(sets='set1', data={})

        assert True

    with it('executes a sub set of rule_sets'):
        ruler = Ruler()

        rule_set = RuleSet(name='set1')
        rule_set.add_rule(Rule(name='rule1', resolver=lambda x: True))

        rule_set2 = RuleSet(name='set2')
        rule_set2.add_rule(Rule(name='rule2', resolver=lambda x: True))

        ruler.add_set(rule_set)
        ruler.add_set(rule_set2)
        ruler.add_set(RuleSet(name='set3'))

        ruler.apply(sets={'set1', 'set2'}, data={})
        ruler.apply(sets=('set1', 'set2'), data={})
        ruler.apply(sets=['set1', 'set2'], data={})

        assert True

    with it('executes all rule_sets'):
        ruler = Ruler()

        rule_set = RuleSet(name='set1')
        rule_set.add_rule(Rule(name='rule1', resolver=lambda x: True))

        rule_set2 = RuleSet(name='set2')
        rule_set2.add_rule(Rule(name='rule2', resolver=lambda x: True))

        rule_set3 = RuleSet(name='set3')
        rule_set3.add_rule(Rule(name='rule3', resolver=lambda x: True))

        ruler.add_set(rule_set)
        ruler.add_set(rule_set2)
        ruler.add_set(rule_set3)

        ruler.apply(sets='all', data={})
        ruler.apply(sets='ALL', data={})
        ruler.apply(sets='All', data={})

        assert True
