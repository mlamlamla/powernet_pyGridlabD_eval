import os
import pandas as pd
import system_analyses as sysev
import house_analyses as hev
import battery_analyses as bev
import EV_analyses as EVev
import market_analyses as mev
import welfare_analyses as wev
from numpy import arange 

import matplotlib.pyplot as ppt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange

#Which run
run = 'FinalReport2'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_final2.csv'
df_settings = pd.read_csv(settings_file)

start = pd.Timestamp(2015, 7, 16)
end = pd.Timestamp(2015, 7, 17)

#Unonstrained
ind = '0083'
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind
directory = run + '/' + run + '_' + ind + '_vis'
df_system1 = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True).loc[start:end]
df_system1['local_demand'] = df_system1['total_load_houses']  + df_system1['flex_EV'] + df_system1['flex_batt_demand']
df_system1 = df_system1[['local_demand','total_load_houses','flex_pv','flex_batt_supply']]

#Constrained
ind = '0082'
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind
directory = run + '/' + run + '_' + ind + '_vis'
df_system2 = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True).loc[start:end]
df_system2['local_demand'] = df_system2['total_load_houses']  + df_system2['flex_EV'] + df_system2['flex_batt_demand']
df_system2 = df_system2[['local_demand','total_load_houses','flex_pv','flex_batt_supply']]

df_system = df_system2 - df_system1 #Change from unconstrained to constrained

df_system['basesupply'] = df_system['local_demand'] - df_system['flex_pv'] - df_system['flex_batt_supply']
df_system['basesupply_d1'] = df_system['basesupply'] + df_system['flex_pv']
df_system['basesupply_d2'] = df_system['basesupply_d1'] + df_system['flex_batt_supply']

df_system['zero'] = 0.0
df_system['basesupply_min'] = df_system[["zero", "basesupply"]].min(axis=1)

#import pdb; pdb.set_trace()

#Start figure
fig = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
ax = fig.add_subplot(111)
lns = None

lw = 1
# ax.fill_between(df_system.index, df_system['basesupply_min'], df_system['basesupply'],color='#1f77b4',alpha=0.5)
# ax.fill_between(df_system.index, df_system['basesupply'], df_system['basesupply_d1'],color='#ff7f0e',alpha=0.5)
# ax.fill_between(df_system.index, df_system['basesupply_d1'], df_system['basesupply_d2'],color='#d62728',alpha=0.5)

# lns = ax.plot(df_system.index,df_system['basesupply'],linewidth=lw,color='#1f77b4',label='WS supply')
# df_system['basesupply_d1'].loc[df_system['flex_pv'] == 0.] = 0.
# lns = lns + ax.plot(df_system.index,df_system['basesupply_d1'],linewidth=lw,color='#ff7f0e',label='PV supply')
# df_system['basesupply_d2'].loc[df_system['flex_batt_supply'] == 0.] = 0.
# lns = lns + ax.plot(df_system.index,df_system['basesupply_d2'],linewidth=lw,color='#d62728',label='battery supply')

lns = ax.plot(df_system.index,df_system['basesupply'],linewidth=lw,color='#1f77b4',label='WS supply')
lns = lns + ax.plot(df_system.index,df_system['flex_pv'],linewidth=lw,color='#ff7f0e',label='PV supply')
lns = lns + ax.plot(df_system.index,df_system['flex_batt_supply'],linewidth=lw,color='#d62728',label='battery supply')


	
ax.plot(df_system.index,[0.0]*len(df_system.index),'k',linewidth=1.0)

ax.set_ylabel('Supply change [MW]')
ax.set_xlim(xmin=start, xmax=end)
#ax.set_ylim(ymin=0.0) #, ymax=2.1)

ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 6)))
ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 3)))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

#Legend
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=len(labs))
ppt.savefig(directory+'/13_disaggregated_deltaSupply.png', bbox_inches='tight')