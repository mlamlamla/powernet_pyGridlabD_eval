# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd

#Parameter of interest
par = 'heating_setpoint'

f = open('houses_Broeer.txt')
i = 0
df_par = pd.DataFrame(columns=[par])

for line in f:
    par_list = line.split(' ')
    if par_list[0].strip() == par:
        par_list[1] = par_list[1].replace(' ',' ')
        par_list[1] = par_list[1].replace(';','')
        par_list[1] = par_list[1].replace('\n','')
        df_par.loc[i] = [par_list[1]]
        i = i+1

df_par = df_par.groupby([par]).size()
print(df_par)