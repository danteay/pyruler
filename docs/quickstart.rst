Quick Start
===========

Installing package
------------------

To install this package to your environment run the next command:

.. code-block:: bash

    # If you are using pip
    pip3 install pyruler

    # If you are using Poetry
    poetry add pyruler

Basic usage
-----------

You can import his resources like this:

.. code-block:: python

    from pyruler import Ruler, RuleSet, Rule


And finally you can implement a simple Ruler like this:

.. code-block:: python

    ruler = Ruler()

    rule_set = RuleSet(name='test-fields')
    rule_set.add_rule(Rule(name='test-name', resolver: lambda info: info['name'] is not None))

    ruler.add_set(rule_set)

    ruler.apply(sets='test-fields', data={'name': 'John'})
