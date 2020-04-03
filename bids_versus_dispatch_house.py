# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 17:49:41 2018

@author: MLA

Shows for a specific house: rewarded bid times versus actual dispatch
"""
import pandas as pd
import os
import market_functions as Mfcts
import datetime
from dateutil import parser
import matplotlib.pyplot as ppt

results = 'Results_3535_directcontrol'
directory = results+'_vis'
if not os.path.exists(directory):
    os.makedirs(directory)

td_min = datetime.datetime(2015, 7, 2, 10, 00)

def plot_bid_vs_dispatch_house(results,directory,house_name=None):
    #Get actual hvac load
    df_hvac_load = pd.read_csv(results+'/hvac_load.csv',skiprows=range(7))
    df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
    df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
    df_hvac_load.set_index('# timestamp',inplace=True)

    if not house_name:
        house_name = df_hvac_load.columns[0][:-10]
        col_name = df_hvac_load.columns[0]
    else:
        col_name = house_name+':hvac_load'
    house = int(col_name.split(':')[0].split('_')[-1])
        
    #Input data
    df_buy_bids = pd.read_csv(results+'/buy_bids.csv',index_col=[0],parse_dates=['timedate'])
    df_prices = pd.read_csv(results+'/market_prices.csv',index_col=[0],parse_dates=['timedate'])
    df_prices_t = pd.read_csv(results+'/clearing_pq.csv',index_col=[0],parse_dates=['timedate'])
    df_prices_t.set_index('timedate',inplace=True)
    df_appliances = pd.read_csv(results+'/market_HVAC.csv',index_col=[0])
    df_appliance_meter = pd.read_csv(results+'/market_HVAC_meter.csv',index_col=[0],parse_dates=['timedate'])
    df_T = pd.read_csv(results+'/market_house_meter.csv',index_col=[0],parse_dates=['timedate'])
    
    #Buy Bids
    house_id = 1
    df_buy_bids_house = df_buy_bids.loc[df_buy_bids['appliance_name'] == 'HVAC_'+str(house)]
    df_buy_bids_house.set_index('timedate',inplace=True)
    df_T_house = df_T.loc[df_T['house_number'] == house_id]
    df_T_house.set_index('timedate',inplace=True)
    
    #Bids awarded/Active
    df_hvac_meter = pd.read_csv(results+'/market_HVAC_meter.csv',index_col=[0],parse_dates=['timedate'])
    df_hvac_meter_01 = df_hvac_meter.loc[df_hvac_meter['appliance_id'] == house]
    df_hvac_meter_01.set_index('timedate',inplace=True)
    
    #Include actual load
    df_hvac_load = pd.read_csv(results+'/hvac_load.csv',skiprows=range(7))
    df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
    df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
    df_hvac_load.set_index('# timestamp',inplace=True)
    df_hvac_load_01 = pd.DataFrame(index=df_hvac_load.index,data=df_hvac_load[col_name])
    
    #Orientation lines: T_max and T_min
    df_appliances['temp'] = df_appliances['appliance_name'].str.split(':',expand=True)[0]
    df_appliances['house_id'] = df_appliances['temp'].str.split('_',expand=True)[4].astype(int)
    k = df_appliances['k'].loc[df_appliances['house_id'] == house].values[0]
    #mean_p = df_prices['mean_price'].loc[df_prices['timedate'] == td].values[0]
    #var_p = df_prices['var_price'].loc[df_prices['timedate'] == td].values[0]
    T_min = df_appliances['T_min'].loc[df_appliances['id'] == house].values[0]
    T_max = df_appliances['T_max'].loc[df_appliances['id'] == house].values[0]
    T_curr = df_T['air_temperature'].loc[df_T['house_number'] == house].values[0]
    
    # Plot
    ppt.clf()
    fig = ppt.figure(dpi=150)
    #Axes
    ax = fig.add_subplot(111)
    ax.set_xlabel('Time t')
    ax.set_ylabel('Temperature T')
    minx = df_buy_bids['timedate'].min()
    maxx = df_buy_bids['timedate'].max()
    miny = T_min - 1.0
    maxy = T_max + 1.0
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    #ppt.vlines(0.5, 0, maxy, colors='r', linestyle='dashed')
    #ppt.annotate(
    #'maximum profit per generation unit', xy=(0.55, maxy-0.5), xycoords='data')
    
    ppt.hlines(T_min, minx, maxx, colors='k', linestyles='dashed')
    ppt.hlines(T_min+(T_max-T_min)/2-1, minx, maxx, colors='k', linestyles='dashed')
    ppt.hlines(T_min+(T_max-T_min)/2+1, minx, maxx, colors='k', linestyles='dashed')
    ppt.hlines(T_max, minx, maxx, colors='k', linestyles='dashed')
    
    colors = ['r','b','g','k','y']
    lns = []
    lns += ax.plot(df_T_house['air_temperature'],color=colors[0],label='temperature profile')
    #Hintergrund
    #lns += ax.plot(df_hvac_meter_01['active']*70,color=colors[3],label='HVAC active')
    
    for i in range(len(df_hvac_meter_01.index)-1):
        if df_hvac_meter_01['active'].loc[df_hvac_meter_01.index[i]] == 1:
            ppt.axvspan(df_hvac_meter_01.index[i], df_hvac_meter_01.index[i+1], facecolor='g', alpha=0.5, label='HVAC active')
    
    ax2 = ax.twinx()
    ax2.set_ylabel('Load in [kW]')
    lns += ax2.step(df_hvac_load_01.index,df_hvac_load_01[col_name]*15,where='post',color=colors[1],label='Actual load')
    
    ##Title
    #title = 'Temperature profile and bidding'
    #T = ppt.suptitle(title, fontsize=15, x=0.5, y=1.1)
    ##Legend
    labs = [l.get_label() for l in lns]
    L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=2)
    
    ppt.savefig(directory+'/04_bids_vs_dispatch_house.png', bbox_extra_artists=(L,), bbox_inches='tight')
    return