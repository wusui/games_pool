#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Find balls that need to be pocketed along a long rail, given the initial setup
"""
from functools import reduce

def reduce_lists(set_of_p):
    """
    concatenate the lists in set_of_p into one list
    """
    return reduce(lambda a, b : a + b, set_of_p)

def get_req_balls(table_p):
    """
    Given a table, return lists of left and right balls required along this
    rail

    @param list table_p -- list of table layout returned from get_table call
    @return list with two elements.  The first is a list of balls that
            need to be pocketed along the left rail.  The second is a list
            of balls that need to be pocketed along the right rail.
    """

    def same_color(blist):
        return list(map(switch_solid_stripe, list(filter(lambda a : a != 8,
                                                         blist))))
    def switch_solid_stripe(ball_no):
        if ball_no > 8:
            return ball_no - 8
        return ball_no + 8

    def get_set_balls(set_of_p):
        return same_color(reduce_lists(set_of_p))

    return [get_set_balls(table_p[1]), get_set_balls(table_p[0])]
