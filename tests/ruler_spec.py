"""Testing ruler core."""

from expects import equal, expect
from mamba import description, it

from pyruler import Rule, Ruler, RuleSet

with description('Should test Ruler configuration') as self:
    with it('creates ruler instance'):
        ruler = Ruler()
        ruler.add_set(RuleSet(name='set1'))
        ruler.add_set(RuleSet(name='set2'))

        expect(ruler.count_sets()).to(equal(2))

    with it('adds many rule sets at once'):
        ruler = Ruler()
        ruler.add_many([RuleSet(name='set1'), RuleSet(name='set2')])

        expect(ruler.count_sets()).to(equal(2))

    with it('checks error by adding many values with conflict for an existing RuleSet'):
        ruler = Ruler()
        rule_set = RuleSet(name='set1')

        ruler.add_set(rule_set)

        try:
            ruler.add_many([rule_set, RuleSet(name='set2')])
            assert False
        except Exception as error:
            expect(error.args[0]).to(equal("RuleSet 'set1' was already configured on the ruler"))

    with it('checks error by adding many values with duplicated rules'):
        ruler = Ruler()
        rule_set = RuleSet(name='set1')

        try:
            ruler.add_many([rule_set, rule_set])
            assert False
        except Exception as error:
            expect(error.args[0]).to(equal("RuleSet 'set1' is duplicated on the given rule sets"))

    with it('checks for rule set names'):
        ruler = Ruler()
        ruler.add_many([RuleSet(name='set1'), RuleSet(name='set2')])

        expect(ruler.rule_set_names()).to(equal(['set1', 'set2']))

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

        ruler.apply(data={})

        assert True

    with it('checks for error when try to execute a non configured rule set'):
        ruler = Ruler()
        ruler.add_set(RuleSet(name='set1'))

        try:
            ruler.apply(sets='set2', data={})
            assert False
        except Exception as error:
            expect(error.args[0]).to(equal("Not found RuleSet 'set2' on Ruler configuration"))
