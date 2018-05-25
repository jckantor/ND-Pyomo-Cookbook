# Welcome to Notre Dame PyomoFest!

We are delighted to be hosting PyomoFest at Notre Dame on June 5-7. Thanks to the gracious support of the Notre Dame Center for Research Computing and Sandia National Laboratory at Albequerque, this unique event will bring together campus researchers from a wide range of disciplines to a build an exciting new community of Pyomo users.

PyomoFest will include a mixture of presentations, hands-on workshop sessions, and opportunities to consult with instructors in developing a model relevant to your own research. To make the most productive use of these opportunities, we urge PyomoFest participants to take several advance actions.  These include:

1. Download and install a Pyomo/Python development environment on the laptop you will bring to the workshop.  The **Getting Started** guides below provide instructions on how to install Python, Pyomo, and a basic set of solvers. 

2. Brush up on the basic conceptual frameworks for optimization modeling. The notebooks in this repository include examples of linear programming (LP), mixed-integer linear programming (MILP), nonlinear programming (NLP), and more. 

3. A key goal of PyomoFest is to help new users apply Pyomo to their own research. We encourage you to identify a potential application of signficance to your research, and bring this with you to the workshop. Data, for example, could be arranged and arranged in the form of simple spreadsheets (.csv files, for example), or literature models could be summarized in your research notes.

4. Professor Jeff Kantor will be offering a pre-workshop session on Friday, June 1, for those interested in a brief high-level overview of basic optimization concepts, or help solve problems you may with getting your laptop ready for the workshop. Details will be sent to registered participants.

## Getting Started with Pyomo

[Pyomo](http://www.pyomo.org/) is a state-of-the-art package for modeling and solving optimization problems embedded within Python. With Pyomo, a modeler can describe complex systems model by specifying an optimization **objective**, decision **variables**, and a rich array of linear, nonlinear, discrete, and dynamical **constraints**. Pyomo includes a rich set of features to enable high-level modeling of complex systems, specifying solvers, and using Python to display the solution.

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
