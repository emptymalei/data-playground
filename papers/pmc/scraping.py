# coding: utf-8

# # PMC Data Scraping and Parsing

# This notebook is for PMC data

# Import modules

# In[4]:


import requests
import xml.etree.ElementTree as ET
import pandas as pd


# Links to data or query etc

# In[5]:


search_key_word = 'depression'

def pmc_url(cm=None):
    if cm == None:
        cm = '*'
        
    return 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query='+ search_key_word + '&resulttype=lite&pageSize=100' + '&cursorMark=' + cm


# Write a parser for XML data and load it to pandas dataframe

# In[20]:


class XML2DF:

    def __init__(self, xml_data):
        self.root = ET.XML(xml_data)
        self.meta = [ child for child in iter(self.root) ]
        self.nextCursorMark = self.meta[2].text
        self.hintCount = self.meta[1].text
        self.results = [ child for child in self.meta[4] ];

    def parse_result_list(self,results):
        return [self.parse_result(child) for child in iter(results)]
        
    def parse_result(self, element, result=None):
        if result is None:
            result = dict()
        for key in element.keys():
            result[key] = element.attrib.get(key)
        if element.text:
            result[element.tag] = element.text
        for child in list(element):
            self.parse_result(child, result)
        return result

    def to_df(self):
        structure_data = self.parse_result_list(self.results)
        return pd.DataFrame(structure_data)



# ## Test Parser

# Load and verify that the xml data was loaded

# In[21]:


xml_data = requests.get(pmc_url()).content


# In[22]:


xml_data;


# Create the XML2DF object from the XML data

# In[23]:


xml2df = XML2DF(xml_data)


# In[24]:


xml2df.hintCount,xml2df.nextCursorMark


# Load the XML into a dataframe

# In[25]:


df_xml = xml2df.to_df()


# Find out all the columns

# In[26]:


col = df_xml.columns


# ## Load All Query Results

# In[27]:


df_total = pd.DataFrame( columns = col )

marker = '*'
marker_store = ''

# while marker != marker_store:
limit = 10000 # for the keyword depression, the total iterations should of the order int(xml2df.hintCount)/100 since the page size is 100
flag = 0

# Set a limit on the loops so that it's not too large
while flag < limit:
    
    xml_data = requests.get(pmc_url(marker)).content
    xml2df = XML2DF(xml_data)
    df_xml = xml2df.to_df()
    
    if df_xml.empty:
        print('no data')
        break
    else:
        df_total = pd.concat( [df_total, df_xml] )
        
    flag = flag + 1
    
#     marker_store = marker
#     marker = xml2df.nextCursorMark


# In[29]:


df_total.shape


# In[30]:


df_total.to_csv('depression.csv', sep=',', encoding='utf-8')
