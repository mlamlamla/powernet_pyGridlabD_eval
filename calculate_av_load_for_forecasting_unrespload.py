# -*- coding: utf-8 -*-
"""
Created on Mon May 13 11:26:48 2019

@author: MLA
"""
import pandas as pd
import datetime

#How to calculate unresponsive loads:
#Measured_real_power
#Subtract all actve loads: Market clearing vol - batt - 

#Inflexible houses are inflexible only
#Flexible houses have flexible and inflexible part

#calculates average unresponsive load
folder = 'Results/0002_nomarket'
folder2 = 'Results/1week_nomarket'
n_inelastic = 1241 - 300

#Read in load at Slack node
df_load = pd.read_csv(folder+'/load_node_149.csv',skiprows=range(8))
df_load['# timestamp'] = df_load['# timestamp'].map(lambda x: str(x)[:-4])
df_load = df_load.iloc[:-1]
df_load['# timestamp'] = pd.to_datetime(df_load['# timestamp'])
df_load.set_index('# timestamp',inplace=True)
df_load['measured_real_power'] = df_load['measured_real_power']/1000

#Active and unresponsive loads
df_cleared = pd.read_csv(folder+'/clearing_pq.csv',parse_dates=['timedate'],usecols=[2,3,4])
df_cleared.set_index('timedate',inplace=True)
df_unresp = pd.read_csv(folder+'/unresponsive_loads.csv',parse_dates=['timedate'],usecols=[2,3,4,5])
df_unresp.set_index('timedate',inplace=True)

df_load= df_load.merge(df_cleared,how='outer',left_index=True,right_index=True)
df_load= df_load.merge(df_unresp,how='outer',left_index=True,right_index=True)
df_load.fillna(method='ffill',inplace=True)

#Calculate active loads and suppliers
#cleared_q - unresponsive (as submitted)
df_load['active_actual'] = df_load['clearing_quantity'] - df_load['unresp_load']
df_load['active_actual'].loc[df_load['active_actual'] < 0.0] = 0.0
df_load['unresp_actual'] = df_load['measured_real_power'] - df_load['active_actual']

#Find forecast: Discard first day and find max of every 5min interval
#df_load = df_load.loc[df_load.index > datetime.datetime(2015,7,1,23,59)]
df_load_max = pd.DataFrame(index=df_load.index,columns=['unresp_actual'],data=df_load['unresp_actual'].resample("5min").max())
df_load_max.dropna(axis=0,inplace=True)
df_load_max.to_csv('perfect_unresp_load_forecast_300.csv')

#Average load forecast
#df_load_max['Time'] = df_load_max.index
#df_load_max['Time'] = df_load_max['Time'].map(lambda x: pd.datetime(x.year, x.month, 1, x.hour, x.minute))
#df_load_max_d = df_load_max.groupby('Time',axis=0).mean() #Average unresponsive load

#Split into elastic (with hvac being flexible) and inelastic houses



#df_awarded = pd.read_csv(folder+'/awarded_bids.csv',parse_dates=['timedate'],index_col=[0])
#df_awarded.drop(['p_bid','id'],axis=1,inplace=True)
#ser_awarded = df_awarded.groupby('timedate').sum()
#df_awarded = pd.DataFrame(index=ser_awarded.index,data=ser_awarded,columns=['Q_bid'])
#
#df_load_max = df_load_max.merge(df_awarded, how='inner', left_index=True, right_index=True)
#df_load_max['unresp_max'] = df_load_max['measured_real_power'] - df_load_max['Q_bid']
#
#df_unresp = pd.read_csv(folder+'/unresponsive_loads.csv',parse_dates=['timedate'],usecols=[2,3,4,5])
#df_unresp.set_index('timedate',inplace=True)
#
#df_load_max = df_load_max.merge(df_unresp, how='inner', left_index=True, right_index=True)
#df_load_max_av = df_load_max['unresp_max'].groupby(df_load_max.index.time).mean()/n_inelastic
#
#df_load_max_av.to_csv('av_unresp_load.csv')
