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

#Which run
run = 'FinalReport2'
battery = 'Bat_inverter_B1_N75_C_0300'
battery_name = 'Battery_B1_N75_C_0300'

settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_final2.csv'
df_settings = pd.read_csv(settings_file)
ind = '0059' #25% PV, 25% Batt, 0 HVAC, 1300 kW; perfect forecast
start = pd.Timestamp(2015, 7, 16)

folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
directory = run + '_' + ind + '_vis'
df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True)

df_P_out = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'_'+ind+'/total_P_Out.csv',skiprows=range(8))
print(df_P_out.columns)
df_P_out = df_P_out[['# timestamp',battery]]
df_P_out['date'] = pd.date_range(start=pd.Timestamp(2015, 7, 15, 0, 0), end=pd.Timestamp(2015, 7, 16, 23,59), freq='1min')
df_P_out.set_index('date',inplace=True)

df_battery_state = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'_'+ind+'/df_battery_state.csv',index_col=[0], parse_dates=True)

threshold_buy = df_battery_state['threshold_buy'].loc[battery_name]
threshold_sell = df_battery_state['threshold_sell'].loc[battery_name]

#import pdb; pdb.set_trace()


#Start figure: prices
fig3 = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
ax = fig3.add_subplot(111)

ax.plot(df_P_out.index,[0.0]*len(df_P_out.index),'k',linewidth=1.0)
lns0 = ax.plot(df_P_out.index,df_P_out[battery]/1000,'b',label='Battery load')

ax.set_ylabel('Battery load in [kW]')
ax.set_xlim(xmin=start, xmax=df_system.index[-1])

ax2 = ax.twinx()
ax2.set_ylabel('Price [USD/MW]')

#lns1 = ax2.plot(df_system.index,df_system['WS'],'g',label='WS market price')
lns3 = ax2.plot(df_system.index,[threshold_buy]*len(df_system.index),'r',dashes=[5,5],label='price thresholds')
lns4 = ax2.plot(df_system.index,[threshold_sell]*len(df_system.index),'r',dashes=[5,5],label='threshold sell')
#ax2.plot(df_system.index,[0.0]*len(df_system.index),'k',linewidth=1.0)
lns2 = ax2.plot(df_system.index,df_system['clearing_price'],'g',label='Local market price')




#ax.set_ylim(ymin=0.0, ymax=2.0)

ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

lns = lns0 + lns2 + lns3
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.4), loc='lower center', ncol=3)
ppt.savefig(run+'/10c_prices_SingleBattery.png', bbox_inches='tight')
