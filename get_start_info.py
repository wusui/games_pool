#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Set ball location information needed at the start of the program
"""
from itertools import permutations
from get_layout_and_picks import get_layout_and_picks

def get_start_info(layout):
    """
    Return a dict with the following information:
        layout:  a dict consisting of the following:
            table: two element list representing the table.  The first
                   element represents the left long rail, and the second
                   element represents the right long rail.  Each of these
                   elements contains three lists corresponding to the top,
                   side, and bottom pockets of the table.  Contents of these
                   lists are the ball numbers in that pocket at the start
            extra_b: Given the initial ball locations, we can determine
                   along which rail balls of the same color have to be.
                   These values are saved in two lists (corresponding to the
                   left and right rails)
            all_set_b: List of all ball numbers in all lists for the two
                   entries above.
        remaining: pairs of ball numbers corresponding to the pairs of
                   same colored balls that are not in layout (this may break
                   if an initial configuration has both balls of the same
                   color in pockets at the start).  These values are
                   vestigial but used to compute guesses (see next entry).
        guesses:   Two lists corresponding to the left and right rails.
                   Each list is the same length and each entry is a possible
                   set of balls for that rail.  Corresponding first index
                   numbers match here.  In other words, when the left rail
                   is guesses[0][0] the right rail will be guesses[1][0],
                   when the left rail is guesses[0][1] the right rail will be
                   guessses[1][1]...
        total_balls: Count of total balls on the left rail, and the total
                   balls on the right rail.  If sum is 14, 8 ball needs to
                   be added later.
        ball_patterns: Possible patterns of the number of balls in each
                   pocket (left rail is first element, right rail is second)

    @param dict layout -- information about balls in pockets.  Each key
           corresponds to a pocket label as used in the original problem
           statement.  The value of the pocket is either a ball number or
           a list of ball numbers in that pocket.  Empty pockets can be
           skipped.  This generalizes the initial start of the puzzle.
    @return dict -- Information about the ball locations.
    """
    def get_bit_patterns(info):
        def brk_down_binary(indx):
            def inner_brk_down_binary(numb):
                return (indx // (2 ** numb)) % 2
            return inner_brk_down_binary
        def step_thru_combos(indx):
            return list(map(brk_down_binary(indx),
                        list(range(0, len(info['remaining'])))))
        def inner_tec():
            return list(map(step_thru_combos,
                    list(range(0, 2 ** len(info['remaining'])))))
        return inner_tec

    def get_remaining(rem_list):
        def get_rem_lev2(rem_list):
            def get_lev2_inner1(bnumbs):
                def get_lev2_inner2(indx0n):
                    return rem_list[indx0n][bnumbs[indx0n]]
                return get_lev2_inner2
            return get_lev2_inner1
        def get_remaining_inner(rem_lst_indx):
            return list(map(get_rem_lev2(rem_list)(rem_lst_indx),
                        list(range(0,len(rem_list)))))
        return get_remaining_inner

    def get_right_list(left_list):
        def fill_one_list(left_list):
            def foli1(indx1):
                def foli2(indx2):
                    if left_list[indx1][indx2] < 8:
                        return left_list[indx1][indx2] + 8
                    return left_list[indx1][indx2] - 8
                return foli2
            def fill_one_list_inner(indx):
                return list(map(foli1(indx), list(range(0,
                                                len(left_list[indx])))))
            return fill_one_list_inner
        def inner_grl():
            return list(map(fill_one_list(left_list),
                        list(range(0, len(left_list)))))
        return inner_grl

    def get_both_lists(left_list):
        return [left_list, list(get_right_list(left_list)())]

    def get_rem(info):
        return list(map(get_remaining(info['remaining']),
                        get_bit_patterns(info)()))

    def get_strt_sides(info):
        def count_pocketed(side):
            return sum(list(map(len, info['layout']['table'][side]))) + len(
                    info['layout']['extra_b'][side]) + len(
                    get_both_lists(get_rem(info))[0][side])
        def get_side_inner():
            return list(map(count_pocketed, [0, 1]))
        return get_side_inner

    def get_start_call(info):
        def one_bpat(bcount):
            if bcount == 8:
                return list(set(permutations([3, 3, 2], 3)))
            return list(set(permutations([3, 3, 1], 3))) + \
                    list(set(permutations([3, 2, 2], 3)))
        def bpatterns(side_info):
            return [one_bpat(side_info[0]), one_bpat(side_info[1])]
        def get_tot_balls_plus_pattern(side_info):
            return dict([["total_balls", side_info],
                         ["ball_patterns", bpatterns(side_info)]])
        def get_start_wrap():
            return info | dict([["guesses", get_both_lists(get_rem(info))]]
                    ) | get_tot_balls_plus_pattern(get_strt_sides(info)())
        return get_start_wrap

    return get_start_call(get_layout_and_picks(layout))()
