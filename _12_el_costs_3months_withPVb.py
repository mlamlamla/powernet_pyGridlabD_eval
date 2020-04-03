import os
import pandas as pd
import numpy as np

def get_monthly(run,ind,month,df_total_load_all=None):
	folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
	directory = run + '_' + ind + '_vis'

	#Procurement costs
	df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0],parse_dates=True).iloc[(24*60):]
	print(str(len(df_system)/(24*60))+' days')
	#df_system = df_system.iloc[24*60:]
	df_system['measured_real_energy'] = df_system['measured_real_power']/60.

	df_system['p_max'] = p_max
	df_system['WS_capped'] = df_system[["WS", "p_max"]].min(axis=1)

	#Total house load no market
	df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8)).iloc[(24*60):]
	df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
	df_total_load = df_total_load.iloc[:-1]
	df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
	df_total_load.set_index('# timestamp',inplace=True)
	df_total_load = df_total_load/1000 #convert to MW
	df_total_load = df_total_load/60. #convert to energy

	df_total_load_gross = df_total_load.copy()

	#Subtract PV generation and add EV consumption
	if month == 'JANUARY':
		df_inv_load = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_0073/total_P_Out.csv',skiprows=range(8))
	elif month == 'JULY':
		df_inv_load = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_0074/total_P_Out.csv',skiprows=range(8))
	elif month == 'OCTOBER':
		df_inv_load = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_0075/total_P_Out.csv',skiprows=range(8))
	else:
		import sys
		sys.exit('no such month')
	df_inv_load['# timestamp'] = df_inv_load['# timestamp'].map(lambda x: str(x)[:-4])
	df_inv_load = df_inv_load.iloc[(24*60):]
	df_inv_load['# timestamp'] = pd.to_datetime(df_inv_load['# timestamp'])
	df_inv_load.set_index('# timestamp',inplace=True)  
	df_inv_load = (df_inv_load/1000000)/60 # to MWh

	#Include PV
	df_PV_appl = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind+'/df_PV_state.csv')
	list_PV = list(pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind+'/df_PV_state.csv')['inverter_name'])  
	df_PV =  df_inv_load[list_PV] #W -> MW (comes from GridlabD)
	for house in df_total_load.columns:
		if house in (df_PV_appl['house_name']).tolist():
			PV_inv = df_PV_appl['inverter_name'].loc[df_PV_appl['house_name'] == house].iloc[0]
			df_total_load[house] = df_total_load[house] - df_PV[PV_inv]

	df_system['measured_real_energy'] = df_system['measured_real_energy'] - df_PV.sum(axis=1)
	df_system['procurement_cost'] = df_system['measured_real_energy']*df_system['WS_capped'] # in MW and USD/MWh

	proc_cost_Jan_nomarket = df_system['procurement_cost'].sum()
	print('Procurement cost in January (no market): '+str(proc_cost_Jan_nomarket))

	if df_total_load_all is None:
		print('df_total_load_all doesnot exist yet')
		df_total_load_all = df_total_load.copy() #Becomes master load df
	else:
		df_total_load_all = df_total_load_all.append(df_total_load)

	energy_nomarket_Jan = df_total_load.sum().sum() # Total net energy
	print('Energy in '+month+' (no market): '+str(energy_nomarket_Jan))

	print(str(len(df_system)/(24*60))+' days')
	print(str(len(df_total_load)/(24*60))+' days')
	print(str(len(df_inv_load)/(24*60))+' days')

	return df_total_load_all, proc_cost_Jan_nomarket, energy_nomarket_Jan

