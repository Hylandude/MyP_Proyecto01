#!/usr/bin/env python3

from enum import Enum

"""
Enumeration that represents the status of an user
"""
class UserStatus(Enum):
    ACTIVE = 1
    AWAY = 2
    BUSY = 3

    """
    To String Method
    """
    def __str__(self):
        return{
            'ACTIVE' : "ACTIVE",
            'AWAY' : "AWAY",
            'BUSY' : "BUSY"
        }[self.name]
