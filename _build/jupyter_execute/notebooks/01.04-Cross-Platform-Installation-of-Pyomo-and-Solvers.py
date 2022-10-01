#!/usr/bin/env python
# coding: utf-8

# # Cross-Platform Installation of Pyomo and Solvers

# The are significant differences on how Pyomo and associated solvers are installed on different platforms. While it is difficult to anticipate all situations, the following code snippet show how to write Python/Pyomo code that will run and install Pyomo and selected solvers on multiple platforms.

# ## Imports
# 
# The following cell can be used in a Jupyter notebook to provide cross-platform use of the ipopt and cbc solvers. 

# In[1]:


import shutil
import sys
import os.path

# check if pyomo has been installed. If not, install with pip
if not shutil.which("pyomo"):
    get_ipython().system('pip install -q pyomo')
assert(shutil.which("pyomo"))

# check if ipopt is installed. If not, install.
if not (shutil.which("ipopt") or os.path.isfile("ipopt")):
    if "google.colab" in sys.modules:
        get_ipython().system('wget -N -q "https://ampl.com/dl/open/ipopt/ipopt-linux64.zip"')
        get_ipython().system('unzip -o -q ipopt-linux64')
    else:
        try:
            get_ipython().system('conda install -c conda-forge ipopt ')
        except:
            pass
assert(shutil.which("ipopt") or os.path.isfile("ipopt"))

# check if COIN-OR CBC is installed. If not, install.
if not (shutil.which("cbc") or os.path.isfile("cbc")):
    if "google.colab" in sys.modules:
        get_ipython().system('apt-get install -y -qq coinor-cbc')
    else:
        try:
            get_ipython().system('conda install -c conda-forge coincbc ')
        except:
            pass
assert(shutil.which("cbc") or os.path.isfile("cbc"))

import pyomo.environ as pyo


# In[ ]:




