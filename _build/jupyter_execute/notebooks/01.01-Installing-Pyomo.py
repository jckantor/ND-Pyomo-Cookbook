#!/usr/bin/env python
# coding: utf-8

# # Installing a Pyomo/Python Development Environment
# 
# The first step in getting started with Pyomo is to choose a development environment. Cloud services work effectively with the Pyomo notebooks in this collection including Google Colaboratory, Microsoft Azure, and [CoCalc](https://cocalc.com/). These online services provide an excellent means for viewing and executing notebooks, even those with complicated Pyomo models.
# 
# For sustained development, however, it is more productive to install a complete python environment on your own laptop. This notebook explains how.
# 
# ---
# |

# ## Step 1. Install Anaconda
# 
# Developing scientific and engineering applications in [Python](https://www.python.org/) requires an interpreter for a particular version of the Python language, a collection of previously developed software libraries, and additional development tools including editors and package managers. Together these elements comprise a Python distribution.
# 
# There are many [Python distributions](https://wiki.python.org/moin/PythonDistributions) available from commercial and free sources.  The Anaconda distribution available from [Anaconda.com](https://www.anaconda.com/) is among the most complete and best known distributions currently available, and is available as a [free download](https://www.anaconda.com/download/) or in commercially supported enterprise version. Anaconda includes
# 
# * a Python interpreter,
# * a user interface [Anaconda Navigator](https://docs.anaconda.com/anaconda/navigator/) providing access to software development tools,
# * pre-installed versions of major python libraries,
# * the [conda](https://conda.io/docs/index.html) package manager to manage python packages and environments. 
# 
# Installation Procedure:
# 
# 1. If you have previously installed Anaconda and wish to start over, then a first step is to [uninstall the earlier version](https://docs.anaconda.com/anaconda/install/uninstall). While it is possible to maintain multiple versions of Anaconda, there are problems that can arise when installing new packages. Uninstalling prior installations of Anaconda installations is the easiest way to avoid those problems.
# 
# 2. [Download](https://www.anaconda.com/download/) a version of Anaconda appropriate for your laptop. Unless you have a specific reason to use an earlier version of the Python language, download the 64-bit graphical installer for the latest version of Python (currently Python 3.6).
# 
# 3. Locate and launch the graphical installer from your download directory. Either follow the prompts or consult these more [detailed instructions](https://docs.anaconda.com/anaconda/install/). Normally you will want to use the default choices to install Anaconda into your home folder (a.k.a. directory) for your use only. Generally there is no need to install the optional Microsoft VSCode. 
# 
# 4. [Verify](https://docs.anaconda.com/anaconda/install/verify-install) that your installation is working. For example, you should be able to locate and lauch a new application Anaconda Navigator.
# 
# 5. Install any available package updates. Open a command line (either the Terminal application on a Mac located look in the Applications/Utilities folder, or the Command Prompt on Windows), and execute the following two commands on separate lines.
# 
# 
#     conda update conda
#     conda update anaconda
#    
# If everything is working correctly, these commands should download and install any recent updates to the Anaconda package.

# ## Step 2. Install Pyomo
# 
# The following commands install Pyomo and dependencies. These commands should be executed one at a time from a [terminal window on MacOS](https://www.wikihow.com/Open-a-Terminal-Window-in-Mac) or a [command window on Windows](https://www.digitalcitizen.life/7-ways-launch-command-prompt-windows-7-windows-8).
# 
#     pip install pyomo
#     
# The Pyomo documentation provides complete instructions on [installing Pyomo](https://pyomo.readthedocs.io/en/stable/installation.html).

# ## Step 3. Install solvers
# 
# Solvers are needed to compute solutions to the optimization models developed using Pyomo.  The solvers [COIN-OR CBC](    conda install -c conda-forge glpk) (mixed integer linear optimization) and [ipopt](https://en.wikipedia.org/wiki/IPOPT) (nonlinear optimization) cover a wide range of optimization models that arise in process systems engineering and provide good starting point for learning Pyomo. These are installed with the following commands (again, executed one at a time from a terminal window or command prompt).  
# 
#     conda install -c conda-forge coincbc
#     conda install -c conda-forge ipopt
#     
# At this point you should have a working installation of a Python/Pyomo development environment.  If you're just getting started with Pyomo, at this point you should be able to use Anaconda Navigator to open a Jupyter session in a browswer, then download and open notebooks from this repository. If all is well, the Pyomo models in these notebooks should produce useful results.

# ## Step 4. Optional: Compile Ipopt with HSL solvers
# 
# The Ipopt package uses third-party packages for solving linear subproblems which are generally the most time-consuming steps in the solution algorithm. By default, ipopt is distributed with the [mumps](http://mumps.enseeiht.fr/) solvers. If you expect make extensive use of Ipopt for nonlinear problems, or to be solving larger models with 10's of thousands of variables, then you may wish to recompile Ipopt to use high-performance linear solvers available under license from other sources.
# 
# In particular, [HSL makes available a collection of high-performance solvers for use with Ipopt](http://www.hsl.rl.ac.uk/ipopt/) under a free personal license or a free academic license (commercial licenses are also available). These solvers frequently provide a 10x improvement in solution speed. [Instructions for downloading, compiling, and installing the necessary software are available from COIN-OR](https://projects.coin-or.org/Ipopt/browser/stable/3.11/Ipopt/doc/documentation.pdf).
# 
# When used with Anaconda, it is convenient to install the recompiled Ipopt directly in the anaconda binary library. Given the instructions above, use the option `--prefix=~anaconda3` when calling `configure`.
# 
# 

# ## Step 5. Optional: Install additional solvers
# 
# The glpk and ipopt solvers are sufficient to handle meaningful Pyomo models with hundreds to several thousand variables and constraints. These solvers are available under open-source licenses and an excellent starting point for building applications in Pyomo. These may be all you need for many problems. However, as applications get large or more complex, there may be a need to install additional solvers. 

# ### Gurobi
# 
# [Gurobi](http://www.gurobi.com/index), for example, is a state-of-the-art high performance commercial solver for large-scale linear, mixed-integer linear, and quadratic programming problems. Unlike glpk, Gurobi is a multi-threaded application taht can take full advantage of a multi-core laptop. Gurobi offers free licenses with one-year terms for academic use, and trial licenses for commercial use. If your application has outgrown glpk, then you'll almost certainly want to give Gurbobi a try.
# 
# To install for use in Pyomo, download the standard Gurobi installer and perform the default installation. Follow instructions for registering your copy and obtaining a license. Because Gurobi will be installed outside of the the default Anaconda installation, you will need to specify the actual Gurobi executable. On MacOS, for example, the executable is `/usr/local/bin/gurobi.sh`. 

# ### GLPK
# 
# Occasionally it is helpful to have access to additional solvers. [GLPK](https://en.wikibooks.org/wiki/GLPK) is an open source solve for mixed integer linear programming problems that can be installed using conda:
# 
#         conda install -c conda-forge glpk
# 
# High performance commercial solvers, such as and [CPLEX](https://www.ibm.com/products/ilog-cplex-optimization-studio/pricing), are also available at no cost for many academic uses (this is a fantastic deal!), and with trial licenses for commercial use.

# In[ ]:




