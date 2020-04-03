import os
import pandas as pd
import system_analyses as sysev
import house_analyses as hev
import battery_analyses as bev
import EV_analyses as EVev
import market_analyses as mev
import welfare_analyses as wev
import warnings
warnings.filterwarnings("ignore")

#Which run
run = 'Paper' #'Paper' #'FinalReport_Jul1d'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_paper.csv'

run = 'FinalReport2' #'Paper' #'FinalReport_Jul1d'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_final2.csv'

df_settings = pd.read_csv(settings_file)

cols = ['ind','houses','PV','EV','Batt','max_real_power','mean_real_power','max_res_load','mean_res_load']
cols += ['max_flex_hvac','mean_flex_hvac','max_inflex_hvac','mean_inflex_hvac','share_hvac_energy','max_pv','mean_pv','PV_energy_share']
cols += ['max_batt_supply','mean_batt_supply','max_batt_demand','mean_batt_demand','Batt_energy_share']
cols += ['max_EV','mean_EV','max_unresp','mean_unresp','max_clear_q','mean_clear_q','mean_p','mean_T','max_T']

# Max measured real power: 2732.93
# Max total residential load: 2596.6053695
# Max flexible hvac load: 1378.19384
# Max inflexible hvac load: 1118.53021
# Max flexible pv infeed: 233.55816000000002
# Max flexible batt load: 436.8
# Max unresponsive load: 1146.4458
# Max WS price: 232.80916
# Max clearing capacity: 2180.095

df_results = pd.DataFrame(columns=cols)

for ind in df_settings['id']:
	ind = "{:04d}".format(ind)
	folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind
	directory = run + '/' + run + '_' + ind + '_vis'
	if not os.path.exists(directory):
		print(str(ind)+' does not exist')
		os.makedirs(directory)
		s_settings = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(ind))]
		try:
			df_system, df_results = sysev.get_systemdata(folder,s_settings,df_results,ind)
			df_system.to_csv(directory+'/df_system.csv')
		except:
			print('Not successful: '+str(ind))
			try:
				os.rmdir(directory)
			except:
				print('Folder non-empty or not found')
	else:
		print(str(ind)+' exists')
	df_results.to_csv(run+'/'+run+'_results.csv')

print(df_results)