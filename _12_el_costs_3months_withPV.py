import os
import pandas as pd
import numpy as np

run = 'FinalReport2' #'FinalReport_Jul1d'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_final2.csv'
df_settings = pd.read_csv(settings_file)
p_max = 100.
risk_prem = 1.025

#market with 1600 (Jan/Jul/Oct) and 25% PV
inds = ['0073','0074','0075']

##############
#JANUARY
##############

print('JANUARY')

ind = '0000'
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
directory = run + '_' + ind + '_vis'

#Procurement costs
df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0],parse_dates=True)
df_system = df_system.iloc[24*60:]
df_system['measured_real_energy'] = df_system['measured_real_power']/60.

#Include PV from Jan
df_inv_load = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + inds[0]+'/total_P_Out.csv',skiprows=range(8))
df_PV_appl = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + inds[0]+'/df_PV_state.csv')
list_PV = list(df_PV_appl['inverter_name'])
df_inv_load['# timestamp'] = df_inv_load['# timestamp'].map(lambda x: str(x)[:-4])
df_inv_load = df_inv_load.iloc[:-1]
df_inv_load['# timestamp'] = pd.to_datetime(df_inv_load['# timestamp'])
df_inv_load.set_index('# timestamp',inplace=True)    
df_PV =  df_inv_load[list_PV]/1000000 #W -> MW (comes from GridlabD)
df_PV = df_PV/60. #convert to energy
df_system['PV_infeed'] = df_PV.sum(axis=1)

df_system['measured_real_energy'] = df_system['measured_real_energy'] - df_system['PV_infeed'] #Net measured power

df_system['p_max'] = p_max
df_system['WS_capped'] = df_system[["WS", "p_max"]].min(axis=1)
df_system['procurement_cost'] = df_system['measured_real_energy']*df_system['WS_capped'] # in MW and USD/MWh

proc_cost_Jan_nomarket = df_system['procurement_cost'].sum()
print('Procurement cost in January (no market): '+str(proc_cost_Jan_nomarket))

#Total house load no market
df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8))
df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
df_total_load = df_total_load.iloc[:-1]
df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
df_total_load.set_index('# timestamp',inplace=True)
df_total_load = df_total_load.iloc[24*60:]/1000 #convert to MW
df_total_load = df_total_load/60. #convert to energy

df_total_load_gross = df_total_load.copy()

#Subtract PV generation
for house in df_total_load.columns:
	if house in list(df_PV_appl['house_name']):
		PV_inv = df_PV_appl['inverter_name'].loc[df_PV_appl['house_name'] == house].iloc[0]
		df_total_load[house] = df_total_load[house] - df_PV[PV_inv]

df_total_load_all = df_total_load.copy()

energy_nomarket_Jan = df_total_load.sum().sum() # Total net energy
print('Energy in January (no market): '+str(energy_nomarket_Jan))



print('\nJULY')

ind = '0001'
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
directory = run + '_' + ind + '_vis'

#Procurement costs
df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0],parse_dates=True)
df_system = df_system.iloc[24*60:]
df_system['measured_real_energy'] = df_system['measured_real_power']/60.

#Include PV from Jul
df_inv_load = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + inds[1]+'/total_P_Out.csv',skiprows=range(8))
list_PV = list(pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + inds[1]+'/df_PV_state.csv')['inverter_name'])
df_inv_load['# timestamp'] = df_inv_load['# timestamp'].map(lambda x: str(x)[:-4])
df_inv_load = df_inv_load.iloc[:-1]
df_inv_load['# timestamp'] = pd.to_datetime(df_inv_load['# timestamp'])
df_inv_load.set_index('# timestamp',inplace=True)    
df_PV =  df_inv_load[list_PV]/1000000 #W -> MW (comes from GridlabD)
df_PV = df_PV/60.
df_system['PV_infeed'] = df_PV.sum(axis=1)
df_system['measured_real_energy'] = df_system['measured_real_energy'] - df_system['PV_infeed'] #Net measured power

df_system['p_max'] = p_max
df_system['WS_capped'] = df_system[["WS", "p_max"]].min(axis=1)
df_system['procurement_cost'] = df_system['measured_real_energy']*df_system['WS_capped'] # in MW and USD/MWh

proc_cost_Jul_nomarket = df_system['procurement_cost'].sum()
print('Procurement cost in July (no market): '+str(proc_cost_Jul_nomarket))

#Total house load no market
df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8))
df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
df_total_load = df_total_load.iloc[:-1]
df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
df_total_load.set_index('# timestamp',inplace=True)
df_total_load = df_total_load.iloc[24*60:]/1000 #convert to MW
df_total_load = df_total_load/60. #convert to energy

df_total_load_gross = df_total_load.copy()

#Subtract PV generation
for house in df_total_load.columns:
	if house in list(df_PV_appl['house_name']):
		PV_inv = df_PV_appl['inverter_name'].loc[df_PV_appl['house_name'] == house].iloc[0]
		df_total_load[house] = df_total_load[house] - df_PV[PV_inv]

df_total_load_all = df_total_load_all.append(df_total_load) #Total net load per house and time step

energy_nomarket_Jul = df_total_load.sum().sum()
print('Energy in July (no market): '+str(energy_nomarket_Jul))




print('\nOCTOBER')

ind = '0002'
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
directory = run + '_' + ind + '_vis'

#Procurement costs
df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0],parse_dates=True)
df_system = df_system.iloc[24*60:]
df_system['measured_real_energy'] = df_system['measured_real_power']/60.

#Include PV from Oct
df_inv_load = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + inds[2]+'/total_P_Out.csv',skiprows=range(8))
list_PV = list(pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + inds[2]+'/df_PV_state.csv')['inverter_name'])
df_inv_load['# timestamp'] = df_inv_load['# timestamp'].map(lambda x: str(x)[:-4])
df_inv_load = df_inv_load.iloc[:-1]
df_inv_load['# timestamp'] = pd.to_datetime(df_inv_load['# timestamp'])
df_inv_load.set_index('# timestamp',inplace=True)    
df_PV =  df_inv_load[list_PV]/1000000 #W -> MW (comes from GridlabD)
df_PV = df_PV/60.
df_system['PV_infeed'] = df_PV.sum(axis=1)
df_system['measured_real_energy'] = df_system['measured_real_energy'] - df_system['PV_infeed'] #Net measured power

df_system['p_max'] = p_max
df_system['WS_capped'] = df_system[["WS", "p_max"]].min(axis=1)
df_system['procurement_cost'] = df_system['measured_real_energy']*df_system['WS_capped'] # in MW and USD/MWh

proc_cost_Oct_nomarket = df_system['procurement_cost'].sum()
print('Procurement cost in October (no market): '+str(proc_cost_Oct_nomarket))

#Total house load no market
df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8))
df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
df_total_load = df_total_load.iloc[:-1]
df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
df_total_load.set_index('# timestamp',inplace=True)
df_total_load = df_total_load.iloc[24*60:]/1000 #convert to MW
df_total_load = df_total_load/60. #convert to energy

df_total_load_gross = df_total_load.copy()

#Subtract PV generation
for house in df_total_load.columns:
	if house in list(df_PV_appl['house_name']):
		PV_inv = df_PV_appl['inverter_name'].loc[df_PV_appl['house_name'] == house].iloc[0]
		df_total_load[house] = df_total_load[house] - df_PV[PV_inv]

df_total_load_all = df_total_load_all.append(df_total_load)

energy_nomarket_Oct = df_total_load.sum().sum()
print('Energy in October (no market): '+str(energy_nomarket_Oct))



#Calculate the retail tariff for procurement of energy
proc_cost_nomarket = proc_cost_Jan_nomarket + proc_cost_Jul_nomarket + proc_cost_Oct_nomarket
energy_nomarket= energy_nomarket_Jan + energy_nomarket_Jul + energy_nomarket_Oct
retail_nomarket = proc_cost_nomarket/energy_nomarket
print('Retail tariff (no market): '+str(retail_nomarket))
df_cost_nomarket = df_total_load_all*retail_nomarket
df_cost = pd.DataFrame(index=df_cost_nomarket.columns,columns=['costs_nomarket'],data=df_cost_nomarket.sum(axis=0))
df_cost['costs_nomarket_riskprem5'] = df_cost['costs_nomarket']*risk_prem

