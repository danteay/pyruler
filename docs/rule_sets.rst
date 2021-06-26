RuleSet definition
==================

A RuleSet object is basically a list of predefined rules that will be executed over a given data. A RuleSet can be
compared with some kind of policy.

RuleSet object needs to have a name that is passed by the constructor and at least 1 Rule object configured to be
applied successfully.

In difference with the Rule object RuleSet doesn't have an `execute` method, instead of this RuleSet has the method
`apply` that receive the data. This method do not return any value on success and raise a `RuleError` if some rule
fails his validation.

Basic Usage
-----------

To define a RuleSet and add a Rule to the list you can simple add the following code:

.. code-block:: python

    from pyruler import RuleSet, Rule

    rule_set = RuleSet(name='policy1')
    rule_set.add_rule(Rule(name='is-gt-10', resolver=lambda x: x > 10))

    rule_set.apply(1)
    # => raise RuleError

Add Multiple Rules
------------------

You can add all the rules you need to a RuleSet. Rules stored by a RuleSet will be executed in the same exact same
order that the rules where added:

.. code-block:: python

    from pyruler import RuleSet, Rule

    rule_set = RuleSet(name='policy1')
    rule_set.add_rule(Rule(name='is-gt-10', resolver=lambda x: x > 10))
    rule_set.add_rule(Rule(name='is-lt-20', resolver=lambda x: x > 20))

    rule_set.apply(15)
    # => None (This is a success validation)

Other way to add multiple rules is by using the method `add_many`:

.. code-block:: python

    from pyruler import RuleSet, Rule

    rule_set = RuleSet(name='policy1')

    rule_set.add_many([
        Rule(name='is-gt-10', resolver=lambda x: x > 10),
        Rule(name='is-lt-20', resolver=lambda x: x < 20),
    ])

    rule_set.apply(15)
    # => None (This is a success validation)

Fail fast execution
-------------------

You can specify when a RuleSet should trigger an error of a Rule validation. This can be configured by the `fail_fast`
param of the `apply` method.

By default `fail_fast` is set to **True**, this raises a RuleError exception with the first negative assertion returned
by a rule of the RuleSet. If `fail_fast` is set to **False** all rules will be executed to collect all errors of each
configured rule before raise a RuleError exception.

.. code-block:: python

    from pyruler import RuleSet, Rule

    rule_set = RuleSet(name='policy1')

    rule_set.add_many([
        Rule(name='has-foo', resolver=lambda x: 'foo' in x.keys()),
        Rule(name='has-bar', resolver=lambda x: 'bar' in x.keys()),
    ])

    rule_set.apply({'baz': True})
    # => raise RuleError exception after execute 'has-foo' rule

    rule_set.apply({'baz': True}, fail_fast=False)
    # => raise RuleError exception after execute 'has-foo' and 'has-bar' rules
