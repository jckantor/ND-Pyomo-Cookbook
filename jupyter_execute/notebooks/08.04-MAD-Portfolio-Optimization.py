#!/usr/bin/env python
# coding: utf-8

# # MAD Portfolio Optimization
# 
# Keywords: glpk usage, portfolio optimization, value at risk, stock price data

# ## Imports

# In[22]:


get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import scipy.stats as stats

import shutil
import sys
import os.path

if not shutil.which("pyomo"):
    get_ipython().system('pip install -q pyomo')
    assert(shutil.which("pyomo"))

if not (shutil.which("glpsol") or os.path.isfile("glpsol")):
    if "google.colab" in sys.modules:
        get_ipython().system('apt-get install -y -qq glpk-utils')
    else:
        try:
            get_ipython().system('conda install -c conda-forge glpk ')
        except:
            pass

assert(shutil.which("glpsol") or os.path.isfile("glpsol"))

from pyomo.environ import *


# ## Investment objectives
# 
# * Maximize returns
# * Reduce Risk through diversification

# ## Why diversify?
# 
# Investment portfolios are collections of investments that are managed for overall investment return.  Compared to investing all of your capital into a single asset, maintaining a portfolio of investments allows you to manage risk through diversification.

# ### Reduce risk through law of large numbers
# 
# Suppose there are a set of independent investment opportunities that will pay back between 0 and 300% of your original investment, and that all outcomes in that range are equally likely. You have $100,000 to invest.  Should you put it all in one opportunity?  Or should you spread it around?
# 
# Here we simulate the outcomes of 1000 trials where we place all the money into a single investment of $100,000.

# In[24]:


W0 = 100000.00

Ntrials = 10000
Profit = list()
for n in range(0, Ntrials):
    W1 = W0*random.uniform(0,3.00)
    Profit.append(W1 - W0)

plt.figure(figsize=(10, 4))
plt.hist(Profit, bins=100)
plt.xlim(-100000, 200000)
plt.xlabel('Profit')
plt.ylabel('Frequency')

print('Average Profit = ${:.0f}'.format(np.mean(Profit)))


# As you would expect, about 1/3 of the time there is a loss, and about 2/3 of the time there is a profit. In the extreme we can lose all of our invested capital. Is this an acceptable investment outcome?
# 
# Now let's see if what happens if we diversify our investment. We'll assume the investment outcomes have exactly the same probabilities. The only difference is that instead of one big investment of \\$100,000, we'll break our capital into 5 smaller sized investments of \\$20,000 each. We'll calculate the probability distribution of outcomes.

# In[4]:


W0 = 100000.00

Ntrials = 10000
Ninvestments = 5

Profit = list()
for n in range(0,Ntrials):
    W1 = sum([(W0/Ninvestments)*random.uniform(0,3.00) for _ in range(0,Ninvestments)])
    Profit.append(W1-W0)

plt.figure(figsize=(10, 4))
plt.hist(Profit, bins=100)
plt.xlim(-100000, 200000)
plt.xlabel('Profit')
plt.ylabel('Frequency')

print('Average Profit = ${:.0f}'.format(np.mean(Profit)))


# What we observe is that even a small amount of diversification can dramatically reduce the downside risk of experiencing a loss. We also see the upside potential has been reduced. What hasn't changed is the that average profit remains at \$50,000. Whether or not the loss of upside potential in order to reduce downside risk is an acceptable tradeoff depends on your individual attitude towards risk. 

# ### Value at risk (VaR)
# 
# [Value at risk (VaR)](https://en.wikipedia.org/wiki/Value_at_risk) is a measure of investment risk. Given a histogram of possible outcomes for the profit of a portfolio, VaR corresponds to negative value of the 5th percentile. That is, 5% of all outcomes would have a lower outcome, and 95% would have a larger outcome. 
# 
# The [conditional value at risk](https://en.wikipedia.org/wiki/Expected_shortfall) (also called the expected shortfall (ES), average value at risk (aVaR), and the expected tail loss (ETL)) is the negative of the average value of the lowest 5% of outcomes. 
# 
# The following cell provides an interactive demonstration. Use the slider to determine how to break up the total available capital into a number of smaller investments in order to reduce the value at risk to an acceptable (to you) level.  If you can accept only a 5% probability of a loss in your portfolio, how many individual investments would be needed?

