#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Find pairs of balls to fill in the rest of the table
"""
from get_layout import get_layout

def get_layout_and_picks(setup):
    """
    Find pairs of balls which are not already accounted for

    @param dict setup -- an initial table configuration labeled with pockets
                         A, B, and C on the right and D, E, and F on the left
    @return dict of layout, and remaining balls which is a list of ball pairs
    """
    def make_pair(numb):
        return [numb, numb + 8]
    def find_lower(layout):
        def inner_find_lower(numb):
            return not numb in layout["all_set_b"]
        return inner_find_lower
    def find_pairs(layout):
        return list(map(make_pair,
            list(filter(find_lower(layout), list(range(1,8))))))
    def get_remaining_balls(layout):
        return({"layout": layout, "remaining": find_pairs(layout)})

    return get_remaining_balls(get_layout(setup))
