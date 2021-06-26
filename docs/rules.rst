Rule definition
===============

Basic Rule
----------

Rules are atomic operations that validates information of a given object. This validations should return a boolean
assertion as return.

.. code-block:: python

    from pyruler import Rule

    rule = Rule(name='rule1', resolver=lambda x: x > 0)

    rule.execute(1)
    # => True

Complex Validations
-------------------

Rules also can be more complex and validate any kind of data passed to the rule.

.. code-block:: python

    from pyruler import Rule

    rule = Rule(
        name='age-gt-10',
        resolver=lambda x: True if 'age' in x.keys() and x['age'] > 10 else age_from_bday(x['bday']) > 10
    )

    rule.execute({'age': 5})
    # => False

Also you can add all the logic that you need to generate your validations by passing a separated function like this:

.. code-block:: python

    from pyruler import Rule

    def age_gt_10(info) -> bool:
        if 'age' not in info.keys()
            return age_from_bday(info['bday']) > 10

        return info['age'] > 10

    rule = Rule(name='age-gt-10', resolver=age_gt_10)

    rule.execute({'age': 11})
    # => True
