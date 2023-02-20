#!/usr/bin/env python
# coding: utf-8

# # Simulation
# 
# 
# Documention:
# 
# * [Dynamic Model Simulation](https://pyomo.readthedocs.io/en/stable/modeling_extensions/dae.html#dynamic-model-simulation)
# 
# Simulator Limitations:
# 
# * Differential equations must be first-order and separable
# * Model can only contain a single ContinuousSet
# * Can’t simulate constraints with if-statements in the construction rules
# * Need to provide initial conditions for dynamic states by setting the value or using fix()
# 

# In[ ]:




