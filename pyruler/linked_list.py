"""Custom creation of a LinkedList."""

# pylint: disable=C0103

from abc import ABC
from typing import Any, AnyStr, Generic, Iterable, NoReturn, Optional, Sized, TypeVar

T = TypeVar('T')


class ListNode:
    """Single list node class."""

    def __init__(self, value: Any):
        self.value = value
        self.next = None

    def __repr__(self) -> Any:
        """Representation of Linked list node"""

        return self.value.__repr__()

    def __str__(self) -> AnyStr:
        """String convert of a ListNode.
        :return AnyStr: Str value
        """

        return str(self.value)


class LinkedList(Generic[T], Sized, Iterable, ABC):
    """Custom LinkedList class."""

    _first: Optional[ListNode]
    _last: Optional[ListNode]
    _size: int

    def __init__(self, values: Iterable[T] = None):
        self._first = None
        self._last = None
        self._size = 0

        if values is not None:
            self._init_with_values(values)

    def first(self) -> T:
        """Return first element of the list.
        :return T: First element value
        """

        return None if self._first is None else self._first.value

    def last(self) -> T:
        """return the last element of the list
        :return T: Last element value
        """

        return None if self._last is None else self._last.value

    def add_last(self, value: T) -> NoReturn:
        """Add new node at the end of the list.
        :param value: New list value
        """

        node = ListNode(value)

        if self._size == 0:
            self._first = node
            self._last = node
        else:
            self._last.next = node
            self._last = node

        self._size += 1

    def add_first(self, value: T) -> NoReturn:
        """Add new node at the beginning of the list."""

        node = ListNode(value)

        if self._size == 0:
            self._first = node
            self._last = node
        else:
            node.next = self._first
            self._first = node

        self._size += 1

    def empty(self) -> bool:
        """Return a boolean assertion if the list is empty.
        :return bool: Assertion
        """

        return self._size < 1

    def _init_with_values(self, values: Iterable[T]):
        """Add Nodes from an iterable object.
        :param values: elements to be added to the list.
        """

        for elem in values:
            self.add_last(elem)

    def __repr__(self):
        node = self._first
        nodes = []

        while node is not None:
            nodes.append(str(node))
            node = node.next

        return f"<LinkedList: {' -> '.join(nodes)}>"

    def __iter__(self) -> T:
        node = self._first

        while node is not None:
            yield node.value
            node = node.next

    def __len__(self):
        return self._size

    def __str__(self) -> AnyStr:
        node = self._first
        str_list = []

        while node is not None:
            str_list.append(str(node))
            node = node.next

        return f"[{' -> '.join(str_list)}]"
