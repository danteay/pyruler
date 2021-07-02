"""Unit testing for Rule objects."""

from expects import be_a, equal, expect
from mamba import description, it

from pyruler import Rule

with description('Should test Rule configuration') as self:
    with it('checks Rule name and execution'):
        rule = Rule(name='test-rule', resolver=lambda x: True)

        expect(rule.name).to(equal('test-rule'))
        expect(rule.execute({'some': 1})).to(equal(True))

    with it('not callable resolver error'):
        rule = Rule(name='test-rule')

        try:
            _ = rule.execute({})
        except Exception as err:
            expect(err.args[0]).to(equal("Rule 'test-rule' doesn't have a Callable resolver"))

    with it('save custom exception'):
        rule = Rule(name='test-rule', resolver=lambda x: False, error=AssertionError('custom error'))

        try:
            if not rule.execute({}):
                raise rule.error
        except Exception as error:
            expect(error).to(be_a(AssertionError))
            expect(error.args[0]).to(equal('custom error'))
