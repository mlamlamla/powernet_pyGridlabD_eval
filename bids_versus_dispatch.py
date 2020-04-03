# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 21:14:13 2018

@author: MLA

Plots rewarded bids/active versus actual loadf: HVAC
"""
import pandas as pd
from numpy import arange
import matplotlib.pyplot as ppt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import os

results = 'Results_3535_directcontrol'
directory = results+'_vis'
if not os.path.exists(directory):
    os.makedirs(directory)

def plot_bid_vs_dispatch(results,directory,house_name=None):
    #Get actual hvac load
    df_hvac_load = pd.read_csv(results+'/hvac_load.csv',skiprows=range(7))
    df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
    df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
    df_hvac_load.set_index('# timestamp',inplace=True)

    if not house_name:
        col_name = df_hvac_load.columns[0]
        house = 1
    else:
        col_name = house_name+':hvac_load'
        house = int(col_name.split(':')[0].split('_')[-1])
    
    #Bids awarded/Active
    df_hvac_meter = pd.read_csv(results+'/market_HVAC_meter.csv',index_col=[0],parse_dates=['timedate'])
    #df_hvac = pd.read_csv(results+'/market_HVAC.csv',index_col=[0])
    
    df_hvac_load_01 = pd.DataFrame(index=df_hvac_load.index,data=df_hvac_load[col_name])
    df_hvac_meter_01 = df_hvac_meter.loc[df_hvac_meter['appliance_id'] == house]
    df_hvac_meter_01.set_index('timedate',inplace=True)
    
    """CORRECT"""
    P = 5.0
    df_hvac_meter_01['load'] = df_hvac_meter_01['active']*P
    
    #Start figure
    fig = ppt.figure(figsize=(12,4),dpi=150)
    
    #House load
    ax = fig.add_subplot(111)
    
    lns2 = ax.plot(df_hvac_load_01[col_name],label='Actual load')
    lns1 = ax.plot(df_hvac_meter_01['load'], label='Awarded bids')
    
    ax.set_ylabel('kW')
    ax.set_xlim(xmin=df_hvac_meter_01.index[0], xmax=df_hvac_meter_01.index[-1])
    
    ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
    #ax.xaxis.set_minor_locator(HourLocator(drange(0, 25, 6)))
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
    
    #Legend
    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]
    L = ax.legend(lns, labs, bbox_to_anchor=(0.3, -0.3), loc='lower left', ncol=1)
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    ppt.savefig(directory+'/02_bids_vs_dispatch.png', bbox_inches='tight')
    return