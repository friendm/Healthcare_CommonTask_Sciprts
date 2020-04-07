#!/usr/bin/env python
# coding: utf-8

# In[109]:


import pandas as pd
import numpy as np
import re
import datetime


 
date_regex1="(\d\d\d\d)[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])" # yyyy-mm-dd
date_regex2="([1-9]|1[012])[- /.]([1-9]{1}|[0-9]{2})[- /.](\d\d\d\d)" #dd-mm-yyyy
pattern1=re.compile(date_regex1)
pattern2=re.compile(date_regex2)
df=df.replace('"',"'")
def convert_to_date(x):
    x=str(x).replace('"','')
    if re.match(date_regex1,str(x)):
        match=re.match(date_regex1,str(x))
        x=datetime.datetime(int(match.group(1)),int(match.group(2)),int(match.group(3)))
        #get match group and turn it into a date
        return x.strftime("%Y-%m-%d")
    elif re.match(date_regex2,str(x)):
        print('second')
        match=re.match(date_regex2,str(x))
        print(x)
        x=datetime.datetime(int(match.group(3)),int(match.group(2)),int(match.group(1)))
        return x.strftime("%Y-%m-%d")

df=pd.read_excel('Desktop\SQL Inserter.xlsx')


# In[110]:


df.replace('', np.nan, inplace=True)

df.dropna(axis=1, inplace=True,thresh=1)
df.dropna(axis=0, inplace=True,thresh=1)
df.fillna('',inplace=True)
num_col=len(df.columns)

#check if colums contain _dates
date_columns=[]
for col in df.columns:
    date1=df[col].astype('str').str.contains(date_regex1)
    date2=df[col].astype('str').str.contains(date_regex2)
    if sum(date1)>0 or sum(date2)>0:
        print("pass")
        date_columns.append(col)

        
for col in date_columns:
    df[col]=df[col].apply(convert_to_date)


print(df)


# In[114]:


command_list=[]
table_name='test_table'
table_header='insert into '+table_name+' ('
if np.any(pd.isnull(df)):
    print("error_in_data null values found, examine loaded spreadsheet for columns with some populated and some unpopulated data")
else:

    for index,row in df.iterrows():
        s=''
        for ind,col in enumerate(df.columns):
            if ind<num_col-1:
                s+="'"+row[col]+"',"
            else:
                 s+="'"+row[col]+"')"
        command_list.append(str(table_header+s).replace('"',''))

print('%s Rows of data to be inserted'  % len(command_list))
print('%s Columns of data to be inserted'  % str(command_list[0].count(",")+1))


# In[111]:


command_df=pd.DataFrame(command_list)
command_df.to_csv('Desktop\sql_commands.csv')


# In[ ]:




