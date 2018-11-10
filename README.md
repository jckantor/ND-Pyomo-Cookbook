# ND-Pyomo-Cookbook

[Pyomo](http://www.pyomo.org/) is a state-of-the-art Python package for modeling and solving optimization problems. Using Pyomo, a user can embed an optimization model consisting of **decision variables**, **constraints**, and an optimization **objective** within Python. Pyomo includes a rich set of features to enable modeling of complex systems, specifying a solver, and accessing the solution.

This repository provides instructions on getting started with Pyomo, and a collection of Pyomo modeling examples that have been developed for instructional purposes at Notre Dame.

PyomoFest at Notre Dame was held June 5-7, 2018. This repository contains the [agenda](PyomoFest.md), [slides](PyomoFest/slides/) and [exercises](PyomoFest/exercises_wo_soln/exercises/) distributed during that event.

| 0. Getting Started |
| :--- | :--- |
| Getting Started with Pyomo | [![Open In Colab](images/badges/colab-badge.svg)](https://colab.research.google.com/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/intro/Getting_Started_with_Pyomo.ipynb) [![nbviewer](images/badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/intro/Getting_Started_with_Pyomo.ipynb) |

## Getting Started

* [Getting Started with Pyomo](notebooks/intro/Getting_Started_with_Pyomo.ipynb)
* [Running Pyomo on the CRC Cluster](docs/CRC.md)
* [Unconstrained Scalar Optimization](notebooks/intro/Unconstrained_Scalar_Optimization.ipynb)

## Linear Programming

* [Production Models with Linear Constraints](notebooks/lp/Production_Models_with_Linear_Constraints.ipynb)
* [Linear Blending Problems](notebooks/lp/Linear_Blending_Problem.ipynb)
* [Mixture Design for a Cold Weather Camping Fuel](notebooks/lp/Mixture_Design_Cold_Weather_Fuel.ipynb)
* [Simple Gasoline Blending Example](notebooks/lp/Gasoline_Blending.ipynb)

## Assignment Problems

* [Transportation Networks](notebooks/assignment/Transportation_Networks.ipynb)

## Scheduling Problems with Disjunctive Constraints

* [Machine Bottleneck](notebooks/scheduling/Machine_Bottleneck.ipynb)
* [Job Shop Scheduling](notebooks/scheduling/Job_Shop_Scheduling.ipynb)
* [Scheduling Multipurpose Batch Processes using State-Task Networks](notebooks/scheduling/Scheduling_Multipurpose_Batch_Processes_using_State-Task_Networks.ipynb)

## Simulation

* [Linear First Order System](notebooks/simulation/Linear_First_Order_System.ipynb)
* [Simulation of an Exothermic Stirred Tank Reactor](notebooks/simulation/Exothermic_CSTR.ipynb)
* [Heat Conduction in Various Geometries](notebooks/simulation/Heat_Conduction_in_Various_Geometries.ipynb)

## Differential Algebraic Equations

* [Maximizing Concentration of an Intermediate in a Batch Reactor](notebooks/dae/Maximizing_Concentration_of_an_Intermediate_in_a_Batch_Reactor.ipynb)
* [Path Planning for a Simple Car Model](notebooks/dae/Path_Planning_for_a_Simple_Car.ipynb)

## Parameter Estimation
* [Parameter Estimation for a Catalytic Reactor](notebooks/estimation/Parameter_Estimation_Catalytic_Reactor.ipynb)

## Finance

* [Binomial Model for Pricing Options](notebooks/finance/Binomial_Model_for_Pricing_Options.ipynb)
* [Historical Stock Data](notebooks/finance/Historical_Stock_Data.ipynb)
* [Charting Stock Data](notebooks/finance/Charting_Stock_Data.ipynb)
* [MAD Portfolio Optimization](notebooks/finance/MAD_Portfolio_Optimization.ipynb)
* [Real Options](notebooks/finance/Real_Options.ipynb)
