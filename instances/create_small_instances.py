#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
import itertools
import os

opt_value = {
"eil51" : 467, "eil15" : 224, 
"pr107" : 49672, "pr20" : 32234, 
"a280" : 2613, "a25" : 942, 
"dsj1000" : 19256640, "dsj30" : 4950839,
}

def create_new_instance(tsp_base, number_of_items_per_city, knapsack_type, knapsack_size, maximum_travel_time, subset_size, preselected_cities):    

    preselected_cities.sort()
    number_of_cities = int(''.join(filter(lambda x: x.isdigit(), tsp_base)))
    number_of_items = (number_of_cities - 2) * number_of_items_per_city
    new_number_of_cities = subset_size
    new_number_of_items = (new_number_of_cities - 2) * number_of_items_per_city
    
    instance_file_name = "%s-thop/%s_%02d_%s_%02d_%02d.thop" % (tsp_base, tsp_base, number_of_items_per_city, knapsack_type, knapsack_size, maximum_travel_time)
    f = open(instance_file_name, 'r')
    lines = f.readlines()
    f.close()

    # lines[0]  // PROBLEM NAME:    a280-ThOP
    lines[0] = lines[0].replace(str(number_of_cities), str(new_number_of_cities))
    # lines[1]  // KNAPSACK DATA TYPE: bounded strongly corr
    # lines[2]  // DIMENSION:  280
    lines[2] = lines[2].replace(str(number_of_cities), str(new_number_of_cities))
    # lines[3]  // NUMBER OF ITEMS: 279
    lines[3] = lines[3].replace(str(number_of_items), str(new_number_of_items))
    # lines[4]  // CAPACITY  OF  KNAPSACK: 25936
    lines[4] = lines[4].replace(lines[4].split()[-1], str(int(int(lines[4].split()[-1]) * (new_number_of_cities / float(number_of_cities)))))
    # lines[5]  // MAX TIME: xxx
    new_time = int(int(lines[5].split()[-1]) * (opt_value[tsp_base.replace(str(number_of_cities), str(new_number_of_cities))] / float(opt_value[tsp_base])))
    _, pos_1_x, pos_1_y = lines[10].split()
    _, pos_n_x, pos_n_y = lines[10+number_of_cities-1].split()
    dist_1_to_n = math.ceil(math.sqrt((float(pos_1_x) - float(pos_n_x))**2 + (float(pos_1_y) - float(pos_n_y))**2))
    new_time = int(max(new_time, dist_1_to_n))
    lines[5] = lines[5].replace(lines[5].split()[-1], str(new_time))
    # lines[6]  // MIN SPEED: 0.1
    min_speed = float(lines[6].split()[-1])
    # lines[7]  // MAX SPEED: 1
    max_speed = float(lines[7].split()[-1])
    # lines[8]  // EDGE_WEIGHT_TYPE: CEIL_2D
    # lines[9]  // NODE_COORD_SECTION(INDEX, X, Y):

    new_index_cities = {}
    new_index = 1
    for i in range(10, 10+number_of_cities):
        index, pos_x, pos_y = lines[i].split()
        if int(index) not in preselected_cities:
            lines[i] = "***"
        else:
            new_index_cities[index] = str(new_index)
            lines[i] = "%s %s %s\n" % (str(new_index), pos_x, pos_y)
            new_index += 1

    # lines[10+number_of_cities]  // ITEMS SECTION(INDEX, PROFIT, WEIGHT, ASSIGNED NODE NUMBER):

    new_index = 1
    for i in range(11+number_of_cities, 11+number_of_cities+number_of_items):
        index, profit, weight, id_city = lines[i].split()
        if int(id_city) not in preselected_cities:
            lines[i] = "***"
        else:
            lines[i] = "%s %s %s %s\n" % (str(new_index), profit, weight, new_index_cities[id_city])
            new_index += 1

    if not os.path.isdir("%s-thop" % (tsp_base.replace(str(number_of_cities), str(new_number_of_cities)))):
        os.system("mkdir %s-thop" % (tsp_base.replace(str(number_of_cities), str(new_number_of_cities))))

    new_instance_file_name = "%s-thop/%s_%02d_%s_%02d_%02d.thop" % (tsp_base.replace(str(number_of_cities), str(new_number_of_cities)), 
                                                                    tsp_base.replace(str(number_of_cities), str(new_number_of_cities)), 
                                                                    number_of_items_per_city, knapsack_type, knapsack_size, maximum_travel_time)
    f = open(new_instance_file_name, 'w')
    for line in lines:
        if "***" not in line:
            f.write(line)
    f.close()

if __name__ == "__main__":

    tsp_base_and_subset_size = [("eil51", [15, ]),
                                ("pr107", [20, ]), 
                                ("a280", [25, ]), 
                                ("dsj1000", [30, ]), ]

    number_of_items_per_city = [1, 3, 5, 10, ]
    knapsack_type = ["bsc", "unc", "usw", ]
    knapsack_size = [1, 5, 10, ]
    maximum_travel_time = [1, 2, 3, ]

    subset_of_cities = {}
    for tsp, subset_size in tsp_base_and_subset_size:
        number_of_cities = int(''.join(filter(lambda x: x.isdigit(), tsp)))
        for _subset_size in subset_size:
            np.random.seed(11235813 * _subset_size)
            _subset_of_cities = {1, number_of_cities}
            while len(_subset_of_cities) < _subset_size:
                _subset_of_cities.add(np.random.randint(2, number_of_cities))                
            subset_of_cities[(tsp, _subset_size)] = _subset_of_cities

    for config in itertools.product(tsp_base_and_subset_size, number_of_items_per_city, knapsack_type, knapsack_size, maximum_travel_time):
        _tsp_base_and_subset_size, _number_of_items_per_city, _knapsack_type, _knapsack_size, _maximum_travel_time = config
        _tsp_base, _subset_size = _tsp_base_and_subset_size
        for __subset_size in _subset_size:        
            create_new_instance(_tsp_base, _number_of_items_per_city, _knapsack_type, _knapsack_size, _maximum_travel_time, __subset_size, list(subset_of_cities[(_tsp_base, __subset_size)]))
