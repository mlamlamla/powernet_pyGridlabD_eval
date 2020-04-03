# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 04:09:07 2019

@author: MLA
"""
import pandas as pd
from numpy import arange 
import matplotlib.pyplot as ppt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange

market_file = 'ercot_2018_2016.csv'

#plots total charging and discharging, depending on price
def plot_EVload(results,df_system,df_system2=None): 
    fig = ppt.figure(figsize=(8,4),dpi=150)   
    ppt.ioff()
    #House load
    ax = fig.add_subplot(111)
    lns1 = ax.plot(df_system['flex_EV'],'r',label='Total EV Load')
    try:
        lns2 = ax.plot(df_system2['flex_EV'],'k',label='Total EV Load 2')
    except:
        pass
    ax.set_ylabel('EV Load in [MW]')
    #ax.set_xlim(xmin=df_batterydata.index[0], xmax=df_batterydata.index[-1])
    
    start = df_system.index[0] #pd.Timestamp(2016, 7, 1, 0, 0)
    end = df_system.index[-1] #pd.Timestamp(2016, 7, 1, 23, 59)
    #df_batterydata.index[0], df_batterydata.index[-1]
    ax.set_xlim(xmin=start, xmax=end)
    ax.set_ylim(ymin=0.0)
    
    ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 24)))
    ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d'))
    
    #ax.xaxis.set_major_locator(HourLocator(interval=1))
    #ax.xaxis.set_minor_locator(HourLocator(drange(0, 25, 6)))
    #ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    
    ppt.hlines(0, start, end, colors='k')
    
    #ax2 = ax.twinx()
    #ax2.set_ylabel('Local Retail Price [USD/MW]')
    #lns2 = ax2.plot(df_system['clearing_price'],'bx',label='Realtime Local Price')
    
    #ax.set_xlim(xmin=start, xmax=end)
    
    #ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 24)))
    #ax.xaxis.set_minor_locator(HourLocator(drange(0, 25, 6)))
    #ax.xaxis.set_major_formatter(DateFormatter('%m-%d'))
    
    #Legend
    try:
        lns = lns1 + lns2
    except:
        lns = lns1
    labs = [l.get_label() for l in lns]
    L = ax.legend(lns, labs, bbox_to_anchor=(0.3, -0.2), loc='lower left', ncol=1)
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    if len(lns) == 1:
        ppt.savefig(results+'/EV_total_load.png', bbox_inches='tight')
    else:
        ppt.savefig(results+'/EV_total_load_comp.png', bbox_inches='tight')
    return

#Creates master table for system data
def get_batterydata(folder,s_settings,battery=None):
    #Get settings
    no_houses = s_settings['flexible_houses'].iloc[0]
    C = s_settings['line_capacity'].iloc[0]
    p_max = s_settings['p_max'].iloc[0]
    interval = s_settings['interval'].iloc[0]
    PV_share = s_settings['PV_share'].iloc[0]
    EV_share = s_settings['EV_share'].iloc[0]
    Batt_share = s_settings['Batt_share'].iloc[0]
    city = s_settings['city'].iloc[0]
    market_file = s_settings['market_data'].iloc[0]
    which_price = s_settings['which_price'].iloc[0]

    #Battery settings
    df_settings = pd.read_csv(folder+'/df_battery_state.csv')
    print(df_settings.iloc[:5])
    
    #Battery physical data
    list_batt = list(df_settings['battery_name'])
    if not battery:
        battery = list_batt[0]
    list_batt_inv = []
    for batt in list_batt:
        list_batt_inv += ['Bat_inverter_'+batt[8:]]   
    df_inv_load = pd.read_csv(folder+'/total_P_Out.csv',skiprows=range(8))
    df_inv_load['# timestamp'] = df_inv_load['# timestamp'].map(lambda x: str(x)[:-4])
    df_inv_load = df_inv_load.iloc[:-1]
    df_inv_load['# timestamp'] = pd.to_datetime(df_inv_load['# timestamp'])
    df_inv_load.set_index('# timestamp',inplace=True)  
    df_all_batt = df_inv_load[list_batt_inv] #Excludes EVs and other inverter based appliances
    df_all_batt.loc[:,'total_batt_load'] = 0.0
    df_all_batt.loc[:,'total_batt_load'] = df_all_batt[list_batt_inv].sum(axis=1) #df_inv_load.iloc[:,list_batt_inv].sum(axis=1)
    df_all_batt = df_all_batt/1000
    print('Max flexible batt load: '+str(df_all_batt['total_batt_load'].max()))
    
    # df_meter = pd.read_csv(folder+'/battery_SOC.csv',usecols=[1,2,3,4,5])
    # df_meter.set_index('timedate',inplace=True)
    # app_id = int(battery.split('_')[-1])
    # df_meter_id = df_meter.loc[df_meter['appliance_id'] == app_id]
    # df_meter_id.rename(columns={'SOC':'SOC_'+battery,'active':'active_'+battery},inplace=True)
    # df_meter_id.drop('id',axis=1,inplace=True)
    # df_meter_id = df_meter_id.drop('appliance_id',axis=1)
    # print('Max SOC for '+battery+': '+str(df_meter_id['SOC_'+battery].max()))
    
    #Bids, mc and prices
    df_buy = pd.read_csv(folder+'/df_buy_bids.csv',index_col=[0],parse_dates=['timestamp'])
    df_buy.rename(columns={'timestamp':'timedate'},inplace=True)
    df_buy.set_index('timedate',inplace=True)
    df_buy = df_buy.loc[df_buy['appliance_name'] == battery]
    df_buy.rename(columns={'bid_quantity':'bid_q_buy'},inplace=True)
    
    df_supply = pd.read_csv(folder+'/df_supply_bids.csv',index_col=[0],parse_dates=['timestamp'])
    df_supply.rename(columns={'timestamp':'timedate'},inplace=True)
    df_supply.set_index('timedate',inplace=True)
    df_supply = df_supply.loc[df_supply['appliance_name'] == battery]
    df_supply.rename(columns={'bid_quantity':'bid_q_sell'},inplace=True)
    
    df_WS = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/glm_generation_'+city+'/'+market_file,parse_dates=[0])
    df_WS.rename(columns={'Unnamed: 0':'timestamp'},inplace=True)
    df_WS.set_index('timestamp',inplace=True)
    df_WS['P_cap'] = p_max
    df_WS['WS'] = df_WS[[which_price, 'P_cap']].min(axis=1)
    
    df_cleared = pd.read_csv(folder+'/df_prices.csv',parse_dates=[0])
    df_cleared.rename(columns={'Unnamed: 0':'timedate'},inplace=True)
    df_cleared.set_index('timedate',inplace=True)

    df_batterydata = df_all_batt.merge(df_buy, how='outer', left_index=True, right_index=True)
    #df_batterydata = df_batterydata.merge(df_meter_id, how='outer', left_index=True, right_index=True)
    df_batterydata = df_batterydata.merge(df_supply, how='outer', left_index=True, right_index=True)
    df_batterydata = df_batterydata.merge(df_WS, how='inner', left_index=True, right_index=True)
    df_batterydata = df_batterydata.merge(df_cleared, how='outer', left_index=True, right_index=True)
    
    return df_batterydata, df_settings
    
#Plots charging behavior and SOC of single battery
def plot_battery(folder,directory,batt_settings,df_batterydata,battery=None):
    #Battery physical data
    list_batt = list(batt_settings['battery_name'])
    if not battery:
        battery = list_batt[0]
    list_batt_inv = []
    for batt in list_batt:
        list_batt_inv += ['Bat_inverter_'+batt[8:]]   

    fig = ppt.figure(figsize=(12,4),dpi=150)   
    ppt.ioff()
    #House load
    ax = fig.add_subplot(111)
    print(df_batterydata.iloc[:5])
    lns1 = ax.plot(df_batterydata['total_batt_load'],'r-',label='Total battery load')
    #lns1 = ax.plot(df_batterydata['SOC_'+battery],'r-',label='Total battery load')
    ax.set_ylabel('kWh')
    ax.set_xlim(xmin=df_batterydata.index[0], xmax=df_batterydata.index[-1])
    
    ax.xaxis.set_major_locator(HourLocator(interval=1))
    #ax.xaxis.set_minor_locator(HourLocator(drange(0, 25, 6)))
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    
    ppt.hlines(0, df_batterydata.index[0], df_batterydata.index[-1], colors='k')
    
    ax2 = ax.twinx()
    ax2.set_ylabel('local retail price')
    lns2 = ax2.plot(df_batterydata['clearing_price'],'bx',label='Realtime WS price')
    
    #Legend
    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]
    L = ax.legend(lns, labs, bbox_to_anchor=(0.3, -0.4), loc='lower left', ncol=1)
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    ppt.savefig(directory+'/'+battery+'_Battload_vs_price.png', bbox_inches='tight')
    return

def plot_thresholds(folder,directory,batt_settings,df_battery,df_system,battery=None,start=None,end=None):
    
    list_batt = list(batt_settings['battery_name'])
    if not battery:
        battery = list_batt[0]
    elif isinstance(battery,int):
        battery = list_batt[battery]
    list_batt_inv = []
    for batt in list_batt:
        list_batt_inv += ['Bat_inverter_'+batt[8:]] 

    df_meter = pd.read_csv(folder+'/df_battery_thresholds_24.csv',index_col=[0])
    threshold_buy = df_meter['threshold_buy'].loc[battery]
    threshold_sell = df_meter['threshold_sell'].loc[battery]
    
    start = df_system.iloc[0]
    end = df_system.iloc[-1]
    
    fig = ppt.figure(figsize=(9,3),dpi=150)   
    ppt.ioff()
    #House load
    ax = fig.add_subplot(111)
    lns1 = ax.plot(df_system['DA'],'k-',label='DA price')
    #lns1b = ax.plot(df_system['RT'],'b-',label='RT price')
    lns2 = ax.plot(df_system['clearing_price'],'b-',label='Local RT price')
    ax.set_ylabel('Price in [USD/MW]')
    start = df_system.index[0] #pd.Timestamp(2016, 7, 1, 0, 0)
    end = df_system.index[-1] #pd.Timestamp(2016, 7, 1, 23, 59)
    ax.set_xlim(xmin=start, xmax=end)
    
    ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 6)))
    #ax.xaxis.set_minor_locator(HourLocator(drange(0, 25, 6)))
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    
    ppt.hlines(threshold_sell, start, end, colors='r', label='sell threshold')
    ppt.hlines(threshold_buy, start, end, colors='r', label='buy threshold')
    
    #Legend
    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]
    L = ax.legend(lns, labs, bbox_to_anchor=(0.3, -0.3), loc='lower left', ncol=2)
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    ppt.savefig(directory+'/'+battery+'_prices_threshold.png', bbox_inches='tight')
    return

def plot_EV_bid(results,df_batterydata,EV): 
    df_buy = pd.read_csv(results+'/buy_bids.csv',index_col=[0],parse_dates=['timedate'])
    df_buy.set_index('timedate',inplace=True)
    df_buy = df_buy.loc[df_buy['appliance_name'] == EV]
    df_buy.rename(columns={'bid_price':'bid_p_buy'},inplace=True)
    
    df_EV = pd.read_csv(results+'/df_EV.csv',index_col=[0])

    fig = ppt.figure(figsize=(6,4),dpi=150)   
    ppt.ioff()
    #House load
    ax = fig.add_subplot(111)
    ax.set_ylabel('Local Retail Price [USD/MW]')
    lns1 = ax.plot(df_batterydata['clearing_price'],'rx',label='Realtime Local Price')
    lns2 = ax.plot(df_buy['bid_p_buy'],'bx',label='EV buy bid')
    
    #ax.axvspan(df_EV.index[0], df_EV.index[-1], facecolor='r', alpha=0.25)
    
    start = pd.Timestamp(2016, 7, 1, 0, 0)
    end = pd.Timestamp(2016, 7, 1, 23, 59)
    #df_batterydata.index[0], df_batterydata.index[-1]
    ax.set_xlim(xmin=start, xmax=end)
    
    ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 6)))
    #ax.xaxis.set_minor_locator(HourLocator(drange(0, 25, 6)))
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    
    #ax.xaxis.set_major_locator(HourLocator(interval=1))
    #ax.xaxis.set_minor_locator(HourLocator(drange(0, 25, 6)))
    #ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    
    ppt.hlines(0, start, end, colors='k')

    ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 6)))
    #ax.xaxis.set_minor_locator(HourLocator(drange(0, 25, 6)))
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    
    #Legend
    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]
    L = ax.legend(lns, labs, bbox_to_anchor=(0.3, -0.4), loc='lower left', ncol=1)
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    ppt.savefig(results+'_vis/'+EV+'_bids.png', bbox_inches='tight')
    return