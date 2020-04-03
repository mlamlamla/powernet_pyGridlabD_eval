# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 04:43:56 2019

@author: MLA
"""
import pandas as pd
from numpy import arange 
import matplotlib.pyplot as ppt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import sys
from datetime import datetime

def get_housedata(folder,house_name,df_system,fixed_price=50,FIT=50):
    #Settings
    settings = dict()
    settings['house_name'] = house_name
    hvac_name = 'HVAC'+house_name[3:]
    settings['hvac_name'] = hvac_name
    house = int(house_name.split('_')[-1])
    settings['house_no'] = house
    
    df_sett_hvac = pd.read_csv(folder+'/df_house_state.csv',usecols=range(2,9))
    try:
        settings['k'] = df_sett_hvac['k'].loc[df_sett_hvac['appliance_name'] == hvac_name].iloc[0]
    except:
        print('Probably no such house in flex list')
    settings['T_min'] = df_sett_hvac['T_min'].loc[df_sett_hvac['appliance_name'] == hvac_name].iloc[0]
    settings['T_max'] = df_sett_hvac['T_max'].loc[df_sett_hvac['appliance_name'] == hvac_name].iloc[0]
    settings['P_heat'] = df_sett_hvac['P_heat'].loc[df_sett_hvac['appliance_name'] == hvac_name].iloc[0]
    settings['P_cool'] = df_sett_hvac['P_cool'].loc[df_sett_hvac['appliance_name'] == hvac_name].iloc[0]
    
    df_sett_batt = pd.read_csv(folder+'/df_battery.csv',usecols=range(2,8))
    try:
        settings['batt_name'] = df_sett_batt['appliance_name'].loc[df_sett_batt['appliance_id'] == house].iloc[0]
        settings['SOC_max'] = df_sett_batt['SOC_max'].loc[df_sett_batt['appliance_name'] == settings['batt_name']].iloc[0]
        settings['u_max'] = df_sett_batt['u_max'].loc[df_sett_batt['appliance_name'] == settings['batt_name']].iloc[0]
        settings['eff'] = df_sett_batt['eff'].loc[df_sett_batt['appliance_name'] == settings['batt_name']].iloc[0]
    except:
        settings['batt_name'] = None
    
    df_sett_pv = pd.read_csv(folder+'/df_PV_state.csv',usecols=range(2,7))
    try:
        settings['pv_name'] = df_sett_pv['appliance_name'].loc[df_sett_pv['appliance_id'] == house].iloc[0]
        settings['rated_power'] = df_sett_pv['rated_power'].loc[df_sett_pv['appliance_name'] == settings['pv_name']].iloc[0]
    except:
        settings['pv_name'] = None

    #Operations
    
    df_houses = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8))
    df_houses['# timestamp'] = df_houses['# timestamp'].map(lambda x: str(x)[:-4])
    df_houses['# timestamp'] = pd.to_datetime(df_houses['# timestamp'])
    df_houses.set_index('# timestamp',inplace=True)
    df_house = pd.DataFrame(index=df_houses.index,columns=[house_name],data=df_houses[house_name])
    df_house.rename(columns={house_name:'total_load'},inplace=True)
    print('Max house real power: '+str(df_house['total_load'].max()))
    
    df_hvac_load = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8))
    df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
    df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
    df_hvac_load.set_index('# timestamp',inplace=True)
    df_hvac_load = pd.DataFrame(index=df_hvac_load.index,columns=[house_name],data=df_hvac_load[house_name])
    df_hvac_load.rename(columns={house_name:'hvac_power'},inplace=True)
    print('Max hvac real power: '+str(df_hvac_load['hvac_power'].max()))
    
    if settings['batt_name']:
        df_batteries = pd.read_csv(folder+'/market_battery_meter.csv',parse_dates=['timedate'],usecols=range(2,6))
        df_battery = df_batteries.loc[df_batteries['appliance_id'] == house]
        df_battery.set_index('timedate',inplace=True)
        df_battery.rename(columns={'active': 'batt_active', 'appliance_id': 'batt_id'},inplace=True)
        print('Max battery real power: '+str(df_battery['SOC'].max()))
    
    #Market operations
    
    df_bids = pd.read_csv(folder+'/buy_bids.csv',parse_dates=['timedate'],usecols=range(2,6))
    df_bids.set_index('timedate',inplace=True)

    df_bids_hvac = df_bids.loc[df_bids['appliance_name'] == hvac_name]
    df_bids_hvac = df_bids_hvac.drop(labels='appliance_name',axis=1)
    df_bids_hvac.rename(columns={'bid_price': 'hvac_p', 'bid_quantity': 'hvac_q'},inplace=True)
    print('Max bid p hvac: '+str(df_bids_hvac['hvac_p'].max()))
    print('Max bid q hvac: '+str(df_bids_hvac['hvac_q'].max()))
    
    if settings['batt_name']:
        df_bids_battery = df_bids.loc[df_bids['appliance_name'] == settings['batt_name']]
        df_bids_battery = df_bids_battery.drop(labels='appliance_name',axis=1)
        df_bids_battery.rename(columns={'bid_price': 'batt_p', 'bid_quantity': 'batt_q'},inplace=True)
        print('Max bid p battery: '+str(df_bids_battery['batt_p'].max()))
        print('Max bid q battery: '+str(df_bids_battery['batt_q'].max()))
    
    df_house_data = df_house.merge(df_hvac_load, how='outer', left_index=True, right_index=True)
    df_house_data = df_house_data.merge(df_bids_hvac, how='outer', left_index=True, right_index=True)
    if settings['batt_name']:
        df_house_data = df_house_data.merge(df_battery, how='outer', left_index=True, right_index=True)
        df_house_data = df_house_data.merge(df_bids_battery, how='outer', left_index=True, right_index=True)
    
    #Physical operations
    
    df_total_load = pd.read_csv(folder+'/total_load_all.csv',usecols=['# timestamp',settings['house_name']],skiprows=range(8))
    df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
    df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
    df_total_load.set_index('# timestamp',inplace=True)
    df_total_load.rename(columns={settings['house_name']: 'total_load_measured'},inplace=True)
    
    df_hvac_load = pd.read_csv(folder+'/hvac_load_all.csv',usecols=['# timestamp',settings['house_name']],skiprows=range(8))
    df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
    df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
    df_hvac_load.set_index('# timestamp',inplace=True)
    df_hvac_load.rename(columns={settings['house_name']: 'hvac_load'},inplace=True)
    
    df_T = pd.read_csv(folder+'/T_all.csv',usecols=['# timestamp',settings['house_name']],skiprows=range(8))
    df_T['# timestamp'] = df_T['# timestamp'].map(lambda x: str(x)[:-4])
    df_T['# timestamp'] = pd.to_datetime(df_T['# timestamp'])
    df_T.set_index('# timestamp',inplace=True)
    df_T.rename(columns={settings['house_name']: 'T_measured'},inplace=True)
    
    df_house_data = df_house_data.merge(df_total_load, how='outer', left_index=True, right_index=True)
    df_house_data = df_house_data.merge(df_hvac_load, how='outer', left_index=True, right_index=True)
    df_house_data = df_house_data.merge(df_T, how='outer', left_index=True, right_index=True)
    
    if settings['pv_name'] or settings['batt_name']:
        cols = ['# timestamp']
        if settings['pv_name']:
            cols += ['PV_inverter_'+settings['pv_name'][3:]]
        if settings['batt_name']:
            cols += ['Bat_inverter_'+settings['pv_name'][3:]]
        df_P_out = pd.read_csv(folder+'/total_P_Out.csv',usecols=cols,skiprows=range(8))
        df_P_out['# timestamp'] = df_P_out['# timestamp'].map(lambda x: str(x)[:-4])
        df_P_out['# timestamp'] = pd.to_datetime(df_P_out['# timestamp'])
        df_P_out.set_index('# timestamp',inplace=True)
        df_P_out = df_P_out/1000 #Convert from [W] to [kW]
        df_house_data = df_house_data.merge(df_P_out, how='outer', left_index=True, right_index=True)

    #Merge prices
    df_system_prices = pd.DataFrame(index=df_system.index,columns=['DA','RT','WS','clearing_price'],data=df_system[['DA','RT','WS','clearing_price']])
    df_house_data = df_house_data.merge(df_system_prices, how='inner', left_index=True, right_index=True)
    df_house_data = df_house_data.iloc[:-1]
    df_house_data['fixed_price'] = fixed_price
    df_house_data['FIT'] = FIT
    print(df_house_data.iloc[:5])
    return df_house_data, settings

def plot_house_load(directory,df_system,df_house,settings,house):
    cols = ['total_load_measured','hvac_load']
    if 'PV_inverter'+house[3:] in df_house.columns:
        cols += ['PV_inverter'+house[3:]]
    if 'Bat_inverter'+house[3:] in df_house.columns:
        cols += ['Bat_inverter'+house[3:]]
    df_house_load = df_house[cols]
    
    ppt.clf()
    fig = ppt.figure(dpi=150,figsize=(20,10))
    #Axes
    ax = fig.add_subplot(111)
    ax.set_xlabel('Time t')
    ax.set_ylabel('Load in [kW]')
    #minx = df_house.index.min()
    #maxx = df_house.index.max()
    #miny = settings['T_min'] - 1.0
    #maxy = settings['T_max'] + 1.0
    #ax.set_xlim(minx, maxx)
    #ax.set_ylim(miny, maxy)
    #ppt.vlines(0.5, 0, maxy, colors='r', linestyle='dashed')
    #ppt.annotate(
    #'maximum profit per generation unit', xy=(0.55, maxy-0.5), xycoords='data')
    
    #ppt.hlines(settings['T_min'], minx, maxx, colors='k', linestyles='dashed')
    #ppt.hlines(settings['T_min']+(settings['T_max']-settings['T_min'])/2-1, minx, maxx, colors='k', linestyles='dashed')
    #ppt.hlines(settings['T_min']+(settings['T_max']-settings['T_min'])/2+1, minx, maxx, colors='k', linestyles='dashed')
    #ppt.hlines(settings['T_max'], minx, maxx, colors='k', linestyles='dashed')
    
    colors = ['r','b','g','k','y']
    lns = []
    for col,c in zip(cols,colors):
        lns += ax.plot(df_house_load[col],color=c,label=col)
    #lns += ax.plot(df_house['hvac_active'],color=colors[3],label='HVAC active')
    #lns += ax.plot(df_house['hvac_load']*10,color=colors[4],label='Actual load')
    
    ax2 = ax.twinx()
    ax2.set_ylabel('local market prices')
    lns += ax2.plot(df_system['clearing_price'],'x',color=colors[-1],label='bid prices')
    
    ##Title
    #title = 'Temperature profile and bidding'
    #T = ppt.suptitle(title, fontsize=15, x=0.5, y=1.1)
    ##Legend
    labs = [l.get_label() for l in lns]
    L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=2)
    
    ppt.savefig(directory+'/'+str(house)+'_load.png', bbox_extra_artists=(L,), bbox_inches='tight')
    
    return

def plot_T_vs_bid(directory,df_system,df_house,settings,house,start=None,end=None):
    #df_house_noNAN = df_house.dropna(axis=0)
    df_house_5min = df_house.loc[df_house.index.minute%5 == 0]
    print(df_house.iloc[:5])
    
    ppt.clf()
    fig = ppt.figure(dpi=150)
    #Axes
    ax = fig.add_subplot(111)
    ax.set_xlabel('Time t')
    ax.set_ylabel('Temperature T')
    
    start = pd.Timestamp(2016, 7, 1, 0, 0)
    end = pd.Timestamp(2016, 7, 1, 23, 59)
    #minx = df_house.index.min()
    #maxx = df_house.index.max()
    #miny = settings['T_min'] - 1.0
    #maxy = settings['T_max'] + 1.0
    ax.set_xlim(start, end)
    ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 6)))
    #ax.xaxis.set_minor_locator(HourLocator(drange(0, 25, 6)))
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    #ax.set_ylim(miny, maxy)
    #ppt.vlines(0.5, 0, maxy, colors='r', linestyle='dashed')
    #ppt.annotate(
    #'maximum profit per generation unit', xy=(0.55, maxy-0.5), xycoords='data')
    
    #ppt.hlines(settings['T_min'], minx, maxx, colors='k', linestyles='dashed')
    #ppt.hlines(settings['T_min']+(settings['T_max']-settings['T_min'])/2-1, minx, maxx, colors='k', linestyles='dashed')
    #ppt.hlines(settings['T_min']+(settings['T_max']-settings['T_min'])/2+1, minx, maxx, colors='k', linestyles='dashed')
    #ppt.hlines(settings['T_max'], minx, maxx, colors='k', linestyles='dashed')
    
    colors = ['r','b','g','k','y']
    lns = []
    lns += ax.plot(df_house_5min['T_measured'],color=colors[0],label='temperature profile')
    #lns += ax.plot(df_house['hvac_active'],color=colors[3],label='HVAC active')
    #lns += ax.plot(df_house['hvac_load']*10,color=colors[4],label='Actual load')
    
    ax2 = ax.twinx()
    ax2.set_ylabel('bid prices')
    lns += ax2.plot(df_house_5min['hvac_p'],'x',color=colors[1],label='bid prices')
    #lns += ax2.plot(df_house_noNAN['hvac_q'],'x',color=colors[2],label='bid quantity')
    ax.set_xlim(start, end)
    ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 6)))
    #ax.xaxis.set_minor_locator(HourLocator(drange(0, 25, 6)))
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    ##Title
    #title = 'Temperature profile and bidding'
    #T = ppt.suptitle(title, fontsize=15, x=0.5, y=1.1)
    ##Legend
    labs = [l.get_label() for l in lns]
    L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=2)
    
    ppt.savefig(directory+'/'+str(house)+'_T_vs_bids.png', bbox_extra_artists=(L,), bbox_inches='tight')
    return

def plot_costs(directory,df_system,df_house, settings,house):
    global_par = open(directory+'/HH_global.py','r')
    for i in global_par:
        if '=' in i and 'interval' in i:
            interval = int(i.split(' ')[2])

    #costs in USD/kW
    df_hvac_costs = pd.DataFrame(index=df_system.index,columns=['clearing_price'],data=df_system['clearing_price']/1000)
    df_hvac_load = pd.DataFrame(index=df_house.index,columns=['hvac_load'],data=df_house['hvac_load'])
    df_hvac_costs = df_hvac_costs.merge(df_hvac_load,how='outer',left_index=True,right_index=True)
    hvac_costs = (df_hvac_costs['clearing_price']*df_hvac_costs['hvac_load']).sum()/(60/interval)
    hvac_load = df_hvac_costs['hvac_load'].sum()/(60/interval) #kWh
    
    ppt.clf()
    fig = ppt.figure(dpi=150)
    #Axes
    ax = fig.add_subplot(111)
    ax.set_xlabel('Fixed tariff in USD/kWh')
    ax.set_ylabel('HVAC costs in USD per day')
    lns1 = ppt.plot([0.0,0.1], [hvac_costs,hvac_costs],'r',label='HVAC participating in local market')
    prices = arange(0., 0.1, 0.001) #prices in USD/kW
    ax.set_xlim(prices[0], prices[-1])
    ax.set_ylim(0.0, 15.0)
    lns2 = ppt.plot(prices, prices*hvac_load,'b',label='HVAC at fixed tariff')
    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]
    L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=2)
    
    ppt.savefig(directory+'/'+str(house)+'_break_even_market.png', bbox_extra_artists=(L,), bbox_inches='tight')
    return