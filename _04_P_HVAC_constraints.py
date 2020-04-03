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
inds = ['0010','0016','0017','0018']

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
	C = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(ind))]['line_capacity'].iloc[0]/1000
	if lns:
		lns = lns + ax.plot(df_system.index,df_system['measured_real_power'],label=str(C)+' MW')
		ax.plot(df_system.index,[C]*len(df_system.index),'r',dashes=[5,5])
	else:
		lns = ax.plot(df_system.index,df_system['measured_real_power'],label='no constraint')
	
ax.plot(df_system.index,[0.0]*len(df_system.index),'k',linewidth=1.0)

ax.set_ylabel('Measured system load [MW]')
ax.set_xlim(xmin=start, xmax=df_system.index[-1])
ax.set_ylim(ymin=0.0, ymax=2.0)

ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

#Legend
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=len(labs))
ppt.savefig(run+'/04_measuredload_50HVAC_constraints.png', bbox_inches='tight')

