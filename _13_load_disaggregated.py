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
run = 'FinalReport2' #'Paper'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_final2.csv'
df_settings = pd.read_csv(settings_file)
ind = '0091'

start = pd.Timestamp(2015, 7, 16)
end = pd.Timestamp(2015, 7, 17)

#Start figure
fig = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
ax = fig.add_subplot(111)
lns = None

folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind
directory = run + '/' + run + '_' + ind + '_vis'
df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True)

df_system['baseload'] = df_system['total_load_houses'] - df_system['flex_hvac'] - df_system['inflex_hvac']
df_system['baseload_d1'] = df_system['baseload'] + df_system['inflex_hvac']
df_system['baseload_d2'] = df_system['baseload_d1'] + df_system['flex_hvac']
df_system['baseload_d3'] = df_system['baseload_d2'] + df_system['flex_EV']
df_system['baseload_d4'] = df_system['baseload_d3'] + df_system['flex_batt_demand']

#df_system['losses']
lw = 1
ax.fill_between(df_system.index, 0, df_system['baseload'],alpha=0.5)
#lns = lns + ax.plot(df_system.index,df_system['baseload_d1'],label='inflexible HVAC') #for 0077: is ZERO
ax.fill_between(df_system.index, df_system['baseload'], df_system['baseload_d2'],alpha=0.5)
ax.fill_between(df_system.index, df_system['baseload_d2'], df_system['baseload_d3'],alpha=0.5)
ax.fill_between(df_system.index, df_system['baseload_d3'], df_system['baseload_d4'],alpha=0.5)

lns = ax.plot(df_system.index,df_system['baseload'],linewidth=lw,label='baseload')
lns = lns + ax.plot(df_system.index,df_system['baseload_d2'],linewidth=lw,label='flexible HVAC')
#df_system['baseload_d3'].loc[df_system['flex_EV'] == 0.] = 0.

#df_system['baseload_d4'].loc[df_system['flex_batt_demand'] == 0.] = 0.
lns = lns + ax.plot(df_system.index,df_system['baseload_d4'],linewidth=lw,color='#d62728',label='battery load')
lns = lns + ax.plot(df_system.index,df_system['baseload_d3'],linewidth=lw,color='#2ca02c',label='EV load')

#import pdb; pdb.set_trace()
#C = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(ind))]['line_capacity'].iloc[0]/1000.
#lns = lns + ax.plot(df_system.index,[C]*len(df_system.index),'r',dashes=[5, 5, 5, 5],linewidth=1.0,label='capacity constraint')
	
ax.plot(df_system.index,[0.0]*len(df_system.index),'k',linewidth=1.0)

ax.set_ylabel('Demand [MW]')
ax.set_xlim(xmin=start, xmax=end)
ax.set_ylim(ymin=0.0, ymax=1.85)

ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 6)))
ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 3)))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
#ax.xaxis.set_major_formatter(DateFormatter('%d:%m %H:%M'))

#import pdb; pdb.set_trace()
# ax2 = ax.twinx()
# ax2.set_ylabel('Price [USD/MW]')
# lns = lns + ax2.plot(df_system.index,df_system['clearing_price'],'g',label='LEM price') 
# lns = lns + ax2.plot(df_system.index,df_system['WS'],'g',dashes=[1, 1],label='WS price') 
# ax2.xaxis.set_major_locator(HourLocator(arange(0, 25, 24)))
# ax2.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
# ax2.xaxis.set_major_formatter(DateFormatter('%m/%d'))
# #ax2.set_ylim(ymin=-50.,ymax=110)

# align_yaxis(ax, 0, ax2, 0)

#Legend
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=len(labs))
ppt.savefig(directory+'/13_disaggregated_load.png', bbox_inches='tight')


