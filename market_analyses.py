# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 04:45:16 2019

@author: MLA
"""
import pandas as pd
from numpy import arange 
import matplotlib.pyplot as ppt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import market_functions as mf

def plot_market_t(folder,dt):
    #Collect bids
    df_buy = pd.read_csv(folder+'/buy_bids.csv',parse_dates=['timedate'],dtype={'bid_quantity': float, 'bid_price': float} )
    df_buy_t = df_buy.loc[df_buy['timedate'] == dt]

    df_supply = pd.read_csv(folder+'/supply_bids.csv',parse_dates=['timedate'],dtype={'bid_quantity': float, 'bid_price': float} )
    df_supply_t = df_supply.loc[df_supply['timedate'] == dt]
    df_PQ = pd.read_csv(folder+'/df_prices.csv',parse_dates=[0])
    df_PQ.rename(columns={'Unnamed: 0':'timedate'},inplace=True)
    df_PQ.set_index('timedate',inplace=True)
    Pd_GLD = df_PQ['clearing_price'].loc[dt]
    
    #Market creation
    retail = mf.Market()
    retail.reset()
    retail.Pmin = 0.0
    retail.Pmax = 150.0
    retail.Pprec = 4
    
    #Submit bids
    for ind in df_buy_t.index:
        retail.buy(df_buy_t['bid_quantity'].loc[ind],df_buy_t['bid_price'].loc[ind],active=0) #,appliance_name=df_buy_t['appliance_name'].loc[ind]
    #for ind in df_unresp_t.index:
    #    retail.buy(df_unresp_t['unresp_load'].loc[ind],active=0) #,appliance_name='WS'
    for ind in df_supply_t.index:
        retail.sell(df_supply_t['bid_quantity'].loc[ind],df_supply_t['bid_price'].loc[ind]) #,gen_name=df_supply_t['gen_name'].loc[ind]

    retail.clear()
    Pd = retail.Pd # cleared demand price
    Qd = retail.Qd #in kW
    print('Market price according to clearing: '+str(Pd))
    print('Market price according to GridlabD simulation: '+str(Pd_GLD))

    retail.plot(folder,dt)    
    return Pd, Qd