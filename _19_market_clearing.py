###Market Clearing###
import market_functions as Mfcts
import pandas as pd

run = 'FinalReport2'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_final2.csv'
df_settings = pd.read_csv(settings_file)
ind = '0054'

folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind
directory = run + '/' + run + '_' + ind + '_vis'
df_buy_bids = pd.read_csv(folder+'/df_buy_bids.csv',index_col=[0], parse_dates=['timestamp'])
df_supply_bids = pd.read_csv(folder+'/df_supply_bids.csv',index_col=[0], parse_dates=['timestamp'])

time_stamp = pd.Timestamp(2015,7,16,16,30)

retail = Mfcts.Market()
retail.Pmax = 100
retail.Qlabel = 'Quantity in [MW]'
retail.Plabel = 'Price in [USD/MW]'

df_buy_bids_t = df_buy_bids.loc[df_buy_bids['timestamp'] == time_stamp]
df_supply_bids_t = df_supply_bids.loc[df_supply_bids['timestamp'] == time_stamp]

for ind in df_buy_bids_t.index:
	if df_buy_bids_t['appliance_name'].loc[ind] == 'unresponsive_loads':
		retail.buy(df_buy_bids_t['bid_quantity'].loc[ind]/1000.,appliance_name=df_buy_bids_t['appliance_name'].loc[ind])
	else:
		retail.buy(df_buy_bids_t['bid_quantity'].loc[ind]/1000.,df_buy_bids_t['bid_price'].loc[ind],appliance_name=df_buy_bids_t['appliance_name'].loc[ind])
for ind in df_supply_bids_t.index:
	retail.sell(df_supply_bids_t['bid_quantity'].loc[ind]/1000.,df_supply_bids_t['bid_price'].loc[ind])

retail.clear()
print(retail.Pd)
#import pdb; pdb.set_trace()
retail.plot(directory,dt=str(time_stamp))
