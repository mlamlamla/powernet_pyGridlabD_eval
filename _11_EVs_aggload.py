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

#folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '/' + run + '_' + ind
ind = '0098'
results = run + '/' + run + '_' + ind + '_vis'
df_system = pd.read_csv(results+'/df_system.csv',index_col=[0], parse_dates=True)

ind = '0099'
results = run + '/' + run + '_' + ind + '_vis'
df_system2 = pd.read_csv(results+'/df_system.csv',index_col=[0], parse_dates=True)

EVev.plot_EVload(results,df_system,df_system2)

# inds = ['0001','0061','0060']

# start = pd.Timestamp(2015, 7, 16)

# #Start figure
# fig = ppt.figure(figsize=(9,3),dpi=150)   
# ppt.ioff()
# ax = fig.add_subplot(111)
# lns = None

# #No devices
# ind = inds[0]
# folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
# directory = run + '_' + ind + '_vis'
# df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True)
# lns = ax.plot(df_system.index,df_system['measured_real_power'],label='no EVs')

# #All devices
# ind = inds[1]
# folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
# directory = run + '_' + ind + '_vis'
# df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True)
# lns = lns + ax.plot(df_system.index,df_system['measured_real_power'],label='25% EVs')

# ax2 = ax.twinx()
# ax2.set_ylabel('Price [USD/MW]')
# #lns = ax2.plot(df_system.index,df_system['WS'],'k',label='WS price',dashes=[2.5,2.5]) 
# lns = lns + ax2.plot(df_system.index,df_system['clearing_price'],'k',label='LEM price') 

# #All devices
# # ind = inds[2]
# # folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
# # directory = run + '_' + ind + '_vis'
# # df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True)
# # lns = lns + ax.plot(df_system.index,df_system['measured_real_power'],label='25% PV/Batt/EVs')

# ax.plot(df_system.index,[0.0]*len(df_system.index),'k',linewidth=1.0)

# ax.set_ylabel('Measured system load [MW]')
# ax.set_xlim(xmin=start, xmax=df_system.index[-1])
# ax.set_ylim(ymin=0.0)

# ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
# ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
# ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))


# #Legend
# labs = [l.get_label() for l in lns]
# L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=len(labs))
# ppt.savefig(run+'/11_measuredload_EV.png', bbox_inches='tight')
