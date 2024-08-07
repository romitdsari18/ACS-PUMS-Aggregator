# -*- coding: utf-8 -*-\

#Importing Requried libraries
import pandas as pd
import numpy as np

#Reading the csv file into a pandas dataframe
df = pd.read_csv("ss13hil.csv")

#TABLE 1: Statistics of HINCP - Household income (past 12 months), grouped by HHT - Household/family type

#Selecting columns for analysis
table1 = df[['HHT', 'HINCP']].copy()

#Converting HHT column to string data type
table1['HHT'] = table1['HHT'].astype(str)

#Replacing numerical codes in HHT column with descriptive strings
table1['HHT'].replace(['1.0', '2.0', '3.0', '4.0', '5.0', '6.0', '7.0'], 
                          ['Married couple household', 
                           'Other family household:Male householder, no wife present',
                           'Other family household:Female householder, no husband present', 
                           'Nonfamily household:Male householder:Living alone',
                           'Nonfamily household:Male householder:Not living alone', 
                           'Nonfamily household:Female householder:Living alone', 
                           'Nonfamily household:Female householder:Not living alone'], 
                          inplace=True)

#Droping rows with missing HINCP values
table1.dropna(subset=['HINCP'], inplace=True)

#Grouping by HHT and calculate descriptive statistics for HINCP
df_stats = table1.groupby('HHT')['HINCP'].agg(['mean', 'std', 'count', 'min', 'max', 'sum'])

#Sorting the dataframe by mean HINCP in descending order
df_stats.sort_values(by='mean', ascending=False, inplace=True)

#Rename the index and select desired columns for display
df_stats.index.names = ['HHT - Household/family type']
df_stats = df_stats[['mean', 'std', 'count', 'min', 'max']]

#Converting the count, min, and max columns to numeric data type
cols = ['count', 'min', 'max']
df_stats[cols] = df_stats[cols].apply(pd.to_numeric, errors='coerce')

#Setting pandas display options for tables
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('max_colwidth', 800)

#Printing the TABLE 1 to console
with pd.option_context('display.colheader_justify', 'left'):
    print('*** Table 1 - Descriptive Statistics of HINCP, grouped by HHT ***')
    print(df_stats)
    
#TABLE 2: HHL - Household language vs. ACCESS - Access to the Internet (Frequency Table)

#Droping rows with missing values for HHL, WGTP, and ACCESS columns
df.dropna(subset=['HHL','WGTP','ACCESS'], inplace=True)

#Creating a list of labels for HHL column
hhl_labels = ['English Only', 'Spanish', 'Other Indo-European Language',
              'Asian and Pacific Island Languages', 'Other Language']

#Creating a copy of the dataframe and replace numerical codes in HHL column with descriptive strings
table2 = df.copy()
table2['HHL'] = table2['HHL'].replace([1, 2, 3, 4, 5], hhl_labels)

#Calculating the sum of WGTP column
wgtp_sum = table2['WGTP'].sum()

#Grouping the data by 'HHL' and 'ACCESS' and sum the 'WGTP' column
groupby_sum = table2.groupby(['HHL','ACCESS'], as_index=False)['WGTP'].sum()

#Pivot the table to show the 'WGTP' totals for each combination of 'HHL' and 'ACCESS'
df_pivot = pd.pivot_table(groupby_sum, values='WGTP', index='HHL', columns='ACCESS', aggfunc=np.sum)

#Calculating the total for each row, column and add it as a new column, row called 'ALL'
df_pivot.loc[:, 'ALL'] = df_pivot.sum(axis=1)
df_pivot.loc['ALL', :] = df_pivot.sum(axis=0)

#Dividing the table by the sum of 'WGTP' to get the frequency percentages
wgtp_sum = groupby_sum['WGTP'].sum()
df_pivot /= wgtp_sum

#Formating the table to display percentages with two decimal places
df_pivot = df_pivot.applymap(lambda x: f"{x:.2%}")

#Renaming the columns and index for readability
df_pivot.columns = ['Yes, w/ Subsrc.', 'Yes, wo/Subsrc.', 'No', 'ALL']
df_pivot.index.name = 'HHL - Household Language'
df_pivot = df_pivot.rename(index={'ALL': 'All'})

#Reorder the rows to match the specified order
df_pivot = df_pivot.reindex(['English Only', 'Spanish', 'Other Indo-European Language',
              'Asian and Pacific Island Languages', 'Other Language', 'All'])

#Printing the table
print('\n*** Table 2 - HHL vs. ACCESS - Frequency Table ***')
print("sum".center(95))
print("WGTP".center(95))
print(df_pivot.to_string())

#TABLE 3: Quantile Analysis of HINCP - Household income (past 12 months)

#Creating a new DataFrame 'table3' with the 'HINCP' column
table3 =  df.reindex(columns=["HINCP"])

#Creating a new DataFrame 'table3_wgtp' with the 'WGTP' column
table3_wgtp = df.reindex(columns=["WGTP"])

#Droping the rows containing NaN values from 'table3'
table3.dropna(axis=0, how='any', inplace=True)

#Grouping the 'HINCP' column into 3 quantiles using pd.qcut(), with labels 'low', 'medium', and 'high'
q_grouping = pd.qcut(table3.HINCP, 3, labels=['low', 'medium', 'high'])

#Grouping the 'HINCP' column by the quantiles created above
q_group_by = table3.HINCP.groupby(q_grouping)

#Creating a dictionary 'table_3_stats' with statistics for each quantile
#The statistics are the minimum, maximum, mean, and sum of 'WGTP' for each quantile
table_3_stats = {
    'min': q_group_by.min(),
    'max': q_group_by.max(),
    'mean': q_group_by.mean(),
    'household_count': table3_wgtp.groupby(q_grouping)['WGTP'].sum()
}

#Converting the 'table_3_stats' dictionary to a DataFrame
table_3_stats = pd.DataFrame(table_3_stats)

#Printing the resulting DataFrame 'table_3_stats' with the statistics for each quantile of 'HINCP'
print("\n*** Table 3 - Quantile Analysis of HINCP - Household income (past 12 months) ***")
print(table_3_stats)



