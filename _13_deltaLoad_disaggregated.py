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
ind = '0090'
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind
directory = run + '/' + run + '_' + ind + '_vis'
df_system1 = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True).loc[start:end]
df_system1['local_demand'] = df_system1['total_load_houses']  + df_system1['flex_EV'] + df_system1['flex_batt_demand']
df_system1 = df_system1[['local_demand','total_load_houses','inflex_hvac','flex_hvac','flex_EV','flex_batt_demand']]

#Constrained
ind = '0091'
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind
directory = run + '/' + run + '_' + ind + '_vis'
df_system2 = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True).loc[start:end]
import pdb; pdb.set_trace()
df_system2['local_demand'] = df_system2['total_load_houses']  + df_system2['flex_EV'] + df_system2['flex_batt_demand']
df_system2 = df_system2[['local_demand','total_load_houses','inflex_hvac','flex_hvac','flex_EV','flex_batt_demand']]

df_system = df_system2 - df_system1 #Change from unconstrained to constrained

df_system['baseload'] = df_system['total_load_houses'] - df_system['flex_hvac'] - df_system['inflex_hvac']
df_system['baseload_d1'] = df_system['baseload'] + df_system['inflex_hvac']
df_system['baseload_d2'] = df_system['baseload_d1'] + df_system['flex_hvac']
df_system['baseload_d3'] = df_system['baseload_d2'] + df_system['flex_EV']
df_system['baseload_d4'] = df_system['baseload_d3'] + df_system['flex_batt_demand']

#import pdb; pdb.set_trace()

df_system['zero'] = 0.0
df_system['baseload_min'] = df_system[["zero", "baseload"]].min(axis=1)

#Start figure
fig = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
ax = fig.add_subplot(111)
lns = None

lw = 1
# ax.fill_between(df_system.index, df_system['baseload_min'], df_system['baseload'],alpha=0.5)
# #lns = lns + ax.plot(df_system.index,df_system['baseload_d1'],label='inflexible HVAC') #for 0077: is ZERO
# ax.fill_between(df_system.index, df_system['baseload'], df_system['baseload_d2'],alpha=0.5)
# ax.fill_between(df_system.index, df_system['baseload_d2'], df_system['baseload_d3'],alpha=0.5)
# ax.fill_between(df_system.index, df_system['baseload_d3'], df_system['baseload_d4'],alpha=0.5)

# lns = ax.plot(df_system.index,df_system['baseload'],linewidth=lw,label='baseload')
# lns = lns + ax.plot(df_system.index,df_system['baseload_d2'],linewidth=lw,label='flexible HVAC')

# lns = lns + ax.plot(df_system.index,df_system['baseload_d4'],linewidth=lw,color='#d62728',label='battery load')
# lns = lns + ax.plot(df_system.index,df_system['baseload_d3'],linewidth=lw,color='#2ca02c',label='EV load')

lns = ax.plot(df_system.index,df_system['baseload'],linewidth=lw,label='baseload')
lns = lns + ax.plot(df_system.index,df_system['flex_hvac'],linewidth=lw,label='flexible HVAC')

lns = lns + ax.plot(df_system.index,df_system['flex_batt_demand'],linewidth=lw,color='#d62728',label='battery load')
lns = lns + ax.plot(df_system.index,df_system['flex_EV'],linewidth=lw,color='#2ca02c',label='EV load')

	
ax.plot(df_system.index,[0.0]*len(df_system.index),'k',linewidth=1.0)

ax.set_ylabel('Demand change [MW]')
ax.set_xlim(xmin=start, xmax=end)
#ax.set_ylim(ymin=0.0) #, ymax=2.1)

ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 6)))
ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 3)))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

#Legend
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=len(labs))
print(directory+'/13_disaggregated_deltaLoad_'+ind+'.png')
ppt.savefig(directory+'/13_disaggregated_deltaLoad'+ind+'.png', bbox_inches='tight')