
# coding: utf-8

# ## History data

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

import seaborn as sns
sns.set_style("white")
fig_w = 2530
fig_h = 1900
my_dpi=200

import dateutil


# Config plot styles

# In[2]:


plt.style.use('ggplot')

from matplotlib import rcParams
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

plt.rc('font', family='BabelStone Han', size=13) # 选择你自己电脑上的字体


# Load data

# In[3]:


# 如果还没有数据，来群里索要数据文件就行

df = pd.read_csv('data/full-data.csv') 


# Validate all the possible columns of data frame

# In[4]:


list(df.columns.values)


# In[5]:


df['time'] = pd.to_datetime(df['time'],unit='s')#.dt.date


# In[195]:


# df;


# ## Group by sects

# Get all the sects by sectname

# In[7]:


sects = df.sectname.unique()
sects[0]


# Create a dataframe to store the average data

# In[194]:


index_store = ['date','tduration', 'tview', 'tcoin', 'tfavorite', 'tlike','totalv','mostaid']

# idx = 3
for idx in np.arange(len(sects) ):
    df_sect = df[df['sectname']==sects[idx]] 

    max_date = df_sect.time.max()
    min_date = df_sect.time.min()
    sect_id_str = str(df_sect.sectid.unique()[0])
    sect_name_str = str(sects[idx])

    dateseries = pd.date_range(start=min_date, end=max_date, freq='10D')


    df_store = pd.DataFrame(columns=index_store)


    ########
    # Loop Through Dates
    ########

    # d_idx = 0

    for d_idx in np.arange(len(dateseries) -1 ):
        df_sect_temp = df_sect[df_sect['time'].between(dateseries[d_idx],dateseries[d_idx+1])]

        if  not df_sect_temp.empty:
            mostviewed_temp = df_sect_temp.loc[df_sect_temp['view'].idxmax()].aid
            totalrows_temp = len(df_sect_temp.index)
            sumviews_temp = np.sum(df_sect_temp['view'].values)
            sumduration_temp = np.sum(df_sect_temp['duration'].values)
            sumcoin_temp = np.sum(df_sect_temp['coin'].values)
            sumfav_temp = np.sum(df_sect_temp['favorite'].values)
            sumlike_temp = np.sum(df_sect_temp['like'].values)

            df_sect_temp2 = df_sect_temp.mean().round(2)

            values_temp = [dateseries[d_idx] , sumduration_temp, sumviews_temp, sumcoin_temp, sumfav_temp, sumlike_temp, totalrows_temp ,mostviewed_temp]

            df_store_temp = pd.DataFrame([values_temp],columns=['date','tduration', 'tview', 'tcoin', 'tfavorite', 'tlike','totalv','mostaid'])


            df_store = (pd.concat([df_store, df_store_temp]) ).reset_index(drop=True)


    df_store.to_csv('export/batch/'+sect_id_str+'-'+sect_name_str+'.csv', sep=',', encoding='utf-8')

