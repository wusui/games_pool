#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Return ball layout information known at the start
"""
from get_table import get_table
from get_req_balls import reduce_lists, get_req_balls

def get_layout(setup):
    """
    Get layout of table (pocketed balls, balls where we know which
    long rail they would be on, all balls that we know which side
    they would be on

    @param dict setup -- an initial table configuration labeled with pockets
                         A, B, and C on the right and D, E, and F on the left
    @return dict of table, extra_b, and all_set_b values
    """
    def get_known_balls(partial_2):
        return {"table": partial_2["table"], "extra_b": partial_2["extra_b"],
                "all_set_b": full_set(partial_2)}

    def full_set(partial_2):
        return reduce_lists(partial_2["table"][0]) + reduce_lists(
                partial_2["table"][1]) + partial_2["extra_b"][0] + \
                partial_2["extra_b"][1]

    def get_opps_part(p_table):
        return {"table": p_table, "extra_b": get_req_balls(p_table)}

    return get_known_balls(get_opps_part(get_table(setup)))
