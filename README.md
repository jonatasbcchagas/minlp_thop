# A mixed-integer nonlinear programming formulation for the thief orienteering problem

This repository contains a mixed-integer nonlinear programming (MINLP) formulation for the thief orienteering problem, which has been implemented using [PySCIPOpt](https://github.com/scipopt/PySCIPOpt), a Python interface for the [SCIP Optimization Suite](https://www.scipopt.org/). Our MINLP is described in detail in the paper ["Efficiently solving the thief orienteering problem with a max-min ant colony optimization algorithm"](https://link.springer.com/article/10.1007/s11590-021-01824-y) by Jonatas B. C. Chagas and Markus Wagner.

### Usage:

```console
$ python main.py [parameters]

Parameters:

  -i, --instance_file_name       inputfile (ThOP format necessary)
  -s, --solution_file_name       outputfile
  -t, --time                     maximum runtime in seconds
  -m, --bigmconstrs              flag to use mathematical model with big Ms constraints
```

#### Example:

```console
$ python main.py -i ../instances/eil51-thop/eil51_01_bsc_01_01.thop -s eil51_01_bsc_01_01.thop.sol -t 3600 -m 
```
