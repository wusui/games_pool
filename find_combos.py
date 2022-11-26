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
                def remove_cons(combs):
                    return list(filter(lambda a :
                        all(list(map(lambda b : True if len(a) < 2
                            else all(map(lambda c : abs(c[0] - c[1]) > 1,
                                list(combinations(b, 2))
                            )), a
                        ))),
                        list(map(lambda b :
                            list(map(lambda a :
                                list(b[a]) +
                                table_data['layout']['table'][rside][a],
                                list(range(0, len(b)))
                            )),
                        combs))
                    ))
                def inner_bpattern_loop(bpattern):
                    return remove_cons(gen_combos([
                        table_data['layout']['extra_b'][rside] +
                        table_data['guesses'][rside][indx],
                        list(map(lambda a : bpattern[a] -
                            len(table_data['layout']['table'][rside][a]),
                            list(range(0, 3))
                        ))
                    ]))
                return inner_bpattern_loop
            def dpt_indx(indx):
                return list(map(bpattern_loop(indx),
                    table_data['ball_patterns'][rside]))
            return dpt_indx
        return list(map(lambda a : [pckt_looper(0)(a), pckt_looper(1)(a)],
            list(range(0, len(table_data['guesses'][0])))
        ))
    return find_combos1(get_start_info(layout))
