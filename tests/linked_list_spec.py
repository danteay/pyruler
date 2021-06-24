"""Unit test of LinkedList."""

from expects import equal, expect
from mamba import context, description, it

from pyruler.linked_list import LinkedList, ListNode

with description('Test LinedList operations:'):
    with context('Should test ListNode'):
        with it('shows Node representation'):
            node = ListNode(1)

            expect(node.__repr__()).to(equal('1'))

    with context('Should create an instance:'):
        with it('takes empty constructor'):
            linked_list = LinkedList()
            expect(linked_list.empty()).to(equal(True))

        with it('takes list of values to the constructor'):
            linked_list = LinkedList([1, 2, 3, 4])

            expect(linked_list.empty()).to(equal(False))
            expect(len(linked_list)).to(equal(4))

        with it('takes set of values to the constructor'):
            linked_list = LinkedList({1, 2, 3, 4})

            expect(linked_list.empty()).to(equal(False))
            expect(len(linked_list)).to(equal(4))

        with it('takes tuple of values to the constructor'):
            linked_list = LinkedList((1, 2, 3, 4))

            expect(linked_list.empty()).to(equal(False))
            expect(len(linked_list)).to(equal(4))

        with it('is created as a typed LinkedList'):
            linked_list: LinkedList[int] = LinkedList[int](('1', 2, 3, 4))

            expect(linked_list.first()).to(equal('1'))
            expect(linked_list.empty()).to(equal(False))
            expect(len(linked_list)).to(equal(4))

    with context('Should add items:'):
        with it('does as last items'):
            linked_list = LinkedList((1, 2, 3, 4))
            linked_list.add_last(5)

            expect(linked_list.last()).to(equal(5))
            expect(linked_list.empty()).to(equal(False))
            expect(len(linked_list)).to(equal(5))

        with it('does as first items'):
            linked_list = LinkedList((1, 2, 3, 4))
            linked_list.add_first(0)

            expect(linked_list.first()).to(equal(0))
            expect(linked_list.empty()).to(equal(False))
            expect(len(linked_list)).to(equal(5))

        with it('adds an item as from as first to an empty list'):
            linked_list = LinkedList()
            linked_list.add_first(1)

            expect(linked_list.first()).to(equal(1))
            expect(linked_list.empty()).to(equal(False))
            expect(len(linked_list)).to(equal(1))

    with context('Should Convert to str and representation'):
        with it('string conversion'):
            linked_list = LinkedList([1, 2])

            expect(str(linked_list)).to(equal('[1 -> 2]'))

        with it('gets representation'):
            linked_list = LinkedList([1, 2])

            expect(linked_list.__repr__()).to(equal('<LinkedList: 1 -> 2>'))
