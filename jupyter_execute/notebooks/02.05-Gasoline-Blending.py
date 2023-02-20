#!/usr/bin/env python
# coding: utf-8

# # Gasoline Blending
# 
# Keywords: blending, cbc usage
# 
# The task is to determine the most profitable blend of gasoline products from given set of refinery streams.
# 
# ![CEP-refinery-diagram](https://github.com/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/figures/CEP-refinery-diagram.png?raw=1)
# 
# Source: Olsen, T. (2014, May). An Oil Refinery Walk-Through. _Chemical Engineering Progress, 34-40._ [pdf available here.](https://www.aiche.org/system/files/cep/20140534_1.pdf)

# ## Imports

# In[1]:


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

import pyomo.environ as pyomo


# ## Gasoline product specifications
# 
# The gasoline products include regular and premium gasoline. In addition to the current price, the specifications include
# 
# * **octane** the minimum road octane number.  Road octane is the computed as the average of the Research Octane Number (RON) and Motor Octane Number (MON).
# * **Reid Vapor Pressure** Upper and lower limits are specified for the Reid vapor pressure. The Reid vapor pressure is the absolute pressure exerted by the liquid at 100°F.
# * **benzene** the maximum volume percentage of benzene allowed in the final product. Benzene helps to increase octane rating, but is also a treacherous environmental contaminant.
# 

# In[2]:


products = {
    'Regular' : {'price': 2.75, 'octane': 87, 'RVPmin': 0.0, 'RVPmax': 15.0, 'benzene': 1.1},
    'Premium' : {'price': 2.85, 'octane': 91, 'RVPmin': 0.0, 'RVPmax': 15.0, 'benzene': 1.1},
}

print(pd.DataFrame.from_dict(products).T)


# ## Stream specifications
# 
# A typical refinery produces many intermediate streams that can be incorporated in a blended gasoline product. Here we provide data on seven streams that include:
# 
# * **Butane** n-butane is a C4 product stream produced from the light components of the crude being processed by the refinery. Butane is a highly volatile of gasoline.
# * **LSR** Light straight run naptha is a 90°F to 190°F cut from the crude distillation column primarily consisting of straight chain C5-C6 hydrocarbons.
# * **Isomerate** is the result of isomerizing LSR to produce branched molecules that results in higher octane number.
# * **Reformate** is result of catalytic reforming heavy straight run napthenes to produce a high octane blending component, as well by-product hydrogen used elsewhere in the refinery for hydro-treating.
# * **Reformate LB** is a is a low benzene variant of reformate.
# * **FCC Naphta** is the product of a fluidized catalytic cracking unit designed to produce gasoline blending components from long chain hydrocarbons present in the crude oil being processed by the refinery.
# * **Alkylate** The alkylation unit reacts iso-butane with low-molecular weight alkenes to produce a high octane blending component for gasoline.
# 
# The stream specifications include research octane and motor octane numbers for each blending component, the Reid vapor pressure, the benzene content, cost, and availability (in gallons per day). The road octane number is computed as the average of the RON and MON.

# In[3]:


streams = {
    'Butane'       : {'RON': 93.0, 'MON': 92.0, 'RVP': 54.0, 'benzene': 0.00, 'cost': 0.85, 'avail': 30000},
    'LSR'          : {'RON': 78.0, 'MON': 76.0, 'RVP': 11.2, 'benzene': 0.73, 'cost': 2.05, 'avail': 35000},
    'Isomerate'    : {'RON': 83.0, 'MON': 81.1, 'RVP': 13.5, 'benzene': 0.00, 'cost': 2.20, 'avail': 0},
    'Reformate'    : {'RON':100.0, 'MON': 88.2, 'RVP':  3.2, 'benzene': 1.85, 'cost': 2.80, 'avail': 60000},
    'Reformate LB' : {'RON': 93.7, 'MON': 84.0, 'RVP':  2.8, 'benzene': 0.12, 'cost': 2.75, 'avail': 0},
    'FCC Naphtha'  : {'RON': 92.1, 'MON': 77.1, 'RVP':  1.4, 'benzene': 1.06, 'cost': 2.60, 'avail': 70000},
    'Alkylate'     : {'RON': 97.3, 'MON': 95.9, 'RVP':  4.6, 'benzene': 0.00, 'cost': 2.75, 'avail': 40000},
}