def get_monthly_wm(run,ind,month,df_total_base_market=None,df_total_flex_market=None,df_cleared_market=None):

	folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
	directory = run + '_' + ind + '_vis'

	#Procurement cost
	df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0],parse_dates=True)
	df_system = df_system #.iloc[24*60:]
	df_system['measured_real_energy'] = df_system['measured_real_power']/60. #MW
	df_system['p_max'] = p_max
	df_system['WS_capped'] = df_system[["WS", "p_max"]].min(axis=1)
	df_system['procurement_cost'] = df_system['measured_real_energy']*df_system['WS_capped'] # in MW and USD/MWh

	proc_cost_Jan_market = df_system['procurement_cost'].sum()
	print('Procurement cost in '+month+' (market): '+str(proc_cost_Jan_market))
	print(str(int(len(df_system)/(24*60)))+' days')

	#Total house load with market
	df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8))
	df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
	df_total_load = df_total_load.iloc[:-1]
	df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
	df_total_load.set_index('# timestamp',inplace=True)
	df_total_load = df_total_load/1000 #convert to MW
	df_total_load = df_total_load/60. #convert to energy

	df_hvac_load = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8))
	df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
	df_hvac_load = df_hvac_load.iloc[:-1]
	df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
	df_hvac_load.set_index('# timestamp',inplace=True)
	df_hvac_load = df_hvac_load/1000 #convert to MW
	df_hvac_load = df_hvac_load/60. #convert to energy

	#Include PV from Oct
	df_inv_load = pd.read_csv(folder+'/total_P_Out.csv',skiprows=range(8))
	df_inv_load['# timestamp'] = df_inv_load['# timestamp'].map(lambda x: str(x)[:-4])
	df_inv_load = df_inv_load.iloc[:-1]
	df_inv_load['# timestamp'] = pd.to_datetime(df_inv_load['# timestamp'])
	df_inv_load.set_index('# timestamp',inplace=True)  
	df_inv_load = (df_inv_load/1000000)/60 # to MWh

	list_PV = list(pd.read_csv(folder+'/df_PV_state.csv')['inverter_name'])  
	df_PV =  df_inv_load[list_PV]

	df_base_load = df_total_load - df_hvac_load #for100% flex hvac!
	df_flex_load = df_hvac_load.copy()
	for house in df_hvac_load.columns:
		if house in (df_PV_appl['house_name']).tolist():
			PV_inv = df_PV_appl['inverter_name'].loc[df_PV_appl['house_name'] == house].iloc[0]
			df_flex_load[house] = df_flex_load[house] - df_PV[PV_inv]

	#Clearing prices
	df_cleared = pd.read_csv(folder+'/df_prices.csv',parse_dates=[0]) #USD/MWh
	df_cleared.rename(columns={'Unnamed: 0':'timedate'},inplace=True)
	df_cleared.set_index('timedate',inplace=True)
	df_cleared = df_cleared[['clearing_price']].iloc[24*12:]
	df_cleared_long = pd.DataFrame(index=df_total_load.index,columns=['clearing_price'],data=df_cleared['clearing_price'])
	df_cleared_long.fillna(method='ffill',inplace=True)

	print(str(int(len(df_system)/(24*60)))+' days')
	print(str(int(len(df_total_load)/(24*60)))+' days')
	print(str(int(len(df_hvac_load)/(24*60)))+' days')
	print(str(int(len(df_inv_load)/(24*60)))+' days')
	print(str(int(len(df_cleared_long)/(24*60)))+' days')

	#Total load
	if df_total_base_market is None:
		print('df_total_load_all_market doesnot exist yet')
		df_total_base_market = df_base_load.copy() #Becomes master load df
		df_total_flex_market = df_flex_load.copy() #Becomes master load df
		df_cleared_market = df_cleared_long.copy()
	else:
		df_total_base_market = df_total_base_market.append(df_base_load)
		df_total_flex_market = df_total_flex_market.append(df_flex_load)
		df_cleared_market = df_cleared_market.append(df_cleared_long)

	energy_nomarket_Jan = df_total_load.sum().sum() - df_PV.sum().sum()

	return df_total_base_market, df_total_flex_market, df_cleared_market, proc_cost_Jan_market, energy_nomarket_Jan

##############
#SETTINGS
##############

run = 'FinalReport2' #'FinalReport_Jul1d'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_final2.csv'
df_settings = pd.read_csv(settings_file)
p_max = 100.
risk_prem = 1.025

df_PV_appl = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_0073/df_PV_state.csv')

##############
#NO MARKET YET
##############

df_total_load_all, proc_cost_Jan_nomarket, energy_nomarket_Jan = get_monthly(run,'0000','JANUARY')
df_total_load_all, proc_cost_Jul_nomarket, energy_nomarket_Jul = get_monthly(run,'0001','JULY',df_total_load_all)
df_total_load_all, proc_cost_Oct_nomarket, energy_nomarket_Oct = get_monthly(run,'0002','OCTOBER',df_total_load_all)

#Calculate the retail tariff for procurement of energy
proc_cost_nomarket = proc_cost_Jan_nomarket + proc_cost_Jul_nomarket + proc_cost_Oct_nomarket
energy_nomarket= energy_nomarket_Jan + energy_nomarket_Jul + energy_nomarket_Oct
retail_nomarket = proc_cost_nomarket/energy_nomarket
print('Retail tariff (no market): '+str(retail_nomarket))

#Calculate cost for houses without a market under a constant retail tariff
df_cost_nomarket = df_total_load_all*retail_nomarket
df_cost = pd.DataFrame(index=df_cost_nomarket.columns,columns=['costs_nomarket'],data=df_cost_nomarket.sum(axis=0))
df_cost['costs_nomarket_riskprem5'] = df_cost['costs_nomarket']*risk_prem

df_cost['PV_exists'] = 0
for house in df_cost.index:
	if house in list(df_PV_appl['house_name']):
		df_cost.at[house,'PV_exists'] = 1

##############
#MARKET
##############

df_total_base_market, df_total_flex_market, df_cleared_market, proc_cost_Jan_market, energy_market_Jan = get_monthly_wm(run,'0073','JANUARY')
df_total_base_market, df_total_flex_market, df_cleared_market, proc_cost_Jul_market, energy_market_Jul = get_monthly_wm(run,'0074','JULY',df_total_base_market, df_total_flex_market,df_cleared_market)
df_total_base_market, df_total_flex_market, df_cleared_market, proc_cost_Oct_market, energy_market_Oct = get_monthly_wm(run,'0075','OCTOBER',df_total_base_market, df_total_flex_market,df_cleared_market)

retail_new = (proc_cost_Jan_market + proc_cost_Jul_market + proc_cost_Oct_market)/(energy_market_Jan + energy_market_Jul + energy_market_Oct)
print('New retail tariff (with market): '+str(retail_new))

#import pdb; pdb.set_trace()
#Calculate consumer costs
df_costs_market = df_total_base_market*retail_nomarket + df_total_flex_market.multiply(df_cleared_market['clearing_price'], axis="index")
df_cost['cost_market_oldRR'] = df_costs_market.sum(axis=0)
df_cost['cost_market_oldRR_riskprem5'] = df_costs_market.sum(axis=0)*risk_prem

df_costs_market = df_total_base_market*retail_new + df_total_flex_market.multiply(df_cleared_market['clearing_price'], axis="index")
df_cost['cost_market_newRR'] = df_costs_market.sum(axis=0)
df_cost['cost_market_newRR_riskprem5'] = df_costs_market.sum(axis=0)*risk_prem

df_cost['abs_change_oldRR'] = (df_cost['cost_market_oldRR'] - df_cost['costs_nomarket'])
df_cost['change_oldRR'] = (df_cost['cost_market_oldRR'] - df_cost['costs_nomarket'])/df_cost['costs_nomarket']*100
print('\nMedian type 1600 old RR')
print(df_cost['change_oldRR'].median())

df_cost['abs_change_newRR'] = (df_cost['cost_market_newRR'] - df_cost['costs_nomarket'])
df_cost['change_newRR'] = (df_cost['cost_market_newRR'] - df_cost['costs_nomarket'])/df_cost['costs_nomarket']*100
print('\nMedian type 1600 new RR')
print(df_cost['change_newRR'].median())

df_cost.to_csv(run+'/cost_changes_procneutral_1600_PVb.csv')

