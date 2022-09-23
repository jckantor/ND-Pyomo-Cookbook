#!/usr/bin/env python
# coding: utf-8

# # Introduction to Disjunctive Programming

# ## Installations and imports

# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

import shutil
import sys
import os.path

if not shutil.which("pyomo"):
    get_ipython().system('pip install -q pyomo')
    assert(shutil.which("pyomo"))

if not (shutil.which("cbc") or os.path.isfile("cbc")):
    if "google.colab" in sys.modules:
        get_ipython().system('apt-get install -y -qq coinor-cbc')
    else:
        try:
            get_ipython().system('conda install -c conda-forge coincbc ')
        except:
            pass

assert(shutil.which("cbc") or os.path.isfile("cbc"))
from pyomo.environ import *
from pyomo.gdp import *
import pandas as pd


# ## Problem statement

# ### Component data

# In[4]:


# load data as dictionary of components
# component data consists of cost and composition 
comp_data = {
    "A": {"cost": 2.0, "Vit A": 0.5, "Vit B": 0.2},
    "B": {"cost": 2.0, "Vit A": 0.4, "Vit B": 0.1},
    "C": {"cost": 5.0, "Vit A": 0.3, "Vit B": 0.3},
}

# use pandas to create a nice display
pd.DataFrame.from_dict(comp_data, orient='index')


# ### Product Composition Requirements
# 
# Find the lowest cost blend
# 
# * Vit A: less than 0.4
# * Vit B: greater than 0.2
# 
# Your code should be able to accept alternative specification for data and product requirements.
# 

# In[5]:


prod_req = {
    "Vit A": {"lb": 0.0, "ub": 0.4},
    "Vit B": {"lb": 0.2, "ub": 1.0},
}
pd.DataFrame.from_dict(prod_req, orient='index')


# ### Component Compatibility
# 
# For this application, we consider an additional type of constraint specifying the incompatability of certain blends of components. For example, suppose we have a constraint:
# 
# * A and B cannot be mixed together in the final product
# 
# The constraint is specified by creating a list of incompatabile pairs.

# In[6]:


excl_pairs = [("A", "B")]


# ## Version 0: Neglecting the compatibility requirments

# In[7]:


m = ConcreteModel()

# define sets that will be used to index decision variables and constraints
# remember to use initialize keyword
m.comp = Set(initialize=comp_data.keys())
m.req = Set(initialize=prod_req.keys())

# decision variables
m.x = Var(m.comp, domain=NonNegativeReals)

# objective function
m.cost = Objective(expr=sum(m.x[c]*comp_data[c]["cost"] for c in m.comp), sense=minimize)

# structural constraints
m.massfraction = Constraint(expr=sum(m.x[c] for c in m.comp)==1)

# composition constraints
m.lb = Constraint(m.req, rule=lambda m, r: sum(m.x[c]*comp_data[c][r] for c in m.comp) >= prod_req[r]["lb"])
m.ub = Constraint(m.req, rule=lambda m, r: sum(m.x[c]*comp_data[c][r] for c in m.comp) <= prod_req[r]["ub"])

solver = SolverFactory('cbc')
solver.solve(m)

for c in m.comp:
    print(f"{c} = {m.x[c]()}")


# ## Version 1: Including compatibility requirements with Big-M
# 
# The challenge of this problem are the disjunctive constraints associated with the component incompatability data. Here we associated a boolean variable for each pair, then use the boolean variable to determine which member of the pair to keep in the blend.

# In[8]:


m = ConcreteModel()

# define sets that will be used to index decision variables and constraints
# remember to use initialize keyword
m.comp = Set(initialize=comp_data.keys())
m.req = Set(initialize=prod_req.keys())

# define a set to that includes the excluded pairs
m.pairs = Set(initialize=excl_pairs)

# decision variables
m.x = Var(m.comp, domain=NonNegativeReals)

