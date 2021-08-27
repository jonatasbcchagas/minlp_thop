#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools
import os
import multiprocessing
import argparse
import math

def launcher(tsp_base, number_of_items_per_city, knapsack_type, knapsack_size, maximum_travel_time):
    inputfile = "../instances/%s-thop/%s_%02d_%s_%02d_%02d.thop" % (tsp_base, tsp_base, number_of_items_per_city, knapsack_type, knapsack_size, maximum_travel_time)
    outputfile = "../solutions/minlp/%s-thop/%s_%02d_%s_%02d_%02d.thop.sol" % (tsp_base, tsp_base, number_of_items_per_city, knapsack_type, knapsack_size, maximum_travel_time)
    if os.path.isfile(outputfile): return
    os.system("python main.py -i %s -s %s -t 3600 > %s" % (inputfile, outputfile, outputfile+".log"))

if __name__ == "__main__":

    tsp_base = ["eil15", "pr20", "a25", "dsj30", ]#"eil51", "pr107", "a280", "dsj1000", ]
    number_of_items_per_city = [1, 3, 5, 10, ]
    knapsack_type = ["bsc", "unc", "usw", ]
    knapsack_size = [1, 5, 10, ]
    maximum_travel_time = [1, 2, 3, ]
    
    pool = multiprocessing.Pool(processes=max(1, multiprocessing.cpu_count() - 2))
    
    for _product in itertools.product(tsp_base, number_of_items_per_city, knapsack_type, knapsack_size, maximum_travel_time):
        _tsp_base, _number_of_items_per_city, _knapsack_type, _knapsack_size, _maximum_travel_time = _product
        pool.apply_async(launcher, args=(_tsp_base, _number_of_items_per_city, _knapsack_type, _knapsack_size, _maximum_travel_time))

    pool.close()
    pool.join()
