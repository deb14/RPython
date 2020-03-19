#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from statsmodels.tsa.stattools import adfuller,kpss
from fitter import Fitter
pandas2ri.activate()


# In[3]:


def seasonlity_test(m_value):
    season_test = """ function(m_value){
    if (!require("forecast")) install.packages("forecast")
    m_value_ts <- ts(m_value, frequency=288)
    fit <- tbats(m_value_ts)
    seasonal <- !is.null(fit$seasonal)
    seasonal
    }
    """
    r_func = robjects.r(season_test)
    seasonal = r_func(m_value)
    return seasonal


# In[ ]:


seasonlity_test(df.m_value)


# In[39]:


def adf_stationarity(m_value):
    adf_res = adfuller(m_value, autolag='AIC')
    if adf_res[0] > 0.05:
        pvalue=1
    else:
        pvalue=0
    cvalue = 0
    for key, value in adf_res[4].items():
        if adf_res[0] > value:
            cvalue =1
            break
    if pvalue==1 and cvalue==1:
        non_stationary=1
    else:
        non_stationary=0
    return non_stationary


# In[40]:


adf_stationarity(df.m_value)


# In[6]:


def kpss_stationarity(m_value):    
    statistic, p_value, _, critical_values = kpss(m_value,regression='ct',lags='auto')
    if p_value < 0.05:
        non_stationary=1
    else:
        non_stationary=0
    return non_stationary


# In[7]:


kpss_stationarity(df.m_value)


# In[13]:


def fit_distribution(m_value):
    f = Fitter(m_value,verbose=False)
    f.fit()
    top_dist = f.summary(plot=False)
    top_dist = top_dist.index[0]
    return top_dist


# In[14]:


fit_distribution(m_value)


# In[ ]:




