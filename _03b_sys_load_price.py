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

def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)

#Which run
run = 'Paper'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_paper.csv'
df_settings = pd.read_csv(settings_file)
ind = '0006'



#Start figure
fig = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
ax = fig.add_subplot(111)
lns = None

folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind
directory = run + '/' + run + '_' + ind + '_vis'
df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True)
start = pd.Timestamp(2015, 7, 14)
start = df_system.index[0]

lns = ax.plot(df_system.index,df_system['measured_real_power'],label='measured real power')

#import pdb; pdb.set_trace()
C = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(ind))]['line_capacity'].iloc[0]/1000.
lns = lns + ax.plot(df_system.index,[C]*len(df_system.index),'r',dashes=[5, 5, 5, 5],linewidth=1.0,label='capacity constraint')
	
ax.plot(df_system.index,[0.0]*len(df_system.index),'k',linewidth=1.0)

ax.set_ylabel('Measured system load [MW]')
ax.set_xlim(xmin=start, xmax=df_system.index[-1])
ax.set_ylim(ymin=-0.4, ymax=2.1)

ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 24)))
ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
ax.xaxis.set_major_formatter(DateFormatter('%m/%d'))
#ax.xaxis.set_major_formatter(DateFormatter('%d:%m %H:%M'))

#import pdb; pdb.set_trace()
ax2 = ax.twinx()
ax2.set_ylabel('Price [USD/MW]')
lns = lns + ax2.plot(df_system.index,df_system['clearing_price'],'g',label='LEM price') 
lns = lns + ax2.plot(df_system.index,df_system['WS'],'g',dashes=[1, 1],label='WS price') 
ax2.xaxis.set_major_locator(HourLocator(arange(0, 25, 24)))
ax2.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
ax2.xaxis.set_major_formatter(DateFormatter('%m/%d'))
#ax2.set_ylim(ymin=-50.,ymax=110)

align_yaxis(ax, 0, ax2, 0)

#Legend
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=len(labs))
ppt.savefig(directory +'/03b_measuredload_price.png', bbox_inches='tight')

###Market Clearing###
import market_functions as Mfcts
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind
df_buy_bids = pd.read_csv(folder+'/df_buy_bids.csv',index_col=[0], parse_dates=['timestamp'])
df_supply_bids = pd.read_csv(folder+'/df_supply_bids.csv',index_col=[0], parse_dates=['timestamp'])

time_stamp = pd.Timestamp(2015,7,16,16,5)

retail = Mfcts.Market()
retail.Pmax = 100
retail.Qlabel = 'Quantity in [MW]'
retail.Plabel = 'Price in [USD/MW]'

df_buy_bids_t = df_buy_bids.loc[df_buy_bids['timestamp'] == time_stamp]
df_supply_bids_t = df_supply_bids.loc[df_supply_bids['timestamp'] == time_stamp]

for ind in df_buy_bids_t.index:
	retail.buy(df_buy_bids_t['bid_quantity'].loc[ind]/1000.,df_buy_bids_t['bid_price'].loc[ind])
for ind in df_supply_bids_t.index:
	retail.sell(df_supply_bids_t['bid_quantity'].loc[ind]/1000.,df_supply_bids_t['bid_price'].loc[ind])

retail.clear()
print(retail.Pd)
#import pdb; pdb.set_trace()
retail.plot(directory,dt=str(time_stamp))
