# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 12:12:07 2018

@author: MLA

Merges Ercot price data to csv which can be read by powernet simulation
"""
import pandas as pd

df_RTP = pd.read_csv(r'C:\Users\MLA\Documents\Promotion\Projekte\09_Powernet with Markets\price_data\RTP_5min_RTW_138H_EB.csv',index_col=[0],usecols=[0,2,4],parse_dates=[2])
df_RTP.set_index('SCEDTimestamp',inplace=True)
df_RTP.rename(columns={'LMP':'RT'},inplace=True)
df_RTP.index = df_RTP.index.floor('min')

df_DA = pd.read_csv(r'C:\Users\MLA\Documents\Promotion\Projekte\09_Powernet with Markets\price_data\DAM_prices_hourly_RTW_138H_EB.csv',index_col=[0],usecols=[0,3,4,5])
for t in range(24):
    df_DA.at[df_DA.index%24 == t, 'HourStarting'] = "%02d:%02d" % (t,0)
df_DA['Timestamp'] = df_DA['DeliveryDate'] + ' ' + df_DA['HourStarting']
df_DA['Timestamp'] = pd.to_datetime(df_DA['Timestamp'])
df_DA.drop(columns=['DeliveryDate','HourStarting','HourEnding'],inplace=True)
df_DA.set_index('Timestamp',inplace=True)
df_DA.rename(columns={'LMP':'DA'},inplace=True)

df_prices = df_RTP.merge(df_DA,how='outer',left_index=True,right_index=True)
df_prices['DA'] = df_prices['DA'].fillna(method='ffill')
df_prices.dropna(axis=0,inplace=True)

startdate = pd.to_datetime('2015-07-01 00:00:00')
delta = startdate - df_prices.index[0]
df_prices.index = df_prices.index + delta
df_prices.index.rename('timestamp',inplace=True)
df_prices.to_csv('ercot_2017.csv')