df_cost['PV_exists'] = 0
for house in df_cost.index:
	if house in list(df_PV_appl['house_name']):
		df_cost.at[house,'PV_exists'] = 1

#with market
print('\nJanuary with market but C = 1600kW')

ind = inds[0]
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
directory = run + '_' + ind + '_vis'

#Procurement cost
df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0],parse_dates=True)
df_system = df_system.iloc[24*60:]
df_system['measured_real_energy'] = df_system['measured_real_power']/60. #MW
df_system['p_max'] = p_max
df_system['WS_capped'] = df_system[["WS", "p_max"]].min(axis=1)
df_system['procurement_cost'] = df_system['measured_real_energy']*df_system['WS_capped'] # in MW and USD/MWh

proc_cost_Jan_market = df_system['procurement_cost'].sum()
print('Procurement cost in January (market): '+str(proc_cost_Jan_market))

#Total house load with market
df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8))
df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
df_total_load = df_total_load.iloc[:-1]
df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
df_total_load.set_index('# timestamp',inplace=True)
df_total_load = df_total_load.iloc[24*60:]/1000 #convert to MW
df_total_load = df_total_load/60. #convert to energy

df_hvac_load = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8))
df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
df_hvac_load = df_hvac_load.iloc[:-1]
df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
df_hvac_load.set_index('# timestamp',inplace=True)
df_hvac_load = df_hvac_load.iloc[24*60:]/1000 #convert to MW
df_hvac_load = df_hvac_load/60. #convert to energy

#Include PV from Oct
df_inv_load = pd.read_csv(folder+'/total_P_Out.csv',skiprows=range(8))
list_PV = list(pd.read_csv(folder+'/df_PV_state.csv')['inverter_name'])
df_inv_load['# timestamp'] = df_inv_load['# timestamp'].map(lambda x: str(x)[:-4])
df_inv_load = df_inv_load.iloc[:-1]
df_inv_load['# timestamp'] = pd.to_datetime(df_inv_load['# timestamp'])
df_inv_load.set_index('# timestamp',inplace=True)    
df_PV =  df_inv_load[list_PV]/1000000 #W -> MW (comes from GridlabD)
df_PV = df_PV/60.

df_base_load = df_total_load - df_hvac_load #for100% flex hvac!
df_flex_load = df_hvac_load.copy()
for house in df_hvac_load.columns:
	if house in list(df_PV_appl['house_name']):
		PV_inv = df_PV_appl['inverter_name'].loc[df_PV_appl['house_name'] == house].iloc[0]
		df_flex_load[house] = df_flex_load[house] - df_PV[PV_inv]

#Clearing prices
df_cleared = pd.read_csv(folder+'/df_prices.csv',parse_dates=[0]) #USD/MWh
df_cleared.rename(columns={'Unnamed: 0':'timedate'},inplace=True)
df_cleared.set_index('timedate',inplace=True)
df_cleared = df_cleared[['clearing_price']].iloc[24*12:]
df_cleared_long = pd.DataFrame(index=df_total_load.index,columns=['clearing_price'],data=df_cleared['clearing_price'])
df_cleared_long.fillna(method='ffill',inplace=True)

#Calculate procurement costs
df_costs_market_Jan = df_base_load*retail_nomarket + df_flex_load.multiply(df_cleared_long['clearing_price'], axis="index")
df_cost['Jan_market_1600'] = df_costs_market_Jan.sum(axis=0)




print('\nJuly with market but C = 1600kW')

ind = inds[1]
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
directory = run + '_' + ind + '_vis'

#Procurement cost
df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0],parse_dates=True)
df_system = df_system.iloc[24*60:]
df_system['measured_real_energy'] = df_system['measured_real_power']/60.
df_system['p_max'] = p_max
df_system['WS_capped'] = df_system[["WS", "p_max"]].min(axis=1)
df_system['procurement_cost'] = df_system['measured_real_energy']*df_system['WS_capped'] # in MW and USD/MWh

proc_cost_Jul_market = df_system['procurement_cost'].sum()
print('Procurement cost in July (market): '+str(proc_cost_Jul_market))

