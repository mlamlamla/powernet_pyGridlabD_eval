import os
import pandas as pd
import numpy as np

run = 'FinalReport2' #'FinalReport_Jul1d'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_final2.csv'
df_settings = pd.read_csv(settings_file)

start = pd.Timestamp(2015, 7, 16)
end = pd.Timestamp(2015, 7, 17)

fixed_retail= 50

##############
#NO MARKET
##############

#CALCULATE PROCUREMENT COSTS

default_id = '0001'

folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + default_id
directory = run + '_' + default_id + '_vis'
if not os.path.exists(directory):
    os.makedirs(directory)

df_system = pd.read_csv(run+'_'+default_id+'_vis/df_system.csv',index_col=[0],parse_dates=True)
df_system = df_system.loc[start:end]
df_system['measured_real_energy'] = df_system['measured_real_power']/60.
df_system['procurement_cost'] = df_system['measured_real_energy']*df_system['WS'] # in MW and USD/MWh

#CALCULATE RETAIL TARIFF

#Total house load
df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8))
df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
df_total_load = df_total_load.iloc[:-1]
df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
df_total_load.set_index('# timestamp',inplace=True)
df_total_load = df_total_load.loc[start:end]/1000 #convert to MW
df_total_load = df_total_load/60. #convert to energy

#import pdb; pdb.set_trace()

df_costs_nomarket_agg = pd.DataFrame(index=df_total_load.sum(axis=0).index,columns=['nomarket_energy'],data=df_total_load.sum(axis=0))

retail_energy = df_system['procurement_cost'].sum()/df_costs_nomarket_agg['nomarket_energy'].sum()
print('Energy component of retail price (no market) is '+str(retail_energy)+' USD/MWh')
print('Energy component of retail price (no market) is '+str(retail_energy/10.)+' cents/MWh')

df_costs_nomarket_agg['nomarket_cost'] = df_costs_nomarket_agg['nomarket_energy']*retail_energy

#########
#WITH MARKET
#########

market_id = '0063'

#Get settings
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + market_id
directory = run + '_' + default_id + '_vis'
if not os.path.exists(directory):
    os.makedirs(directory)

s_settings = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(market_id))]
no_houses = s_settings['flexible_houses'].iloc[0]
PV_share = s_settings['PV_share'].iloc[0]
EV_share = s_settings['EV_share'].iloc[0]
Batt_share = s_settings['Batt_share'].iloc[0]

#CALCULATE PROCUREMENT COSTS

df_system = pd.read_csv(run+'_'+default_id+'_vis/df_system.csv',index_col=[0],parse_dates=True)
df_system = df_system.loc[start:end]
df_system['measured_real_energy'] = df_system['measured_real_power']/60.
df_system['procurement_cost'] = df_system['measured_real_energy']*df_system['WS'] # in MW and USD/MWh

#CALCULATE COUNTERFACTUAL RETAIL TARIFF

#Total house load
df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8))
df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
df_total_load = df_total_load.iloc[:-1]
df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
df_total_load.set_index('# timestamp',inplace=True)
df_total_load = df_total_load.loc[start:end]/1000 #convert to MW
df_total_load = df_total_load/60. #convert to energy

energy_market = df_total_load.sum().sum()
retail_energy_market = df_system['procurement_cost'].sum()/energy_market
print('Energy component of retail price (market) is '+str(retail_energy_market)+' USD/MWh')
print('Energy component of retail price (market) is '+str(retail_energy_market/10.)+' cents/kWh')

#CALCULATE EXPENSES WITH TS

df_cleared = pd.read_csv(folder+'/df_prices.csv',parse_dates=[0]) #USD/MWh
df_cleared.rename(columns={'Unnamed: 0':'timedate'},inplace=True)
df_cleared.set_index('timedate',inplace=True)
df_cleared = df_cleared[['clearing_price']].loc[start:end]
df_cleared_long = pd.DataFrame(index=df_total_load.index,columns=['clearing_price'],data=df_cleared['clearing_price'])
df_cleared_long.fillna(method='ffill',inplace=True)

df_costs_market = df_total_load.multiply(df_cleared_long['clearing_price'], axis="index")
market_data = np.vstack((df_total_load.sum(axis=0).values,df_costs_market.sum(axis=0).values)).transpose()
df_costs_market_agg = pd.DataFrame(index=df_costs_market.sum(axis=0).index,columns=['market_energy','market_cost'],data=market_data)

df_costs_market_agg = df_costs_market_agg.merge(df_costs_nomarket_agg,left_index=True,right_index=True)

total_revenue = df_costs_market_agg['market_cost'].sum()

df_costs_market_agg['cost_change'] = (df_costs_market_agg['market_cost']/df_costs_market_agg['nomarket_cost'] - 1.)*100

ax = df_costs_market_agg['cost_change'].hist()
fig = ax.get_figure()
fig.xlabel = 'Cost change in [%]'
fig.savefig(run+'_'+market_id+'_vis/hist_prices_procneutral_withshifting.png')


print(df_costs_market_agg['cost_change'].median())

#df_costs_market_agg['market_cost_noshift'] = df_costs_market_agg['nomarket_energy']*
#df_costs_market_agg['cost_change_noshift'] = (df_costs_market_agg['market_cost_noshift']/df_costs_market_agg['nomarket_cost'] - 1.)*100
