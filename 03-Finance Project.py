#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___

# # Finance Data Project 
# 
# In this data project we will focus on exploratory data analysis of stock prices. 
# ____
# We'll focus on bank stocks and see how they progressed throughout the Covid-19 pandemic times all the way to 2022.

# ## Getting the Data
# 
# In this section pandas has been used to directly read data from Google finance!
# 
# First we need to start with the proper imports.
# 
# *Note: [We need to install pandas-datareader for this to work!](https://github.com/pydata/pandas-datareader) Pandas datareader allows us to [read stock information directly from the internet](http://pandas.pydata.org/pandas-docs/stable/remote_data.html)*
# 
# ### The Imports

# In[5]:


pip install pandas-datareader


# In[34]:


from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Data
# 
# We need to get data using pandas datareader. We will get stock information for the following banks:
# *  Bank of America
# * CitiGroup
# * Goldman Sachs
# * JPMorgan Chase
# * Morgan Stanley
# * Wells Fargo
# 
# ** The stock data from Jan 1st 2018 to Dec 31st 2021 for each of these banks. 
# Setting each bank to be a separate dataframe, with the variable name for that bank being its ticker symbol. This will involve a few steps:**
# 1. Using datetime to set start and end datetime objects.
# 2. Figure out the ticker symbol for each bank.
# 2. Figure out how to use datareader to grab info on the stock.
# 
# ** Use [this documentation page](https://pandas-datareader.readthedocs.io/en/latest/remote_data.html) for hints and instructions (it should just be a matter of replacing certain values. 
# Here yahoo finance has been used as a source, for example:**
#     
#     # Bank of America
#     BAC = data.DataReader("BAC", 'yahoo', start, end)
# 
# ### WARNING: MAKE SURE TO CHECK THE LINK ABOVE FOR THE LATEST WORKING API. "yahoo" MAY NOT ALWAYS WORK. 
# ------------

# In[12]:


start = datetime.datetime(2018, 1, 1)
end = datetime.datetime(2022, 1, 1)


# In[13]:


# Bank of America
BAC = data.DataReader("BAC", 'yahoo', start, end)

# CitiGroup
C = data.DataReader("C", 'yahoo', start, end)

# Goldman Sachs
GS = data.DataReader("GS", 'yahoo', start, end)

# JPMorgan Chase
JPM = data.DataReader("JPM", 'yahoo', start, end)

# Morgan Stanley
MS = data.DataReader("MS", 'yahoo', start, end)

# Wells Fargo
WFC = data.DataReader("WFC", 'yahoo', start, end)


# In[15]:


#OR (for a panel of objects):
df = data.DataReader(['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC'],'yahoo', start, end)


# **Creating a list of the ticker symbols (as strings) in alphabetical order. Call this list: tickers**

# In[16]:


tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']


# **Using pd.concat to concatenate the bank dataframes together to a single data frame called bank_stocks.**

# In[17]:


bank_stocks = pd.concat([BAC, C, GS, JPM, MS, WFC],axis=1,keys=tickers)


# **Setting the column name levels:**

# In[18]:


bank_stocks.columns.names = ['Bank Ticker','Stock Info']


# **Checking the head of the bank_stocks dataframe.**

# In[22]:


bank_stocks.head()


# # EDA
# 
# Let's explore the data a bit! 
# 
# **What is the max Close price for each bank's stock throughout the time period?**

# .xs() returns cross-section from the Series/DataFrame.

# In[27]:


bank_stocks.xs(level='Stock Info',key='Close',axis=1).max()


# ** Creating a new empty DataFrame called returns. This dataframe will contain the returns for each bank's stock. returns are typically defined by:**
# 
# $$r_t = \frac{p_t - p_{t-1}}{p_{t-1}} = \frac{p_t}{p_{t-1}} - 1$$

# In[29]:


returns=pd.DataFrame()


# ** We can use pandas pct_change() method on the Close column to create a column representing this return value. pct_change() calculates the % change between the current and a prior element.**
# 
# **Creating a for loop that for each Bank Stock Ticker creates returns column and sets it as a column in the returns DataFrame.**

# In[31]:


for i in tickers:
    returns[i]=bank_stocks[i]['Close'].pct_change()


# In[32]:


returns.head()


# **Creating a pairplot using seaborn of the returns dataframe.**

# In[42]:


sns.pairplot(returns[1:])


# **What dates each bank stock had the best and worst single day returns.**

# In[47]:


# worst drop
returns.idxmin()


#  5 of the banks share the same day for the worst drop, did anything significant happen that day?
#  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7343658/
#  The day has been marked as **black monday** because of the stock market crash due to Covid-19.

# In[48]:


#best single day gain
returns.idxmax()


# **Which stock would you classify as the riskiest over the entire time period?**

# In[50]:


returns.std() #citi group is the riskiest


# **Riskiest stock for 2021?**

# In[57]:


returns['2021-1-1':'2021-12-31'].std() #wells fargo


# **Creating a distplot using seaborn of the 2021 returns for Wells Fargo **

# In[76]:


sns.displot(returns['2021-1-1':'2021-12-31']['MS'],color='green',bins=50)


# ____
# # More Visualization
# 
# A lot of this project will focus on visualizations. Feel free to use any of your preferred visualization libraries to try to recreate the described plots below, seaborn, matplotlib, plotly and cufflinks, or just pandas.
# 
# ### Imports

# In[16]:


import plotly
import cufflinks as cf
cf.go_offline()


# **Creating a line plot showing Close price for each bank for the entire index of time.**

# In[97]:


bank_stocks.xs(level='Stock Info',key='Close',axis=1).iplot()


# In[19]:





# ## Moving Averages
# 
# Let's analyze the moving averages for these stocks in the year 2020. 
# 
# **Plotting the rolling 30 day average against the Close Price for Bank Of America's stock for the year 2020**

# In[107]:


sns.set_style('whitegrid')
plt.figure(figsize=(10,7))
BAC['Close']['2019-1-1':'2020-1-1'].rolling(window=30).mean().plot(label='30 day average')
BAC['Close']['2019-1-1':'2020-1-1'].plot()
plt.legend()


# **Creating a heatmap of the correlation between the stocks Close Price.**

# In[115]:


sns.heatmap(bank_stocks.xs(level='Stock Info',key='Close',axis=1).corr(),annot=True,cmap='magma')


# **Using clustermap to cluster the correlations together:**

# In[124]:


sns.clustermap(bank_stocks.xs(level='Stock Info',key='Close',axis=1).corr(),annot=True,cmap='turbo')


# In[42]:





# # Technocal Analysis Plots
# 
# This part of the project is experimental due to its heavy reliance on the cuffinks project.

# **Creating a candle plot of Bank of America's stock from Jan 1st 2018 to Jan 1st 2019.**

# In[134]:


BAC[['Open', 'High', 'Low', 'Close']]['2018-01-01':'2019-01-01'].iplot(kind='candle')


# **creating a Simple Moving Averages plot of Goldman Sachs for the year 2018.**

# In[136]:


GS['Close']['2018-01-01':'2019-01-01'].ta_plot(study='sma',periods=[13,21,55],title='Simple Moving Averages')


# **Creating a Bollinger Band Plot for Bank of America for the year 2018.**

# In[137]:


BAC['Close']['2018-01-01':'2019-01-01'].ta_plot(study='boll')


# # Great Job!
# 
# Definitely a lot of more specific finance topics here, so don't worry if you didn't understand them all! The only thing you should be concerned with understanding are the basic pandas and visualization oeprations.
