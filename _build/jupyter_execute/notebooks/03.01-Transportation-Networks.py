#!/usr/bin/env python
# coding: utf-8

# # Transportation Networks
# 
# Keywords: transportation, assignment, cbc usage
# 
# This notebook demonstrates the solution of transportation network problems using Pyomo and GLPK. The problem description and data are adapted from Chapter 5 of Johannes Bisschop, ["AIMMS Optimization Modeling", AIMMS B. V., 2014](http://download.aimms.com/aimms/download/manuals/AIMMS3_OM.pdf).
# 

# ## Imports

# In[1]:


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


# ## Background
# 
# The prototypical transportation problem deals with the distribution of a commodity from a set of sources to a set of destinations. The object is to minimize total transportation costs while satisfying constraints on the supplies available at each of the sources, and satisfying demand requirements at each of the destinations.
# 
# Here we illustrate the transportation problem using an example from Chapter 5 of Johannes Bisschop, "AIMMS Optimization Modeling", Paragon Decision Sciences, 1999. In this example there are two factories and six customer sites located in 8 European cities as shown in the following map. The customer sites are labeled in red, the factories are labeled in blue.

# ![TransportationNetworksMap.png](https://github.com/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/figures/TransportationNetworksMap.png?raw=1)

# Transportation costs between sources and destinations are given in units of &euro;/ton of goods shipped, and list in the following table along with source capacity and demand requirements.
# 

# ### Table of transportation costs, customer demand, and available supplies
# 
# | Customer\Source | Arnhem [&euro;/ton] | Gouda [&euro;/ton] | Demand [tons]|
# | :--: | :----: | :---: | :----: |
# | London | n/a | 2.5 | 125 |
# | Berlin | 2.5 | n/a | 175 |
# | Maastricht | 1.6 | 2.0 | 225 |
# | Amsterdam | 1.4 | 1.0 | 250 |
# | Utrecht | 0.8 | 1.0 | 225 |
# | The Hague | 1.4 | 0.8 | 200 |
# | **Supply [tons]** | 550 tons | 700 tons |  |
# 
# The situation can be modeled by links connecting a set nodes representing sources to a set of nodes representing customers.
# 
# ![TransportNet.png](https://github.com/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/figures/TransportNet.png?raw=1)
# 
# For each link we can have a parameter $T[c,s]$ denoting the cost of shipping a ton of goods over the link. What we need to determine is the amount of goods to be shipped over each link, which we will represent as a non-negative decision variable $x[c,s]$.
# 
# The problem objective is to minimize the total shipping cost to all customers from all sources. 
# 
# $$\mbox{minimize:}\quad \mbox{Cost} = \sum_{c \in Customers}\sum_{s \in Sources} T[c,s] x[c,s]$$
# 
# Shipments from all sources can not exceed the manufacturing capacity of the source.
# 
# $$\sum_{c \in Customers} x[c,s] \leq \mbox{Supply}[s] \qquad \forall s \in Sources$$
# 
# Shipments to each customer must satisfy their demand.
# 
# $$\sum_{s\in Sources} x[c,s] = \mbox{Demand}[c] \qquad \forall c \in Customers$$

# ## Pyomo model

# ### Data File

# In[2]:


Demand = {
   'Lon':   125,        # London
   'Ber':   175,        # Berlin
   'Maa':   225,        # Maastricht
   'Ams':   250,        # Amsterdam
   'Utr':   225,        # Utrecht
   'Hag':   200         # The Hague
}

Supply = {
   'Arn':   600,        # Arnhem
   'Gou':   650         # Gouda
}

T = {
    ('Lon','Arn'): 1000,
    ('Lon','Gou'): 2.5,
    ('Ber','Arn'): 2.5,
    ('Ber','Gou'): 1000,
    ('Maa','Arn'): 1.6,
    ('Maa','Gou'): 2.0,
    ('Ams','Arn'): 1.4,
    ('Ams','Gou'): 1.0,
    ('Utr','Arn'): 0.8,
    ('Utr','Gou'): 1.0,
    ('Hag','Arn'): 1.4,
    ('Hag','Gou'): 0.8
}


# ### Model file

# In[3]:


# Step 0: Create an instance of the model
model = ConcreteModel()
model.dual = Suffix(direction=Suffix.IMPORT)

# Step 1: Define index sets
CUS = list(Demand.keys())
SRC = list(Supply.keys())

# Step 2: Define the decision 
model.x = Var(CUS, SRC, domain = NonNegativeReals)

# Step 3: Define Objective
model.Cost = Objective(
    expr = sum([T[c,s]*model.x[c,s] for c in CUS for s in SRC]),
    sense = minimize)

