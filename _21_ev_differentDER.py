import os
import pandas as pd
import numpy as np

def get_monthly(run,ind,month,df_total_load_all=None):
	folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind
	directory = run + '_' + ind + '_vis'

	#Procurement costs
	df_system = pd.read_csv(run+'/' + directory +'/df_system.csv',index_col=[0],parse_dates=True).iloc[(24*60):]
	#df_system = df_system.iloc[24*60:]
	df_system['measured_real_energy'] = df_system['measured_real_power']/60.

	df_system['p_max'] = p_max
	df_system['WS_capped'] = df_system[["WS", "p_max"]].min(axis=1)
	df_system['procurement_cost'] = df_system['measured_real_energy']*df_system['WS_capped'] # in MW and USD/MWh

	proc_cost_Jan_nomarket = df_system['procurement_cost'].sum()
	print('Procurement cost in '+month+' (no market): '+str(proc_cost_Jan_nomarket))

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
	df_PV_appl = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind+'/df_PV_state.csv')
	list_PV = list(pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind+'/df_PV_state.csv')['inverter_name']) 
	list_EV = list(pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind+'/df_EV_state.csv')['EV_name']) 
	list_EV_inv = []
	for EV in list_EV:
		EV_inv = 'EV_inverter'+EV[2:]
		list_EV_inv += [EV_inv]

	if len(list_PV) + len(list_EV) > 0:
		df_inv_load = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind+'/total_P_Out.csv',skiprows=range(8)).iloc[(24*60):]
		df_inv_load['# timestamp'] = df_inv_load['# timestamp'].map(lambda x: str(x)[:-4])
		df_inv_load = df_inv_load.iloc[:-1]
		df_inv_load['# timestamp'] = pd.to_datetime(df_inv_load['# timestamp'])
		df_inv_load.set_index('# timestamp',inplace=True)  
		df_inv_load = (df_inv_load/1000000)/60 # to MWh

	#Include PV
	if len(list_PV) > 0:
		df_PV =  df_inv_load[list_PV] #W -> MW (comes from GridlabD)
		for house in df_total_load.columns:
			if house in (df_PV_appl['house_name']).tolist():
				PV_inv = df_PV_appl['inverter_name'].loc[df_PV_appl['house_name'] == house].iloc[0]
				df_total_load[house] = df_total_load[house] - df_PV[PV_inv]

	#Include EV consumption
	if len(list_EV):
		df_EV_appl = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind+'/df_EV_state.csv')
		df_EV =  df_inv_load[list_EV_inv]
		for house in df_total_load.columns:
			if house in (df_EV_appl['house_name']).tolist():
				EV_inv = 'EV_inverter'+df_EV_appl['EV_name'].loc[df_EV_appl['house_name'] == house].iloc[0][2:]
				df_total_load[house] = df_total_load[house] - df_EV[EV_inv] #EV_inv is negatively defined

	if df_total_load_all is None:
		#print('df_total_load_all doesnot exist yet')
		df_total_load_all = df_total_load.copy() #Becomes master load df
	else:
		df_total_load_all = df_total_load_all.append(df_total_load)

	energy_nomarket_Jan = df_total_load.sum().sum() # Total net energy
	print('Energy in '+month+' (no market): '+str(energy_nomarket_Jan))

	# print(str(len(df_system)/(24*60))+' days')
	# print(str(len(df_total_load)/(24*60))+' days')
	# print(str(len(df_inv_load)/(24*60))+' days')

	return df_total_load_all, proc_cost_Jan_nomarket, energy_nomarket_Jan

def get_monthly_wm(run,ind,month,df_total_base_market=None,df_total_flex_market=None,df_cleared_market=None):

	folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '/' + run + '_' + ind
	directory = run + '/' + run + '_' + ind + '_vis'

	#Procurement cost
	df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0],parse_dates=True).iloc[(24*60):]
	df_system = df_system #.iloc[24*60:]
	df_system['measured_real_energy'] = df_system['measured_real_power']/60. #MW
	df_system['p_max'] = p_max
	df_system['WS_capped'] = df_system[["WS", "p_max"]].min(axis=1)
	df_system['procurement_cost'] = df_system['measured_real_energy']*df_system['WS_capped'] # in MW and USD/MWh

	proc_cost_Jan_market = df_system['procurement_cost'].sum()
	print('Procurement cost in '+month+' (market): '+str(proc_cost_Jan_market))
	#print(str(len(df_system)/(24*60))+' days')

	#Total house load with market
	df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8)).iloc[(24*60):]
	df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
	df_total_load = df_total_load.iloc[:-1]
	df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
	df_total_load.set_index('# timestamp',inplace=True)
	df_total_load = df_total_load/1000 #convert to MW
	df_total_load = df_total_load/60. #convert to energy

	df_hvac_load = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8)).iloc[(24*60):]
	df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
	df_hvac_load = df_hvac_load.iloc[:-1]
	df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
	df_hvac_load.set_index('# timestamp',inplace=True)
	df_hvac_load = df_hvac_load/1000 #convert to MW
	df_hvac_load = df_hvac_load/60. #convert to energy

	df_base_load = df_total_load.copy()
	df_flex_load = df_total_load.copy()
	df_total_load.data = 0.0

	#Get list of flexible appliances
	df_PV_appl = pd.read_csv(folder+'/df_PV_state.csv')
	list_PV = list(df_PV_appl['inverter_name'])  
	df_EV_appl = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind+'/df_EV_state.csv')
	list_EV = list(df_EV_appl['EV_name']) 
	list_EV_inv = []
	for EV in list_EV:
		EV_inv = 'EV_inverter'+EV[2:]
	df_Bat_appl = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind +'/df_battery_state.csv')
	list_Bat = list(df_Bat_appl['battery_name'])
	list_Bat_inv = []
	for Bat in list_Bat:
		Bat_inv = 'Bat_inverter'+Bat[7:]
		list_Bat_inv += [Bat_inv]

	if len(list_PV) + len(list_Bat) + len(list_EV_inv) > 0:
		df_inv_load = pd.read_csv(folder+'/total_P_Out.csv',skiprows=range(8)).iloc[(24*60):]
		df_inv_load['# timestamp'] = df_inv_load['# timestamp'].map(lambda x: str(x)[:-4])
		df_inv_load = df_inv_load.iloc[:-1]
		df_inv_load['# timestamp'] = pd.to_datetime(df_inv_load['# timestamp'])
		df_inv_load.set_index('# timestamp',inplace=True)  
		df_inv_load = (df_inv_load/1000000)/60 # to MWh

		df_PV =  df_inv_load[list_PV]
		df_EV =  df_inv_load[list_EV_inv]
		df_Bat = df_inv_load[list_Bat_inv]

		df_base_load = df_total_load - df_hvac_load #for100% flex hvac!
		df_flex_load = df_hvac_load.copy()
		for house in df_hvac_load.columns:
			if len(list_PV) > 0:
				if house in (df_PV_appl['house_name']).tolist():
					PV_inv = df_PV_appl['inverter_name'].loc[df_PV_appl['house_name'] == house].iloc[0]
					df_flex_load[house] = df_flex_load[house] - df_PV[PV_inv]
			if len(list_EV_inv):
				if house in (df_EV_appl['house_name']).tolist():
					EV_inv = 'EV_inverter'+df_EV_appl['EV_name'].loc[df_EV_appl['house_name'] == house].iloc[0][2:]
					df_flex_load[house] = df_flex_load[house] - df_EV[EV_inv] #EV_inv is negatively defined
			if len(list_Bat) > 0:
				if house in (df_Bat_appl['house_name']).tolist():
					Bat_inv = 'Bat_inverter'+df_Bat_appl['battery_name'].loc[df_Bat_appl['house_name'] == house].iloc[0][7:]
					df_flex_load[house] = df_flex_load[house] - df_Bat[Bat_inv] #Bat_inv is negatively defined

	#Clearing prices
	df_cleared = pd.read_csv(folder+'/df_prices.csv',parse_dates=[0]).iloc[24*12:] #USD/MWh
	df_cleared.rename(columns={'Unnamed: 0':'timedate'},inplace=True)
	df_cleared.set_index('timedate',inplace=True)
	df_cleared = df_cleared[['clearing_price']]
	df_cleared_long = pd.DataFrame(index=df_total_load.index,columns=['clearing_price'],data=df_cleared['clearing_price'])
	df_cleared_long.fillna(method='ffill',inplace=True)

	# print(str(len(df_system)/(24*60))+' days')
	# print(str(len(df_total_load)/(24*60))+' days')
	# print(str(len(df_hvac_load)/(24*60))+' days')
	# print(str(len(df_inv_load)/(24*60))+' days')
	# print(str(len(df_cleared_long)/(24*60))+' days')

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

	energy_nomarket_Jan = df_total_load.sum().sum()
	if len(list_PV) > 0:
		energy_nomarket_Jan -= df_PV.sum().sum() 
	if len(list_EV) > 0:
		energy_nomarket_Jan -= df_EV.sum().sum() 
	if len(list_Bat) > 0:
		energy_nomarket_Jan -= df_Bat.sum().sum()

	#Use baseload only
	df_system['measured_real_energy_base'] = df_base_load.sum(axis=1)
	df_system['procurement_cost_base'] = df_system['measured_real_energy_base']*df_system['WS_capped'] # in MW and USD/MWh
	proc_cost_Jan_market = df_system['procurement_cost_base'].sum()
	energy_nomarket_Jan = df_system['measured_real_energy_base'].sum()
	print('Energy in '+month+' (market): '+str(energy_nomarket_Jan))

	return df_total_base_market, df_total_flex_market, df_cleared_market, proc_cost_Jan_market, energy_nomarket_Jan

