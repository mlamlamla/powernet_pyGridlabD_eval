# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 16:08:15 2019

@author: MLA
"""
import pandas as pd
import system_analyses as sysev

def calculate_welfare(folder,df_system,df_nomarket,df_T_nomarket,fixed_price=50,FIT=50):
    #internal T
    df_T = pd.read_csv(folder+'/T_all.csv',skiprows=range(8))
    df_T['# timestamp'] = df_T['# timestamp'].map(lambda x: str(x)[:-4])
    df_T['# timestamp'] = pd.to_datetime(df_T['# timestamp'])
    df_T.set_index('# timestamp',inplace=True)
    
    #no market
    #df_nomarket, df_T_nomarket = sysev.get_nomarketdata(folder_nomarket)
    df_results = pd.DataFrame(columns=['Parameter','No market','Market'])
    
    #prices
    df_results.loc[0] = ['Maximum load',df_nomarket['measured_real_power'].max(),df_system['measured_real_power'].max()]
    df_results.loc[1] = ['Maximum house load',df_nomarket['sum_houseload'].max(),df_system['total_load_houses'].max()]
    df_results.loc[2] = ['PV generation',df_nomarket['sum_PV'].max(),df_system['flex_pv'].max()]
    
    df_results.loc[3] = ['Average local market price',fixed_price,df_system['clearing_price'].mean()]
    df_results.loc[4] = ['Average WS market price',df_system['WS'].mean(),df_system['WS'].mean()]
    
    df_results.loc[5] = ['Costs for flexible hvac',0.0,(df_system['clearing_price']*df_system['flex_hvac']).sum()]
    df_results.loc[6] = ['Net income from batteries',0.0,(df_system['clearing_price']*df_system['flex_batt']).sum()]
    df_results.loc[7] = ['Income from PV',FIT*df_nomarket['sum_PV'].sum(),(df_system['clearing_price']*df_system['flex_pv']).sum()]
    
    flex_costs = (df_system['clearing_price']*df_system['flex_hvac']).sum()
    inflex_costs = (df_system['clearing_price']*(df_system['total_load_houses'] - df_system['flex_hvac'])).sum()
    df_results.loc[8] = ['Total costs for households',df_nomarket['sum_houseload'].sum()*fixed_price,flex_costs + inflex_costs]
    
    df_results.loc[9] = ['Av T',df_nomarket['av_T'].mean(),df_T.mean(axis=1).mean()]
        
    df_results.loc[10] = ['Fixed price/FIT',fixed_price,FIT]
    
    df_results.to_csv(folder+'_vis/welfare.csv')
    return df_results