# for each excluded pair, create a boolean variable. The value of the boolean
# variable will determine which member of the pair is allowed in the product
m.y = Var(m.pairs, domain=Boolean)

# objective function
m.cost = Objective(expr=sum(m.x[c]*comp_data[c]["cost"] for c in m.comp), sense=minimize)

# structural constraints
m.massfraction = Constraint(expr=sum(m.x[c] for c in m.comp)==1)

# composition constraints
m.lb = Constraint(m.req, rule=lambda m, r: sum(m.x[c]*comp_data[c][r] for c in m.comp) >= prod_req[r]["lb"])
m.ub = Constraint(m.req, rule=lambda m, r: sum(m.x[c]*comp_data[c][r] for c in m.comp) <= prod_req[r]["ub"])

# component incompatability constraints
M = 100
m.disj = ConstraintList()
for pair in m.pairs:
    a, b = pair
    m.disj.add(m.x[a] <= M*m.y[pair])
    m.disj.add(m.x[b] <= M*(1-m.y[pair]))

solver = SolverFactory('cbc')
solver.solve(m)

for c in m.comp:
    print(f"{c} = {m.x[c]()}")


# ## Version 2. Disjunctive Constraints

# In[9]:


m = ConcreteModel()

# define sets that will be used to index decision variables and constraints
# remember to use initialize keyword
m.comp = Set(initialize=comp_data.keys())
m.req = Set(initialize=prod_req.keys())

# define a set to that includes the excluded pairs
m.pairs = Set(initialize=excl_pairs)

# decision variables
m.x = Var(m.comp, domain=NonNegativeReals, bounds=(0, 1))

# objective function
m.cost = Objective(expr=sum(m.x[c]*comp_data[c]["cost"] for c in m.comp), sense=minimize)

# structural constraints
m.massfraction = Constraint(expr=sum(m.x[c] for c in m.comp)==1)

# composition constraints
m.lb = Constraint(m.req, rule=lambda m, r: sum(m.x[c]*comp_data[c][r] for c in m.comp) >= prod_req[r]["lb"])
m.ub = Constraint(m.req, rule=lambda m, r: sum(m.x[c]*comp_data[c][r] for c in m.comp) <= prod_req[r]["ub"])

# component incompatability constraints
m.disj = Disjunction(m.pairs, rule=lambda m, a, b: [m.x[a] == 0, m.x[b] == 0])

# apply transformations
TransformationFactory('gdp.hull').apply_to(m)

# solve
solver = SolverFactory('cbc')
solver.solve(m)

for c in m.comp:
    print(f"{c} = {m.x[c]()}")


# ## Analysis 

# In[10]:


comp_data = {
    "A": {"cost": 2.0, "Vit A": 0.5, "Vit B": 0.2},
    "B": {"cost": 2.0, "Vit A": 0.4, "Vit B": 0.1},
    "C": {"cost": 4.0, "Vit A": 0.3, "Vit B": 0.3},
}

prod_req = {
    "Vit A": {"lb": 0.0, "ub": 0.4},
    "Vit B": {"lb": 0.2, "ub": 1.0},
}

excl_pairs = [("A", "B")]


# $$
# \begin{align*}
# x_A + x_B + x_C & = 1 \\
# 0.5 x_A + 0.4 x_B + 0.3 x_C & \leq 0.4 \\
# 0.2 x_A + 0.1 x_B + 0.3 x_C & \geq 0.2 \\
# \end{align*}
# $$
# 
# Solving for x_C
# 
# $$
# \begin{align*}
# x_C & = 1 - x_A - x_B
# \end{align*}
# $$
# 
# Substitution
# 
# $$
# \begin{align*}
# 0.2 x_A + 0.1 x_B & \leq 0.1 \\
# -0.1 x_A - 0.2 x_B & \geq -0.1 \\
# \end{align*}
# $$

# In[11]:


TransformationFactory


# In[ ]:




