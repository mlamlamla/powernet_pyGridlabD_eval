# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 04:07:29 2019

@author: MLA
"""
import os
import pandas as pd
import system_analyses as sysev
import house_analyses as hev
import battery_analyses as bev
import EV_analyses as EVev
import market_analyses as mev
import welfare_analyses as wev
import warnings
warnings.filterwarnings("ignore")

"""
Graphs:
    
System:
    - total system load
    - total system load vs. prices
    - total battery load vs. prices
    - load and generation disaggregated (check batteries !!!)

House
    - generation versus consumption (TO DO)
    - bid prices vs. hvac and total load
    - T vs. bid
    - T with market vs. T without market (TO DO)
    
Battery
    - aggregated battery load
    - specific battery: charge/discharge vs. SOC

Market
    - S vs. D for any time (TO DO)

TO DO

include EVs
check if PV is accounted for in house connection/total_load
calculate av el costs for flexible and inflexible houses

"""

#Which run
run = 'FinalReport2' #'FinalReport_Jul1d'
ind = '0014'
#settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_Jan_1d.csv'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_final2.csv'

folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
folder_nomarket = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
directory = run + '_' + ind + '_vis'

if not os.path.exists(directory):
    os.makedirs(directory)

df_settings = pd.read_csv(settings_file)
s_settings = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(ind))]

#System
#df_system = sysev.get_systemdata(folder,folder_nomarket,s_settings)
#df_system.to_csv(directory+'/df_system.csv')
#df_system_nomarket.to_csv(directory+'/df_system_nomarket.csv')
#df_T.to_csv(directory+'/df_T.csv')

df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True)
#df_system_nomarket = pd.read_csv(directory+'/df_system_nomarket.csv',index_col=[0], parse_dates=True)
#df_T = pd.read_csv(directory+'/df_T.csv',index_col=[0], parse_dates=True)
#import pdb; pdb.set_trace()
sysev.plot_system_prices_week(directory,df_system,s_settings)

#print('Max real power on 15/07: '+str(df_system['measured_real_power'].iloc[2880:4320].max()))

print('Average load: '+str(df_system['measured_real_power'].mean()))
print('Share hvac/total load: '+str(df_system['inflex_hvac'].sum()/df_system['total_load_houses'].sum()))
print('Losses: '+str(df_system['total_load_houses'].sum()/df_system['measured_real_power'].sum()))

sysev.plot_systemload_short(directory,df_system,s_settings)
sysev.plot_systemload(directory,df_system,s_settings)

#sysev.plot_systemload_womarkets(directory,df_system,df_system_nomarket,s_settings)

sysev.plot_load_disagg(directory,df_system,s_settings)
#sysev.plot_load_disaggbars(directory,df_system,s_settings,start=pd.Timestamp(2016, 7, 1, 11),end=pd.Timestamp(2016, 7, 1, 17))
sysev.plot_load_curve(directory,df_system,s_settings,values=216,set_max_load=False, perc_max=1.025)

try:
    df_sysop = sysev.plot_sysop(directory,df_system,s_settings,pd.Timestamp(year=2016, month=7, day=1, hour=14),pd.Timestamp(year=2016, month=7, day=1, hour=17))
except:
    print('No systems operations')

if s_settings['flexible_houses'].iloc[0] > 0:
    df_flex_load = sysev.plot_flex_HVAC(folder,directory,216,s_settings)
if s_settings['flexible_houses'].iloc[0] < 1120:
    df_flex_load = sysev.plot_inflex_HVAC(folder,directory,216,s_settings)

#Specific house
# house = 'GLD_B1_N48_C_0001' #'GLD_B1_N66_C_0164'
# df_house, settings = hev.get_housedata(folder,house,df_system)
# try:
#     hev.plot_house_load(directory,df_system,df_house,settings,house)
#     hev.plot_T_vs_bid(directory,df_system,df_house, settings,house)
#     hev.plot_costs(directory,df_system,df_house, settings,house)
# except:
#     pass

# #Specific battery
# #battery = 'Battery_B1_N77_B_0531'
# try:
#     df_battery, batt_settings = bev.get_batterydata(folder,s_settings)
#     df_battery = df_battery.iloc[int(len(df_battery)/2):] 
#     df_system = df_system.iloc[int(len(df_system)/2):]
#     bev.plot_batteries(directory,df_battery)
#     bev.plot_battery(folder,directory,batt_settings,df_battery)
#     bev.plot_thresholds(folder,directory,batt_settings,df_battery,df_system,2)
# except:
#     pass

#Plot EV load
if s_settings['EV_share'].iloc[0] > 0:
    EVev.plot_EVload(directory,df_system)


#Specific EV- 00012_market
#EV = 'EV_B1_N100_C_0160'
#bev.plot_EV_bid(folder,df_battery,EV)



#market data
#find price distribution
#mev.plot_market_t(folder,pd.Timestamp(year=2016, month=7, day=1, hour=13, minute=0))

#welfare
# df_WF = wev.calculate_welfare(folder,df_system, df_system_nomarket, df_T)
# print(df_WF)