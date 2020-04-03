import os
import pandas as pd
import matplotlib.pyplot as ppt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from numpy import arange 

plot_type = 'Cap' #'flex_houses'

#Which run
run = 'FinalReport' #'FinalReport_Jul1d'
inds = ['0013','0032','0033','0034']
inds = ['0035','0036','0037','0038']
perc = 10.0

#settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_Jan_1d.csv'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_final.csv'

#PREPARE measured load data
df_measured_load = pd.DataFrame()
for ind in inds:
	folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
	df_slack = pd.read_csv(folder+'/load_node_149.csv',skiprows=range(8))
	df_slack['# timestamp'] = df_slack['# timestamp'].map(lambda x: str(x)[:-4])
	df_slack = df_slack.iloc[:-1]
	df_slack['# timestamp'] = pd.to_datetime(df_slack['# timestamp'])
	df_slack.set_index('# timestamp',inplace=True)
	df_slack['measured_real_power'] = df_slack['measured_real_power']/1000
	try:
		df_PV = pd.read_csv(folder+'/total_P_Out.csv',skiprows=range(8))
		colNames = df_PV.columns[df_PV.columns.str.contains(pat = 'PV_')] 
		print('Max PV infeed for '+str(ind)+': '+str(df_PV[colNames].iloc[int(len(df_PV)/2):].sum(axis=1).max()/1000))
	except:
		pass
	df_measured_load[ind] = df_slack['measured_real_power']

df_measured_load.dropna(inplace=True)
df_measured_load = df_measured_load.iloc[int(len(df_measured_load)/2):]

N = int(round(len(df_measured_load)*perc/100,0)) + 5

fig = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
#House load
ax = fig.add_subplot(111)

df_measured_load.sort_values(by=inds[0],ascending=False,inplace=True)
df_measured_load['index'] = range(len(df_measured_load))
df_measured_load['index'] = df_measured_load['index']/len(df_measured_load)*100
df_measured_load.set_index('index',inplace=True)
lns1 = ax.plot(df_measured_load[inds[0]].iloc[:N]/1000,'r',label='no constraint')

df_measured_load.sort_values(inds[1],ascending=False,inplace=True)
df_measured_load['index2'] = range(len(df_measured_load))
df_measured_load['index2'] = df_measured_load['index2']/len(df_measured_load)*100
df_measured_load.set_index('index2',inplace=True)
ax.plot(df_measured_load.index,[1.7]*len(df_measured_load.index),'b',dashes=[5,5])
lns2 = ax.plot(df_measured_load[inds[1]].iloc[:N]/1000,'b',label='C = 1.5 MW')

df_measured_load.sort_values(inds[2],ascending=False,inplace=True)
df_measured_load['index3'] = range(len(df_measured_load))
df_measured_load['index3'] = df_measured_load['index3']/len(df_measured_load)*100
df_measured_load.set_index('index3',inplace=True)
ax.plot(df_measured_load.index,[1.6]*len(df_measured_load.index),'g',dashes=[5,5])
lns3 = ax.plot(df_measured_load[inds[2]].iloc[:N]/1000,'g',label='C = 1.4 MW')

df_measured_load.sort_values(inds[3],ascending=False,inplace=True)
df_measured_load['index4'] = range(len(df_measured_load))
df_measured_load['index4'] = df_measured_load['index4']/len(df_measured_load)*100
df_measured_load.set_index('index4',inplace=True)
ax.plot(df_measured_load.index,[1.5]*len(df_measured_load.index),'y',dashes=[5,5])
lns4 = ax.plot(df_measured_load[inds[3]].iloc[:N]/1000,'y',label='C = 1.3 MW')

ax.set_xlabel('Percentiles [%]')
ax.set_ylabel('Measured system load [MW]')
ax.set_xlim(xmin=0,xmax=perc)

#Legend
lns = lns1 + lns2 + lns3 + lns4
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.4), loc='lower center', ncol=len(labs))
#L.get_texts()[0].set_text('Total system load')
#L.get_texts()[1].set_text('Total unresponsive system load')
ppt.savefig(run+'load_curve_1120.png', bbox_inches='tight')