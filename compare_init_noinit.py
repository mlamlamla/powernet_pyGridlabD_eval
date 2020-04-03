# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 23:54:13 2019

@author: MLA
"""
import pandas as pd

df_init = pd.read_csv('Vgl_initC_hvac_load_all.csv',skiprows=range(8))
df_init['# timestamp'] = df_init['# timestamp'].map(lambda x: str(x)[:-4])
df_init = df_init.iloc[:-1]
df_init['# timestamp'] = pd.to_datetime(df_init['# timestamp'])
df_init.set_index('# timestamp',inplace=True)   
                  
df_init['Sum_t'] = df_init.sum(axis=1)
df_init['Sum_t+1'] = df_init['Sum_t'].shift(-1)
df_init_s = df_init[['Sum_t','Sum_t+1']].iloc[10:-1]
df_init_s['Diff'] = abs(df_init_s['Sum_t+1'] - df_init_s['Sum_t'])
print('Max jump init: '+str(df_init_s['Diff'].max()))

df_noinit = pd.read_csv('Vgl_noinit_hvac_load_all.csv',skiprows=range(8))
df_noinit['# timestamp'] = df_noinit['# timestamp'].map(lambda x: str(x)[:-4])
df_noinit = df_noinit.iloc[:-1]
df_noinit['# timestamp'] = pd.to_datetime(df_noinit['# timestamp'])
df_noinit.set_index('# timestamp',inplace=True) 

df_noinit['Sum_t'] = df_noinit.sum(axis=1)
df_noinit['Sum_t+1'] = df_noinit['Sum_t'].shift(-1)
df_noinit_s = df_noinit[['Sum_t','Sum_t+1']].iloc[10:-1]
df_noinit_s['Diff'] = abs(df_noinit_s['Sum_t+1'] - df_noinit_s['Sum_t'])
print('Max jump no init: '+str(df_noinit_s['Diff'].max()))

print('Max hvac load (init): '+str(df_init['Sum_t'].max()))

kwargs = dict(histtype='stepfilled', alpha=0.3, density=True, ec="k")
df_noinit_s['Diff'].hist(**kwargs)
df_init_s['Diff'].hist(**kwargs)

#(df_init_s['Diff'] - df_noinit_s['Diff']).hist()

#Number of active periods
#df_init[df_init > 0.0] = 1
#df_init[df_init == 0.0] = 0
#df_init.drop(['Sum_t','Sum_t+1'],axis=1,inplace=True)
#print('% of time on: '+str(100*df_init.sum().sum()/df_init.count().sum()))

#mean_durations = []
#for col in df_init.columns:
#    i = 0
#    durations = []
#    for ind in df_init.index:
#        if df_init[col].loc[ind] == 1:
#            i += 1
#        elif i > 0:
#            durations += [i]
#            i = 0
#        else:
#            i = 0
#    mean_durations += [sum(durations) / len(durations) ] 
#print('Mean duration: '+ str(sum(mean_durations) / len(mean_durations)))