# In[5]:


#@title Value at Risk (VaR) Demo { run: "auto", vertical-output: true }
Ninvestments = 8 #@param {type:"slider", min:1, max:20, step:1}

from statsmodels.distributions import ECDF

W0 = 100000.00
Ntrials = 10000

def sim(Ninvestments = 5):

    Profit = list()
    for n in range(0, Ntrials):
        W1 = sum([(W0/Ninvestments)*random.uniform(0,3.00) for _ in range(0,Ninvestments)])
        Profit.append(W1-W0)
        
    print('Average Profit = ${:.0f}'.format(np.mean(Profit)).replace('$-','-$'))

    VaR = -sorted(Profit)[int(0.05*Ntrials)]
    print('Value at Risk (95%) = ${:.0f}'.format(VaR).replace('$-','-$'))
    
    cVaR = -sum(sorted(Profit)[0:int(0.05*Ntrials)])/(0.05*Ntrials)
    print('Conditional Value at Risk (95%) = ${:.0f}'.format(cVaR).replace('$-','-$'))

    plt.figure(figsize=(10,6))
    plt.subplot(2, 1, 1)
    plt.hist(Profit, bins=100)
    plt.xlim(-100000, 200000)
    plt.plot([-VaR, -VaR], plt.ylim())
    plt.xlabel('Profit')
    plt.ylabel('Frequency')

    plt.subplot(2, 1, 2)
    ecdf = ECDF(Profit)
    x = np.linspace(min(Profit), max(Profit))
    plt.plot(x, ecdf(x))
    plt.xlim(-100000, 200000)
    plt.ylim(0,1)
    plt.plot([-VaR, -VaR], plt.ylim())
    plt.plot(plt.xlim(), [0.05, 0.05])
    plt.xlabel('Profit')
    plt.ylabel('Cumulative Probability');
    
sim(Ninvestments)


# ## Import historical stock price data

# In[42]:


S_hist = pd.read_csv('data/Historical_Adjusted_Close.csv', index_col=0)

S_hist.dropna(axis=1, how='any', inplace=True)
S_hist.index = pd.DatetimeIndex(S_hist.index)

portfolio = list(S_hist.columns)
print(portfolio)
S_hist.tail()


# ## Select a recent subperiod of the historical data

# In[43]:


nYears = 1.5
start = S_hist.index[-int(nYears*252)]
end = S_hist.index[-1]

print('Start Date:', start)
print('  End Date:', end)

S = S_hist.loc[start:end]
S.head()


# In[44]:


fig, ax = plt.subplots(figsize=(14,9))
S.plot(ax=ax, logy=True)

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.grid(True)


# ## Return on a portfolio
# 
# Given a portfolio with value $W_t$ at time $t$, return on the portfolio at $t_{t +\delta t}$ is defined as
# 
# $$
# \begin{align*}
# r_{t + \delta t} & = \frac{W_{t + \delta t} - W_{t}}{W_{t}}
# \end{align*}
# $$
# 
# For the period from $[t, t+\delta t)$ we assume there are $n_{j,t}$ shares of asset $j$ with a starting value of $S_{j,t}$ per share. The initial and final values of the portfolio are then 
# 
# $$
# \begin{align*}
# W_t & = \sum_{j=1}^J n_{j,t}S_{j,t} \\
# W_{t+\delta t} & = \sum_{j=1}^J n_{j,t}S_{j,t + \delta t}
# \end{align*}
# $$
# 
# The return of the portfolio is given by
# 
# $$
# \begin{align*}
# r_{t+\delta t} & = \frac{W_{t + \delta t} - W_{t}}{W_{t}} \\
# & = \frac{\sum_{j=1}^Jn_{j,t}S_{j,t+\delta t} - \sum_{j=1}^J n_{j,t}S_{j,t}}{W_{t}} \\
# & = \frac{\sum_{j=1}^J n_{j,t}S_{j,t}r_{j, t+\delta t}}{W_{t}} \\
# & = \sum_{j=1}^J \frac{n_{j,t}S_{j,t}}{W_{t}} r_{j, t+\delta t}
# \end{align*}
# $$
# 
# where $r_{j,t+\delta t}$ is the return on asset $j$ at time $t+\delta t$. 
# 
# Defining $W_{j,t} = n_{j,t}S_{j,t}$ as the wealth invested in asset $j$ at time $t$, then $w_{j,t} = n_{j,t}S_{j,t}/W_{t}$ is the fraction of total wealth invested in asset $j$ at time $t$. The portfolio return is then given by 
# 
# $$
# \begin{align*}
# r_{t+\delta t} & = \sum_{j=1}^J w_{j,t} r_{j, t+\delta t} 
# \end{align*}
# $$
# 
# on a single interval extending from $t$ to $t + \delta t$.

