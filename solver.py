#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Solve the pool table problem
"""
from get_req_balls import reduce_lists
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
    def sort2(pocket):
        return sorted(pocket)
    def sort1(answer):
        return list(map(sort2, answer))
    def lst2dct(answer):
        return dict(zip('ABCDEF', answer))
    def solver_main(solutions):
        def gen_8_vals(solution):
            def really_add_8(pdigit):
                def really_add_8_inner(number):
                    if number == pdigit:
                        return solution[number] + [8]
                    return solution[number]
                return really_add_8_inner
            def add_8_to(pdigit):
                return list(map(really_add_8(pdigit), list(range(0, 6))))
            def gen_8_inner(pdigit):
                def chk_8_val(pdigit):
                    if len(solution[pdigit]) == 3:
                        return []
                    if 7 in solution[pdigit]:
                        return []
                    if 9 in  solution[pdigit]:
                        return []
                    return add_8_to(pdigit)
                return [chk_8_val(pdigit[0]), chk_8_val(5 - pdigit[0])]
            return gen_8_inner
        def chk_low(solution):
            def chk_low_inner(number):
                return sum(solution[number] + solution[5 - number]) == 32
            return chk_low_inner
        def find_pair(solution):
            return list(filter(chk_low(solution), list(range(0,3))))
        def check_odd_pair(solution):
            return gen_8_vals(solution)(find_pair(solution))
        if sum(reduce_lists(solutions[0])) == 120:
            return [solutions]
        return list(map(check_odd_pair, solutions))

    return list(map(lst2dct,
                list(map(sort1,
                    list(filter(lambda a : a, reduce_lists(
                        solver_main(solution_groups(layout)))))))))

if __name__ == "__main__":
    print(solver({"B": 11, "D": 12, "F": 1}))
    input()
