#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Solve the pool table problem.  Perform unclean I/O operations
"""
import json
from solver import solver

if __name__ == "__main__":
    with open('starting_layout.json', 'r', encoding='utf8') as ifd:
        outputd = solver(json.load(ifd))
        json_object = json.dumps(outputd, indent=4)
        with open("answer.json", "w", encoding='utf8') as outfile:
            outfile.write(json_object)
