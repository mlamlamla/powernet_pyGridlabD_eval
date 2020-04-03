import os
import pandas as pd
import system_analyses as sysev
import house_analyses as hev
import battery_analyses as bev
import EV_analyses as EVev
import market_analyses as mev
import welfare_analyses as wev

#Which run
run = 'Paper'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_paper.csv'

run = 'FinalReport2'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_final2.csv'
df_settings = pd.read_csv(settings_file)

def plot_weekload(ind,start=None,end=None):
	folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind
	directory = run + '/' + run + '_' + ind + '_vis'
	s_settings = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(ind))]

	df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True)
	sysev.plot_system_prices_week(directory,df_system,s_settings,start=start,end=end)

# #without appliances
# plot_weekload('0000')
# plot_weekload('0001')
# plot_weekload('0002')

# #with appliances
# plot_weekload('0003')
# plot_weekload('0004')
# plot_weekload('0005')
# plot_weekload('0009',start=pd.Timestamp(2016, 7, 16),end = pd.Timestamp(2016, 7, 17))

plot_weekload('0088')
plot_weekload('0089')