# Running Pyomo on the CRC Cluster

This documentation gives a brief overview for using Pyomo on the CRC clusters with a variety of solvers.

## Preliminaries

Before proceeding with this tutorial, you need to obtain a CRC account and install a private copy of Pyomo on the CRC cluster.

### Request a CRC Account

First, you must [register for a CRC account](https://wiki.crc.nd.edu/w/index.php/How_to_Obtain_a_CRC_Account). These are free for all ND researchers.


### Install Pyomo on CRC Cluster

Per CRC policies, standalone Python packages such as Pyomo are not centrally installed or maintained. Instead, users must install their own private copy on the CRC cluster. This can be easily done on a few steps:

First, `ssh` into a CRC interative node. For example,

```bash
ssh crcfe02.crc.nd.edu
```

Next, load your preferred version of Python. Pyomo supports both 2.7 and 3.x:

```bash
module load python/3.6.4
```

Then, install Pyomo using `pip`, a popular package manager for Python:

```bash
pip install --user pyomo
```

By default, Pyomo will be installed in ```.local/bin```.

After the base Pyomo install is complete, install the extras (including the DAE toolbox):

TODO: Rebug error message and update instructions.

## Running on the CRC

There are two ways to run Pyomo on the CRC cluster: on an interactive mode (for testing only) or by submitting a job to the queue. The following shows how to do this for a simple optimization problem.

### Test Problem

We will consider the following simple linear program to test Pyomo on the CRC:

```python
# Load Pyomo
from pyomo.environ import *

# Create model
m = ConcreteModel()
m.x = Var([1,2,3], domain=NonNegativeReals)
m.c1 = Constraint(expr = m.x[1] + m.x[2] + m.x[3] <= 1)
m.c2 = Constraint(expr = m.x[1] + 2*m.x[2] >= 0.3)
m.OBJ = Objective(expr = m.x[3], sense=maximize) 

# Specify solver
solver=SolverFactory('ipopt')

# Solve model
solver.solve(m, tee=True)
```

Copy this code and save it on your CRC AFS space as `pyomo_test.py`.

### Running From the Command Line

The easest option is to directly run this code on an interactive node on the CRC cluster.

1. Login to the CRC cluster:

```bash
ssh crcfe02.crc.nd.edu
```

2. Load your preferred version of python and your favorite optimization solver.

```bash
module load python/3.6.0
module load ipopt
```

3. Run the Python script

```bash
python pyomo_test.py
```

You should see the following output:

```
Ipopt 3.12.8: 

******************************************************************************
This program contains Ipopt, a library for large-scale nonlinear optimization.
 Ipopt is released as open source code under the Eclipse Public License (EPL).
         For more information visit http://projects.coin-or.org/Ipopt
******************************************************************************

This is Ipopt version 3.12.8, running with linear solver ma27.

Number of nonzeros in equality constraint Jacobian...:        0
Number of nonzeros in inequality constraint Jacobian.:        5
Number of nonzeros in Lagrangian Hessian.............:        0

Total number of variables............................:        3
                     variables with only lower bounds:        3
                variables with lower and upper bounds:        0
                     variables with only upper bounds:        0
Total number of equality constraints.................:        0
Total number of inequality constraints...............:        2
        inequality constraints with only lower bounds:        1
   inequality constraints with lower and upper bounds:        0
        inequality constraints with only upper bounds:        1

iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
   0 -9.9999900e-03 2.70e-01 6.00e-01  -1.0 0.00e+00    -  0.00e+00 0.00e+00   0
   1 -2.3096613e-02 1.48e-01 3.42e+00  -1.7 1.87e-01    -  1.10e-01 4.70e-01h  1
   2 -7.1865937e-02 0.00e+00 8.39e-01  -1.7 1.42e-01    -  4.87e-01 1.00e+00f  1
   3 -8.1191843e-01 0.00e+00 4.70e-01  -1.7 1.47e+00    -  1.00e+00 5.02e-01f  1
   4 -7.9286713e-01 0.00e+00 2.00e-07  -1.7 1.91e-02    -  1.00e+00 1.00e+00f  1
   5 -8.4402296e-01 0.00e+00 3.48e-03  -3.8 5.61e-02    -  9.40e-01 9.12e-01f  1
   6 -8.4949514e-01 0.00e+00 1.50e-09  -3.8 7.04e-03    -  1.00e+00 1.00e+00f  1
   7 -8.4999437e-01 0.00e+00 1.84e-11  -5.7 4.99e-04    -  1.00e+00 1.00e+00f  1
   8 -8.5000001e-01 0.00e+00 2.51e-14  -8.6 5.65e-06    -  1.00e+00 1.00e+00f  1

Number of Iterations....: 8

                                   (scaled)                 (unscaled)
Objective...............:  -8.5000001246787615e-01   -8.5000001246787615e-01
Dual infeasibility......:   2.5143903682766679e-14    2.5143903682766679e-14
Constraint violation....:   0.0000000000000000e+00    0.0000000000000000e+00
Complementarity.........:   2.5342284749259295e-09    2.5342284749259295e-09
Overall NLP error.......:   2.5342284749259295e-09    2.5342284749259295e-09


Number of objective function evaluations             = 9
Number of objective gradient evaluations             = 9
Number of equality constraint evaluations            = 0
Number of inequality constraint evaluations          = 9
Number of equality constraint Jacobian evaluations   = 0
Number of inequality constraint Jacobian evaluations = 9
Number of Lagrangian Hessian evaluations             = 8
Total CPU secs in IPOPT (w/o function evaluations)   =      0.004
Total CPU secs in NLP function evaluations           =      0.000

EXIT: Optimal Solution Found.
```

### Submitting to a Queue

Per CRC policies, the interative nodes should only be used for testing short computational jobs. All other jobs should be submitted to a queue.

** Jacob and Xian - please fill this in **

## Available Solvers

The CRC clusters supports three (and counting) high-performance optimization solvers that are directly callable from Pyomo. This makes it increadily easy - often one only needs to change a few lines of code - to try different solvers for an optimization problem.

The following contains instructions on using solvers currently available on the CRC cluster. By modifying the `SolverFactory` in `pyomo_test.py`, you can try all of these solvers on the simple test problem.

### CPLEX

First load the module:

```module load cplex```

This will update your environmental variables and the Gurobi executable should be callable from Pyomo:

```python
solver=SolverFactory('cplex')
```

Here is the output for the test problem:

```
Welcome to IBM(R) ILOG(R) CPLEX(R) Interactive Optimizer 12.7.1.0
  with Simplex, Mixed Integer & Barrier Optimizers
5725-A06 5725-A29 5724-Y48 5724-Y49 5724-Y54 5724-Y55 5655-Y21
Copyright IBM Corp. 1988, 2017.  All Rights Reserved.

Type 'help' for a list of available commands.
Type 'help' followed by a command name for more
information on commands.

CPLEX> Logfile 'cplex.log' closed.
Logfile '/afs/crc.nd.edu/user/a/adowling/Private/tmp103f3a.cplex.log' open.
CPLEX> Problem '/afs/crc.nd.edu/user/a/adowling/Private/tmpdhMJXY.pyomo.lp' read.
Read time = 0.01 sec. (0.00 ticks)
CPLEX> Problem name         : /afs/crc.nd.edu/user/a/adowling/Private/tmpdhMJXY.pyomo.lp
Objective sense      : Maximize
Variables            :       4
Objective nonzeros   :       1
Linear constraints   :       3  [Less: 1,  Greater: 1,  Equal: 1]
  Nonzeros           :       6
  RHS nonzeros       :       3

Variables            : Min LB: 0.000000         Max UB: all infinite   
Objective nonzeros   : Min   : 1.000000         Max   : 1.000000       
Linear constraints   :
  Nonzeros           : Min   : 1.000000         Max   : 2.000000       
  RHS nonzeros       : Min   : 0.3000000        Max   : 1.000000       
CPLEX> CPXPARAM_Read_APIEncoding                        "UTF-8"
Tried aggregator 1 time.
LP Presolve eliminated 1 rows and 1 columns.
Reduced LP has 2 rows, 3 columns, and 5 nonzeros.
Presolve time = 0.00 sec. (0.00 ticks)
Initializing dual steep norms . . .

Iteration log . . .
Iteration:     1   Dual objective     =             0.850000

Dual simplex - Optimal:  Objective =  8.5000000000e-01
Solution time =    0.00 sec.  Iterations = 1 (0)
Deterministic time = 0.00 ticks  (4.51 ticks/sec)

CPLEX> Solution written to file '/afs/crc.nd.edu/user/a/adowling/Private/tmp0ryhXG.cplex.sol'.
```

### Gurobi

First load the module:

```module load gurobi```

This will update your environmental variables and the Gurobi executable should be callable from Pyomo:

```python
solver=SolverFactory('gurobi')
```

Here is the output for the test problem:
```
Optimize a model with 3 rows, 4 columns and 6 nonzeros
Coefficient statistics:
  Matrix range     [1e+00, 2e+00]
  Objective range  [1e+00, 1e+00]
  Bounds range     [0e+00, 0e+00]
  RHS range        [3e-01, 1e+00]
Presolve removed 1 rows and 1 columns
Presolve time: 0.02s
Presolved: 2 rows, 3 columns, 5 nonzeros

Iteration    Objective       Primal Inf.    Dual Inf.      Time
       0    1.0000000e+00   1.500000e-01   0.000000e+00      0s
       1    8.5000000e-01   0.000000e+00   0.000000e+00      0s

Solved in 1 iterations and 0.02 seconds
Optimal objective  8.500000000e-01
Freed default Gurobi environment
```

### Ipopt

Two versions (modules) of Ipopt are available to CRC users: `ipopt/3.12.8` and `ipopt/hsl/3.12.8`. The latter supports HSL linear algebra routines whereas the former does not (and relies on the open-source library MUMPS). In general, the HSL linear algebra routines are more stable and are significantly faster for large-scale problems. All IPOPT users are strongly encouraged to use the HSL libraries. To obtain access to `ipopt/hsl/3.12.8`, ND users must apply for a [free academic license](http://www.hsl.rl.ac.uk/download/coinhsl/2015.06.23/) and then forward the approval email to CRCSupport@nd.edu. 

To use either version of Ipopt, first load the module. For example,

```module load ipopt/hsl/3.12.8```

This will update your environmental variables and the ipopt executable should be callable from Pyomo:

```python
solver=SolverFactory('ipopt')
```

If needed, you can also directly specify the path to the Ipopt executable to Pyomo:

```python
solver=SolverFactory('ipopt', executable="/afs/crc.nd.edu/x86_64_linux/i/ipopt/3.12.8-hsl/bin/ipopt")
```

Next, you may want to customize some of the [Ipopt options](https://www.coin-or.org/Ipopt/documentation/node40.html). For example, specify the linear algebra routine (use MA57 from the HSL library):

```python
solver.options['linear_solver'] = "ma57"
```

Here is the output when using MA57:

```
Ipopt 3.12.8: linear_solver=ma57


******************************************************************************
This program contains Ipopt, a library for large-scale nonlinear optimization.
 Ipopt is released as open source code under the Eclipse Public License (EPL).
         For more information visit http://projects.coin-or.org/Ipopt
******************************************************************************

This is Ipopt version 3.12.8, running with linear solver ma57.

Number of nonzeros in equality constraint Jacobian...:        0
Number of nonzeros in inequality constraint Jacobian.:        5
Number of nonzeros in Lagrangian Hessian.............:        0

Total number of variables............................:        3
                     variables with only lower bounds:        3
                variables with lower and upper bounds:        0
                     variables with only upper bounds:        0
Total number of equality constraints.................:        0
Total number of inequality constraints...............:        2
        inequality constraints with only lower bounds:        1
   inequality constraints with lower and upper bounds:        0
        inequality constraints with only upper bounds:        1

iter    objective    inf_pr   inf_du lg(mu)  ||d||  lg(rg) alpha_du alpha_pr  ls
   0 -9.9999900e-03 2.70e-01 6.00e-01  -1.0 0.00e+00    -  0.00e+00 0.00e+00   0
   1 -2.3096613e-02 1.48e-01 3.42e+00  -1.7 1.87e-01    -  1.10e-01 4.70e-01h  1
   2 -7.1865937e-02 0.00e+00 8.39e-01  -1.7 1.42e-01    -  4.87e-01 1.00e+00f  1
   3 -8.1191843e-01 0.00e+00 4.70e-01  -1.7 1.47e+00    -  1.00e+00 5.02e-01f  1
   4 -7.9286713e-01 0.00e+00 2.00e-07  -1.7 1.91e-02    -  1.00e+00 1.00e+00f  1
   5 -8.4402296e-01 0.00e+00 3.48e-03  -3.8 5.61e-02    -  9.40e-01 9.12e-01f  1
   6 -8.4949514e-01 0.00e+00 1.50e-09  -3.8 7.04e-03    -  1.00e+00 1.00e+00f  1
   7 -8.4999437e-01 0.00e+00 1.84e-11  -5.7 4.99e-04    -  1.00e+00 1.00e+00f  1
   8 -8.5000001e-01 0.00e+00 2.51e-14  -8.6 5.65e-06    -  1.00e+00 1.00e+00f  1

Number of Iterations....: 8

                                   (scaled)                 (unscaled)
Objective...............:  -8.5000001246787615e-01   -8.5000001246787615e-01
Dual infeasibility......:   2.5143903682766679e-14    2.5143903682766679e-14
Constraint violation....:   0.0000000000000000e+00    0.0000000000000000e+00
Complementarity.........:   2.5342284749259295e-09    2.5342284749259295e-09
Overall NLP error.......:   2.5342284749259295e-09    2.5342284749259295e-09


Number of objective function evaluations             = 9
Number of objective gradient evaluations             = 9
Number of equality constraint evaluations            = 0
Number of inequality constraint evaluations          = 9
Number of equality constraint Jacobian evaluations   = 0
Number of inequality constraint Jacobian evaluations = 9
Number of Lagrangian Hessian evaluations             = 8
Total CPU secs in IPOPT (w/o function evaluations)   =      0.004
Total CPU secs in NLP function evaluations           =      0.000

EXIT: Optimal Solution Found.
```

### Coming Soon

* SCIP
* Bonmin
* Cbc and Clp
* Couenne
