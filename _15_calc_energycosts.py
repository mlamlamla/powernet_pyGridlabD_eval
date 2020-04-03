import os
import pandas as pd
import numpy as np

#Calculates energy costs in a single run
def get_costs_perhouse(run,ind,df_cost):
	folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '/' + run + '_' + ind
	directory = run + '/' + run + '_' + ind + '_vis'

	#Get clearing price
	df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0],parse_dates=True).iloc[(24*60):]
	df_system = pd.DataFrame(index=df_system.index,columns=['clearing_price'],data=df_system['clearing_price'])

	#Total house load incl. HVAC
	df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8)).iloc[(24*60):]
	df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
	#df_total_load = df_total_load.iloc[:-1]
	df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
	df_total_load.set_index('# timestamp',inplace=True)
	df_total_load = df_total_load/1000 #convert to MW
	df_total_load = df_total_load/60. #convert to energy

	#HVAC load
	df_hvac_load = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8)).iloc[(24*60):]
	df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
	df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
	df_hvac_load.set_index('# timestamp',inplace=True)
	df_hvac_load = df_hvac_load/1000 #convert to MW
	df_hvac_load = df_hvac_load/60. #convert to energy

	df_hvac_load_cost = df_hvac_load.multiply(df_system['clearing_price'],axis="index")
	df_cost['hvac_cost'] = df_hvac_load_cost.sum(axis=0)

	#Inverter load
	df_inv_load = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '/' + run + '_' + ind+'/total_P_Out.csv',skiprows=range(8)).iloc[(24*60):]
	df_inv_load['# timestamp'] = df_inv_load['# timestamp'].map(lambda x: str(x)[:-4])
	df_inv_load['# timestamp'] = pd.to_datetime(df_inv_load['# timestamp'])
	df_inv_load.set_index('# timestamp',inplace=True)  
	df_inv_load = (df_inv_load/1000000)/60 # to MWh

	df_inv_load_cost = df_inv_load.multiply(df_system['clearing_price'],axis="index")
	sum_inv = df_inv_load_cost.sum(axis=0)
	df_cost['PV_income'] = 0.0
	df_cost['EV_cost'] = 0.0
	df_cost['Bat_income'] = 0.0
	for inv in sum_inv.index:
		if 'PV' in inv:
			house_ind = df_cost.loc[df_cost['PV_inv'] == inv].index[0]
			df_cost.at[house_ind,'PV_income'] = sum_inv.loc[inv]
		if 'EV' in inv:
			house_ind = df_cost.loc[df_cost['EV_inv'] == inv].index[0]
			df_cost.at[house_ind,'EV_cost'] = -sum_inv.loc[inv]
		if 'Bat' in inv:
			house_ind = df_cost.loc[df_cost['Bat_inv'] == inv].index[0]
			df_cost.at[house_ind,'Bat_income'] = sum_inv.loc[inv]

	df_cost['total'] = df_cost['hvac_cost'] - df_cost['PV_income'] + df_cost['EV_cost'] - df_cost['Bat_income']
	return df_cost

##############
#SETTINGS
##############

run = 'Paper' #'FinalReport_Jul1d'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_paper.csv'
ind = '0006'
risk_prem = 1.025

df_settings = pd.read_csv(settings_file,index_col=[0])
p_max = df_settings['p_max'].loc[int(ind)]

df_house = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '/' + run + '_' + ind + '/df_house_state.csv')
df_PV_appl = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '/' + run + '_' + ind + '/df_PV_state.csv')
df_EV_appl = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '/' + run + '_' + ind + '/df_EV_state.csv')
list_EV = list(pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '/' + run + '_' + ind + '/df_EV_state.csv')['EV_name'])
list_EV_inv = []
EV_dict = dict()
for EV in list_EV:
	EV_inv = 'EV_inverter'+EV[2:]
	EV_dict[EV] = EV_inv
	list_EV_inv += [EV_inv]
df_Bat_appl = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '/' + run + '_' + ind + '/df_battery_state.csv')
list_Bat = list(df_Bat_appl['battery_name'])
list_Bat_inv = []
Bat_dict = dict()
for Bat in list_Bat:
	Bat_inv = 'Bat_inverter'+Bat[7:]
	Bat_dict[Bat] = Bat_inv
	list_Bat_inv += [Bat_inv]

##############
#APPLIANCES
##############
df_cost = pd.DataFrame(index=df_house['house_name'])

df_cost['PV_exists'] = 0
df_cost['PV_inv'] = None
for house in df_cost.index:
	if house in list(df_PV_appl['house_name']):
		df_cost.at[house,'PV_exists'] = 1
		df_cost.at[house,'PV_inv'] = df_PV_appl['inverter_name'].loc[df_PV_appl['house_name'] == house].iloc[0]

df_cost['EV_exists'] = 0
df_cost['EV_inv'] = None
for house in df_cost.index:
	if house in list(df_EV_appl['house_name']):
		df_cost.at[house,'EV_exists'] = 1
		EV_name = df_EV_appl['EV_name'].loc[df_EV_appl['house_name'] == house].iloc[0]
		df_cost.at[house,'EV_inv'] = EV_dict[EV_name]

df_cost['Bat_exists'] = 0
df_cost['Bat_inv'] = None
for house in df_cost.index:
	if house in list(df_Bat_appl['house_name']):
		df_cost.at[house,'Bat_exists'] = 1
		Bat_name = df_Bat_appl['battery_name'].loc[df_Bat_appl['house_name'] == house].iloc[0]
		df_cost.at[house,'Bat_inv'] = Bat_dict[Bat_name]

#Forward prices
df_cost_6 = df_cost.copy()
df_cost_6 = get_costs_perhouse(run,ind,df_cost_6)

#Historical prices
df_cost_7 = df_cost.copy()
df_cost_7 = get_costs_perhouse(run,'0007',df_cost_7)

#Histogram
xlabel = 'Estimated daily absolute cost [USD]'
ymax = 2.

ax = df_cost_6['total'].hist(bins=20,histtype='step',label='forward market prices',normed=True,linewidth=2,color='orange')
ax.vlines(df_cost_6['total'].median(),0.,ymax,color='orange',linestyles='dashed') #dashes=[5, 5])

ax = df_cost_7['total'].hist(bins=20,histtype='step',label='historical prices',normed=True,linewidth=2,color='green')
ax.vlines(df_cost_7['total'].median(),0.,ymax,color='green',linestyles='dashed')

fig = ax.get_figure()
ax.set(xlabel=xlabel,ylabel='Density of households')
ax.set_ylim(0.,ymax)
#ax.annotate('Median cost changes',xy=(-0.025,18.))

L = ax.legend(bbox_to_anchor=(0.5, -0.25), loc='lower center', ncol=3)

fig.savefig(run+'/_15_costs_forward_vs_historical_0006_0007.png', bbox_inches='tight',dpi=300)

