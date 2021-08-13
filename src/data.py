#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

EPS = 10e-4

class Data:

    def __init__(self, instance_file_name):

        file = open(instance_file_name, 'r')
        lines = file.readlines()
        
        # lines[0]  // PROBLEM NAME:    a280-ThOP
        # lines[1]  // KNAPSACK DATA TYPE: bounded strongly corr
        # lines[2]  // DIMENSION:  280
        self.number_of_cities = int(lines[2].split()[-1])
        # lines[3]  // NUMBER OF ITEMS: 279
        self.number_of_items = int(lines[3].split()[-1])
        # lines[4]  // CAPACITY  OF  KNAPSACK: 25936
        self.capacity_of_knapsack = int(lines[4].split()[-1])
        # lines[5]  // MAX TIME: xxx
        self.max_time = float(lines[5].split()[-1])
        # lines[6]  // MIN SPEED: 0.1
        self.min_speed = float(lines[6].split()[-1])
        # lines[7]  // MAX SPEED: 1
        self.max_speed = float(lines[7].split()[-1])
        # lines[8]  // EDGE_WEIGHT_TYPE: CEIL_2D
        # lines[9]  // NODE_COORD_SECTION(INDEX, X, Y):

        self.cities = {}
        for line in lines[10:10+self.number_of_cities]:
            index, pos_x, pos_y = line.split()
            self.cities[int(index)] = {"x": float(pos_x), "y": float(pos_y)}

        # lines[10+number_of_cities]  // ITEMS SECTION(INDEX, PROFIT, WEIGHT, ASSIGNED NODE NUMBER):

        self.items = {}
        for line in lines[11+self.number_of_cities:11+self.number_of_cities+self.number_of_items]:
            index, profit, weight, id_city = line.split()
            self.items[int(index)] = {"profit": float(profit), "weight": float(weight), "city": int(id_city)}
        file.close()

    def distance(self, city1, city2):
        return math.ceil(math.sqrt(
                                    (self.cities[city1]["x"]-self.cities[city2]["x"])**2 +
                                    (self.cities[city1]["y"]-self.cities[city2]["y"])**2
                                  )
                         )