# calculate road octane as (R+M)/2
for s in streams.keys():
    streams[s]['octane'] = (streams[s]['RON'] + streams[s]['MON'])/2
    
# display feed information
print(pd.DataFrame.from_dict(streams).T)


# ## Blending model
# 
# This simplified blending model assumes the product attributes can be computed as linear volume weighted averages of the component properties. Let the decision variable $x_{s,p} \geq 0$ be the volume, in gallons, of blending component $s \in S$ used in the final product $p \in P$.
# 
# The objective is maximize profit, which is the difference between product revenue and stream costs. 
# 
# $$
# \begin{align}
# \mbox{profit} & = \max_{x_{s,p}}\left( \sum_{p\in P} \mbox{Price}_p \sum_{s\in S} x_{s,p}
# - \sum_{s\in S} \mbox{Cost}_s \sum_{p\in P} x_{s,p}\right)
# \end{align}
# $$
# or
# $$
# \begin{align}
# \mbox{profit} & = \max_{x_{s,p}}\left( \sum_{p\in P}  \sum_{s\in S} x_{s,p}\mbox{Price}_p - \sum_{p\in P}  \sum_{s\in S} x_{s,p}\mbox{Cost}_s \right)
# \end{align}
# $$
# 
# The blending constraint for octane can be written as 
# 
# $$
# \begin{align}
# \frac{\sum_{s \in S} x_{s,p} \mbox{Octane}_s}{\sum_{s \in S} x_{s,p}} & \geq \mbox{Octane}_p & \forall p \in P
# \end{align}
# $$
# 
# where $\mbox{Octane}_s$ refers to the octane rating of stream $s$, whereas $\mbox{Octane}_p$ refers to the octane rating of product $p$. Multiplying through by the denominator, and consolidating terms gives
# 
# $$
# \begin{align}
# \sum_{s \in S} x_{s,p}\left(\mbox{Octane}_s - \mbox{Octane}_p\right) & \geq  0 & \forall p \in P
# \end{align}
# $$
# 
# The same assumptions and development apply to the benzene constraint
# 
# $$
# \begin{align}
# \sum_{s \in S} x_{s,p}\left(\mbox{Benzene}_s - \mbox{Benzene}_p\right) & \leq  0 & \forall p \in P
# \end{align}
# $$
# 
# Reid vapor pressure, however, follows a somewhat different mixing rule.  For the Reid vapor pressure we have
# 
# $$
# \begin{align}
# \sum_{s \in S} x_{s,p}\left(\mbox{RVP}_s^{1.25} - \mbox{RVP}_{min,p}^{1.25}\right) & \geq  0 & \forall p \in P \\
# \sum_{s \in S} x_{s,p}\left(\mbox{RVP}_s^{1.25} - \mbox{RVP}_{max,p}^{1.25}\right) & \leq  0 & \forall p \in P
# \end{align}
# $$

# ## Pyomo implementation
# 
# This model is implemented in the following cell.

# In[4]:


# create model
m = pyomo.ConcreteModel()

# create decision variables
S = streams.keys()
P = products.keys()
m.x = pyomo.Var(S,P, domain=pyomo.NonNegativeReals)
    
# objective
revenue = sum(sum(m.x[s,p]*products[p]['price'] for s in S) for p in P)
cost = sum(sum(m.x[s,p]*streams[s]['cost'] for s in S) for p in P)
m.profit = pyomo.Objective(expr = revenue - cost, sense=pyomo.maximize)

# constraints
m.cons = pyomo.ConstraintList()
for s in S:
    m.cons.add(sum(m.x[s,p] for p in P) <= streams[s]['avail'])
