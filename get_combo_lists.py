#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Calculate all combinations of balls possible for a set of three pockets
"""
from itertools import combinations
from get_req_balls import reduce_lists

def gen_combos(combo_data):
    """
    Generate combinations of ball layouts into three pockets (left rail or
    right rail).

    @param combo_data list containing two lists.  The first list contains
                      ball numbers.  The second list is the distribution of
                      these balls into three pockets.

    @return list of lists.  Each sublist consists of three tuples representing
            the ball numbers in three pockets.
    """

    def shrink(balls):
        def shrink_wrap(pset):
            def shrink_test(theset):
                def inner_test(ball):
                    if ball in theset:
                        return False
                    return True
                return inner_test
            return list(filter(shrink_test(pset), balls))
        return shrink_wrap

    def combotest(balls):
        def combo_ball(buckets):
            def reploop(pset):
                if len(buckets) == 1:
                    return [pset]
                return [pset] + combotest(shrink(balls)(pset))(buckets[1:])
            return list(map(reploop, list(combinations(balls, buckets[0]))))
        return combo_ball

    def make_combos(combo_data):
        def flatten_combos(balls):
            def handle_later(root_pocket):
                def handle_inner(rest_o_pockets):
                    return [root_pocket, rest_o_pockets[0],
                            rest_o_pockets[1][0]]
                return handle_inner
            def handle_first(combo_data):
                return list(map(handle_later(combo_data[0]), combo_data[1:]))
            def inner_flat(buckets):
                return list(map(handle_first, combotest(balls)(buckets)))
            return inner_flat
        return flatten_combos(combo_data[0])(combo_data[1])

    return reduce_lists(make_combos(combo_data))
