#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyscipopt import Model, quicksum
import networkx as nx
import time
from data import *
import itertools

class MINLP:

    def __init__(self, data, big_M_constrs=False):

        self.data = data
        self.model = Model()

        n = self.data.number_of_cities
        m = self.data.number_of_items

        self.C = set(range(1, n+1))
        self.A = set((i, j) for i in self.C - {n} for j in self.C - {1})
        self.I = set(range(1, m+1))
        self.Ic = {i: set(k for k in self.I if self.data.items[k]["city"] == i) for i in self.C}

        # decision variables:
        self.x = {(i, j): self.model.addVar(vtype='B') for (i, j) in self.A}
        self.y = {i: self.model.addVar(vtype='B') for i in self.C}
        self.z = {k: self.model.addVar(vtype='B') for k in self.I}
        self.q = {i: self.model.addVar(vtype='I', lb=0, ub=self.data.capacity_of_knapsack) for i in range(1, self.data.number_of_cities+1)}
        self.t = {i: self.model.addVar(vtype='C', lb=0, ub=self.data.max_time) for i in range(1, self.data.number_of_cities+1)}
        
        # objective
        self.model.setObjective(quicksum(self.z[k] * self.data.items[k]["profit"] for k in self.I), "maximize")

        # constraints:
        self.model.addCons(quicksum(self.z[k] * self.data.items[k]["weight"] for k in self.I) <= self.data.capacity_of_knapsack)

        for i in self.C:
            for k in self.Ic[i]:
                self.model.addCons(self.y[i] >= self.z[k])      

        for i in self.C - {1, n}:
            self.model.addCons(self.y[i] <= quicksum(self.z[k] for k in self.Ic[i]))                

        self.model.addCons(self.y[1] == 1)   
        self.model.addCons(self.y[n] == 1)   

        for i in self.C - {n}:
            self.model.addCons(quicksum(self.x[i, j] for j in self.C if (i, j) in self.A) == self.y[i])

        for j in self.C - {1}:
            self.model.addCons(quicksum(self.x[i, j] for i in self.C if (i, j) in self.A) == self.y[j])

        v = (self.data.max_speed - self.data.min_speed) / self.data.capacity_of_knapsack

        if big_M_constrs == True:
            M_line = {j: self.data.capacity_of_knapsack + sum(self.data.items[k]["weight"] for k in self.Ic[j]) for j in self.C}
            for (i, j) in self.A:
                self.model.addCons(self.q[j] >= self.q[i] + quicksum(self.z[k]*self.data.items[k]["weight"] for k in self.Ic[j]) - M_line[j] * (1 - self.x[i, j]))
            M_2lines = {(i, j): self.data.max_time + self.data.distance(i, j) / (self.data.min_speed) for (i, j) in self.A}
            for (i, j) in self.A:
                self.model.addCons(self.t[j] >= self.t[i] + self.data.distance(i, j) / (self.data.max_speed - v * self.q[i]) - M_2lines[i, j] * (1 - self.x[i, j]))
        else:
            for (i, j) in self.A:
                self.model.addCons(self.q[j] >= (self.q[i] + quicksum(self.z[k]*self.data.items[k]["weight"] for k in self.Ic[j])) * self.x[i, j])
            for (i, j) in self.A:
                self.model.addCons(self.t[j] >= (self.t[i] + self.data.distance(i, j) / (self.data.max_speed - v * self.q[i])) * self.x[i, j])
        

    def solve(self, number_of_threads=1, time_limit=3600, output_file_name=None):
        
        self.model.setIntParam('lp/threads', number_of_threads)
        self.model.setRealParam('limits/time', time_limit)
        self.model.optimize()
                
        #print("\n\nLB: %.5f\n" % (self.model.getObjVal()))

        graph = nx.Graph()
        for (i, j) in self.A:
            if self.model.getVal(self.x[i, j]) >= 0.5:
                graph.add_edge(i, j)
        tour = list(nx.dfs_preorder_nodes(graph, source=1))

        packing = [k for k in self.I if self.model.getVal(self.z[k]) >= 0.5]
    
        f = open(output_file_name, 'w')
        f.write("[%s]\n[%s]\n" % (','.join([str(c) for c in tour[1:-1]]), ','.join([str(i) for i in packing])))
        f.close()

if __name__ == "__main__":

    data = Data("../../instances/eil15-thop/eil15_01_bsc_01_01.thop")
    minlp = MINLP(data=data, big_M_constrs=True)
    minlp.solve(number_of_threads=1, time_limit=60, output_file_name="minlp_test.sol")
