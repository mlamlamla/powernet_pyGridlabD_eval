# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 17:49:41 2018

@author: MLA

Shows for the whole system: rewarded bids versus actual dispatch
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

#td_min = datetime.datetime(2015, 7, 2, 10, 00)

def plot_bid_vs_dispatch_all(results,directory):
    #Input data
    df_buy_bids = pd.read_csv(results+'/buy_bids.csv',index_col=[0],parse_dates=['timedate'])
    df_prices = pd.read_csv(results+'/market_prices.csv',index_col=[0],parse_dates=['timedate'])
    df_prices_t = pd.read_csv(results+'/clearing_pq.csv',index_col=[0],parse_dates=['timedate'])
    df_prices_t.set_index('timedate',inplace=True)
    df_hvac = pd.read_csv(results+'/market_HVAC.csv',index_col=[0])
    df_hvac_meter = pd.read_csv(results+'/market_HVAC_meter.csv',index_col=[0],parse_dates=['timedate'])
    df_T = pd.read_csv(results+'/market_house_meter.csv',index_col=[0],parse_dates=['timedate'])
    
    #Buy Bids
    #house_id = 1
    #df_buy_bids_house = df_buy_bids.loc[df_buy_bids['appliance_name'] == 'HVAC_'+str(house_id)]
    #df_buy_bids_house.set_index('timedate',inplace=True)
    #df_T_house = df_T.loc[df_T['house_number'] == house_id]
    #df_T_house.set_index('timedate',inplace=True)
    
    """Flexible loads"""
    
    #Bids awarded/Active
    df_hvac_meter = pd.read_csv(results+'/market_HVAC_meter.csv',index_col=[0],parse_dates=['timedate'])
    
    houses = 14
    cols = []
    for house in range(1,houses+1):
        cols += ['active_'+str(house),'load_'+str(house)]
    
    #Active according to market
    df_activity = pd.DataFrame(index=df_prices['timedate'])
    df_activity['sum_actual_load'] = 0.0
    df_activity['num_active_load'] = 0
    df_activity['num_actual_load'] = 0
    df_activity['free_capacity'] = 0.0
    #Actual activity
    df_hvac_load = pd.read_csv(results+'/hvac_load.csv',skiprows=range(7))
    df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
    df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
    df_hvac_load.set_index('# timestamp',inplace=True)
    
    for house in range(1,houses+1):
        #Active according to market
        df_active = pd.DataFrame(data=df_hvac_meter[['active','timedate']].loc[df_hvac_meter['appliance_id'] == house])
        df_active = df_active.set_index('timedate')
        df_activity['active_'+str(house)] = df_active['active']   
        df_activity['num_active_load'] += df_active['active'] 
        
        #in min                  
        df_hvac_load_single = pd.DataFrame(index=df_hvac_load.index,data=df_hvac_load['GLD_00'+'{0:02d}'.format(house)+':hvac_load'])
        df_activity = df_activity.merge(df_hvac_load_single,left_index=True,right_index=True)
        df_activity['sum_actual_load'] += df_activity['GLD_00'+'{0:02d}'.format(house)+':hvac_load']
        df_activity['num_actual_load'].loc[df_activity['GLD_00'+'{0:02d}'.format(house)+':hvac_load'] > 0] += df_activity['active_'+str(house)].loc[df_activity['GLD_00'+'{0:02d}'.format(house)+':hvac_load'] > 0]
    
    """System analysis"""
    df_nodeSLACK = pd.read_csv(results+'/load_node_149.csv',skiprows=range(8))
    df_nodeSLACK['# timestamp'] = df_nodeSLACK['# timestamp'].map(lambda x: str(x)[:-4])
    df_nodeSLACK = df_nodeSLACK[:-1]
    df_nodeSLACK['# timestamp'] = pd.to_datetime(df_nodeSLACK['# timestamp'])
    df_nodeSLACK.set_index('# timestamp',inplace=True)
    df_nodeSLACK['measured_real_power'] = df_nodeSLACK['measured_real_power']/1000
    
    df_supply_bids = pd.read_csv(results+'/supply_bids.csv',index_col=[4],parse_dates=['timedate'])
    df_supply_bids = df_supply_bids.drop(labels=['Unnamed: 0','id','bid_price','gen_name'],axis=1)
    df_supply_bids.rename(columns={'bid_quantity': 'C'},inplace=True)
    
    df_system = df_nodeSLACK.merge(df_supply_bids,how='outer',left_index=True,right_index=True)
    df_system['cleared'] = 0.0
    
    df_unresp = pd.read_csv(results+'/unresponsive_loads.csv',parse_dates=['timedate'])
    df_unresp = df_unresp.drop(labels=['Unnamed: 0','id'],axis=1)
    df_unresp.set_index('timedate',inplace=True)
    df_system = df_system.merge(df_unresp, how='inner', left_index=True, right_index=True)
    
    df_system = df_system.merge(df_activity[['sum_actual_load']], how='inner', left_index=True, right_index=True)
    
    df_buy_bids_agg = pd.DataFrame(data=df_buy_bids[['bid_quantity','timedate']].groupby('timedate').sum())
    df_system = df_system.merge(df_buy_bids_agg, how='inner', left_index=True, right_index=True)
    df_system['cleared'] = df_system['sum_actual_load'] + df_system['unresp_load']
    
    #Awarded load
    df_hvac_meter['appliance_name'] = 'HVAC_'
    df_hvac_meter['appliance_name'] = df_hvac_meter['appliance_name'] + df_hvac_meter['appliance_id'].map(str)
    df_buy_bids = df_buy_bids.merge(df_hvac_meter,on=['timedate','appliance_name'])
    df_buy_bids['sum_rewarded'] = df_buy_bids['active']*df_buy_bids['bid_quantity']
    df_buy_bids_agg = pd.DataFrame(data=df_buy_bids[['sum_rewarded','timedate']].groupby('timedate').sum())
    df_system = df_system.merge(df_buy_bids_agg, how='inner', left_index=True, right_index=True)
    
    #Price effects
    df_supply_bids = pd.read_csv(results+'/supply_bids.csv',index_col=[4],parse_dates=['timedate'])
    df_supply_bids = df_supply_bids.drop(labels=['Unnamed: 0','id','gen_name','bid_quantity'],axis=1)
    df_supply_bids.rename(columns={'bid_price': 'MC'},inplace=True)
    df_buy_bids = df_buy_bids.merge(df_supply_bids,how='outer',on='timedate')
    df_buy_bids['bids_over_MC'] = 0
    df_buy_bids.at[df_buy_bids['bid_price'] >= df_buy_bids['MC'],'bids_over_MC'] = 1
    df_buy_bids['bids_over_MC'] = df_buy_bids['bids_over_MC']*df_buy_bids['bid_quantity']
    df_buy_bids_agg = pd.DataFrame(data=df_buy_bids[['bids_over_MC','timedate']].groupby('timedate').sum())
    df_system = df_system.merge(df_buy_bids_agg, how='inner', left_index=True, right_index=True)
    #Add power
    #Sum and merge with system
    return