#!/usr/bin/env python
# coding: utf-8

# # Running Pyomo on Google Colab

# This note notebook shows how to install the basic pyomo package on Google Colab, and then demonstrates the subsequent installation and use of various solvers including
# 
# * GLPK
# * COIN-OR CBC
# * COIN-OR Ipopt
# * COIN-OR Bonmin
# * COIN-OR Couenne
# 
# **Note: This notebook has been updated to use solvers associated with the ID

# ## Basic installation of Pyomo
# 
# We'll do a quiet installation of pyomo using `pip`.  This needs to be done once at the start of each Colab session.

# In[5]:


get_ipython().run_cell_magic('capture', '', "import sys\nimport os\n\nif 'google.colab' in sys.modules:\n    !pip install idaes-pse --pre\n    !idaes get-extensions\n    os.environ['PATH'] += '/root/.idaes/bin'")


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


# ## GLPK installation
# 
# Keywords: GLPK
# 
# [GLPK](https://en.wikibooks.org/wiki/GLPK) is a the open-source **G**NU **L**inear **P**rogramming **K**it available for use under the GNU General Public License 3. GLPK is a single-threaded simplex solver generally suited to small to medium scale linear-integer programming problems. It is written in C with minimal dependencies and is therefore highly portable among computers and operating systems. GLPK is often 'good enough' for many examples. For larger problems users should consider higher-performance solvers, such as COIN-OR CBC, that can take advantage of multi-threaded processors.

# In[5]:


SolverFactory('glpk', executable='/usr/bin/glpsol').solve(model).write()

# display solution
print('\nProfit = ', model.profit())

print('\nDecision Variables')
print('x = ', model.x())
print('y = ', model.y())

print('\nConstraints')
print('Demand  = ', model.demand())
print('Labor A = ', model.laborA())
print('Labor B = ', model.laborB())


# ## COIN-OR CBC installation
# 
# Keywords: cbc installation
# 
# [COIN-OR CBC](https://github.com/coin-or/Cbc) is a multi-threaded open-source **C**oin-or **b**ranch and **c**ut mixed-integer linear programming solver written in C++ under the Eclipse Public License (EPL). CBC is generally a good choice for a general purpose MILP solver for medium to large scale problems.

# In[7]:


SolverFactory('cbc', executable='/usr/bin/cbc').solve(model).write()

# display solution
print('\nProfit = ', model.profit())

print('\nDecision Variables')
print('x = ', model.x())
print('y = ', model.y())

print('\nConstraints')
print('Demand  = ', model.demand())
print('Labor A = ', model.laborA())
print('Labor B = ', model.laborB())


# ## COIN-OR Ipopt installation
# 
# Keywords: Ipopt installation
# 
# [COIN-OR Ipopt](https://github.com/coin-or/Ipopt) is an open-source **I**nterior **P**oint **Opt**imizer for large-scale nonlinear optimization available under the Eclipse Public License (EPL). It is well-suited to solving nonlinear programming problems without integer or binary constraints.

# In[9]:


SolverFactory('ipopt', executable='/content/ipopt').solve(model).write()

# display solution
print('\nProfit = ', model.profit())

print('\nDecision Variables')
print('x = ', model.x())
print('y = ', model.y())

print('\nConstraints')
print('Demand  = ', model.demand())
print('Labor A = ', model.laborA())
print('Labor B = ', model.laborB())


# ## COIN-OR Bonmin installation
# 
# [COIN-OR Bonmin](https://www.coin-or.org/Bonmin/Intro.html) is a **b**asic **o**pen-source solver for **n**onlinear **m**ixed-**in**teger programming problems (MINLP). It utilizes CBC and Ipopt for solving relaxed subproblems.

# In[11]:


SolverFactory('bonmin', executable='/content/bonmin').solve(model).write()

# display solution
print('\nProfit = ', model.profit())

print('\nDecision Variables')
print('x = ', model.x())
print('y = ', model.y())

print('\nConstraints')
print('Demand  = ', model.demand())
print('Labor A = ', model.laborA())
print('Labor B = ', model.laborB())


# ## COIN-OR Couenne installation
# 
# [COIN-OR Couenne](https://www.coin-or.org/Couenne/)  is attempts to find global optima for mixed-integer nonlinear programming problems (MINLP).

# In[ ]:


get_ipython().system('wget -N -q "https://ampl.com/dl/open/couenne/couenne-linux64.zip"')
get_ipython().system('unzip -o -q couenne-linux64')


# In[13]:


SolverFactory('couenne', executable='/content/couenne').solve(model).write()

# display solution
print('\nProfit = ', model.profit())

print('\nDecision Variables')
print('x = ', model.x())
print('y = ', model.y())

print('\nConstraints')
print('Demand  = ', model.demand())
print('Labor A = ', model.laborA())
print('Labor B = ', model.laborB())


# In[ ]:




