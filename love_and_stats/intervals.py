import bisect
import functools
from math import inf, isnan


@functools.total_ordering
class NumberLineDivider:
    """
    A numeric value strictly non-equal to any other "plain" numeric value.

    Maintains "total ordering"s.
    """

    __slots__ = ('value', 'on_pos_side')

    def __init__(self, value, is_on_pos_side=False):
        """
        Construct an object.

        Not convenient for end API use. Consider `x+eps` or `x-eps` instead.
        """
        self.value = value
        self.on_pos_side = is_on_pos_side

    @classmethod
    def as_divider(cls, obj):
        """
        Convert a value to a `NumberLineDivider` type.

        If the input is already of `NumberLineDivider` type, the object is
        returned w/o instantiating a new `NumberLineDivider`.
        """
        if isinstance(obj, cls):
            return obj
        return cls(obj)

    @classmethod
    def as_value(cls, obj):
        """
        Convert a value to a raw numeric value.

        If the input is not of `NumberLineDivider` type, the object is
        returned directly.
        """
        if isinstance(obj, cls):
            return obj.value
        return obj

    def __repr__(self):
        """Generate repr str."""
        return (
            f"<{self.__class__.__name__} ({self.value},"
            f" {({True: '+', False: '-', None: '?'}[self.on_pos_side])})>"
        )

    def __str__(self):
        """Generate str."""
        return (
            f"{self.value}"
            f" {({True: '+', False: '-', None: '?'}[self.on_pos_side])} ε"
        )

    # -------------------------------------------------------------------------
    def __eq__(self, rhs):
        """
        Check object for equality.

        Does not compare equal to any non-`NumberLineDivider` object.
        """
        if not isinstance(rhs, self.__class__):
            return isnan(self.value - rhs)

        if (self.value, self.on_pos_side) != (rhs.value, rhs.on_pos_side):
            return isnan(self.value - rhs.value)
        return self.on_pos_side is not None

    def __lt__(self, rhs):
        """Check if object is les than input value."""
        if not isinstance(rhs, self.__class__):
            rhs = self.__class__(rhs, rhs != inf)

        return (self.value, self.on_pos_side) < (rhs.value, rhs.on_pos_side)

    # -------------------------------------------------------------------------
    def __add__(self, rhs):
        """Add object to value."""
        if not isinstance(rhs, self.__class__):
            return NumberLineDivider(self.value + rhs, self.on_pos_side)

        return NumberLineDivider(
            self.value + rhs.value,
            (
                self.on_pos_side if self.on_pos_side == rhs.on_pos_side
                else None
            ),
        )

    def __radd__(self, lhs):
        """Add value to object."""
        if not isinstance(lhs, self.__class__):
            return NumberLineDivider(lhs + self.value, self.on_pos_side)

        return NumberLineDivider(
            lhs.value + self.value,
            (
                lhs.on_pos_side if self.on_pos_side == lhs.on_pos_side
                else None
            ),
        )

    def __sub__(self, rhs):
        """Subtract value from object."""
        if not isinstance(rhs, self.__class__):
            return NumberLineDivider(self.value - rhs, self.on_pos_side)

        return NumberLineDivider(
            self.value - rhs.value,
            (
                self.on_pos_side
                if self.on_pos_side == (not rhs.on_pos_side)
                and (not self.on_pos_side) == rhs.on_pos_side
                else None
            ),
        )

    def __rsub__(self, lhs):
        """Subtract object from value."""
        if not isinstance(lhs, self.__class__):
            return NumberLineDivider(
                lhs - self.value,
                None if self.on_pos_side is None else not self.on_pos_side
            )

        return NumberLineDivider(
            lhs.value + self.value,
            (
                lhs.on_pos_side
                if self.on_pos_side == (not lhs.on_pos_side)
                and (not self.on_pos_side) == lhs.on_pos_side
                else None
            ),
        )


eps = NumberLineDivider(0, True)
ε = eps