# ### Equally weighted portfolio
# 
# An equally weighted portfolio allocates an equal amount of capital to each component of the portfolio. The allocation can be done once and held fixed thereafter, or could be reallocated periodically as asset prices change in relation to one another.

# #### Constant fixed allocation
# 
# If the initial allocation among $J$ assets takes place at $t=0$, then
# 
# $$w_{j,0} = \frac{1}{J} = \frac{n_{j,0} S_{j, t=0}}{W_{0}}$$
# 
# The number of assets of type $j$ included in the portfolio is given by
# 
# $$n_{j,0} = \frac{W_0}{J S_{j,0}} $$
# 
# which is then fixed for all later times $t > 0$. The value of the portfolio is given by
# 
# $$
# \begin{align*}
# W_t & = \sum_{j=1}^J n_{j,0}S_{j,t} \\
# & = \frac{W_{0}}{J} \sum_{j=1}^J \frac{S_{j,t}}{S_{j,0}}
# \end{align*}
# $$
# 
# Note that this portfolio is guaranteed to be equally weighted only at $t=0$. Changes in the relative prices of assets cause the relative weights of assets in the portfolio to change over time.

# #### Continually rebalanced
# 
# Maintaining an equally weighted portfolio requires buying and selling of component assets as prices change relative to each other. To maintain an equally portfolio comprised of $J$ assets where the weights are constant in time,
# 
# $$
# \begin{align*}
# w_{j,t} & = \frac{1}{J} = \frac{n_{j,t}S_{j,t}}{W_t} & \forall j, t
# \end{align*}
# $$
# 
# Assuming the rebalancing occurs at fixed points in time $t_k$ separated by time steps $\delta t$, then on each half-closed interval $[t_k, t_k+\delta t)$
# 
# $$
# \begin{align*}
# n_{j,t} & = \frac{W_{t_k}}{J S_{j,t_k}} \\
# \end{align*}
# $$
# 
# The portfolio
# 
# $$
# \begin{align*}
# W_{t_k + \delta t} & = \sum_{j=1}^J n_{j,t_k} S_{j, t_k + \delta t}
# \end{align*}
# $$
# 
# $$
# \begin{align*}
# W_{t_k + \delta t} & = W_{t_k} \sum_{j=1}^J  \frac{S_{j, t_k + \delta t}}{J S_{j,t_k}}
# \end{align*}
# $$
# 
# Letting $t_{k+1} = t_k + \delta t$, then the following recursion describes the dynamics of an equally weighted,  continually rebalanced portfolio at the time steps $t_0, t_1, \ldots$. Starting with values $W_{t_0}$ and $S_{j, t_0}$, 
# 
# $$
# \begin{align*}
# n_{j,t_k} & = \frac{W_{t_k}}{J S_{j,t_k}} \\
# W_{t_{k+1}} & = \sum_{j=1}^J  n_{j,t_k} S_{j, t_{k+1}}
# \end{align*}
# $$
# 
# which can be simulated as a single equation
# 
# $$
# \begin{align*}
# W_{t_{k+1}} & = W_{t_k} \sum_{j=1}^J  \frac{S_{j, t_{k+1}}}{J S_{j,t_k}}
# \end{align*}
# $$
# 
# or in closed-form
# 
# $$
# \begin{align*}
# W_{t_{K}} & = W_{0} \prod_{k=0}^{K-1} \sum_{j=1}^J  \frac{S_{j, t_{k+1}}}{J S_{j,t_k}}
# \end{align*}
# $$

# In[45]:


plt.figure(figsize=(12,6))

portfolio = S.columns
J = len(portfolio)

# equal weight with no rebalancing
n = 100.0/S.iloc[0]/J
W_fixed = sum(n[s]*S[s] for s in portfolio)
W_fixed.plot(color='r',lw=4)

