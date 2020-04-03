# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 00:36:24 2019

@author: MLA
"""

import pandas as pd
import matplotlib.pyplot as ppt

df_T = pd.read_csv('T_all.csv',skiprows=range(8))
df_T['# timestamp'] = df_T['# timestamp'].map(lambda x: str(x)[:-4])
df_T['# timestamp'] = pd.to_datetime(df_T['# timestamp'])
df_T.set_index('# timestamp',inplace=True)

df_T_mass = pd.read_csv('Tm_all.csv',skiprows=range(8))
df_T_mass['# timestamp'] = df_T_mass['# timestamp'].map(lambda x: str(x)[:-4])
df_T_mass['# timestamp'] = pd.to_datetime(df_T_mass['# timestamp'])
df_T_mass.set_index('# timestamp',inplace=True)
                    
fig = ppt.figure(figsize=(8,8),dpi=150)   
ppt.ioff()
ax = fig.add_subplot(111)

lns2 = ax.plot(df_T.iloc[0],df_T.iloc[0],'r')
lns1 = ax.plot(df_T.iloc[0],df_T_mass.iloc[0],marker='x',ls='None')

ax.set_xlabel('air temperature')
ax.set_ylabel('mass temperature')
fig.show()
ppt.savefig('Results/air_vs_mass_temperature_atinit.png', bbox_inches='tight')

fig, ax = ppt.subplots()
df_T.iloc[0].hist(ax=ax)
fig.savefig('Results/init_T_air_distribution.png')

fig, ax = ppt.subplots()
df_T.iloc[-1].hist(ax=ax)
fig.savefig('Results/1month_T_air_distribution.png')

fig, ax = ppt.subplots()
df_T_mass.iloc[-1].hist(ax=ax)
fig.savefig('Results/1month_T_mass_distribution.png')

#In time for a single house
col = df_T.columns[0]

fig = ppt.figure(figsize=(8,8),dpi=150)   
ppt.ioff()
ax = fig.add_subplot(111)

lns2 = ax.plot(df_T[col],df_T[col],'r')
lns1 = ax.plot(df_T[col],df_T_mass[col],marker='x',ls='-')

ax.set_xlabel('air temperature')
ax.set_ylabel('mass temperature')
fig.show()
ppt.savefig('Results/air_vs_mass_temperature_house.png', bbox_inches='tight')