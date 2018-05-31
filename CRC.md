# Running Pyomo on the CRC Cluster

Add some introductory text here

## Preliminaries

### Request a CRC Account

### Install Pyomo on CRC Cluster

## Submitting a Job

Add sample code here.

Add script here

## Available Solvers

Add instructions on how to specify the solver. For each solver listed below, give the link 

### Gurobi

### Ipopt

Two versions (modules) of Ipopt are available to CRC users: `ipopt/3.12.8` and `ipopt/hsl/3.12.8`. The latter supports HSL linear algebra routines whereas the former does not (and relies on the open-source library MUMPS). In general, the HSL linear algebra routines are more stable and are significantly faster for large-scale problems. All IPOPT users are strongly encouraged to use the HSL libraries. To obtain access to `ipopt/hsl/3.12.8`, ND users must apply for a [free academic license](http://www.hsl.rl.ac.uk/download/coinhsl/2015.06.23/) and then forward the approval email to crcsupport@crc.nd.edu. 

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

### MOSEK

### CPLEX

### Coming Soon

* SCIP
* Bonmin
* Cbc and Clp
* Couenne
