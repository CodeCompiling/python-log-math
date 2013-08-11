#!/usr/bin/env python
# coding: utf-8

from __future__ import division
from __future__ import unicode_literals

import math
import numbers

_NEG_INF = -float('inf')

def _convert_to_logspace(val):
    """ Converts a given value to log space if it's not there already """
    if not isinstance(val, numbers.Number):
        raise TypeError("Must be numeric.")
    elif isinstance(val, LogSpaceNumber):
        return val._value
    elif val == 0.0:
        return _NEG_INF
    elif val < 0.0:
        raise ValueError("Negative values not supported.")
    else:
        return math.log(val)

def _logspace_add(x, y):
    if x == _NEG_INF:
        return y
    elif y == _NEG_INF:
        return x
    return max(x, y) + math.log1p(math.exp(-math.fabs(x - y)))

def _logspace_sub(x, y):
    if x < y:
        raise ValueError("Cannot take the log of a negative number.")
    elif x == y:
        return _NEG_INF
    elif y == _NEG_INF:
        return x
    return x + math.log1p(-math.exp(y-x))

class LogSpaceNumber(numbers.Number):

    __slots__ = ["_value"]

    def __init__(self, value=0.0, log_value=None):
        if log_value is not None and value != 0.0:
            raise ValueError("Cannot initialize with both value and log_value")
        elif log_value is not None:
            self._value = log_value
        else:
            self._value = _convert_to_logspace(value)

    def __repr__(self):
        return "LogSpaceNumber(log_value={0})".format(self._value)

    def __unicode__(self):
        if self._value == _NEG_INF:
            return "0"
        return "exp({0})".format(self._value)

    def __str__(self):
        return self.__unicode__()

    def __bytes__(self):
        return self.__unicode__().encode("utf-8")

    def __lt__(self, other):
        return self._value < _convert_to_logspace(other)

    def __le__(self, other):
        return self._value <= _convert_to_logspace(other)

    def __eq__(self, other):
        return self._value == _convert_to_logspace(other)

    def __ne__(self, other):
        return self._value <> _convert_to_logspace(other)

    def __gt__(self, other):
        return self._value > _convert_to_logspace(other)

    def __ge__(self, other):
        return self._value >= _convert_to_logspace(other)

    def __cmp__(self, other):
        return cmp(self._value, _convert_to_logspace(other))

    def __hash__(self):
        return hash(repr(self.value))

    def __nonzero__(self):
        return self._value != __NEG_INF

    def __add__(self, other):
        return LogSpaceNumber(
            log_value=_logspace_add(self._value, _convert_to_logspace(other)))

    def __sub__(self, other):
        return LogSpaceNumber(
            log_value=_logspace_sub(self._value, _convert_to_logspace(other)))

    def __mul__(self, other):
        return LogSpaceNumber(log_value=self._value+_convert_to_logspace(other))

    def __div__(self, other):
        return LogSpaceNumber(log_value=self._value-_convert_to_logspace(other))

    def __truediv__(self, other):
        return self.__div__(other)

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return LogSpaceNumber(
            log_value=_logspace_sub(_convert_to_logspace(other), self._value))

    def __rmul__(self, other):
        return self * other

    def __rdiv__(self, other):
        return LogSpaceNumber(log_value=_convert_to_logspace(other)-self._value)

    def __rtruediv__(self, other):
        return self.__rdiv__(other)

    def __iadd__(self, other):
        self._value = _logspace_add(self._value, _convert_to_logspace(other))
        return self

    def __isub__(self, other):
        self._value = _logspace_sub(self._value, _convert_to_logspace(other))
        return self

    def __imul__(self, other):
        self._value += _convert_to_logspace(other)
        return self

    def __idiv__(self, other):
        self._value -= _convert_to_logspace(other)
        return self

    def __itruediv__(self, other):
        return self.__idiv__(other)

    def __coerce__(self, other):
        if isinstance(other, numbers.Number):
            return (self, LogSpaceNumber(other))
