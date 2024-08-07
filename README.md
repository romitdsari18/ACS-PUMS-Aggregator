# ACS-PUMS-Aggregator

To create a program in Python that performs the following using the pandas packages: 

Loads the ss13hil.csv file that contains the PUMS dataset (assume it's in the current directory) and create a Data Frame object from it if you use Python. 

Create 3 tables: 

1. TABLE 1: Statistics of HINCP - Household income (past 12 months), grouped by HHT - Household/family type 
            Table should use the HHT types (text descriptions) as the index 
            Columns should be: mean, std, count, min, max 
            Rows should be sorted by the mean column value in descending order 
2. TABLE 2: HHL - Household language vs. ACCESS - Access to the Internet (Frequency Table) 
            Table should use the HHL types (text descriptions) as the index 
            Columns should be the text descriptions of ACCESS values 
            Each table entry is the sum of WGTP column for the given HHL/ACCESS combination, divided by the sum of WGTP values in the data. Entries need to be formatted as percentages. 
            Any rows containing NA values in HHL, ACCESS, or WGTP columns should be excluded. 
3. TABLE 3: Quantile Analysis of HINCP - Household income (past 12 months) 
            Rows should correspond to different quantiles of HINCP: low (0-1/3), medium (1/3-2/3), high (2/3-1)
            Columns displayed should be: min, max, mean, household_count 
            The household_count column contains entries with the sum of WGTP values for the corresponding range of HINCP values (low, medium, or high) 

4. Display the tables to the screen as shown in the sample output on the last page.

# Explaination

1. Initially we have imported the required libraries.

2. Then by using the Pandas data frame we have imported the ‘ss13hil.csv’ file.

3. Then we have created three tasks in which the tables will be created.
  
   The tasks are as follows.

   3.1 The first task is to create a table that shows the descriptive statistics of household income (HINCP) grouped by household/family type (HHT). This is done by selecting the columns for          analysis, converting the HHT column to a string data type, replacing numerical codes in the HHT column with descriptive strings, dropping rows with missing HINCP values, grouping by            HHT, and calculating descriptive statistics for HINCP. The resulting table is sorted by mean HINCP in descending order.
   
   3.2 The second task is to create a frequency table that shows the relationship between household language (HHL) and access to the Internet (ACCESS). This is done by dropping rows with              missing values for HHL, WGTP, and ACCESS columns, creating a list of labels for the HHL column, replacing numerical codes in the HHL column with descriptive strings, calculating the sum        of the WGTP column, grouping the data by HHL and ACCESS, pivoting the table to show the WGTP totals for each combination of HHL and ACCESS, calculating the total for each row and column        and adding it as a new column and row called "ALL," dividing the table by the sum of WGTP to get the frequency percentages, formatting the table to display percentages with two decimal         places, renaming the columns and index for readability, and reordering the rows to match the specified order.

   3.3 The third task is to create a table that shows the quantile analysis of household income (HINCP). This is done by creating a new DataFrame with the HINCP column, creating a new                 DataFrame with the HINCP column and the weighting variable (WGTP), grouping by HINCP, and calculating the weighted quantiles. The resulting table shows the weighted quantiles for the           entire dataset as well as for each household/family type (HHT).

