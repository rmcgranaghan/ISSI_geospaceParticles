
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from datetime import timedelta, datetime


# In[4]:


def hist6hr(data):
    hr6 = [data[i-timedelta(hours=6.5):i-timedelta(hours=5.5)].mean().values
           for i in data.index]
    columns = [i+'_6hr' for i in data.columns]
    return pd.DataFrame(hr6, index=data.index,columns=columns)

def hist5hr(data):
    hr5 = [data[i-timedelta(hours=5.5):i-timedelta(hours=4.5)].mean().values
           for i in data.index]
    columns = [i+'5hr' for i in data.columns]
    return pd.DataFrame(hr5, index=data.index,columns=columns)

def hist3hr(data):
    hr3 = [data[i-timedelta(hours=3.25):i-timedelta(hours=2.75)].mean().values
           for i in data.index]
    columns = [i+'_3hr' for i in data.columns]
    return pd.DataFrame(hr3, index=data.index,columns=columns)

def hist1hr(data):
    hr1 = [data[i-timedelta(hours=1.25):i-timedelta(hours=0.75)].mean().values
           for i in data.index]
    columns = [i+'_1hr' for i in data.columns]
    return pd.DataFrame(hr1, index=data.index,columns=columns)


# In[6]:


def hist45min(data):
    min45 = [data.loc[i-timedelta(minutes=45)].values
             for i in data.index
             if i >= data.index[0]+timedelta(minutes=45)]
    columns = [i+'_45min' for i in data.columns]
    return pd.DataFrame(min45, index=data.index[int(45/5):],columns=columns)

def hist30min(data):
    min30 = [data.loc[i-timedelta(hours=0.5)].values
             for i in data.index
             if i >= data.index[0]+timedelta(minutes=30)]
    columns = [i+'_30min' for i in data.columns]
    return pd.DataFrame(min30, index=data.index[int(30/5):],columns=columns)

def hist15min(data):
    min15 = [data.loc[i-timedelta(hours=0.25)].values
             for i in data.index
             if i >= data.index[0]+timedelta(minutes=15)]
    columns = [i+'_15min' for i in data.columns]
    return pd.DataFrame(min15, index=data.index[int(15/5):],columns=columns)

def hist10min(data):
    min10 = [data.loc[i-timedelta(minutes=10)].values
             for i in data.index
             if i >= data.index[0]+timedelta(minutes=10)]
    columns = [i+'_10min' for i in data.columns]
    return pd.DataFrame(min10, index=data.index[int(10/5):],columns=columns)


# In[10]:


def time_history(data):
    '''
    Function which calculates time history information
    given an input dataframe.
    
    Averages are centred on the respective time-history
    specified.
    
    Input:
    data - a Pandas DataFrame containing data.
    
    Output:
    A concatenated DataFrame containing
        - the original data
        - t-6hrs (1hr avg)
        - t-5hrs (1hr avg)
        - t-3hrs (30min avg)
        - t-1hrs (30min avg)
        - t-45min (instant)
        - t-30min (instant)
        - t-15min (instant)
        - t-10min (instant)
    '''
    return pd.concat((data,
                      hist6hr(data),hist5hr(data),
                      hist3hr(data),hist1hr(data),
                      hist45min(data),hist30min(data),
                      hist15min(data),hist10min(data)),axis=1)

