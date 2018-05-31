# Welcome to Notre Dame PyomoFest!

We are delighted to be hosting [PyomoFest at Notre Dame on June 5-7](ND-Pyomo-Workshop-Agenda.pdf). Thanks to gracious support from the Notre Dame Center for Research Computing and Sandia National Laboratory at Albequerque, this unique event will bring together campus researchers from a wide range of disciplines to a build an exciting new community of Pyomo users.

PyomoFest will include a mixture of presentations, hands-on sessions, and opportunities to consult with instructors on model development relevant to your own research. To make the best use of these opportunities, we urge PyomoFest participants to take several actions in preparation for the event.  These include:

1. Download and install a Pyomo/Python development environment that you can use at the workshop.  The **Getting Started** guides below provide instructions on how to install Python, Pyomo, and a basic set of solvers. 

2. Review basic conceptual frameworks for optimization modeling. The notebooks in this repository include examples of linear programming (LP), mixed-integer linear programming (MILP), nonlinear programming (NLP), and more. 

3. A goal of PyomoFest is to help new users apply Pyomo to their research. We encourage you to bring a research relevant application problem with you to the workshop. Unique data sets could arranged as simple spreadsheet.csv files, for example, and literature models could be summarized in some mathematical form.

4. A pre-workshop session will be held at 10-12am on Friday, June 1, in Room 116 DeBartolo Hall. The first hour provide a brief high-level overview of basic optimization concepts. During the second hour, we will offer help getting your laptop or a research problem ready for the workshop.

## What to Bring to PyomoFest

1. (Required) A laptop computer with Python, Pyomo, and a few solvers installed. See **Getting Started** for more information. Don't forget your power cord!

2. (Recommended) A simple optimization problem that is relavent to your research. This may come from literature or be adapted from the Pyomo examples (see below for some informaton).

Need help either installing Pyomo or identifying a getting started problem? Please take advantage of these opportunities:
* 10 AM - 12 PM on Friday, June 1 in Room 116 DeBartolo Hall. Pre-workshop tutorial and one-on-one help.
* 10 AM - 12 PM on Monday, June 4 in Room 182 Fitzpatrick Hall. One-on-one help.
* Setup an appointment with Prof. Alex Dowling (adowling at nd.edu) or Prof. Jeff Kantor (kantor.1 at nd.edu) for advice on identifying a getting started problem.
* Setup an appointment with Jacob Gerace (jgerace at nd.edu) for help installing software.

## PyomoFest Agenda and Location

[Printable agenda with supplemental Pyomo installation instructions](ND-Pyomo-Workshop-Agenda.pdf)

### Day 1 - Tuesday, June 5

B01 McCourtney Hall (entire day)

8:30 AM - 12:00 PM
* Python Tutorial
* Pyomo Fundamentals & Overview
* Introductory Excercises


12:00 PM - 1:00 PM
* Lunch Break


1:00 PM - 4:30 PM
* Introduction to Mixed Integer Programming (MIP) Algorithms
* MIP Excercises
* Pyomo Cookbooks by Prof. Kantor


### Day 2 - Wednesday, June 6

B01 McCourtney Hall (entire day)

8:30 AM - 12:00 PM
* Nonlinear Programming (NLP) Algorithms
* Introduction to IPOPT
* NLP Excercises
* Structured Modeling and Pyomo Blocks
* Transformations


12:00 PM - 1:00 PM
* Lunch Break


1:00 PM - 4:30 PM
* Pyomo.DAE: Dynamic Optimization
* Pyomo.GDP: Sequencing and Switching
* Other Advanced Capabilities of Pyomo

### Day 3 - Thursday, June 7

B01 McCourtney Hall (morning)

8:30 AM - 12:00 PM
* Pyomo.PySP: Stochastic Programming


W210 Duncan Student Center (lunch and afternoon)

12:00 PM - 1:00 PM
* Lunch Break


1:00 PM - 4:30 PM
* Collaboration Time

## Getting Started with Pyomo

[Pyomo](http://www.pyomo.org/) is a state-of-the-art package for modeling and solving optimization problems embedded within Python. Using Pyomo, complex models are described by specifying an optimization **objective**, one or more sets of decision **variables**, and collections of linear, nonlinear, discrete, and dynamical **constraints**. Pyomo includes a rich set of features to enable high-level modeling of complex systems, specifying solvers, and using Python to display the solution.

* [Installing Pyomo](notebooks/intro/Installing_Pyomo.ipynb)
* [Pyomo Basics](notebooks/intro/Pyomo_Basics.ipynb)
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

## Finance

* [Binomial Model for Pricing Options](notebooks/finance/Binomial_Model_for_Pricing_Options.ipynb)
* [Historical Stock Data](notebooks/finance/Historical_Stock_Data.ipynb)
* [Charting Stock Data](notebooks/finance/Charting_Stock_Data.ipynb)
* [MAD Portfolio Optimization](notebooks/finance/MAD_Portfolio_Optimization.ipynb)
* [Real Options](notebooks/finance/Real_Options.ipynb)