##############
#GENERAL SETTINGS
##############

run = 'FinalReport2' #'FinalReport_Jul1d'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_final2.csv'
df_settings = pd.read_csv(settings_file)
p_max = 100.
risk_prem = 1.025

##############
#SETTINGS: Only HVAC, no other DER
#
#NO market: 64,65,66
#With market: 70,71,72 // 103, 104, 105 (with reference price based on forward prices)
##############

print('Only HVAC, no other DER')

##############
#NO MARKET YET
##############

df_total_load_all, proc_cost_Jan_nomarket, energy_nomarket_Jan = get_monthly(run,'0064','JANUARY')
df_total_load_all, proc_cost_Jul_nomarket, energy_nomarket_Jul = get_monthly(run,'0065','JULY',df_total_load_all)
df_total_load_all, proc_cost_Oct_nomarket, energy_nomarket_Oct = get_monthly(run,'0066','OCTOBER',df_total_load_all)

#Calculate the retail tariff for procurement of energy
proc_cost_nomarket = proc_cost_Jan_nomarket + proc_cost_Jul_nomarket + proc_cost_Oct_nomarket
print('Procurement cost (no market, no DER): '+str(proc_cost_nomarket))

energy_nomarket= energy_nomarket_Jan + energy_nomarket_Jul + energy_nomarket_Oct
retail_nomarket = proc_cost_nomarket/energy_nomarket
print('Retail tariff (no market, no DER): '+str(retail_nomarket))

#Calculate cost for houses without a market under a constant retail tariff
df_cost_nomarket = df_total_load_all*retail_nomarket
df_cost = pd.DataFrame(index=df_cost_nomarket.columns,columns=['costs_nomarket'],data=df_cost_nomarket.sum(axis=0))
df_cost['costs_nomarket_riskprem5'] = df_cost['costs_nomarket']*risk_prem
print('Total customer bills (no market, no DER) over three weeks: '+str(df_cost['costs_nomarket_riskprem5'].sum()))
#print('Calculate for year')

##############
#MARKET
##############

df_total_base_market, df_total_flex_market, df_cleared_market, proc_cost_Jan_market, energy_market_Jan = get_monthly_wm(run,'0106','JANUARY')
df_total_base_market, df_total_flex_market, df_cleared_market, proc_cost_Jul_market, energy_market_Jul = get_monthly_wm(run,'0107','JULY',df_total_base_market, df_total_flex_market,df_cleared_market)
df_total_base_market, df_total_flex_market, df_cleared_market, proc_cost_Oct_market, energy_market_Oct = get_monthly_wm(run,'0108','OCTOBER',df_total_base_market, df_total_flex_market,df_cleared_market)

proc_cost_market = proc_cost_Jan_market + proc_cost_Jul_market + proc_cost_Oct_market
print('Procurement cost (market, HVAC only): '+str(proc_cost_market))

retail_new = (proc_cost_market)/(energy_market_Jan + energy_market_Jul + energy_market_Oct)
print('New retail tariff (with market): '+str(retail_new))

#Calculate consumer costs
df_costs_market = df_total_base_market*retail_nomarket + df_total_flex_market.multiply(df_cleared_market['clearing_price'], axis="index")
df_cost['cost_market_oldRR'] = df_costs_market.sum(axis=0)
df_cost['cost_market_oldRR_riskprem5'] = df_costs_market.sum(axis=0)*risk_prem
print('Total customer bills (market, HVAC only) at old RR: '+str(df_cost['cost_market_oldRR_riskprem5'].sum()))

df_costs_market = df_total_base_market*retail_new + df_total_flex_market.multiply(df_cleared_market['clearing_price'], axis="index")
df_cost['cost_market_newRR'] = df_costs_market.sum(axis=0)
df_cost['cost_market_newRR_riskprem5'] = df_costs_market.sum(axis=0)*risk_prem
print('Total customer bills (market, HVAC only) at new RR: '+str(df_cost['cost_market_newRR_riskprem5'].sum()))

df_cost['abs_change_oldRR'] = (df_cost['cost_market_oldRR'] - df_cost['costs_nomarket'])
df_cost['change_oldRR'] = (df_cost['cost_market_oldRR'] - df_cost['costs_nomarket'])/df_cost['costs_nomarket']*100
print('\nMedian type 1600 old RR')
print(df_cost['change_oldRR'].median())

df_cost['abs_change_newRR'] = (df_cost['cost_market_newRR'] - df_cost['costs_nomarket'])
df_cost['change_newRR'] = (df_cost['cost_market_newRR'] - df_cost['costs_nomarket'])/df_cost['costs_nomarket']*100
print('\nMedian type 1600 new RR')
print(df_cost['change_newRR'].median())

