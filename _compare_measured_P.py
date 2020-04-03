import os
import pandas as pd
import matplotlib.pyplot as ppt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from numpy import arange 

plot_type = 'Cap' #'flex_houses'

#Which run
run = 'FinalReport2' #'FinalReport_Jul1d'

if plot_type == 'PV':
	inds = ['0001','0003','0004','0005']
elif plot_type == 'Batt':
	inds = ['0001','0004','0035','0025']
elif plot_type == 'flex_houses':
	inds = ['0006','0009','0012','0015']
elif plot_type == 'Cap':
	inds = ['0010','0016','0017','0018']
	#inds = ['0013','0032','0033','0034']
	#inds = ['0025','0036','0038','0040']
else:
	import sys
	sys.exit('No such flex type')

#settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_Jan_1d.csv'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_final.csv'
market_file = 'CAISO_KETTNER_2015_7.csv'


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
for ind in inds:
	print('Max load for '+str(ind)+': '+str(df_measured_load[ind].max()))


#PREPARE WS market price
df_WS = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/glm_generation_SanDiego/'+market_file,parse_dates=[0])
df_WS.rename(columns={'Unnamed: 0':'timestamp'},inplace=True)
df_WS.set_index('timestamp',inplace=True)
df_WS['P_cap'] = 100.
df_WS['WS'] = df_WS[['DA', 'P_cap']].min(axis=1)

fig = ppt.figure(figsize=(12,4),dpi=150)   
ppt.ioff()
#House load
ax = fig.add_subplot(111)
if plot_type == 'PV':
	lns1 = ax.plot(df_measured_load.index,df_measured_load[inds[0]]/1000,label='0% PV')
	lns2 = ax.plot(df_measured_load.index,df_measured_load[inds[1]]/1000,label='10% PV')
	lns3 = ax.plot(df_measured_load.index,df_measured_load[inds[2]]/1000,label='25% PV')
	lns4 = ax.plot(df_measured_load.index,df_measured_load[inds[3]]/1000,label='50% PV')
if plot_type == 'Batt':
	lns1 = ax.plot(df_measured_load.index,df_measured_load[inds[0]]/1000,label='no flexible devices')
	lns2 = ax.plot(df_measured_load.index,df_measured_load[inds[1]]/1000,label='25% PV, 0% Batteries')
	lns3 = ax.plot(df_measured_load.index,df_measured_load[inds[2]]/1000,label='25% PV, 10% Batteries')
	lns4 = ax.plot(df_measured_load.index,df_measured_load[inds[3]]/1000,label='25% PV, 25% Batteries')
elif plot_type == 'flex_houses':
	ax2 = ax.twinx()
	ax2.set_ylabel('Price [USD/MW]')
	lns5 = ax2.plot(df_WS.index,df_WS['WS'],'k',label='WS price') 

	lns1 = ax.plot(df_measured_load.index,df_measured_load[inds[0]]/1000,label='0% HVAC')
	lns2 = ax.plot(df_measured_load.index,df_measured_load[inds[1]]/1000,label='25% HVAC')
	lns3 = ax.plot(df_measured_load.index,df_measured_load[inds[2]]/1000,label='50% HVAC')
	lns4 = ax.plot(df_measured_load.index,df_measured_load[inds[3]]/1000,label='100% HVAC')
elif plot_type == 'Cap':
	ax2 = ax.twinx()
	ax2.set_ylabel('Price [USD/MW]')
	#import pdb; pdb.set_trace()
	df_cleared = pd.read_csv(folder+'/df_prices.csv',parse_dates=[0])
	df_cleared.rename(columns={'Unnamed: 0':'timedate'},inplace=True)
	df_cleared.set_index('timedate',inplace=True)
	df_cleared = df_cleared.iloc[int(len(df_cleared)/2):]

	ax.plot(df_measured_load.index,[1.4]*len(df_measured_load.index),'r',dashes=[5,5])
	ax.plot(df_measured_load.index,[1.3]*len(df_measured_load.index),'r',dashes=[5,5])
	ax.plot(df_measured_load.index,[1.2]*len(df_measured_load.index),'r',dashes=[5,5])

	lns5 = ax2.plot(df_cleared.index,df_cleared['clearing_price'],'k',label='LEM price') 
	lns6 = ax2.plot(df_WS.index,df_WS['WS'],'k',dashes=[5, 5, 5, 5],label='WS price') 

	lns1 = ax.plot(df_measured_load.index,df_measured_load[inds[0]]/1000,label='no market')
	lns2 = ax.plot(df_measured_load.index,df_measured_load[inds[1]]/1000,label='C = 1.4 MW')
	
	lns3 = ax.plot(df_measured_load.index,df_measured_load[inds[2]]/1000,label='C = 1.2 MW')
	
	lns4 = ax.plot(df_measured_load.index,df_measured_load[inds[3]]/1000,label='C = 1.0 MW')
	

ax.plot(df_measured_load.index,[0.0]*len(df_measured_load.index),'k',linewidth=1.0)
#ax.axhline(0.0,df_measured_load.index[0],df_measured_load.index[-1])

ax.set_ylabel('Measured system load [MW]')
ax.set_xlim(xmin=df_measured_load.index[0], xmax=df_measured_load.index[-1])
#ax2.set_xlim(xmin=df_measured_load.index[0], xmax=df_measured_load.index[-1])

ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
#ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

#Legend
lns = lns1 + lns2 + lns3 + lns4 # + lns5 + lns6
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.2), loc='lower center', ncol=len(labs))
#L.get_texts()[0].set_text('Total system load')
#L.get_texts()[1].set_text('Total unresponsive system load')
ppt.savefig(run+'/'+run+'load_diff_'+plot_type+'.png', bbox_inches='tight')
