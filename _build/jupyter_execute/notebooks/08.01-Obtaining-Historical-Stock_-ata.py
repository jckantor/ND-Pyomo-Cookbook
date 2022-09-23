#!/usr/bin/env python
# coding: utf-8

# # Obtaining Historical Stock Data
# 
# Keywords: stock price data
# 
# The purpose of this notebook is to download historical trading data for a selected group of the stocks from Alpha Vantage for use with other notebooks. Use of this notebook requires you so enter your personal Alpha Vantage api key into a file `data/api_key.txt`.  The trading data is stored as individual `.csv` files in a designated directory. Subsequent notebooks read and consolidate that data into a singe file.  
# 
# You only need to run this notebook if you wish to analyze a different set of stocks, if you wish to update data for the existing set.

# ## Imports

# In[1]:


import os
import pandas as pd
import requests
import time


# ## Select Stocks to Download

# In[7]:


djia = ['AXP','BA','CAT','CSCO','CVX','DD','DIS','GE',         'GS','HD','IBM','INTC','JNJ','JPM','KO','MCD',         'MMM','MRK','MSFT','NKE','PFE','PG','T','TRV',         'UNH','UTX','V','VZ','WMT','XOM']

favs = ['AAPL']

stocks = favs + djia

data_dir = os.path.join('data', 'stocks')
os.makedirs(data_dir, exist_ok=True)


# ## Alpha Vantage
# 
# The following cells retrieve a history of daily trading data for a specified set of stock ticker symbols. These functions use the free [Alpha Vantage](https://www.alphavantage.co/) data service. The free service tier provides up to 5 queries per minute.
# 
# The service requires an personal api key which can be claimed [here](https://www.alphavantage.co/support/#api-key) in just a few seconds. Place the key as a string in a file `data/api_key.txt` in the data directory as this notebook (note: api_key.txt is not distributed with the github repository). The function `api_key()` returns the key stored in `api_key.txt`.

# In[3]:


def api_key():
    "Read api_key.txt and return api_key"
    try:
        with open('data/api_key.txt') as fp:
            line = fp.readline()
    except:
        raise RuntimeError('Error while attempting to read data/api_key.txt')
    return line.strip()


# The function `alphavantage(s)` returns a pandas dataframe holding historical trading data for a stocker ticker symbol specified by `s`.

# In[4]:


import os
import requests
import pandas as pd

def alphavantage(symbol=None):
    if symbol is None: 
        raise ValueError("No symbol has been provided")
    payload = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "outputsize": "full",
        "datatype": "json",
        "apikey": api_key(), 
    }
    api_url = "https://www.alphavantage.co/query"
    try:
        response = requests.get(api_url, params=payload)
    except:
        raise ValueError("No response using api key: " + api_key)
    data = response.json()
    k = list(data.keys())
    metadata = data[k[0]]
    timeseries = data[k[1]]
    S = pd.DataFrame.from_dict(timeseries).T
    S = S.apply(pd.to_numeric)
    S.columns = [h.lstrip('12345678. ') for h in S.columns]
    return S

alphavantage('AAPL').head()


# `get_stock_data(symbols)` retrieves trading data for a list of symbols and stores each in seperate file in the data directory. The file name is the ticker symbol with a `.csv` suffix.

# In[5]:


def get_stock_data(symbols, service=alphavantage):
    if isinstance(symbols, str):
        symbols = [symbols]
    assert all(isinstance(s, str) for s in symbols)
    for s in symbols:
        print('downloading', s, end='')
        k = 5
        while k > 0:
            try:
                k -= 1
                S = service(s)
                S.to_csv(os.path.join(data_dir, s + '.csv'))
                print(' success')
                break
            except:
                print('.', end='')
                time.sleep(12)
        if k < 0: print('fail')
            
get_stock_data(['AAPL'])


# ## Download selected ticker Symbols

# In[6]:


get_stock_data(stocks)


# In[ ]:




