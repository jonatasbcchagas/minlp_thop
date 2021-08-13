#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import math
from data import *
from minlp import *

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    mandatory_args = parser.add_argument_group('mandatory arguments')
    mandatory_args.add_argument("-i", "--instance_file_name", action="store", dest="instance_file_name", type=str, required=True)
    mandatory_args.add_argument("-s", "--solution_file_name", action="store", dest="solution_file_name", type=str, required=True)
    mandatory_args.add_argument("-t", "--time", action="store", dest="time_limit", type=int, required=True)
    parser.add_argument("-m", "--bigmconstrs", help="create model with big Ms constraints", action="store_true")
    args = parser.parse_args()

    data = Data(args.instance_file_name)
    minlp = MINLP(data=data, big_M_constrs=args.bigmconstrs)
    minlp.solve(number_of_threads=1, time_limit=args.time_limit, output_file_name=args.solution_file_name)
