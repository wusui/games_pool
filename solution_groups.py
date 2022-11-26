#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Solve the pool table problem
"""
from get_start_data import reduce_lists
from find_combos import find_combos

def solution_groups(layout):
    """
    Given possible sets of balls in rails (data extracted from find_combos),
    try all permutations of long rail combinations to find possible solutions.

    @param layout -- dict representation of the pool table at the start
    @return Permutations of the two separate rail results that form valid
            solutions.
    """
    def check_if_ok(possible_solution):
        if not all(list(map(lambda b :
                all(list(filter(lambda a :
                a + 8 not in possible_solution[b[0]] and
                a - 8 not in possible_solution[b[0]],
                possible_solution[b[1]]))), [[0, 3], [2, 5]]))):
            return []
        if not all(list(map(lambda a :
                sum(possible_solution[a[0]]) +
                sum(possible_solution[a[1]]) in [32, 40],
                [[0, 5], [1, 4], [2, 3]]))):
            return []
        return possible_solution

    def make_rail_pairs(lrails):
        return list(map(lambda b : list(map(lambda a :
                check_if_ok(a + b), lrails[1])), lrails[0]))

    def cleanup(tables_w_empties):
        return list(map(lambda c : list(map(lambda b :
                    list(filter(lambda a : a, b)),
                    c)), tables_w_empties))

    return reduce_lists(reduce_lists(
                cleanup(cleanup(list(map(make_rail_pairs,
                list(map(lambda a : list(
                     map(reduce_lists, a)),
                     list(find_combos(layout))))))))))
