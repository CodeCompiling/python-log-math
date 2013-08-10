#!/usr/bin/env python
# coding: utf-8

from __future__ import division
from __future__ import unicode_literals

import math
import numbers

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

class LogSpaceNumber(numbers.Number):

    _NEG_INF = -float('inf')

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
