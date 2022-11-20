#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Solve the pool table problem
"""
from itertools import combinations
from get_start_info import get_start_info
from get_combo_lists import gen_combos

def find_combos(layout):
    """
    First step in the solution.  Extract data from get_start_info.  Come up
    with lists of possible ball solutions for each long rail (left side
    of the table and right side of the table).

    @param layout -- dict representation of the pool table at the start
    @return List of possible combinations solutions without the 8 ball
             if that ball is not in an intial hole.  Solutions are
             at this point independent of rails. Makes extensive use
             of get_start_info data.
    """
    def find_combos1(table_data):
        def pckt_looper(rside):
            def bpattern_loop(indx):
                def chk_pair(combo):
                    return abs(combo[0] - combo[1]) > 1
                def chk_cons_pock(one_pock):
                    if len(one_pock) < 2:
                        return True
                    return all(map(chk_pair, list(combinations(one_pock, 2))))
                def cons_check(chk_comb):
                    return all(list(map(chk_cons_pock, chk_comb)))
                def includepp(ind_con):
                    def includepp_inner(hval):
                        return list(ind_con[hval]) + \
                                table_data['layout']['table'][rside][hval]
                    return includepp_inner
                def chk_a_cons(ind_con):
                    return list(map(includepp(ind_con),
                                    list(range(0, len(ind_con)))))
                def cons_loop(a_cons):
                    return list(map(chk_a_cons, a_cons))
                def remove_cons(combs):
                    return list(filter(cons_check, cons_loop(combs)))
                def b_adj():
                    return table_data['layout']['extra_b'][rside] + \
                            table_data['guesses'][rside][indx]
                def fix_pockets(bpattern):
                    def fix_pockets_inner(indxf):
                        return bpattern[indxf] - len(
                                table_data['layout']['table'][rside][indxf])
                    return fix_pockets_inner
                def p_adj(bpattern):
                    def p_adj_inner():
                        return list(map(fix_pockets(bpattern),
                                        list(range(0, 3))))
                    return p_adj_inner
                def inner_bpattern_loop(bpattern):
                    return remove_cons(gen_combos([b_adj(),
                            p_adj(bpattern)()]))
                return inner_bpattern_loop
            def dpt_indx(indx):
                return list(map(bpattern_loop(indx),
                                table_data['ball_patterns'][rside]))
            return dpt_indx
        def guess_loop(indx):
            return [pckt_looper(0)(indx), pckt_looper(1)(indx)]
        def inner_find_combos():
            return list(map(guess_loop, list(
                    range(0, len(table_data['guesses'][0])))))
        return inner_find_combos
    return find_combos1(get_start_info(layout))()