class DisjointInterval:
    """The union of a set of continuous disjoint intervals."""

    __slots__ = ('_bounds',)

    def __init__(self):
        """
        Construct a null interval.

        Use `from_ranges` to construct a non-empty interval.
        """
        self._bounds = ()

    def __str__(self):
        """Generate str."""
        if not self:
            return "\u2205"

        return '\u222a'.join(
            "( "
            f"{'(' if i.on_pos_side else '['}{i.value}, "
            f"{j.value}{']' if j.on_pos_side else ')'}"
            " )"
            for i, j in self._ranges
        )

    def __repr__(self):
        """Generate repr str."""
        return (
            f"<{self.__class__.__name__} "
            f"{', '.join(repr(itvl) for itvl in self._ranges)}>"
        )

    def __eq__(self, other):
        """Check object for equality."""
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self._bounds == other._bounds

    @staticmethod
    def from_ranges(*pairs):
        """
        Construct a new disjoint interval.

        :param pairs: a set of intervals.
        :returns: a disjoint interval representing the union of the intervals
            defined by the input value pairs.
        """
        bounds = []
        for val1, val2 in pairs:
            if val1 is None:
                val1 = -inf
            if val2 is None:
                val2 = inf
            val1 = NumberLineDivider.as_divider(val1)
            val2 = NumberLineDivider.as_divider(val2)
            if val1 >= val2:
                continue

            idx1 = bisect.bisect_left(bounds, val1)
            idx2 = bisect.bisect_right(bounds, val2, idx1)

            bounds[idx1:idx2] = (
                ([val1] if idx1 % 2 == 0 else [])
                + ([val2] if idx2 % 2 == 0 else [])
            )
            assert len(bounds) % 2 == 0

        assert all(b.on_pos_side is not None for b in bounds)

        comp_interval = DisjointInterval()
        comp_interval._bounds = tuple(bounds)
        return comp_interval

    @property
    def _ranges(self):
        """Iterate over all sub-intervals whose union defines the space."""
        return zip(self._bounds[::2], self._bounds[1::2])

    def __contains__(self, val):
        """Test item containment."""
        return bisect.bisect_right(self._bounds, val) % 2 == 1

    def breadth(self):
        """Calculate summed length of all disjoint sub-intervals."""
        return sum(j.value-i.value for i, j in self._ranges)

    def __bool__(self):
        """Test if interval is empty."""
        return bool(self._bounds)

    def intersection(self, other):
        """
        Intersect with another disjoint interval.

        :param other: a disjoint interval.
        :returns: the intersection between self and other.
        """
        if not isinstance(other, self.__class__):
            raise TypeError("cannot intersect interval with object of type {}"
                            .format(type(other)))

        def paused_iter(iterable):
            """Iterate viewing the previous item with `i.send(True)`."""
            iterator = iter(iterable)

            while True:
                try:
                    value = next(iterator)
                except StopIteration:
                    return

                while (yield value):
                    pass

        bounds = []

        if self and other:
            ranges1 = paused_iter(self._ranges)
            ranges2 = paused_iter(other._ranges)

            next(ranges1)
            next(ranges2)

            while True:
                bnd1 = max(ranges1.send(True)[0], ranges2.send(True)[0])
                bnd2 = min(ranges1.send(True)[1], ranges2.send(True)[1])

                if bnd1 < bnd2:
                    bounds.append(bnd1)
                    bounds.append(bnd2)

                try:
                    next(min(ranges1, ranges2, key=lambda r: r.send(True)[1]))
                except StopIteration:
                    break

        comp_interval = DisjointInterval()
        comp_interval._bounds = tuple(bounds)
        return comp_interval

    def union(self, other):
        """
        Unite with another disjoint interval.

        :param other: a disjoint interval.
        :returns: the union between self and other.
        """
        if not isinstance(other, self.__class__):
            raise TypeError("cannot unite interval with object of type {}"
                            .format(type(other)))

        if not self:
            return other
        if not other:
            return self

        def iter_merged_sorteds(iter1, iter2):
            """Iterate in sorted order all items of two sorted collections."""
            iter1 = iter(iter1)
            iter2 = iter(iter2)

            try:
                item1 = next(iter1)
            except StopIteration:
                yield from iter2
                return

            while True:
                for item2 in iter2:
                    if item2 <= item1:
                        yield item2
                    else:
                        yield item1
                        break
                else:
                    yield item1
                    yield from iter1
                    return

                item1 = item2
                iter1, iter2 = iter2, iter1

        sorted_itvls = iter_merged_sorteds(self._ranges, other._ranges)
        bounds = [*next(sorted_itvls)]

        for itvl in sorted_itvls:
            if itvl[0] < bounds[-1]:
                bounds[-1] = itvl[1]
            else:
                bounds.append(itvl[0])
                bounds.append(itvl[1])

        comp_interval = DisjointInterval()
        comp_interval._bounds = tuple(bounds)
        return comp_interval
