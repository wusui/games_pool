#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Solve the pool table problem
"""
from get_start_data import reduce_lists
from solution_groups import solution_groups

def solver(layout):
    """
    Final steps in the solution.  At this point, most of the heavy lifting
    has been done by solutions_group and find_combos.  If the eight ball
    did not start in one of the pockets, it needs to be added now.  This
    code checks and adds the eight ball to each rail.  The outer layers
    of the code here converts the result to a dict format similar to the
    format used in the layout parameter, and makes sure that the numbers
    in the pockets are sorted.

    @param layout -- dict representation of the pool table at the start
    @return list of dict entries of valid solutions
    """
    def solver_main(solutions):
        def gen_8_vals(solution):
            def gen_8_inner(pdigit):
                def chk_8_val(pdigit):
                    if len(solution[pdigit]) == 3 or len(
                            set([7, 9]).intersection(solution[pdigit])) > 0:
                        return []
                    return list(map(lambda a : solution[a] + [8] if
                                a == pdigit else solution[a],
                                list(range(0, 6))))
                return [chk_8_val(pdigit[0]), chk_8_val(5 - pdigit[0])]
            return gen_8_inner
        def check_odd_pair(solution):
            return gen_8_vals(solution)(
                list(filter(
                    lambda a : sum(solution[a] + solution[5 - a]) == 32,
                    list(range(0,3))
                )))

        if sum(reduce_lists(solutions[0])) == 120:
            return [solutions]
        return list(map(check_odd_pair, solutions))

    return list(map(lambda a : dict(zip('ABCDEF', a)),
           list(map(lambda a : list(map(sorted, a)),
           list(filter(lambda a : a, reduce_lists(
           solver_main(solution_groups(layout)))))))))

if __name__ == "__main__":
    print(solver({"B": 11, "D": 12, "F": 1}))
    input()
