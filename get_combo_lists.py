#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Calculate all combinations of balls possible for a set of three pockets
"""
from itertools import combinations
from get_start_data import reduce_lists

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
    def combotest(balls):
        def combo_ball(buckets):
            def reploop(pset):
                if len(buckets) == 1:
                    return [pset]
                return [pset] + combotest(
                    list(filter(lambda a : a not in pset, balls))
                    )(buckets[1:])
            return list(map(reploop, list(combinations(balls, buckets[0]))))
        return combo_ball

    def flatten_combos(balls):
        def inner_flat(buckets):
            return list(map(lambda a :
                list(map(lambda b : [a[0], b[0], b[1][0]], a[1:])),
                combotest(balls)(buckets)))
        return inner_flat

    return reduce_lists(flatten_combos(combo_data[0])(combo_data[1]))