#df_cost.to_csv(run+'/cost_changes_procneutral_1600_all.csv')

# ##############
# #SETTINGS: Only other DER, no HVAC
# #
# #NO market: 79,80,81
# #With market: 70,71,72
# ##############

# print('No HVAC, only other DER')

# ##############
# #NO MARKET YET
# ##############

# df_total_load_all, proc_cost_Jan_nomarket, energy_nomarket_Jan = get_monthly(run,'0079','JANUARY')
# df_total_load_all, proc_cost_Jul_nomarket, energy_nomarket_Jul = get_monthly(run,'0080','JULY',df_total_load_all)
# df_total_load_all, proc_cost_Oct_nomarket, energy_nomarket_Oct = get_monthly(run,'0081','OCTOBER',df_total_load_all)

# #Calculate the retail tariff for procurement of energy
# proc_cost_nomarket = proc_cost_Jan_nomarket + proc_cost_Jul_nomarket + proc_cost_Oct_nomarket
# print('Procurement cost (no market, with PV and EV): '+str(proc_cost_nomarket))

# energy_nomarket= energy_nomarket_Jan + energy_nomarket_Jul + energy_nomarket_Oct
# retail_nomarket = proc_cost_nomarket/energy_nomarket
# print('Retail tariff (no market, with PV and EV): '+str(retail_nomarket))

# #Calculate cost for houses without a market under a constant retail tariff
# df_cost_nomarket = df_total_load_all*retail_nomarket
# df_cost = pd.DataFrame(index=df_cost_nomarket.columns,columns=['costs_nomarket'],data=df_cost_nomarket.sum(axis=0))
# df_cost['costs_nomarket_riskprem5'] = df_cost['costs_nomarket']*risk_prem
# print('Total customer bills (no market, with PV and EV): '+str(df_cost['costs_nomarket_riskprem5'].sum()))
# print('Calculate for year')

# ##############
# #MARKET
# ##############

# df_total_base_market, df_total_flex_market, df_cleared_market, proc_cost_Jan_market, energy_market_Jan = get_monthly_wm(run,'0076','JANUARY')
# df_total_base_market, df_total_flex_market, df_cleared_market, proc_cost_Jul_market, energy_market_Jul = get_monthly_wm(run,'0077','JULY',df_total_base_market, df_total_flex_market,df_cleared_market)
# df_total_base_market, df_total_flex_market, df_cleared_market, proc_cost_Oct_market, energy_market_Oct = get_monthly_wm(run,'0078','OCTOBER',df_total_base_market, df_total_flex_market,df_cleared_market)

# proc_cost_market = proc_cost_Jan_market + proc_cost_Jul_market + proc_cost_Oct_market
# print('Procurement cost (market, other DER): '+str(proc_cost_market))

# retail_new = (proc_cost_market)/(energy_market_Jan + energy_market_Jul + energy_market_Oct)
# print('New retail tariff (with market): '+str(retail_new))

# #Calculate consumer costs
# df_costs_market = df_total_base_market*retail_nomarket + df_total_flex_market.multiply(df_cleared_market['clearing_price'], axis="index")
# df_cost['cost_market_oldRR'] = df_costs_market.sum(axis=0)
# df_cost['cost_market_oldRR_riskprem5'] = df_costs_market.sum(axis=0)*risk_prem
# print('Total customer bills (market, other DER) at old RR: '+str(df_cost['cost_market_oldRR_riskprem5'].sum()))

# df_costs_market = df_total_base_market*retail_new + df_total_flex_market.multiply(df_cleared_market['clearing_price'], axis="index")
# df_cost['cost_market_newRR'] = df_costs_market.sum(axis=0)
# df_cost['cost_market_newRR_riskprem5'] = df_costs_market.sum(axis=0)*risk_prem
# print('Total customer bills (market, other DER) at new RR: '+str(df_cost['cost_market_newRR_riskprem5'].sum()))

# df_cost['abs_change_oldRR'] = (df_cost['cost_market_oldRR'] - df_cost['costs_nomarket'])
# df_cost['change_oldRR'] = (df_cost['cost_market_oldRR'] - df_cost['costs_nomarket'])/df_cost['costs_nomarket']*100
# print('\nMedian type 1600 old RR')
# print(df_cost['change_oldRR'].median())

# df_cost['abs_change_newRR'] = (df_cost['cost_market_newRR'] - df_cost['costs_nomarket'])
# df_cost['change_newRR'] = (df_cost['cost_market_newRR'] - df_cost['costs_nomarket'])/df_cost['costs_nomarket']*100
# print('\nMedian type 1600 new RR')
# print(df_cost['change_newRR'].median())
