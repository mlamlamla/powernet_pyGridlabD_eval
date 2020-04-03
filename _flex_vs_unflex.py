#Calculates up time of flexible and inflexible HVACs 
import pandas as pd
import matplotlib.pyplot as ppt

from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from numpy import arange 

run = 'FinalReport2' #'FinalReport_Jul1d'
no_houses = 560

start = int(12*9) #1
end= 12*18 #-1

#Detailed analysis
ind = '0010'
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
C = 1.2

df_measured_load = pd.DataFrame()

fig = ppt.figure(figsize=(12,4),dpi=150)   
ppt.ioff()
ax = fig.add_subplot(111)

#Clearing quantity
df_cleared = pd.read_csv(folder+'/df_prices.csv',parse_dates=[0])
df_cleared.rename(columns={'Unnamed: 0':'timedate'},inplace=True)
df_cleared.set_index('timedate',inplace=True)
df_cleared = df_cleared.iloc[int(len(df_cleared)/2):]
lns1 = ax.step(df_cleared.index,df_cleared['clearing_quantity']/1000.,'r',where='post',label='clearing quantity') 

#Measured real power
df_slack = pd.read_csv(folder+'/load_node_149.csv',skiprows=range(8))
df_slack['# timestamp'] = df_slack['# timestamp'].map(lambda x: str(x)[:-4])
df_slack = df_slack.iloc[:-1]
df_slack['# timestamp'] = pd.to_datetime(df_slack['# timestamp'])
df_slack.set_index('# timestamp',inplace=True)
df_slack['measured_real_power'] = df_slack['measured_real_power']/1000
df_slack = df_slack.iloc[int(len(df_slack)/2):]
#import pdb; pdb.set_trace()
lns2 = ax.plot(df_slack.index,df_slack['measured_real_power']/1000.,'g',label='measured real power') 

#Unresp load
df_unresp = pd.read_csv(folder+'/df_buy_bids.csv',parse_dates=True)
df_unresp = df_unresp.loc[df_unresp['appliance_name'] == 'unresponsive_loads']
df_unresp.drop(['appliance_name','Unnamed: 0'],axis=1,inplace=True)
df_unresp.rename(columns={'bid_quantity': 'unresp_load'}, inplace=True)
df_unresp['timestamp'] = pd.to_datetime(df_unresp['timestamp'])
df_unresp.set_index('timestamp',inplace=True)
df_unresp = df_unresp.iloc[int(len(df_unresp)/2):]
lns3 = ax.step(df_unresp.index,df_unresp['unresp_load']/1000.,'b',where='post',label='estimate unresp. load') 

#Total load
df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8))
df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
df_total_load = df_total_load.iloc[:-1]
df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
df_total_load.set_index('# timestamp',inplace=True)
#df_total_load = pd.DataFrame(index=df_total_load.index,columns=['total_load_houses'],data=df_total_load.sum(axis=1))
df_total_load = df_total_load.sum(axis=1)
df_total_load = df_total_load.iloc[int(len(df_total_load)/2):]

#Hvac load
df_hvac_load = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8))
df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
df_hvac_load = df_hvac_load.iloc[:-1]
df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
df_hvac_load.set_index('# timestamp',inplace=True)                         
all_flexhvac = df_hvac_load.iloc[:,:no_houses].sum(axis=1)
all_inflexhvac = df_hvac_load.iloc[:,no_houses:].sum(axis=1)
all_flexhvac = all_flexhvac.iloc[int(len(all_flexhvac)/2):]

#import pdb; pdb.set_trace()
lns4 = ax.plot(df_total_load.index,(df_total_load-all_flexhvac)/1000.,'y',label='actual inflexible load') 
#lns5 = ax.plot(df_total_load.index,(df_total_load)/1000.,'y',label='total load') 

ax.plot(df_total_load.index,[C]*len(df_total_load.index),'r',dashes=[5,5])

ax.set_ylabel('Measured system load [MW]')
ax.set_xlim(xmin=df_cleared.index[start], xmax=df_cleared.index[end])
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

lns = lns1 + lns2 + lns3 + lns4 #+ lns5
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.2), loc='lower center', ncol=len(labs))

ppt.savefig(run+'_'+ind+'_vis/load_diff_cleared_vs_measured.png', bbox_inches='tight')


#Error plot
# fig = ppt.figure(figsize=(12,4),dpi=150)   
# ppt.ioff()
# ax = fig.add_subplot(111)




