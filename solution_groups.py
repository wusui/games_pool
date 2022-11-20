#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Solve the pool table problem
"""
from get_req_balls import reduce_lists
from find_combos import find_combos

def solution_groups(layout):
    """
    Given possible sets of balls in rails (data extracted from find_combos),
    try all permutations of long rail combinations to find possible solutions.

    @param layout -- dict representation of the pool table at the start
    @return Permutations of the two separate rail results that form valid
            solutions.  Eight ball is not accounted for.
    """
    def loop_rside(rside_info):
        return reduce_lists(rside_info)
    def loop_guesses(guess_info):
        return list(map(loop_rside, guess_info))
    def sol_grp(one_rail):
        def check_if_ok(possible_solution):
            def bp_chk(in_list):
                def bp_chk_inner(ball2):
                    if ball2 + 8 in in_list or ball2 - 8 in in_list:
                        return False
                    return True
                return bp_chk_inner
            def rail_bad(pockets):
                return not all(list(filter(bp_chk(
                        possible_solution[pockets[0]]),
                        possible_solution[pockets[1]])))
            def not_add_up(pockets):
                return sum(possible_solution[pockets[0]]
                           ) + sum(possible_solution[pockets[1]]
                           ) not in [32, 40]
            def inner_ciok():
                if rail_bad([0, 3]):
                    return []
                if rail_bad([2, 5]):
                    return []
                if not_add_up([0, 5]):
                    return []
                if not_add_up([1, 4]):
                    return []
                if not_add_up([2, 3]):
                    return []
                return possible_solution
            return inner_ciok
        def pair_em(rail_no):
            def pair_em_inner(rail_f):
                return check_if_ok(rail_f + rail_no)()
            return pair_em_inner
        def sol_grp_inner(rail_2):
            return list(map(pair_em(rail_2), one_rail))
        return sol_grp_inner
    def make_rail_pairs(two_rails):
        return list(map(sol_grp(two_rails[1]), two_rails[0]))

    def cleanup(tables_w_empties):
        def clean_empties(data):
            return len(data) != 0
        def new_parts(ind_guess):
            return list(filter(clean_empties, ind_guess))
        def cloop_guesses(guess_info):
            return list(map(new_parts, guess_info))
        return list(map(cloop_guesses, tables_w_empties))

    return reduce_lists(reduce_lists(
                cleanup(cleanup(list(map(make_rail_pairs,
                list(map(loop_guesses, list(find_combos(layout))))))))
           ))