# equal weighting with continual rebalancing
R = (S[1:]/S.shift(1)[1:]).sum(axis=1)/len(portfolio)
W_rebal = 100*R.cumprod()
W_rebal.plot(color='b', lw=4)

# individual assets
for s in portfolio:
    (100.0*S[s]/S[s][0]).plot(lw=0.4)
    
plt.legend(['Fixed Allocation','Continually Rebalanced'])
plt.ylabel('Value');
plt.title('Value of an equally weighted portfolio')
plt.grid(True)


# In[49]:


plt.figure(figsize=(10,6))

plt.subplot(2,1,1)
W_fixed.plot()
W_rebal.plot()
plt.legend(['Fixed Allocation','Continually Rebalanced'])
plt.ylabel('Value')
plt.title('Comparing a Fixed and Continually Rebalanced Portfolio')
plt.grid(True)

plt.subplot(2,1,2)
(100.0*(W_rebal-W_fixed)/W_fixed).plot()
plt.title('Added value of a Rebalanced Portfolio relative to a Fixed Portfolio')
plt.ylabel('percent')
plt.grid(True)

plt.tight_layout()


# ### Component returns
# 
# Given data on the prices for a set of assets over an historical period $t_0, t_1, \ldots, t_K$, an estimate the mean arithmetic return is given by the mean value
# 
# $$
# \begin{align*}
# \hat{r}_{j,t_K} & = \frac{1}{K}\sum_{k=1}^{K} r_{t_k} \\
# & = \sum_{k=1}^{K} \frac{S_{j,t_{k}}-S_{j,t_{k-1}}}{S_{j,t_{k-1}}}
# \end{align*}
# $$
# 
# At any point in time, $t_k$, a mean return can be computed using the previous $H$ intervals
# 
# $$
# \begin{align*}
# \hat{r}^H_{j,t_k} & = \frac{1}{H}\sum_{h=0}^{H-1} r_{t_{k-h}} \\
# & = \frac{1}{H} \sum_{h=0}^{H-1}\frac{S_{j,t_{k-h}} - S_{j,t_{k-h-1}}}{S_{j,t_{k-h-1}}}
# \end{align*}
# $$
# 
# Arithmetic returns are computed so that subsequent calculations combine returns across components of a portfolio.

# ## Measuring deviation in component returns

# ### Mean absolute deviation

# In[30]:


def roll(H):
    """Plot mean returns, mean absolute deviation, and standard deviation for last H days."""
    K = len(S.index)
    R = S[K-H-1:K].diff()[1:]/S[K-H-1:K].shift(1)[1:]
    AD = abs(R - R.mean())
    
    plt.figure(figsize = (12, 0.35*len(R.columns)))
    ax = [plt.subplot(1,3,i+1) for i in range(0,3)]
    
    idx = R.columns.argsort()[::-1]

    R.mean().iloc[idx].plot(ax=ax[0], kind='barh')
    ax[0].set_title('Mean Returns');
    
    AD.mean().iloc[idx].plot(ax=ax[1], kind='barh')
    ax[1].set_title('Mean Absolute Difference')

    R.std().iloc[idx].plot(ax=ax[2], kind='barh')
    ax[2].set_title('Standard Deviation')
    
    for a in ax: a.grid(True)
    plt.tight_layout()

roll(500)


# ### Comparing mean absolute deviation to standard deviation

# In[51]:


R = (S.diff()[1:]/S.shift(1)[1:]).dropna(axis=0, how='all')
AD = abs(R - R.mean())

plt.plot(R.std(), AD.mean(), 'o')
plt.xlabel('Standard Deviation')
plt.ylabel('Mean Absolute Deviation')

plt.plot([0,R.std().max()],[0,np.sqrt(2.0/np.pi)*R.std().max()])
plt.legend(['Portfolio Components','sqrt(2/np.pi)'],loc='best')
plt.grid(True)


# ### Return versus mean absolute deviation for an equally weighted continually rebalanced portfolio

# In[52]:


plt.figure(figsize=(10,6))
for s in portfolio:
    plt.plot(AD[s].mean(), R[s].mean(),'s')
    plt.text(AD[s].mean()*1.03, R[s].mean(), s)
    
