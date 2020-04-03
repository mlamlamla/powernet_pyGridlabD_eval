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
run = 'Paper'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_paper.csv'
df_settings = pd.read_csv(settings_file)

#folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '/' + run + '_' + ind
ind = '0009'
results = run + '/' + run + '_' + ind + '_vis'
df_system_PVgen = pd.read_csv(results+'/df_system.csv',index_col=[0], parse_dates=True)

df_bids = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run+'_'+ind+'/'+'df_supply_bids.csv', parse_dates=True)
df_bids.drop(index=df_bids.loc[df_bids['appliance_name'] == 'WS'].index,axis=0,inplace=True)
df_bids_PV = df_bids.groupby('timestamp').sum()
df_bids_PV.index = pd.to_datetime(df_bids_PV.index)

#import pdb; pdb.set_trace()

# Start figure
fig = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
ax = fig.add_subplot(111)

lns1 = ax.plot(df_system_PVgen.index,df_system_PVgen['flex_pv'],label='PV generation')
lns2 = ax.step(df_bids_PV.index,df_bids_PV['bid_quantity']/1000,where='post',label='PV bids')

#ax2 = ax.twinx()
#ax2.set_ylabel('Price [USD/MW]')
#lns = ax2.plot(df_system.index,df_system['WS'],'k',label='WS price',dashes=[2.5,2.5]) 
#lns = lns + ax2.plot(df_system.index,df_system['clearing_price'],'k',label='LEM price') 

#All devices
# ind = inds[2]
# folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
# directory = run + '_' + ind + '_vis'
# df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True)
# lns = lns + ax.plot(df_system.index,df_system['measured_real_power'],label='25% PV/Batt/EVs')

ax.plot(df_system_PVgen.index,[0.0]*len(df_system_PVgen.index),'k',linewidth=1.0)

ax.set_ylabel('PV generation [MW]')
start = pd.Timestamp(2016, 7, 16) # df_system_fast.index[0]
end = pd.Timestamp(2016, 7, 17) # df_system_fast.index[-1]
ax.set_xlim(xmin=start, xmax=end)
ax.set_ylim(ymin=0.0)

ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 1)))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

ax2 = ax.twinx()

df = pd.DataFrame(index=df_system_PVgen.index,columns=['flex_pv'],data=df_system_PVgen['flex_pv'])
df2 = pd.DataFrame(index=df_bids_PV.index,columns=['bid_quantity'],data=df_bids_PV['bid_quantity'])
df_comp = df.merge(df2, how='outer', left_index=True, right_index=True)

#import pdb; pdb.set_trace()

df_comp['bid_quantity'].iloc[0] = 0.0
df_comp['bid_quantity'].loc[df2.index[-1] + pd.Timedelta('5min')] = 0.0
df_comp.fillna(method='ffill',inplace=True)

df_comp['delta'] = df_comp['flex_pv'] - df_comp['bid_quantity']/1000
ax2.set_ylabel('Error in [kW]')
lns3 = ax2.plot(df_comp['delta']*1000,color='green',label='PV error')

#import pdb; pdb.set_trace()

lns = lns1 + lns2 + lns3

#Legend
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=len(labs))
ppt.savefig(results+'/20_measuredPV.png', bbox_inches='tight')
