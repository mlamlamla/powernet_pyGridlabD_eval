# -*- coding: utf-8 -*-
"""
Created on Wed May 22 12:15:38 2019

@author: MLA

Calculate unresponsive load based on appliances
Total_load of all inelastic houses + non-HVAC load of elastic houses
"""

# -*- coding: utf-8 -*-
import pandas as pd
import datetime
import matplotlib.pyplot as ppt

folder = 'Results/0006_market'
folder2 = 'Results/1week_nomarket'
n_all = 1241
n_elastic = 300

df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8))
df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
df_total_load = df_total_load.iloc[:-1]
df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
df_total_load.set_index('# timestamp',inplace=True)
df_total_load_el = pd.DataFrame(index=df_total_load.index,columns=['total_load_el'],data=df_total_load.iloc[:,:n_elastic].sum(axis=1))
df_total_load_inel = pd.DataFrame(index=df_total_load.index,columns=['total_load_inel'],data=df_total_load.iloc[:,n_elastic:].sum(axis=1))
df_unresp_load = df_total_load_el.merge(df_total_load_inel,how='outer',left_index=True,right_index=True)

df_hvac_load = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8))
df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
df_hvac_load = df_hvac_load.iloc[:-1]
df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
df_hvac_load.set_index('# timestamp',inplace=True)                           
df_hvac_load_el = pd.DataFrame(index=df_hvac_load.index,columns=['hvac_load_el'],data=df_hvac_load.iloc[:,:n_elastic].sum(axis=1))
df_hvac_load_inel = pd.DataFrame(index=df_hvac_load.index,columns=['hvac_load_inel'],data=df_hvac_load.iloc[:,n_elastic:].sum(axis=1))
df_unresp_load = df_unresp_load.merge(df_hvac_load_el,how='outer',left_index=True,right_index=True)
df_unresp_load = df_unresp_load.merge(df_hvac_load_inel,how='outer',left_index=True,right_index=True)

fig = ppt.figure(figsize=(12,4),dpi=150)   
ax = fig.add_subplot(111)
lns1 = ax.plot(df_unresp_load['total_load_el'],'b',label='Elastic load')
lns2 = ax.plot(df_unresp_load['total_load_inel'],'g',label='Inelastic load')
ppt.show()

fig = ppt.figure(figsize=(12,4),dpi=150)   
ax = fig.add_subplot(111)
lns1 = ax.plot(df_unresp_load['hvac_load_el'],'b',label='Elastic load')
lns2 = ax.plot(df_unresp_load['hvac_load_inel'],'g',label='Inelastic load')
ppt.show()

#Question: Does total load include Batteries and EVs and PV?
df_unresp_load['unresp_actual1'] = df_unresp_load['total_load_inel'] + df_unresp_load['total_load_el'] - df_unresp_load['hvac_load_el']
df_unresp_load['unresp_nonel'] = df_unresp_load['total_load_inel']/n_all
df_unresp_load['unresp_el'] = (df_unresp_load['total_load_el'] - df_unresp_load['hvac_load_el'])/n_elastic

col1 = df_total_load.columns[163]
col2 = df_total_load.columns[164]
col3 = df_total_load.columns[165]
col4 = df_total_load.columns[166]
fig = ppt.figure(figsize=(20,4),dpi=150)   
ax = fig.add_subplot(111)
start = 0
end = 24*20
lns1 = ax.plot(df_total_load[col1].iloc[start:end],'r')#,label='Elastic load')
lns1b = ax.plot(df_hvac_load[col1].iloc[start:end],'b')#,label='Elastic load')
#lns2 = ax.plot(df_total_load[col2].iloc[start:end],'g',label='Inelastic load')
#lns3 = ax.plot(df_total_load[col3].iloc[start:end],'b',label='Elastic load')
#lns4 = ax.plot(df_total_load[col4].iloc[start:end],'k',label='Inelastic load')
ppt.show()

#Maybe grid losses missing (is also unresponsive load)? From aggregate level breaking down
#Total load + PV + Batt supply - Batt demand - EVs - active house bids

#Read in load at Slack node
df_load = pd.read_csv(folder+'/load_node_149.csv',skiprows=range(8))
df_load['# timestamp'] = df_load['# timestamp'].map(lambda x: str(x)[:-4])
df_load = df_load.iloc[:-1]
df_load['# timestamp'] = pd.to_datetime(df_load['# timestamp'])
df_load.set_index('# timestamp',inplace=True)
df_load['measured_real_power'] = df_load['measured_real_power']/1000

#+ for infeed, - for consumption
df_P_out = pd.read_csv(folder+'/total_P_Out.csv',skiprows=range(8))
df_P_out['# timestamp'] = df_P_out['# timestamp'].map(lambda x: str(x)[:-4])
df_P_out['# timestamp'] = pd.to_datetime(df_P_out['# timestamp'])
df_P_out.set_index('# timestamp',inplace=True)  
df_P_out = pd.DataFrame(index=df_P_out.index,columns=['total_inverter_inf'],data=df_P_out.sum(axis=1)/1000)
df_unresp_load2 = df_load.merge(df_P_out,how='outer',left_index=True,right_index=True)

#- awarded elastic hvacs  (now rather actual technical realization)
df_unresp_load2 = df_unresp_load2.merge(df_hvac_load_el,how='outer',left_index=True,right_index=True)
df_unresp_load2['unresp_actual2'] = df_unresp_load2['measured_real_power'] + df_unresp_load2['total_inverter_inf'] - df_unresp_load2['hvac_load_el']

fig = ppt.figure(figsize=(20,4),dpi=150)   
ax = fig.add_subplot(111)
start = 0
end = 60*24*7
lns1 = ax.plot(df_unresp_load['unresp_actual1'].iloc[start:end],'r')#,label='Elastic load')
lns2 = ax.plot(df_unresp_load2['unresp_actual2'].iloc[start:end],'b')#,label='Elastic load')
ppt.show()

#Save
df_unresp_load_all = df_unresp_load.merge(df_unresp_load2,how='outer',left_index=True,right_index=True)
df_unresp_load_all['unresp_actual'] = df_unresp_load_all[['unresp_actual1','unresp_actual2']].max(axis=1) 
df_unresp_load_all = pd.DataFrame(index=df_unresp_load_all.index,columns=['unresp_actual','unresp_el','unresp_nonel'],data=df_unresp_load_all[['unresp_actual','unresp_el','unresp_nonel']].resample("5min").max())
df_unresp_load_all.dropna(axis=0,inplace=True)
#Take max of both columns
#Take max of 5min
#Unrep load per flex house
#Unresp load per inelast house
df_unresp_load_all.to_csv(folder+'/perfect_unresp_load_forecast.csv')

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
