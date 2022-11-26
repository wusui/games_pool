#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Find pairs of balls to fill in the rest of the table
"""
from functools import reduce

def reduce_lists(set_of_p):
    """
    concatenate the lists in set_of_p into one list
    """
    return reduce(lambda a, b : a + b, set_of_p)

def get_start_data(setup):
    """
    Find pairs of balls which are not already accounted for

    @param dict setup -- an initial table configuration labeled with pockets
                         A, B, and C on the right and D, E, and F on the left
    @return dict of layout, and remaining balls which is a list of ball pairs
    """
    def find_pairs(layout):
        return list(map(lambda a : [a, a + 8],
            list(filter(lambda a : not a in layout["all_set_b"],
                        list(range(1,8))))))

    def get_remaining_balls(layout):
        return({"layout": layout, "remaining": find_pairs(layout)})

    def get_table(setup):
        def config_start(init_pos):
            def inner_config(pletter):
                if pletter in init_pos:
                    if isinstance(init_pos[pletter], list):
                        return init_pos[pletter]
                    return [init_pos[pletter]]
                return []
            return inner_config

        def setup_table(init_pos):
            return list(map(config_start(init_pos[0]), init_pos[1]))

        return [setup_table([setup, "DEF"]), setup_table([setup, "ABC"])]

    def get_req_balls(table_p):
        def get_set_balls(set_of_p):
            return list(map(lambda b :
                        b - 8 if b > 8 else b + 8,
                        list(filter(lambda a : a != 8,
                        reduce_lists(set_of_p)))))

        return [get_set_balls(table_p[1]), get_set_balls(table_p[0])]

    def get_layout(setup):
        def get_known_balls(partial_2):
            return {"table": partial_2["table"],
                    "extra_b": partial_2["extra_b"],
                    "all_set_b": (reduce_lists(partial_2["table"][0]) +
                    reduce_lists(partial_2["table"][1]) +
                    partial_2["extra_b"][0] +
                    partial_2["extra_b"][1])}

        def get_opps_part(p_table):
            return {"table": p_table, "extra_b": get_req_balls(p_table)}

        return get_known_balls(get_opps_part(get_table(setup)))

    return get_remaining_balls(get_layout(setup))
