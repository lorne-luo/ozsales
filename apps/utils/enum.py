__author__ = 'Lorne'

from collections import namedtuple


def Enum(*keys):
    return namedtuple('Enum', keys)(*keys)