#Total house load with market
df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8))
df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
df_total_load = df_total_load.iloc[:-1]
df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
df_total_load.set_index('# timestamp',inplace=True)
df_total_load = df_total_load.iloc[24*60:]/1000 #convert to MW
df_total_load = df_total_load/60. #convert to energy

df_hvac_load = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8))
df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
df_hvac_load = df_hvac_load.iloc[:-1]
df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
df_hvac_load.set_index('# timestamp',inplace=True)
df_hvac_load = df_hvac_load.iloc[24*60:]/1000 #convert to MW
df_hvac_load = df_hvac_load/60. #convert to energy

#Include PV from Oct
df_inv_load = pd.read_csv(folder+'/total_P_Out.csv',skiprows=range(8))
list_PV = list(pd.read_csv(folder+'/df_PV_state.csv')['inverter_name'])
df_inv_load['# timestamp'] = df_inv_load['# timestamp'].map(lambda x: str(x)[:-4])
df_inv_load = df_inv_load.iloc[:-1]
df_inv_load['# timestamp'] = pd.to_datetime(df_inv_load['# timestamp'])
df_inv_load.set_index('# timestamp',inplace=True)    
df_PV =  df_inv_load[list_PV]/1000000 #W -> MW (comes from GridlabD)
df_PV = df_PV/60.

df_base_load = df_total_load - df_hvac_load #for100% flex hvac!
df_flex_load = df_hvac_load.copy()
for house in df_hvac_load.columns:
	if house in list(df_PV_appl['house_name']):
		PV_inv = df_PV_appl['inverter_name'].loc[df_PV_appl['house_name'] == house].iloc[0]
		df_flex_load[house] = df_flex_load[house] - df_PV[PV_inv]

#Clearing prices
df_cleared = pd.read_csv(folder+'/df_prices.csv',parse_dates=[0]) #USD/MWh
df_cleared.rename(columns={'Unnamed: 0':'timedate'},inplace=True)
df_cleared.set_index('timedate',inplace=True)
df_cleared = df_cleared[['clearing_price']].iloc[24*12:]
df_cleared_long = pd.DataFrame(index=df_total_load.index,columns=['clearing_price'],data=df_cleared['clearing_price'])
df_cleared_long.fillna(method='ffill',inplace=True)

#Calculate procurement costs
df_costs_market_Jul = df_base_load*retail_nomarket + df_flex_load.multiply(df_cleared_long['clearing_price'], axis="index")
df_cost['Jul_market_1600'] = df_costs_market_Jul.sum(axis=0)



print('\nOctober with market but C = 1600kW')

ind = inds[2]
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
directory = run + '_' + ind + '_vis'

#Procurement cost
df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0],parse_dates=True)
df_system = df_system.iloc[24*60:]
df_system['measured_real_energy'] = df_system['measured_real_power']/60.
df_system['p_max'] = p_max
df_system['WS_capped'] = df_system[["WS", "p_max"]].min(axis=1)
df_system['procurement_cost'] = df_system['measured_real_energy']*df_system['WS_capped'] # in MW and USD/MWh

proc_cost_Oct_market = df_system['procurement_cost'].sum()
print('Procurement cost in October (market): '+str(proc_cost_Oct_market))

#Total house load with market
df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8))
df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
df_total_load = df_total_load.iloc[:-1]
df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
df_total_load.set_index('# timestamp',inplace=True)
df_total_load = df_total_load.iloc[24*60:]/1000 #convert to MW
df_total_load = df_total_load/60. #convert to energy

df_hvac_load = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8))
df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
df_hvac_load = df_hvac_load.iloc[:-1]
df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
df_hvac_load.set_index('# timestamp',inplace=True)
df_hvac_load = df_hvac_load.iloc[24*60:]/1000 #convert to MW
df_hvac_load = df_hvac_load/60. #convert to energy

#Include PV from Oct
df_inv_load = pd.read_csv(folder+'/total_P_Out.csv',skiprows=range(8))
list_PV = list(pd.read_csv(folder+'/df_PV_state.csv')['inverter_name'])
df_inv_load['# timestamp'] = df_inv_load['# timestamp'].map(lambda x: str(x)[:-4])
df_inv_load = df_inv_load.iloc[:-1]
df_inv_load['# timestamp'] = pd.to_datetime(df_inv_load['# timestamp'])
df_inv_load.set_index('# timestamp',inplace=True)    
df_PV =  df_inv_load[list_PV]/1000000 #W -> MW (comes from GridlabD)
df_PV = df_PV/60.