R_equal = W_rebal.diff()[1:]/W_rebal[1:]
M_equal = abs(R_equal-R_equal.mean()).mean()

plt.plot(M_equal, R_equal.mean(), 'ro', ms=15)

plt.xlim(0, 1.1*max(AD.mean()))
plt.ylim(min(0, 1.1*min(R.mean())), 1.1*max(R.mean()))
plt.plot(plt.xlim(),[0,0],'r--');
plt.title('Risk/Return for an Equally Weighted Portfolio')
plt.xlabel('Mean Absolute Deviation')
plt.ylabel('Mean Daily Return');
plt.grid(True)


# ## MAD porfolio

# The linear program is formulated and solved using the pulp package. 

# In[15]:


R.head()


# The decision variables will be indexed by date/time.  The pandas dataframes containing the returns data are indexed by timestamps that include characters that cannot be used by the GLPK solver. Therefore we create a dictionary to translate the pandas timestamps to strings that can be read as members of a GLPK set. The strings denote seconds in the current epoch as defined by python.

# In[16]:


a = R - R.mean()
a.head()


# In[17]:


from pyomo.environ import *

a = R - R.mean()

m = ConcreteModel()

m.w = Var(R.columns, domain=NonNegativeReals)
m.y = Var(R.index, domain=NonNegativeReals)

m.MAD = Objective(expr=sum(m.y[t] for t in R.index)/len(R.index), sense=minimize)

m.c1 = Constraint(R.index, rule = lambda m, t: m.y[t] + sum(a.loc[t,s]*m.w[s] for s in R.columns) >= 0)
m.c2 = Constraint(R.index, rule = lambda m, t: m.y[t] - sum(a.loc[t,s]*m.w[s] for s in R.columns) >= 0)
m.c3 = Constraint(expr=sum(R[s].mean()*m.w[s] for s in R.columns) >= R_equal.mean())
m.c4 = Constraint(expr=sum(m.w[s] for s in R.columns)==1)

SolverFactory('glpk').solve(m)

w = {s: m.w[s]() for s in R.columns}

plt.figure(figsize = (15,0.35*len(R.columns)))

plt.subplot(1,3,1)
pd.Series(w).plot(kind='barh')
plt.title('Porfolio Weight');

plt.subplot(1,3,2)
R.mean().plot(kind='barh')
plt.title('Mean Returns');

plt.subplot(1,3,3)
AD.mean().plot(kind='barh')
plt.title('Mean Absolute Difference');


# In[54]:


P_mad = pd.Series(0, index=S.index)
for s in portfolio:
    P_mad += 100.0*w[s]*S[s]/S[s][0]
    
plt.figure(figsize=(12,6))
P_mad.plot()
W_rebal.plot()
plt.legend(['MAD','Equal'],loc='best')
plt.ylabel('Unit Value')
plt.grid(True)


# In[19]:


plt.figure(figsize=(10,6))
for s in portfolio:
    plt.plot(AD[s].mean(), R[s].mean(),'s')
    plt.text(AD[s].mean()*1.03, R[s].mean(), s)
    
#R_equal = P_equal.diff()[1:]/P_equal[1:]
R_equal = np.log(W_rebal/W_rebal.shift(+1))
M_equal = abs(R_equal-R_equal.mean()).mean()

plt.plot(M_equal, R_equal.mean(), 'ro', ms=15)

#R_mad = P_mad.diff()[1:]/P_mad[1:]
R_mad = np.log(P_mad/P_mad.shift(+1))
M_mad = abs(R_mad-R_mad.mean()).mean()

plt.plot(M_mad, R_mad.mean(), 'go', ms=15)

for s in portfolio:
    if w[s] >= 0.0001:
        plt.plot([M_mad, AD[s].mean()],[R_mad.mean(), R[s].mean()],'g--')
    if w[s] <= -0.0001:
        plt.plot([M_mad, AD[s].mean()],[R_mad.mean(), R[s].mean()],'r--')

plt.xlim(0, 1.1*max(AD.mean()))
plt.ylim(min(0, 1.1*min(R.mean())), 1.1*max(R.mean()))
plt.plot(plt.xlim(),[0,0],'r--');
plt.title('Risk/Return for an Equally Weighted Portfolio')
plt.xlabel('Mean Absolute Deviation')
plt.ylabel('Mean Daily Return')

