
# ND Pyomo Cookbook

**ND Pyomo Cookbook** is a collection of notebooks showing the use [Pyomo](http://www.pyomo.org/) to solve
modeling and optimization problems. With Pyomo, one can embed within Python an optimization model consisting of
**decision variables**, **constraints**, and an optimization **objective**. Pyomo includes a rich set of features enables the modeling and analysis of complex systems.

The notebooks in this collection were developed for instructional purposes at Notre Dame. Originally
developed using the [Anaconda distribution of Python](https://www.anaconda.com/download/), the notebooks have been
updated to open directly [Google Colaboratory](https://colab.research.google.com/) where they can be run using
only a browser window. 

This collection was originally developed as a followup to PyomoFest at Notre Dame that was held June 5-7, 2018. Notes distributed at the event are included in this repository:
[agenda](https://github.com/jckantor/ND-Pyomo-Cookbook/tree/master/PyomoFest/PyomoFest.md),
[slides](https://github.com/jckantor/ND-Pyomo-Cookbook/tree/master/PyomoFest/slides) and
[exercises](https://github.com/jckantor/ND-Pyomo-Cookbook/tree/master/PyomoFest/exercises_wo_soln/exercises)

**September, 2022 Update** This repository has been revised using [JupyterBook](https://jupyterbook.org/en/stable/intro.html). Some notebooks have been updated with more consistent use of Pyomo. Where appropriate, constraints, objectives, and expressions have been rewritten using the Pyomo decorator syntax. New notebooks include 5.4 Diffusion and Adsorption in Polymers.


## [1.0 Getting Started with Pyomo](notebooks/01.00-Getting-Started-with-Pyomo.ipynb)
- [1.1 Installing a Pyomo/Python Development Environment](notebooks/01.01-Installing-Pyomo.ipynb)
- [1.2 Running Pyomo on Google Colab](notebooks/01.02-Running-Pyomo-on-Google-Colab.ipynb)
- [1.3 Running Pyomo on the Notre Dame CRC Cluster](notebooks/01.03-Running-Pyomo-on-the-Notre-Dame-CRC-Cluster.ipynb)
- [1.4 Cross-Platform Installation of Pyomo and Solvers](notebooks/01.04-Cross-Platform-Installation-of-Pyomo-and-Solvers.ipynb)

## [2.0 Linear Programming](notebooks/02.00-Linear-Programming.ipynb)
- [2.1 Production Models with Linear Constraints](notebooks/02.01-Production-Models-with-Linear-Constraints.ipynb)
- [2.3 Production Model Sensitivity Analysis](notebooks/02.02-Production-Model-Sensitivity-Analysis.ipynb)
- [2.3 Linear Blending Problem](notebooks/02.03-Linear-Blending-Problem.ipynb)
- [2.4 Design of a Cold Weather Fuel for a Camping Stove](notebooks/02.04-Mixture-Design-Cold-Weather-Fuel.ipynb)
- [2.5 Gasoline Blending](notebooks/02.05-Gasoline-Blending.ipynb)
- [2.6 Model Predictive Control of a Double Integrator](notebooks/02.06-Model-Predictive-Control-of-a-Double-Integrator.ipynb)

## [3.0 Assignment Problems](notebooks/03.00-Assignment-Problems.ipynb)
- [3.1 Transportation Networks](notebooks/03.01-Transportation-Networks.ipynb)

## [4.0 Scheduling with Disjunctive Constraints](notebooks/04.00-Scheduling-with-Disjunctive-Constraints.ipynb)
- [4.1 Introduction to Disjunctive Programming](notebooks/04.01-Introduction_to_Disjunctive_Programming.ipynb)
- [4.2 Machine Bottleneck](notebooks/04.02-Machine-Bottleneck.ipynb)
- [4.3 Job Shop Scheduling](notebooks/04.03-Job-Shop-Scheduling.ipynb)
- [4.4 Maintenance Planning](notebooks/04.04-Maintenance-Planning.ipynb)
- [4.5 Scheduling Multipurpose Batch Processes using State-Task Networks](notebooks/04.05-Scheduling-Multipurpose-Batch-Processes-using-State-Task_Networks.ipynb)
- [4.6 Unit Commitment](notebooks/04.06-Unit-Commitment.ipynb)

## [5.0 Simulation](notebooks/05.00-Simulation.ipynb)
- [5.1 Response of a First Order System to Step and Square Wave Inputs](notebooks/05.01-Response-of-a-First-Order-System-to-Step-and-Square-Wave-Inputs.ipynb)
- [5.2 Exothermic CSTR](notebooks/05.02-Exothermic-CSTR.ipynb)
- [5.3 Transient Heat Conduction in Various Geometries](notebooks/05.03-Heat_Conduction_in_Various_Geometries.ipynb)
- [5.4 Diffusion with Adsorption in Polymers](notebooks/05.04-Diffusion_Adsorption_in_Polymers.ipynb)

## [6.0 Differential-Algebraic Equations](notebooks/06.00-Differential-Algebraic-Equations.ipynb)
- [6.1 Unconstrained Scalar Optimization](notebooks/06.01-Unconstrained-Scalar-Optimization.ipynb)
- [6.2 Maximizing Concentration of an Intermediate in a Batch Reactor](notebooks/06.02-Maximizing-Concentration-of-an-Intermediate-in-a-Batch-Reactor.ipynb)
- [6.3 Path Planning for a Simple Car](notebooks/06.03-Path-Planning-for-a-Simple-Car.ipynb)
- [6.4 Soft Landing Apollo 11 on the Moon](notebooks/06.04-Soft-Landing-Apollo-11-on-the-Moon.ipynb)

## [7.0 Parameter Estimation](notebooks/07.00-Parameter-Estimation.ipynb)
- [7.1 Parameter estimation](notebooks/07.01-Parameter-Estimation-Catalytic-Reactor.ipynb)

## [8.0 Financial Applications](notebooks/08.00-Financial-Applications.ipynb)
- [8.1 Obtaining Historical Stock Data](notebooks/08.01-Obtaining-Historical-Stock_-ata.ipynb)
- [8.2 Consolidating and Charting Stock Data](notebooks/08.02-Consolidating-and-Charting-Stock-Data.ipynb)
- [8.3 Binomial Model for Pricing Options](notebooks/08.03-Binomial-Model-for-Pricing-Options.ipynb)
- [8.4 MAD Portfolio Optimization](notebooks/08.04-MAD-Portfolio-Optimization.ipynb)
- [8.5 Real Options](notebooks/08.05-Real-Options.ipynb)

## [9.0 Style Guide](notebooks/09.00-pyomo-coding-guide.md)
- [9.1 Notebook Style Guide](notebooks/09.01-notebook-style-guide.ipynb)

## [10.0 Index](genindex.md)