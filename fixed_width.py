"""
Copyright 2021 supakeen

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import enum

from typing import Optional, Any


class _behavior_overflow(enum.Enum):
    EXCEPTION = enum.auto()
    TRUNCATE = enum.auto()


class _behavior_promotion(enum.Enum):
    EXCEPTION = enum.auto()


class _behavior:
    overflow: _behavior_overflow
    promotion: _behavior_promotion

    def __init__(self, overflow, promotion):
        self.overflow = overflow
        self.promotion = promotion

    def __repr__(self) -> str:
        return f"_behavior({self.overflow=}, {self.promotion=})"


class _context:
    """Contexts are for storing various flags about what happened to types used
    within them."""

    overflow: bool
    promotion: bool

    def __init__(self):
        self.overflow = False
        self.promotion = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass


class _value:
    """A value, we store the raw 'python' integer and only go into/out of bits
    and fixed width on certain operations. This allows for easier conversion
    during calculation.
    """

    def __init__(self, rule, integer: int, context: Optional[_context] = None):
        self._rule = rule
        self._integer = integer
        self._context = context

    def __int__(self) -> int:
        if self._rule._behavior.overflow == _behavior_overflow.TRUNCATE:
            return self._integer & (2 ** self._rule._width - 1)
        else:
            self._integer & (2 ** self._rule._width - 1)

    def __repr__(self) -> str:
        return f"_value({self._integer=}, {self._rule=})"

    def __add__(self, other: Any):
        if isinstance(other, int):
            other = self._rule(other)


class _type:
    _context: Optional[_context]
    _width: int
    _behavior: _behavior

    def __init__(
        self,
        width: int,
        behavior: _behavior,
        context: Optional[_context] = None,
    ) -> None:
        self._width = width
        self._behavior = behavior
        self._context = context

    def __call__(self, integer: int):
        return _value(self, integer, self._context)

    def __repr__(self) -> str:
        return f"_{self.__class__.__name__}({self._width=}, {self._behavior=})"


class _unsigned(_type):
    pass


class _signed(_type):
    pass


class c_stdint(_context):
    _signed_behavior = _behavior(
        overflow=_behavior_overflow.TRUNCATE,
        promotion=_behavior_promotion.EXCEPTION,
    )

    int8_t = _signed(8, _signed_behavior)
    int16_t = _signed(16, _signed_behavior)
    int32_t = _signed(32, _signed_behavior)
    int64_t = _signed(64, _signed_behavior)

    _unsigned_behavior = _behavior(
        overflow=_behavior_overflow.TRUNCATE,
        promotion=_behavior_promotion.EXCEPTION,
    )

    uint8_t = _unsigned(8, _unsigned_behavior)
    uint16_t = _unsigned(16, _unsigned_behavior)
    uint32_t = _unsigned(32, _unsigned_behavior)
    uint64_t = _unsigned(64, _unsigned_behavior)