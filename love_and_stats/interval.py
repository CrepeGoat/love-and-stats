from enum import Enum
from math import inf


class NumberSides(Enum):
    NEGATIVE = False
    POSITIVE = True

    def __repr__(self):
        return '.'.join([self.__class__.__name__, self.name])

    def __lt__(self, rhs):
        if self.__class__ is not rhs.__class__:
            return NotImplemented

        return self.value < rhs.value

    def __gt__(self, rhs):
        if self.__class__ is not rhs.__class__:
            return NotImplemented

        return self.value > rhs.value


class NumberLineDivider:
    __slots__ = 'value side'.split()

    def __init__(self, value, side):
        self.value = value
        self.side = side

    def __repr__(self):
        return self.__class__.__name__ + '({!r}, {!r})'.format(
            self.value, self.side,
        )

    def __lt__(self, rhs):
        if self.__class__ is not rhs.__class__:
            return (self.value, self.side) < (rhs, NumberSides.POSITIVE)

        return (self.value, self.side) < (rhs.value, rhs.side)

    def __gt__(self, rhs):
        if self.__class__ is not rhs.__class__:
            return (self.value, self.side) > (rhs, NumberSides.NEGATIVE)

        return (self.value, self.side) > (rhs.value, rhs.side)

    def __le__(self, rhs):
        if self.__class__ is not rhs.__class__:
            return NotImplemented

        return (self.value, self.side) <= (rhs.value, rhs.side)

    def __ge__(self, rhs):
        if self.__class__ is not rhs.__class__:
            return NotImplemented

        return (self.value, self.side) >= (rhs.value, rhs.side)


class Interval:
    __slots__ = 'lower_bound upper_bound'.split()

    def __init__(self, lbound, ubound, allow_inversion=False):
        self.lower_bound, self.upper_bound = (
            sorted([lbound, ubound]) if allow_inversion
            else (lbound, max(lbound, ubound))
        )

    @staticmethod
    def from_values(lower_bound=-inf, upper_bound=inf,
                    include_lower=True, include_upper=False,
                    allow_inversion=False):
        lbound = NumberLineDivider(lower_bound, NumberSides(not include_lower))
        ubound = NumberLineDivider(upper_bound, NumberSides(include_upper))

        return Interval(lbound, ubound, allow_inversion)

    def __str__(self):
        return '{}{!s}, {!s}{}'.format(
            '[' if self.lower_bound.side is NumberSides.NEGATIVE else '(',
            self.lower_bound.value,
            self.upper_bound.value,
            ']' if self.upper_bound.side is NumberSides.POSITIVE else ')',
        )

    def __repr__(self):
        return self.__class__.__name__ + '({!r}, {!r})'.format(
            self.lower_bound, self.upper_bound,
        )

    def __contains__(self, val):
        if self.__class__ is not val.__class__:
            return self.lower_bound < val and self.upper_bound > val

        return (
            self.lower_bound <= val.lower_bound
            and self.upper_bound >= val.upper_bound
        )

    def __len__(self):
        return self.upper_bound.value - self.lower_bound.value

    def __bool__(self):
        return self.lower_bound < self.upper_bound

    def intersection(self, other):
        if self.__class__ is not other.__class__:
            raise TypeError("cannot intersect interval with object of type {}"
                            .format(type(other)))

        return Interval(
            lbound=max(self.lower_bound, other.lower_bound),
            ubound=min(self.upper_bound, other.upper_bound),
            allow_inversion=False,
        )

    def __eq__(self, rhs):
        if self.__class__ is not rhs.__class__:
            return len(self) == 0 and rhs in self

        return (
            self.lower_bound == rhs.lower_bound
            and self.upper_bound == rhs.upper_bound
        )

    def split_along(self, divider):
        return (
            [self] if divider not in self
            else [Interval(self.lower_bound, divider),
                  Interval(divider, self.upper_bound)]
        )

    # Methods that may result in non-convex intervals (TODO)
    '''
    def __or__(self, arg):
    def __xor__(self, arg):
    def __sub__(self, arg):
    '''
