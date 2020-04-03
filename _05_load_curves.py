import os
import pandas as pd
import matplotlib.pyplot as ppt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from numpy import arange 

#Which run
run = 'FinalReport2'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_final2.csv'
df_settings = pd.read_csv(settings_file)
inds = ['0010','0016','0017','0018']
inds = ['0013','0052','0051','0050']
inds = ['0010','0056','0053','0054','0055']

start = pd.Timestamp(2015, 7, 16)

#Start figure
fig = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
ax = fig.add_subplot(111)
lns = None

for ind in inds:
	folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
	directory = run + '_' + ind + '_vis'
	df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], usecols=[0,1], parse_dates=True)
	df_system = df_system.loc[df_system.index >= start]
	df_system.sort_values(by='measured_real_power',ascending=False,inplace=True)
	df_system['time']= df_system.index
	df_system['index'] = range(len(df_system))
	df_system['index'] = df_system['index']/len(df_system)*100
	df_system.set_index('index',inplace=True)
	C = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(ind))]['line_capacity'].iloc[0]/1000
	print(ind+' with C = '+str(C))
	if lns:
		lns = lns + ax.plot(df_system.index,df_system['measured_real_power'],label=str(C)+' MW')
		ax.plot(df_system.index,[C]*len(df_system.index),'r',dashes=[5,5])
		df_system_C = df_system.loc[df_system['measured_real_power'] > C]
		if len(df_system_C) > 0:
			print('max: '+str(df_system_C['measured_real_power'].iloc[0]))
			print('no of times C was exceeded: '+str(len(df_system_C.index)))
			print('percentage of times C was exceeded: '+str(df_system_C.index[-1]))
			print('total energy for times C was exceeded: '+str(df_system_C['measured_real_power'].sum()))
			print('mean energy for times C was exceeded: '+str(df_system_C['measured_real_power'].mean()))
			df_system_C_market = df_system_C.loc[df_system_C['time'].dt.minute%5 == 0]
			print('no of times C was exceeded at interval: '+str(len(df_system_C.index)))
		else:
			print('Constraint not violated')
	else:
		lns = ax.plot(df_system.index,df_system['measured_real_power'],label='no constraint')

ax.set_xlabel('Percentile of market intervals [%], sorted by measured real power')	
ax.set_ylabel('Measured system load [MW]')
ax.set_xlim(xmin=0.0, xmax=3.0)
ax.set_ylim(ymin=1.4, ymax=1.9)

#Legend
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.4), loc='lower center', ncol=len(labs))
#ppt.savefig(run+'/05_HVACwConstraints_loadcurve.png', bbox_inches='tight')
ppt.savefig(run+'/09_HVACwConstraints_perfectforecast_560.png', bbox_inches='tight')
