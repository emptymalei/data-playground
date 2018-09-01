
# coding: utf-8

# ## History data

# In[8]:


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

# In[41]:


# 如果还没有数据，来群里索要数据文件就行

df = pd.read_csv('data/full-data.csv') 


# Validate all the possible columns of data frame

# In[42]:


list(df.columns.values)


# In[43]:


df['time'] = pd.to_datetime(df['time'],unit='s')#.dt.date


# In[44]:


df


# ## Group by sects

# Get all the sects by sectname

# In[45]:


sects = df.sectname.unique()
sects[0]


# Create a dataframe to store the average data

# In[46]:


max_date = df.time.max()
min_date = df.time.min()
max_date,min_date

dateseries = pd.date_range(start=min_date, end=max_date, freq='10D')


# In[50]:


df[df['time'].between(dateseries[0],dateseries[1])]


# In[162]:


i = 23
df_temp = df[df['time'].between(dateseries[i],dateseries[i+1])].groupby('sectname')['time', 'duration', 'view', 'coin', 'favorite', 'like', 'sectname','sectid'].mean().round(2)
df_temp = df_temp.reset_index()
df_temp['time']=dateseries[i]
list_temp = []
for idx, sect in enumerate(df[df['time'].between(dateseries[i],dateseries[i+1])].sectname.unique()):
    df_temp2 = df[df['time'].between(dateseries[i],dateseries[i+1])]
    df_temp2 = df_temp2[ df_temp2['sectname']==sect]
    list_temp.append(df_temp2.loc[df_temp2['view'].idxmax()].aid)

#     df_temp[df_temp['sectname'] == sect].mostaid = 
df_temp['mostaid'] = list_temp

# df[df['time'].between(dateseries[idx],dateseries[idx+1])].groupby('sectname')['view','aid'].max()




# In[163]:


df_temp


# In[ ]:


index_du = ['time', 'duration', 'view', 'coin', 'favorite', 'like', 'sectname','sectid','mostaid']
df_store = pd.DataFrame(columns=index_du)

for i in np.arange(len(dateseries) -1 ):
# i = 0
    df_temp = df[df['time'].between(dateseries[i],dateseries[i+1])].groupby('sectname')['time', 'duration', 'view', 'coin', 'favorite', 'like', 'sectname','sectid'].mean().round(2)
    df_temp = df_temp.reset_index()
    df_temp['time']=dateseries[i]
    # df_temp['vidcount'] = df[df['time'].between(dateseries[idx],dateseries[idx+1])].groupby('sectname')['view'].count().reset_index()['view'].values
    list_temp = []
    for idx, sect in enumerate(df[df['time'].between(dateseries[i],dateseries[i+1])].sectname.unique()):
        df_temp2 = df[df['time'].between(dateseries[i],dateseries[i+1])]
        df_temp2 = df_temp2[ df_temp2['sectname']==sect]
        list_temp.append(df_temp2.loc[df_temp2['view'].idxmax()].aid)

    #     df_temp[df_temp['sectname'] == sect].mostaid = 
    df_temp['mostaid'] = list_temp

    df_store = pd.concat([df_store,df_temp])



# In[ ]:


df_store


# In[ ]:


df_store.to_csv('export/history-views-10-withaid-script.csv', sep=',', encoding='utf-8')


# ### Visualization
