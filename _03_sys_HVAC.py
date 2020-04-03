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
inds = ['0001','0007','0010','0013']

start = pd.Timestamp(2015, 7, 16)

#Start figure
fig = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
ax = fig.add_subplot(111)
lns = None

for ind in inds:
	folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
	directory = run + '_' + ind + '_vis'
	df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True)
	flex_houses = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(ind))]['flexible_houses']
	if lns:
		lns = lns + ax.plot(df_system.index,df_system['measured_real_power'],label=str(int(flex_houses/1120*100))+'% HVAC')
	else:
		lns = ax.plot(df_system.index,df_system['measured_real_power'],label=str(int(flex_houses/1120*100))+'% HVAC')
	
ax.plot(df_system.index,[0.0]*len(df_system.index),'k',linewidth=1.0)

ax.set_ylabel('Measured system load [MW]')
ax.set_xlim(xmin=start, xmax=df_system.index[-1])
ax.set_ylim(ymin=0.0, ymax=2.0)

ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

ax2 = ax.twinx()
ax2.set_ylabel('Price [USD/MW]')
lns = lns + ax2.plot(df_system.index,df_system['WS'],'k',label='LEM price') 
#lns = lns + ax2.plot(df_system.index,df_system['WS'],'k',dashes=[5, 5, 5, 5],label='WS price') 
ax2.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
ax2.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
ax2.xaxis.set_major_formatter(DateFormatter('%H:%M'))

#Legend
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=len(labs))
ppt.savefig(run+'/03_measuredload_HVAC.png', bbox_inches='tight')

#Zoom figure
ax.set_xlim(xmin=pd.Timestamp(2015, 7, 16, 7), xmax=pd.Timestamp(2015, 7, 16, 9))
ax.set_ylim(ymin=0.0, ymax=0.75)
ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 1)))
fig.set_size_inches(4,3)
ax.get_legend().remove()
ppt.savefig(run+'/03_measuredload_HVAC_07_09.png', bbox_inches='tight')

ax.set_xlim(xmin=pd.Timestamp(2015, 7, 16, 17), xmax=pd.Timestamp(2015, 7, 16, 19))
ax.set_ylim(ymin=0.0, ymax=2.0)
fig.set_size_inches(4,3)
ppt.savefig(run+'/03_measuredload_HVAC_17_19.png', bbox_inches='tight')