# Step 4: Constraints
model.src = ConstraintList()
for s in SRC:
    model.src.add(sum([model.x[c,s] for c in CUS]) <= Supply[s])
        
model.dmd = ConstraintList()
for c in CUS:
    model.dmd.add(sum([model.x[c,s] for s in SRC]) == Demand[c])
    
results = SolverFactory('cbc').solve(model)
results.write()


# ## Solution

# In[4]:


for c in CUS:
    for s in SRC:
        print(c, s, model.x[c,s]())


# In[5]:


if 'ok' == str(results.Solver.status):
    print("Total Shipping Costs = ",model.Cost())
    print("\nShipping Table:")
    for s in SRC:
        for c in CUS:
            if model.x[c,s]() > 0:
                print("Ship from ", s," to ", c, ":", model.x[c,s]())
else:
    print("No Valid Solution Found")


# The solution has the interesting property that, with the exception of Utrecht, customers are served by just one source.
# 
# ![TransportNet_soln.png](https://github.com/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/figures/TransportNet_soln.png?raw=1)
# 

# ## Sensitivity analysis

# ### Analysis by source

# In[6]:


if 'ok' == str(results.Solver.status):
    print("\nSources:")
    print("Source      Capacity   Shipped    Margin")
    for m in model.src.keys():
        s = SRC[m-1]
        print("{0:10s}{1:10.1f}{2:10.1f}{3:10.4f}".format(s,Supply[s],model.src[m](),model.dual[model.src[m]]))
else:
    print("No Valid Solution Found")


# The 'marginal' values are telling us how much the total costs will be increased for each one ton increase in the available supply from each source. The optimization calculation says that only 650 tons of the 700 available from Gouda should used for a minimum cost solution, which rules out any further cost reductions by increasing the available supply. In fact, we could decrease the supply Gouda without any harm. The marginal value of Gouda is 0.
# 
# The source at Arnhem is a different matter. First, all 550 available tons are being used. Second, from the marginal value we see that the total transportations costs would be reduced by 0.2 Euros for each additional ton of supply.  
# 
# The management conclusion we can draw is that there is excess supply available at Gouda which should, if feasible, me moved to Arnhem.
# 
# Now that's a valuable piece of information!

# ### Analysis by customer

# In[7]:


if 'ok' == str(results.Solver.status):    
    print("\nCustomers:")
    print("Customer      Demand   Shipped    Margin")
    for n in model.dmd.keys():
        c = CUS[n-1]
        print("{0:10s}{1:10.1f}{2:10.1f}{3:10.4f}".format(c,Demand[c],model.dmd[n](),model.dual[model.dmd[n]]))
else:
    print("No Valid Solution Found")


# Looking at the demand constraints, we see that all of the required demands have been met by the optimal solution.
# 
# The marginal values of these constraints indicate how much the total transportation costs will increase if there is an additional ton of demand at any of the locations. In particular, note that increasing the demand at Berlin will increase costs by 2.7 Euros per ton. This is actually **greater** than the list price for shipping to Berlin which is 2.5 Euros per ton.  Why is this?
# 
# To see what's going on, let's resolve the problem with a one ton increase in the demand at Berlin.
# 
# We see the total cost has increased from 1715.0 to 1717.7 Euros, an increase of 2.7 Euros just as predicted by the marginal value assocated with the demand constraint for Berlin.
# 
# Now let's look at the solution.
# 
# Here we see that increasing the demand in Berlin resulted in a number of other changes. This figure shows the changes shipments.
# 
# ![TransportNet_sens.png](https://github.com/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/figures/TransportNet_sens.png?raw=1)
# 
# * Shipments to Berlin increased from 175 to 176 tons, increasing costs for that link from 437.5 to 440.0, or a net increase of 2.5 Euros.
# * Since Arnhem is operating at full capacity, increasing the shipments from Arnhem to Berlin resulted in decreasing the shipments from Arhhem to Utrecht from 150 to 149 reducing those shipping costs from 120.0 to 119.2, a net decrease of 0.8 Euros.
# * To meet demand at Utrecht, shipments from Gouda to Utrecht had to increase from 75 to 76, increasing shipping costs by a net amount of 1.0 Euros.
# * The net effect on shipping costs is 2.5 - 0.8 + 1.0 = 2.7 Euros.
# 
# The important conclusion to draw is that when operating under optimal conditions, a change in demand or supply can have a ripple effect on the optimal solution that can only be measured through a proper sensitivity analysis.

# ## Exercises
# 
# 1. Move 50 tons of supply capacity from Gouda to Arnhem, and repeat the sensitivity analysis. How has the situation improved?  In practice, would you recommend this change, or would you propose something different?
# 2. What other business improvements would you recommend?

# In[ ]:




