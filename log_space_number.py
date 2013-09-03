#!/usr/bin/env python
# coding: utf-8

from __future__ import division
from __future__ import unicode_literals

import math
import numbers

_NEG_INF = -float('inf')

def _pos_num(val):
    if not isinstance(val, numbers.Number):
        raise TypeError("Must be numeric.")
    elif isinstance(val, LogSpaceNumber):
        return val._is_pos
    else:
        return val >= 0.0

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
    """ Takes two log-space numbers, and returns the log-space sum """
    
    if x == _NEG_INF:
        return y
    elif y == _NEG_INF:
        return x
    return max(x, y) + math.log1p(math.exp(-math.fabs(x - y)))

def _logspace_sub(x, y):
    """ Takes two log-space numbers, and returns the log-space difference.

    Requirement: x >= y """
    
    if x < y:
        raise ValueError("Cannot take the log of a negative number.")
    elif x == y:
        return _NEG_INF
    elif y == _NEG_INF:
        return x
    return x + math.log1p(-math.exp(y-x))

class LogSpaceNumber(numbers.Number):

    __slots__ = ["_value", "_is_pos"]

    def __init__(self, value=0.0, log_value=None, log_pos=True):
        if (log_value is not None or log_pos is not None) and value != 0.0:
            raise ValueError("Cannot initialize with both value and "
                             "log_value or log_pos")
        elif log_value is not None:
            self._value = log_value
            self._is_pos = log_pos
        else:
            self._value = _convert_to_logspace(abs(value))
            self._is_pos = _pos_num(value)

    def from_logspace(self):
        """ Returns the actual, non-logspace value for this number.

        MAY LOSE PRECISION. """

        if self._is_pos:
            return math.exp(self._value)
        else:
            return - math.exp(self._value)

    def __repr__(self):
        return "LogSpaceNumber(log_value={0}, log_pos={1})".format(
            self._value, self._is_pos)

    def __unicode__(self):
        if self._value == _NEG_INF:
            return "0.0"
        elif self._is_pos:
            return "exp({0})".format(self._value)
        else:
            return "-exp({0})".format(self._value)

    def __str__(self):
        return self.__unicode__()

    def __bytes__(self):
        return self.__unicode__().encode("utf-8")

    def __lt__(self, other):
        other_pos = _pos_num(other)
        if self._is_pos and other_pos:
            return self._value < _convert_to_logspace(other)
        elif self._is_pos: # this is positive, other is negative
            return False
        elif other_pos: # this is negative, other is positive
            return True
        else: # both are negative
            return self._value > _convert_to_logspace(abs(other))

    def __le__(self, other):
        other_pos = _pos_num(other)
        if self._is_pos and other_pos:
            return self._value <= _convert_to_logspace(other)
        elif self._is_pos: # this is positive, other is negative
            return False
        elif other_pos: # this is negative, other is positive
            return True
        else: # both are negative
            return self._value >= _convert_to_logspace(abs(other))

    def __eq__(self, other):
        return (self._value == _convert_to_logspace(abs(other)) and
                self._is_pos == _pos_num(other))

    def __ne__(self, other):
        return (self._value <> _convert_to_logspace(abs(other)) or
                self._is_pos <> _pos_num(other))

    def __gt__(self, other):
        other_pos = _pos_num(other)
        if self._is_pos and other_pos:
            return self._value > _convert_to_logspace(other)
        elif self._is_pos: # this is positive, other is negative
            return True
        elif other_pos: # this is negative, other is positive
            return False
        else: # both are negative
            return self._value < _convert_to_logspace(abs(other))

    def __ge__(self, other):
        other_pos = _pos_num(other)
        if self._is_pos and other_pos:
            return self._value >= _convert_to_logspace(other)
        elif self._is_pos: # this is positive, other is negative
            return True
        elif other_pos: # this is negative, other is positive
            return False
        else: # both are negative
            return self._value <= _convert_to_logspace(abs(other))

    def __cmp__(self, other):
        sign_comparison = cmp(self._is_pos, _pos_num(other))
        if sign_comparison:
            return sign_comparison

        # signs must be the same
        elif self._is_pos: # both positive
            return cmp(self._value, _convert_to_logspace(other))
        else: # both negative
            return -cmp(self.value, _convert_to_logspace(abs(other)))

    def __hash__(self):
        return hash((self._is_pos, repr(self._value)))

    def __nonzero__(self):
        return self._value != __NEG_INF

    def __add__(self, other):
        other_pos = _pos_num(other)
        if self._is_pos and _pos_num:
            return LogSpaceNumber(
                log_value=_logspace_add(self._value,
                                        _convert_to_logspace(other)),
                log_pos=True)
        elif self._is_pos: # this is positive, other is negative
            other_val = _convert_to_logspace(abs(other))
            if self._value > other_val:
                return LogSpaceNumber(
                    log_value=_logspace_sub(self._value, other_val),
                    log_pos=True)
            else:
                return LogSpaceNumber(
                    log_value=_logspace_sub(other_val, self._value),
                    log_pos=False)
        elif other_pos: # this is negative, other is positive
            other_val = _convert_to_logspace(other)
            if self._value > other_val:
                return LogSpaceNumber(
                    log_value=_logspace_sub(self._value, other_val),
                    log_pos=False)
            else:
                return LogSpaceNumber(
                    log_value=_logspace_sub(other_val, self._value),
                    log_pos=True)
        else: # both are negative
            return LogSpaceNumber(
                log_value=_logspace_add(self._value,
                                        _convert_to_logspace(abs(other))),
                log_pos=False)

    def __sub__(self, other):
        other_pos = _pos_num(other)
        if self._is_pos and other_pos:
            other_val = _convert_to_logspace(other)
            if self._value > other_val:
                return LogSpaceNumber(
                    log_value=_logspace_sub(self._value, other_val),
                    log_pos=True)
            else:
                return LogSpaceNumber(
                    log_value=_logspace_sub(other_val, self._value),
                    log_pos=False)

        elif self._is_pos: # this is positive, other is negative
            return LogSpaceNumber(
                log_value=_logspace_add(self._value,
                                        _convert_to_logspace(abs(other))),
                log_pos=True)
            
        elif other_pos: # this is negative, other is positive
            return LogSpaceNumber(
                log_value=_logspace_add(self._value,
                                        _convert_to_logspace(other)),
                log_pos=False)
            
        else: # both are negative
            other_val = _convert_to_logspace(abs(other))
            if self._value > other_val:
                return LogSpaceNumber(
                    log_value=_logspace_sub(self._value, other_val),
                    log_pos=False)
            else:
                return LogSpaceNumber(
                    log_value=_logspace_sub(other_val, self._value),
                    log_pos=True)

    def __mul__(self, other):
        return LogSpaceNumber(log_value=self._value+_convert_to_logspace(other))

    def __div__(self, other):
        return LogSpaceNumber(log_value=self._value-_convert_to_logspace(other))

    def __truediv__(self, other):
        return self.__div__(other)

    def __pow__(self, other):
        if isinstance(other, LogSpaceNumber):
            return LogSpaceNumber(
                log_value=other.from_logspace() * self._value)
        elif isinstance(other, numbers.Number):
            return LogSpaceNumber(
                log_value=other * self._value)
        raise ValueError("cannot take pow to a non-number")

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

    def __rpow__(self, other):
        return LogSpaceNumber(
            log_value=self.from_logspace() * _convert_to_logspace(other))

    def __coerce__(self, other):
        if isinstance(other, numbers.Number):
            return (self, LogSpaceNumber(other))
