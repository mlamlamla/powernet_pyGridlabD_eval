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
run = 'FinalReport2'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_final2.csv'
df_settings = pd.read_csv(settings_file)
ind = '0091'

start = pd.Timestamp(2016, 7, 16)
end = pd.Timestamp(2016, 7, 17)
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

#import pdb; pdb.set_trace()
df_system['local_demand'] = df_system['total_load_houses']  + df_system['flex_EV'] + df_system['flex_batt_demand']

df_system['basesupply'] = df_system['local_demand'] - df_system['flex_pv'] - df_system['flex_batt_supply']
df_system['basesupply_d1'] = df_system['basesupply'] + df_system['flex_pv']
df_system['basesupply_d2'] = df_system['basesupply_d1'] + df_system['flex_batt_supply']


df_system_d = df_system.loc[start:end]
#import pdb; pdb.set_trace()
print('Price LEM')
print(df_system_d['clearing_price'].mean())
print(df_system_d['clearing_price'].var())
print('Price WS')
print(df_system_d['WS'].mean())
print(df_system_d['WS'].var())
print('Deviation LEM')
print((df_system_d['clearing_price']-df_system_d['WS']).mean())
#df_system_d = df_system_d.loc[df_system_d['basesupply'] < 0]
df_system_energy = df_system_d.sum(axis=0)/60.
print(df_system_energy)

#df_system['losses']
lw = 1
#lns = ax.plot(df_system.index,df_system['basesupply'],linewidth=lw,label='WS supply')
#ax.fill_between(df_system.loc[df_system['basesupply'] > 0].index, 0*df_system['basesupply'].loc[df_system['basesupply'] > 0], df_system['basesupply'].loc[df_system['basesupply'] > 0],alpha=0.5)
#lns = lns + ax.plot(df_system.index,df_system['basesupply_d1'],linewidth=lw,label='PV supply')
#ax.fill_between(df_system.loc[df_system['basesupply'] > 0].index, df_system['basesupply'].loc[df_system['basesupply'] > 0], df_system['basesupply_d1'].loc[df_system['basesupply'] > 0],alpha=0.5)
#lns = lns + ax.plot(df_system.index,df_system['basesupply_d2'],linewidth=lw,label='battery supply')
#ax.fill_between(df_system.loc[df_system['basesupply'] > 0].index, df_system['basesupply_d1'].loc[df_system['basesupply'] > 0], df_system['basesupply_d2'].loc[df_system['basesupply'] > 0],alpha=0.5)

#Piecewise
df_system_pos1 = df_system.loc[:pd.Timestamp(2016, 7, 16,18)]
ax.fill_between(df_system_pos1.index, 0, df_system_pos1['basesupply'],color='#1f77b4',alpha=0.5)
ax.fill_between(df_system_pos1.index, df_system_pos1['basesupply'], df_system_pos1['basesupply_d1'],color='#ff7f0e',alpha=0.5)
ax.fill_between(df_system_pos1.index, df_system_pos1['basesupply_d1'], df_system_pos1['basesupply_d2'],color='#d62728',alpha=0.5)

# df_system_neg1 = df_system.loc[pd.Timestamp(2016, 7, 16,18):pd.Timestamp(2015, 7, 16,20,29)]
# #ax.fill_between(df_system_neg1.index, 0, df_system_neg1['basesupply'],alpha=0.5)
# ax.fill_between(df_system_neg1.index, df_system_neg1['basesupply'], df_system_neg1['basesupply_d1'],color='#ff7f0e',alpha=0.5)
# ax.fill_between(df_system_neg1.index, df_system_neg1['basesupply_d1'], df_system_neg1['basesupply_d2'],color='#d62728',alpha=0.5)

# df_system_pos2 = df_system.loc[pd.Timestamp(2016, 7, 16,20,29):]
# ax.fill_between(df_system_pos2.index, 0, df_system_pos2['basesupply'],color='#1f77b4',alpha=0.5)
# ax.fill_between(df_system_pos2.index, df_system_pos2['basesupply'], df_system_pos2['basesupply_d1'],color='#ff7f0e',alpha=0.5)
# ax.fill_between(df_system_pos2.index, df_system_pos2['basesupply_d1'], df_system_pos2['basesupply_d2'],color='#d62728',alpha=0.5)

lns = ax.plot(df_system.index,df_system['basesupply'],linewidth=lw,color='#1f77b4',label='WS supply')
df_system['basesupply_d1'].loc[df_system['flex_pv'] == 0.] = 0.
lns = lns + ax.plot(df_system.index,df_system['basesupply_d1'],linewidth=lw,color='#ff7f0e',label='PV supply')
df_system['basesupply_d2'].loc[df_system['flex_batt_supply'] == 0.] = 0.
lns = lns + ax.plot(df_system.index,df_system['basesupply_d2'],linewidth=lw,color='#d62728',label='battery supply')

#import pdb; pdb.set_trace()
#C = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(ind))]['line_capacity'].iloc[0]/1000.
#lns = lns + ax.plot(df_system.index,[C]*len(df_system.index),'r',dashes=[5, 5, 5, 5],linewidth=1.0,label='capacity constraint')
	
ax.plot(df_system.index,[0.0]*len(df_system.index),'k',linewidth=1.0)

ax.set_ylabel('Supply [MW]')
ax.set_xlim(xmin=start, xmax=end)
ax.set_ylim(ymin=-0.25,ymax=2.0) #, ymax=2.1)

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
print(directory+'/13_disaggregated_supply.png')
ppt.savefig(directory+'/13_disaggregated_supply.png', bbox_inches='tight')