df_base_load = df_total_load - df_hvac_load #for100% flex hvac!
df_flex_load = df_hvac_load.copy()
for house in df_hvac_load.columns:
	if house in list(df_PV_appl['house_name']):
		PV_inv = df_PV_appl['inverter_name'].loc[df_PV_appl['house_name'] == house].iloc[0]
		df_flex_load[house] = df_flex_load[house] - df_PV[PV_inv]

#Clearing prices
df_cleared = pd.read_csv(folder+'/df_prices.csv',parse_dates=[0]) #USD/MWh
df_cleared.rename(columns={'Unnamed: 0':'timedate'},inplace=True)
df_cleared.set_index('timedate',inplace=True)
df_cleared = df_cleared[['clearing_price']].iloc[24*12:]
df_cleared_long = pd.DataFrame(index=df_total_load.index,columns=['clearing_price'],data=df_cleared['clearing_price'])
df_cleared_long.fillna(method='ffill',inplace=True)

#Calculate procurement costs
df_costs_market_Oct = df_base_load*retail_nomarket + df_flex_load.multiply(df_cleared_long['clearing_price'], axis="index")
df_cost['Oct_market_1600'] = df_costs_market_Oct.sum(axis=0)


df_cost['market_1600'] = df_cost['Jan_market_1600'] + df_cost['Jul_market_1600'] + df_cost['Oct_market_1600'] 



df_cost['abs_change_1600'] = (df_cost['market_1600'] - df_cost['costs_nomarket'])
df_cost['change_1600'] = (df_cost['market_1600'] - df_cost['costs_nomarket'])/df_cost['costs_nomarket']*100
print('\nMedian type 1600')
print(df_cost['change_1600'].median())

# ax3 = df_cost['change_1600'].hist()
# fig3 = ax3.get_figure()
# fig3.xlabel = 'Cost change in [%]'
# fig3.savefig(run+'/hist_prices_procneutral_1600.png')

df_cost['abs_change_1600_riskprem5'] = (df_cost['market_1600'] - df_cost['costs_nomarket_riskprem5'])

df_cost['change_1600_riskprem5'] = (df_cost['market_1600'] - df_cost['costs_nomarket_riskprem5'])/df_cost['costs_nomarket_riskprem5']*100
print('\nMedian type 1600 risk')
print(df_cost['change_1600_riskprem5'].median())

df_cost.to_csv(run+'/cost_changes_procneutral_1600_PV.csv')


# ax = df_cost['change_5000'].hist(bins=20,histtype='step',normed=True)
# ax = df_cost['change_5000_riskprem5'].hist(bins=20,histtype='step',normed=True)
# ax = df_cost['change_1600'].hist(bins=20,histtype='step',normed=True)
# ax = df_cost['change_1600_riskprem5'].hist(bins=20,histtype='step',normed=True)
# fig = ax.get_figure()
# fig.xlabel = 'Cost change in [%]'
# fig.ylabel = 'Share of households in [%]'

# L = ax.legend(bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=2)

# fig.savefig(run+'/hist_prices_procneutral_all.png', bbox_inches='tight')







##############
#NO MARKET
##############

#CALCULATE PROCUREMENT COSTS

# default_id = '0064'

# folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + default_id
# directory = run + '_' + default_id + '_vis'
# if not os.path.exists(directory):
#     os.makedirs(directory)

# df_system = pd.read_csv(run+'_'+default_id+'_vis/df_system.csv',index_col=[0],parse_dates=True)
# df_system = df_system.loc[start:end]
# df_system['measured_real_energy'] = df_system['measured_real_power']/60.
# df_system['procurement_cost'] = df_system['measured_real_energy']*df_system['WS'] # in MW and USD/MWh

# #CALCULATE RETAIL TARIFF

# #Total house load
# df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8))
# df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
# df_total_load = df_total_load.iloc[:-1]
# df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
# df_total_load.set_index('# timestamp',inplace=True)
# df_total_load = df_total_load.loc[start:end]/1000 #convert to MW
# df_total_load = df_total_load/60. #convert to energy

