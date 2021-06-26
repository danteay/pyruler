Ruler definition
================

A Ruler object can be consider as a Policy layer. It stores many RuleSet objects that can be applied over some data.
Rulers can apply one single RuleSet policy, a list of the configured RuleSets or all configured RuleSet policies.

Basic usage
-----------

To create and configure a Ruler you can add the next code:

.. code-block:: python

    from pyruler import Ruler, RuleSet, Rule

    has_foo = Rule(name='has-foo', resolver=lambda x: 'foo' in x.keys())
    has_bar = Rule(name='has-bar', resolver=lambda x: 'bar' in x.keys())
    has_baz = Rule(name='has-baz', resolver=lambda x: 'baz' in x.keys())
    has_bis = Rule(name='has-bis', resolver=lambda x: 'bis' in x.keys())

    policy1 = RuleSet(name='policy1')
    policy1.add_many([has_foo, has_bar])

    policy2 = RuleSet(name='policy2')
    policy2.add_rule(has_baz)

    policy3 = RuleSet(name='policy3')
    policy3.add_rule(has_bis)

    ruler = Ruler()
    ruler.add_set(policy1)
    ruler.add_set(policy2)
    ruler.add_set(policy3)

Also you can add RuleSet policies using the `add_many` method of the Ruler object:

.. code-block:: python

    ruler.add_many([policy1, policy2, policy3])

Applying RuleSet policies
-------------------------

The Ruler object has the method `apply` that execute RuleSet policy validations over a given data:

.. code-block:: python

    # apply one single RuleSet policy
    ruler.apply({'foo': True, 'bar': True}, sets='policy1')

    # apply a list of RuleSet policies
    ruler.apply({'foo': True, 'bar': True, 'baz': True}, sets=['policy1', 'policy2'])

    # apply all RuleSet policies
    ruler.apply({'foo': True, 'bar': True, 'baz': True, 'bis': True})
