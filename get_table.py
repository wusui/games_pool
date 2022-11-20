#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Convert dict definition of initial layout into a nested list layout
"""
def get_table(setup):
    """
    Earliest table conversion

    @param dict setup -- an initial table configuration labeled with pockets
                         A, B, and C on the right and D, E, and F on the left
    @return list of two lists.  Each of these lists consist of three lists.
            The contents of these lists are the starting balls in each pocket
            with an empty pocket represented by an empty list
    """
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
