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
inds = ['0001','0025','0059']

start = pd.Timestamp(2015, 7, 16)

#Start figure
fig = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
ax = fig.add_subplot(111)
lns = None

ind = inds[1]
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
directory = run + '_' + ind + '_vis'
df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True)
C = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(ind))]['line_capacity'].iloc[0]/1000
ax.plot(df_system.index,[C]*len(df_system.index),'r',linewidth=1.0,dashes=[5,5])
ax.plot(df_system.index,[0.0]*len(df_system.index),'k',linewidth=1.0)

ax2 = ax.twinx()
ax2.set_ylabel('Price [USD/MW]')
lns = ax2.plot(df_system.index,df_system['WS'],'k',label='WS price',dashes=[2.5,2.5]) 
lns = lns + ax2.plot(df_system.index,df_system['clearing_price'],'k',label='LEM price') 

labels= ['no market/no devices','25% PV/25% Batteries, no constraint','25% PV/25% Batteries, C = '+str(C)+' MW']

i = 0
for ind in inds:
	folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
	directory = run + '_' + ind + '_vis'
	df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True)
	flex_houses = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(ind))]['flexible_houses']
	lns = lns + ax.plot(df_system.index,df_system['measured_real_power'],label=labels[i])
	i += 1

ax.set_ylabel('Measured system load [MW]')
ax.set_xlim(xmin=start, xmax=df_system.index[-1])
#ax.set_ylim(ymin=0.0, ymax=2.0)

ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))


#lns = lns + ax2.plot(df_system.index,df_system['WS'],'k',dashes=[5, 5, 5, 5],label='WS price') 
ax2.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
ax2.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
ax2.xaxis.set_major_formatter(DateFormatter('%H:%M'))

#Legend
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.4), loc='lower center', ncol=3)
ppt.savefig(run+'/10_measuredload_Batteries.png', bbox_inches='tight')