for p in P:
    m.cons.add(sum(m.x[s,p]*(streams[s]['octane'] -    products[p]['octane'])       for s in S) >= 0)
    m.cons.add(sum(m.x[s,p]*(streams[s]['RVP']**1.25 - products[p]['RVPmin']**1.25) for s in S) >= 0)
    m.cons.add(sum(m.x[s,p]*(streams[s]['RVP']**1.25 - products[p]['RVPmax']**1.25) for s in S) <= 0)
    m.cons.add(sum(m.x[s,p]*(streams[s]['benzene'] -   products[p]['benzene'])      for s in S) <= 0)

# solve
solver = pyomo.SolverFactory('cbc')
solver.solve(m)

# display results
vol = sum(m.x[s,p]() for s in S for p in P)
print("Total Volume =", round(vol, 1), "gallons.")
print("Total Profit =", round(m.profit(), 1), "dollars.")
print("Profit =", round(100*m.profit()/vol,1), "cents per gallon.")


# ## Displaying the solution

# ### by refinery stream

# In[5]:


stream_results = pd.DataFrame()
for s in S:
    for p in P:
        stream_results.loc[s,p] = round(m.x[s,p](), 1)
    stream_results.loc[s,'Total'] = round(sum(m.x[s,p]() for p in P), 1)
    stream_results.loc[s,'Available'] = streams[s]['avail']
    
stream_results['Unused (Slack)'] = stream_results['Available'] - stream_results['Total']
print(stream_results)


# ### by refinery product

# In[6]:


product_results = pd.DataFrame()
for p in P:
    product_results.loc[p,'Volume'] = round(sum(m.x[s,p]() for s in S), 1)
    product_results.loc[p,'octane'] = round(sum(m.x[s,p]()*streams[s]['octane'] for s in S)
                                            /product_results.loc[p,'Volume'], 1)
    product_results.loc[p,'RVP'] = round((sum(m.x[s,p]()*streams[s]['RVP']**1.25 for s in S)
                                            /product_results.loc[p,'Volume'])**0.8, 1)
    product_results.loc[p,'benzene'] = round(sum(m.x[s,p]()*streams[s]['benzene'] for s in S)
                                            /product_results.loc[p,'Volume'], 1)
print(product_results)


# ## Exercises

# ### 1. Expand product list with mid-grade gasoline
# 
# The marketing team says there is an opportunity to create a mid-grade gasoline product with a road octane number of 89 that would sell for $2.82/gallon, and with all other specifications the same. Could an additional profit be created?
# 
# Create a new cell (or cells) below to compute a solution to this exercise.

# In[ ]:





# ### 2. Impact of regulatory change
# 
# New environmental regulations have reduced the allowable benzene levels from 1.1 vol% to 0.62 vol%, and the maximum Reid vapor pressure from 15.0 to 9.0.
# 
# Compared to the base case (i.e., without the midgrade product), how does this change profitability? 

# In[ ]:





# ### 3. Impact of a change in refinery operations
# 
# Given the new product specifications in Exercise 2, let's consider using different refinery streams. In place of Reformate, the refinery could produce Reformate LB. (That is, one or the other of the two streams could be 60000 gallons per day, but not both).  Same for LSR and Isomerate.  How should the refinery be operated to maximize profitability?  (Hint: You will need to introduce at least two extra decision variables corresponding to the decisions to use the alternative processes.)

# In[ ]:





# ### Mini-Project: Transfer Pricing (Sensitivity Analysis)
# 
# The profitability of this refinery is determined by the amount of each blending stream that is available. It may be possible to purchase additional quantities of each stream in the market. Assume the pre-conditions of exercises 1, 2, and 3 are all in effect. Also assume that all seven streams could be available for purchase and blending even if they are not produced in the refinery. 
# 
# What is the maximum price you would be willing to pay for each of the seven streams?

# In[ ]:




