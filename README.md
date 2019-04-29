
# ND Pyomo Cookbook

T[Pyomo](http://www.pyomo.org/) is a state-of-the-art Python package for 
modeling and solving optimization problems. Using Pyomo, a user can embed an 
optimization model consisting of **decision variables**, **constraints**, and 
an optimization **objective** within Python. Pyomo includes a rich set of 
features to enable modeling of complex systems, specifying a solver, and 
accessing the solution.

This repository provides instructions on getting started with Pyomo, and a 
collection of Pyomo modeling notebooks that have been developed for 
instructional purposes at Notre Dame. The notebooks were originally developed 
using the [Anaconda distribution of Python](https://www.anaconda.com/download/).
The notebooks have been recently updated to open directly on 
[Google Colaboratory](https://colab.research.google.com/) which enables their 
using only a browser window.

PyomoFest at Notre Dame was held June 5-7, 2018. This repository contains the 
[agenda](PyomoFest.md), [slides](PyomoFest/slides/) and 
[exercises](PyomoFest/exercises_wo_soln/exercises/) distributed during that 
event.

## Contents
---

### [Chapter 1. Installing a Pyomo/Python Development Environment](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/01.00-Installing-Pyomo.ipynb)
- [1.1 Getting Started with Pyomo on Google Colab](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/01.01-Getting-Started-with-Pyomo-on-Google-Colab.ipynb)
- [1.2 Running Pyomo on the Notre Dame CRC Cluster](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/01.02-Running-Pyomo-on-the-Notre-Dame-CRC-Cluster.ipynb)

### [Chapter 2. Linear Programming](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/02.00-Linear-Programming.ipynb)
- [2.1 Production Models with Linear Constraints](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/02.01-Production-Models-with-Linear-Constraints.ipynb)
- [2.2 Linear Blending Problem](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/02.02-Linear-Blending-Problem.ipynb)
- [2.3 Design of a Cold Weather Fuel for a Camping Stove](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/02.03-Mixture-Design-Cold-Weather-Fuel.ipynb)
- [2.4 Gasoline Blending](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/02.04-Gasoline-Blending.ipynb)
- [2.5 Model Predictive Control of a Double Integrator](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/02.05-Model-Predictive-Control-of-a-Double-Integrator.ipynb)

### [Chapter 3. Assignment Problems](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/03.00-Assignment-Problems.ipynb)
- [3.1 Transportation Networks](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/03.01-Transportation-Networks.ipynb)

### [Chapter 4. Scheduling with Disjunctive Constraints](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/04.00-Scheduling-with-Disjunctive-Constraints.ipynb)
- [4.1 Machine Bottleneck](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/04.01-Machine-Bottleneck.ipynb)
- [4.2 Job Shop Scheduling](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/04.02-Job-Shop-Scheduling.ipynb)
- [4.3 Maintenance Planning](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/04.03-Maintenance-Planning.ipynb)
- [4.4 Scheduling Multipurpose Batch Processes using State-Task Networks](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/04.04-Scheduling-Multipurpose-Batch-Processes-using-State-Task_Networks.ipynb)

### [Chapter 5. Simulation](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/05.00-Simulation.ipynb)
- [5.1 Linear First Order System](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/05.01-Linear-First-Order-System.ipynb)
- [5.2 Exothermic CSTR](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/05.02-Exothermic-CSTR.ipynb)
- [5.3 Transient Heat Conduction in Various Geometries](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/05.03-Heat_Conduction_in_Various_Geometries.ipynb)

### [Chapter 6. Differential-Algebraic Equations](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/06.00-Differential-Algebraic-Equations.ipynb)
- [6.1 Unconstrained Scalar Optimization](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/06.01-Unconstrained-Scalar-Optimization.ipynb)
- [6.2 Maximizing Concentration of an Intermediate in a Batch Reactor](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/06.02-Maximizing-Concentration-of-an-Intermediate-in-a-Batch-Reactor.ipynb)
- [6.3 Path Planning for a Simple Car](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/06.03-Path-Planning-for-a-Simple-Car.ipynb)

### [Chapter 7. Parameter Estimation](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/07.00-Parameter-Estimation.ipynb)
- [7.1 Parameter Estimation](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/07.01-Parameter-Estimation-Catalytic-Reactor.ipynb)

### [Chapter 8. Financial Applications](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/08.00-Financial-Applications.ipynb)
- [8.1 Binomial Model for Pricing Options](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/08.01-Binomial-Model-for-Pricing-Options.ipynb)
- [8.2 Historical Stock Data](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/08.02-Historical-Stock_-ata.ipynb)
- [8.3 Charting Stock Data](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/08.03-Charting-Stock-Data.ipynb)
- [8.4 MAD Portfolio Optimization](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/08.04-MAD-Portfolio-Optimization.ipynb)
- [8.5 Real Options](http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/08.05-Real-Options.ipynb)