__author__ = 'Lorne'

from collections import namedtuple


def enum(*keys):
    return namedtuple('Enum', keys)(*keys)