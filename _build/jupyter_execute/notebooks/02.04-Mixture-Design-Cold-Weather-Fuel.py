#!/usr/bin/env python
# coding: utf-8

# # Design of a Cold Weather Fuel for a Camping Stove

# ## Imports

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import numpy as np
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


# ## Problem statement
# 
# The venerable alcohol stove has been invaluable camping accessory for generations. They are simple, reliable, and in a pinch, can be made from aluminum soda cans. 
# 
# ![alcohol-stove.jpeg](https://github.com/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/figures/alcohol-stove.jpeg?raw=1)
# 
# Alcohol stoves are typically fueled with denatured alcohol. Denatured alcohol, sometimes called methylated spirits, is a generally a mixture of ethanol and other alcohols and compounds designed to make it unfit for human consumption. An MSDS description of one [manufacturer's product](https://www.korellis.com/wordpress/wp-content/uploads/2016/05/Alcohol-Denatured.pdf) describes a roughly fifity/fifty mixture of ethanol and methanol.
# 
# The problem with alcohol stoves is they can be difficult to light in below freezing weather. The purpose of this notebook is to design of an alternative cold weather fuel that could be mixed from other materials commonly available from hardware or home improvement stores.

# ## Vapor pressure data
# 
# The following data was collected for potential fuels commonly available at hardware and home improvement stores. The data consists of price (\$/gal.) and parameters to predict vapor pressure using the Antoine equation,
# 
# $$
# \begin{align}
# \log_{10}P^{vap}_{s}(T) & = A_s - \frac{B_s}{T + C_s}
# \end{align}
# $$
# 
# where the subscript $s$ refers to species, temperature $T$ is in units of degrees Celcius, and pressure $P$ is in units of mmHg. The additional information for molecular weight and specific gravity will be needed to present the final results in volume fraction.

# In[2]:


data = {
    'ethanol'          : {'MW':  46.07, 'SG': 0.791, 'A': 8.04494, 'B': 1554.3,  'C': 222.65},
    'methanol'         : {'MW':  32.04, 'SG': 0.791, 'A': 7.89750, 'B': 1474.08, 'C': 229.13},
    'isopropyl alcohol': {'MW':  60.10, 'SG': 0.785, 'A': 8.11778, 'B': 1580.92, 'C': 219.61},
    'acetone'          : {'MW':  58.08, 'SG': 0.787, 'A': 7.02447, 'B': 1161.0,  'C': 224.0},
    'xylene'           : {'MW': 106.16, 'SG': 0.870, 'A': 6.99052, 'B': 1453.43, 'C': 215.31},
    'toluene'          : {'MW':  92.14, 'SG': 0.865, 'A': 6.95464, 'B': 1344.8,  'C': 219.48},
}


# The first step is to determine the vapor pressure of denatured alcohol over a typical range of operating temperatures. For this we assume denatured alcohol is a 40/60 (mole fraction) mixture of ethanol and methanol. 

# In[3]:


def Pvap(T, s):
    return 10**(data[s]['A'] - data[s]['B']/(T + data[s]['C']))

def Pvap_denatured(T):
    return 0.4*Pvap(T, 'ethanol') + 0.6*Pvap(T, 'methanol')

T = np.linspace(0, 40, 200)

plt.plot(T, Pvap_denatured(T))
plt.title('Vapor Pressure of denatured alcohol')
plt.xlabel('temperature / °C')
plt.ylabel('pressure / mmHg')
print("Vapor Pressure at 0C =", round(Pvap_denatured(0),1), "mmHg")
plt.grid(True)


# ## Cold weather product requirements
# 
# We seek a cold weather fuel with increased vapor pressure at 0°C and lower, and also provides safe and normal operation of the alcohol stove at higher operating temperatures. 
# 
# For this purpose, we seek a mixture of commonly available liquids with a vapor pressure of at least 22 mmHg at the lowest possible temperature, and no greater than the vapor pressure of denatured alcohol at temperatures 30°C and above.

# In[4]:


for s in data.keys():
    plt.plot(T, Pvap(T,s))
plt.plot(T, Pvap_denatured(T), 'k', lw=3)
plt.legend(list(data.keys()) + ['denatured alcohol'])
plt.title('Vapor Pressure of selected compounds')
plt.xlabel('temperature / °C')
plt.ylabel('pressure / mmHg')
plt.grid(True)


# ## Optimization model
# 
# The first optimization model is to create a mixture that maximizes the vapor pressure at -10°C while having a vapor pressure less than or equal to denatured alcohol at 30°C and above. 
# 
# The decision variables in the optimization model correspond to $x_s$, the mole fraction of each species $s \in S$ from the set of available species $S$. By definition, the mole fractions must satisfy
# 
# $$
# \begin{align}
# x_s & \geq 0 & \forall s\in S \\
# \sum_{s\in S} x_s & = 1
# \end{align}
# $$
# 
# The objective is to maximize the vapor pressure at low temperatures, say -10°C, while maintaing a vapor pressure less than or equal to denatured alcohol at 30°C. Using Raoult's law for ideal mixtures,
# 
# $$
# \begin{align}
# \max_{x_s} \sum_{s\in S} x_s P^{vap}_s(-10°C) \\
# \end{align}
# $$
# subject to
# $$
# \begin{align}
# \sum_{s\in S} x_s P^{vap}_s(30°C) & \leq P^{vap}_{denatured\ alcohol}(30°C) \\
# \end{align}
# $$

# ## Pyomo implementation and solution
# 
# This optimization model is implemented in Pyomo in the following cell.

# In[5]:


m = pyomo.ConcreteModel()

S = data.keys()
m.x = pyomo.Var(S, domain=pyomo.NonNegativeReals)

def Pmix(T):
    return sum(m.x[s]*Pvap(T,s) for s in S)

m.obj = pyomo.Objective(expr = Pmix(-10), sense=pyomo.maximize)

m.cons = pyomo.ConstraintList()

m.cons.add(sum(m.x[s] for s in S)==1)
m.cons.add(Pmix(30) <= Pvap_denatured(30))
m.cons.add(Pmix(40) <= Pvap_denatured(40))

solver = pyomo.SolverFactory('cbc')
solver.solve(m)

print("Vapor Pressure at -10°C =", m.obj(), "mmHg")

T = np.linspace(-10,40,200)
plt.plot(T, Pvap_denatured(T), 'k', lw=3)
plt.plot(T, [Pmix(T)() for T in T], 'r', lw=3)
plt.legend(['denatured alcohol'] + ['cold weather blend'])
plt.title('Vapor Pressure of selected compounds')
plt.xlabel('temperature / °C')
plt.ylabel('pressure / mmHg')
plt.grid(True)


# The Pandas library is useful for summarizing the solution in tabular form.

# In[6]:


s = data.keys()
results = pd.DataFrame.from_dict(data).T
for s in S:
    results.loc[s,'mole fraction'] = m.x[s]()
    
MW = sum(m.x[s]()*data[s]['MW'] for s in S)
for s in S:
    results.loc[s,'mass fraction'] = m.x[s]()*data[s]['MW']/MW
    
vol = sum(m.x[s]()*data[s]['MW']/data[s]['SG'] for s in S)
for s in S:
    results.loc[s,'vol fraction'] = m.x[s]()*data[s]['MW']/data[s]['SG']/vol

results


# In[ ]:




