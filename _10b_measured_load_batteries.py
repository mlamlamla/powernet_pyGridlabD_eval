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

#Three diagrams: aggregate power, price, battery only

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
ind = '0059' #25% PV, 25% Batt, 0 HVAC, 1300 kW; perfect forecast
start = pd.Timestamp(2015, 7, 16)

folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '/' + run + '_' + ind
directory = run + '/' + run + '_' + ind + '_vis'
df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True)
C = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(ind))]['line_capacity'].iloc[0]/1000

df_system_nobatt = pd.read_csv(run + '/' + run + '_' + '0004' + '_vis'+'/df_system.csv',index_col=[0], parse_dates=True)
#df_system_noconstraint = pd.read_csv(run + '/' + run + '_' + '0025' + '_vis'+'/df_system.csv',index_col=[0], parse_dates=True)

print(df_system.columns)

#import pdb; pdb.set_trace()

#Start figure: power
fig = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
ax = fig.add_subplot(111)

lns1 = ax.plot(df_system.index,[C]*len(df_system.index),'r',linewidth=1.0,dashes=[5,5],label='capacity constraint')
ax.plot(df_system.index,[0.0]*len(df_system.index),'k',linewidth=1.0)

lns3 = ax.plot(df_system_nobatt.index,df_system_nobatt['measured_real_power'],label='no market, no batteries')
#lns4 = ax.plot(df_system_noconstraint.index,df_system_noconstraint['measured_real_power'],label='25% batteries, no constraint')
lns2 = ax.plot(df_system.index,df_system['measured_real_power'],label='25% batteries, C = '+str(C)+'MW')

# ax2 = ax.twinx()
# ax2.set_ylabel('Price [USD/MW]')
# lns3 = ax2.plot(df_system.index,df_system['WS'],'r',label='local market price')

ax.set_ylabel('Measured system load [MW]')
ax.set_xlim(xmin=start, xmax=df_system.index[-1])
ax.set_ylim(ymax=1.5)

ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 6)))
ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 3)))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

# ax2.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
# ax2.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
# ax2.xaxis.set_major_formatter(DateFormatter('%H:%M'))

ax2 = ax.twinx()
ax2.set_ylabel('Price [USD/MW]')
lns4 = ax2.plot(df_system['clearing_price'],'#2ca02c',label='LEM price')    
lns5 = ax2.plot(df_system.index,df_system['WS'],'#2ca02c', linestyle='dashed',label='WS prices') 
#ax2.plot(df_systemdata.index,[0.0]*len(df_systemdata.index),'k',label='WS prices') 
#ax2.set_ylim(ymin=min(min(df_system['WS'].min()*1.05,0.0),df_system['clearing_price'].min()*1.05),ymax=df_system['WS'].max()*1.05)
#ax2.axhline(y=0,xmin=start, xmax=end)

#ppt.hlines(max_load, df_systemdata.index[0], df_systemdata.index[-1], colors='r', linestyles='dashed') 
ax2.set_xlim(xmin=start, xmax=df_system.index[-1])
#ax2.set_ylim(ymin=0.0)
ax2.xaxis.set_major_locator(HourLocator(arange(0, 25, 6)))
ax2.xaxis.set_minor_locator(HourLocator(arange(0, 25, 3)))
ax2.xaxis.set_major_formatter(DateFormatter('%H:%M'))

align_yaxis(ax, 0, ax2, 0)

lns =  lns3 + lns2 + lns4 + lns5 + lns1
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.4), loc='lower center', ncol=3)
ppt.savefig(run+'/10b_measuredload_Batteries.png', bbox_inches='tight')

#Start figure: prices
fig3 = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
ax = fig3.add_subplot(111)

lns1 = ax.plot(df_system.index,df_system['WS'],'b',label='WS market price')
ax.plot(df_system.index,[0.0]*len(df_system.index),'k',linewidth=1.0)
lns2 = ax.plot(df_system.index,df_system['clearing_price'],'g',label='Local market price')

ax.set_ylabel('Price in [USD/MW]')
ax.set_xlim(xmin=start, xmax=df_system.index[-1])
#ax.set_ylim(ymin=0.0, ymax=2.0)

ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

lns = lns1 + lns2
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.4), loc='lower center', ncol=3)
ppt.savefig(run+'/10b_prices_Batteries.png', bbox_inches='tight')

#Start figure: power
fig2 = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
ax = fig2.add_subplot(111)

lns1 = ax.plot(df_system.index,-df_system['flex_batt'],'b',label='battery load')
ax.plot(df_system.index,[0.0]*len(df_system.index),'k',linewidth=1.0)

ax.set_ylabel('Measured battery load [MW]')
ax.set_xlim(xmin=start, xmax=df_system.index[-1])
#ax.set_ylim(ymin=0.0, ymax=2.0)

ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

lns = lns1
labs = [l.get_label() for l in lns]
#L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.4), loc='lower center', ncol=3)
ppt.savefig(run+'/10b_battonly_Batteries.png', bbox_inches='tight')