# #import pdb; pdb.set_trace()

# df_costs_nomarket_agg = pd.DataFrame(index=df_total_load.sum(axis=0).index,columns=['nomarket_energy'],data=df_total_load.sum(axis=0))

# retail_energy = df_system['procurement_cost'].sum()/df_costs_nomarket_agg['nomarket_energy'].sum()
# print('Energy component of retail price (no market) is '+str(retail_energy)+' USD/MWh')
# print('Energy component of retail price (no market) is '+str(retail_energy/10.)+' cents/MWh')

# df_costs_nomarket_agg['nomarket_cost'] = df_costs_nomarket_agg['nomarket_energy']*retail_energy

# #########
# #WITH MARKET
# #########

# market_id = '0063'

# #Get settings
# folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + market_id
# directory = run + '_' + default_id + '_vis'
# if not os.path.exists(directory):
#     os.makedirs(directory)

# s_settings = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(market_id))]
# no_houses = s_settings['flexible_houses'].iloc[0]
# PV_share = s_settings['PV_share'].iloc[0]
# EV_share = s_settings['EV_share'].iloc[0]
# Batt_share = s_settings['Batt_share'].iloc[0]

# #CALCULATE PROCUREMENT COSTS

# df_system = pd.read_csv(run+'_'+default_id+'_vis/df_system.csv',index_col=[0],parse_dates=True)
# df_system = df_system.loc[start:end]
# df_system['measured_real_energy'] = df_system['measured_real_power']/60.
# df_system['procurement_cost'] = df_system['measured_real_energy']*df_system['WS'] # in MW and USD/MWh

# #CALCULATE COUNTERFACTUAL RETAIL TARIFF

# #Total house load
# df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8))
# df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
# df_total_load = df_total_load.iloc[:-1]
# df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
# df_total_load.set_index('# timestamp',inplace=True)
# df_total_load = df_total_load.loc[start:end]/1000 #convert to MW
# df_total_load = df_total_load/60. #convert to energy

# energy_market = df_total_load.sum().sum()
# retail_energy_market = df_system['procurement_cost'].sum()/energy_market
# print('Energy component of retail price (market) is '+str(retail_energy_market)+' USD/MWh')
# print('Energy component of retail price (market) is '+str(retail_energy_market/10.)+' cents/kWh')

# #CALCULATE EXPENSES WITH TS

# df_cleared = pd.read_csv(folder+'/df_prices.csv',parse_dates=[0]) #USD/MWh
# df_cleared.rename(columns={'Unnamed: 0':'timedate'},inplace=True)
# df_cleared.set_index('timedate',inplace=True)
# df_cleared = df_cleared[['clearing_price']].loc[start:end]
# df_cleared_long = pd.DataFrame(index=df_total_load.index,columns=['clearing_price'],data=df_cleared['clearing_price'])
# df_cleared_long.fillna(method='ffill',inplace=True)

# df_costs_market = df_total_load.multiply(df_cleared_long['clearing_price'], axis="index")
# market_data = np.vstack((df_total_load.sum(axis=0).values,df_costs_market.sum(axis=0).values)).transpose()
# df_costs_market_agg = pd.DataFrame(index=df_costs_market.sum(axis=0).index,columns=['market_energy','market_cost'],data=market_data)

# df_costs_market_agg = df_costs_market_agg.merge(df_costs_nomarket_agg,left_index=True,right_index=True)

# total_revenue = df_costs_market_agg['market_cost'].sum()

# df_costs_market_agg['cost_change'] = (df_costs_market_agg['market_cost']/df_costs_market_agg['nomarket_cost'] - 1.)*100

# ax = df_costs_market_agg['cost_change'].hist()
# fig = ax.get_figure()
# fig.xlabel = 'Cost change in [%]'
# fig.savefig(run+'_'+market_id+'_vis/hist_prices_procneutral_withshifting.png')


# print(df_costs_market_agg['cost_change'].median())

#df_costs_market_agg['market_cost_noshift'] = df_costs_market_agg['nomarket_energy']*
#df_costs_market_agg['cost_change_noshift'] = (df_costs_market_agg['market_cost_noshift']/df_costs_market_agg['nomarket_cost'] - 1.)*100
