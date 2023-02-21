#!/usr/bin/env python
# coding: utf-8

# # Running Pyomo on Google Colab

# Google Colab offers a web-based computational platform for Python and Jupyter notebooks, which can be accessed through a simple web browser. By using this service, users can avoid the burden of setting up and managing a complicated computing environment on their personal computers.
# 
# This notebook provides instructions on how to install the pyomo package and open-source solvers on Google Colab. The solvers that will be installed are:
# 
# | Solver | Description |
# | :-- | :-- |
# | GLPK | MILP |
# | [COIN-OR CLP](https://github.com/coin-or/Clp) | LP
# | [COIN-OR CBC](https://github.com/coin-or/Cbc) | MILP |
# | [COIN-OR Ipopt](https://github.com/coin-or/Ipopt) | NLP | |
# | [COIN-OR Bonmin](https://github.com/coin-or/Bonmin) | MINLP |
# | [COIN-OR Couenne](https://github.com/coin-or/Couenne) | Global MINLP |
# 
# Additionally, the notebook tests each solver using a small example problem.
# 
# **Note: This notebook has been updated to use pyomo and solvers associated with the [IDAES project](https://idaes.org/). As of this writing (Feb, 2023), IDAES is undergoing an update to Version 2.0. This notebook will be updated as needed to stay current with IDAES.**

# ## Installing Pyomo and Solvers
# 
# An installation of pyomo and solvers needs to be done once at the start of each Colab session. The following cell tests if it is being run on Google Colab and, if so, installs Pyomo and solvers from the IDAES proejct. The [cell magic](https://ipython.readthedocs.io/en/stable/interactive/magics.html#cellmagic-capture) `%%capture` captures the lengthy output from the installation scripts. See the documentation for [installing the IDAES PSE framework](https://idaes-pse.readthedocs.io/en/latest/tutorials/getting_started/index.html) for additional detail.

# In[1]:


get_ipython().run_cell_magic('capture', '', "import sys\nimport os\n\nif 'google.colab' in sys.modules:\n    !pip install idaes-pse --pre\n    !idaes get-extensions\n    !apt-get install -y -qq glpk-utils  \n    os.environ['PATH'] += ':/usr/bin:/root/.idaes/bin'")


# ## Test Model

# The installation of pyomo can be verified by entering a simple model. We'll use the model again in subsequent cells to demonstrate the installation and execution of various solvers.

# In[2]:


from pyomo.environ import *

# create a model
model = ConcreteModel()

# declare decision variables
model.x = Var(domain=NonNegativeReals)
model.y = Var(domain=NonNegativeReals)

# declare objective
model.profit = Objective(expr = 40*model.x + 30*model.y, sense=maximize)

# declare constraints
model.demand = Constraint(expr = model.x <= 40)
model.laborA = Constraint(expr = model.x + model.y <= 80)
model.laborB = Constraint(expr = 2*model.x + model.y <= 100)

model.pprint()

def display_solution(model):

    # display solution
    print('\nProfit = ', model.profit())

    print('\nDecision Variables')
    print('x = ', model.x.value)
    print('y = ', model.y())

    print('\nConstraints')
    print('Demand  = ', model.demand())
    print('Labor A = ', model.laborA())
    print('Labor B = ', model.laborB())


# ## GLPK
# 
# [GLPK](https://en.wikibooks.org/wiki/GLPK) is a the open-source **G**NU **L**inear **P**rogramming **K**it available for use under the GNU General Public License 3. GLPK is a single-threaded simplex solver generally suited to small to medium scale linear-integer programming problems. It is written in C with minimal dependencies and therefore is highly portable among computers and operating systems
# 
# GLPK is often 'good enough' for many examples. For larger problem, however, users should consider higher-performance solvers, such as COIN-OR CLP, that take advantage of multi-threaded processors.

# In[3]:


SolverFactory('glpk').solve(model, tee=True).write()

# display solution
print('\nProfit = ', model.profit())

print('\nDecision Variables')
print('x = ', model.x())
print('y = ', model.y())

print('\nConstraints')
print('Demand  = ', model.demand())
print('Labor A = ', model.laborA())
print('Labor B = ', model.laborB())


# ## COIN-OR Clp
# 
# [COIN-OR Clp](https://github.com/coin-or/Clp) is a multi-threaded open-source linear programming solver written in C++ and distributed under the Eclipse Public License (EPL). Clp is generally a good choice for linear programs that do not include any binary or integer variables. 

# In[4]:


SolverFactory('clp').solve(model, tee=True).write()

display_solution(model)


# ## COIN-OR Cbc
# 
# [COIN-OR CBC](https://github.com/coin-or/Cbc) is a multi-threaded open-source **C**oin-or **b**ranch and **c**ut mixed-integer linear programming solver written in C++ under the Eclipse Public License (EPL). CBC is generally a good choice for a general purpose MILP solver for medium to large scale problems.

# In[5]:


SolverFactory('cbc').solve(model, tee=True).write()

display_solution(model)


# ## COIN-OR Ipopt installation
# 
# [COIN-OR Ipopt](https://github.com/coin-or/Ipopt) is an open-source **I**nterior **P**oint **Opt**imizer for large-scale nonlinear optimization available under the Eclipse Public License (EPL). It is well-suited to solving nonlinear programming problems without integer or binary constraints.

# In[6]:


SolverFactory('ipopt').solve(model, tee=True).write()

display_solution(model)


# ## COIN-OR Bonmin installation
# 
# [COIN-OR Bonmin](https://www.coin-or.org/Bonmin/Intro.html) is a **b**asic **o**pen-source solver for **n**onlinear **m**ixed-**in**teger programming problems (MINLP). It utilizes CBC and Ipopt for solving relaxed subproblems.

# In[7]:


SolverFactory('bonmin').solve(model, tee=True).write()

display_solution(model)


# ## COIN-OR Couenne installation
# 
# [COIN-OR Couenne](https://www.coin-or.org/Couenne/)  is attempts to find global optima for mixed-integer nonlinear programming problems (MINLP).

# In[8]:


SolverFactory('couenne').solve(model, tee=True).write()

display_solution(model)


# In[8]:




