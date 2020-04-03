import pandas as pd
import numpy as np

##############
#SETTINGS
##############

run = 'Paper' #'FinalReport_Jul1d'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_paper.csv'
ind = '0006'

folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run+'_'+ind
df_settings = pd.read_csv(settings_file,index_col=[0])

# #HVAC: Dispatch
# df_hvac_load = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8)).iloc[(24*60):]
# df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
# df_hvac_load = df_hvac_load.iloc[:-1]
# df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
# df_hvac_load.set_index('# timestamp',inplace=True)   
# no_houses = df_settings['flexible_houses'].loc[int(ind)]
# df_hvac_load = pd.DataFrame(index=df_hvac_load.index,columns=df_hvac_load.columns[:no_houses],data=df_hvac_load.values)

# #HVAC: Bids
# df_buy_bids = pd.read_csv(folder+'/df_buy_bids.csv',index_col=[0],parse_dates=True)
# df_buy_bids.drop('bid_price',inplace=True,axis=1)
# df_buy_bids.set_index(['timestamp', 'appliance_name'])
# df_buy_bids_pivot = pd.pivot_table(df_buy_bids, values='bid_quantity', index=['timestamp'],columns=['appliance_name'], aggfunc=np.sum)
# for col in df_buy_bids_pivot.columns:
# 	if not 'HVAC' in col:
# 		df_buy_bids_pivot.drop(col,inplace=True,axis=1)
# df_buy_bids_pivot = df_buy_bids_pivot.iloc[(24*12):]
# #import pdb; pdb.set_trace()

# #Extend to 1min data and fill NaN
# df_buy_bids_full = pd.DataFrame(index=df_hvac_load.index)
# df_buy_bids_full = df_buy_bids_full.join(df_buy_bids_pivot,how='outer')
# for col in df_buy_bids_full.columns:
# 	for t in df_buy_bids_full.index:
# 		if (t.minute%5 == 0) and (df_buy_bids_full[col].isnull().loc[t]):
# 			df_buy_bids_full.at[t,col] = 0.
# df_buy_bids_full.fillna(method='ffill',inplace=True)

# #Sort columns (houses are sorted,HVAC needs tobe sorted)
# for col in df_buy_bids_full.columns:
# 	df_buy_bids_full.rename(columns={col:col.split('_')[-1]},inplace=True)
# df_buy_bids_full = df_buy_bids_full.sort_index(axis=1)
# df_buy_bids_full = df_buy_bids_full.iloc[:-1]

# #import pdb; pdb.set_trace()

# assert len(df_hvac_load.columns) == len(df_buy_bids_full.columns)
# df_buy_bids_full = pd.DataFrame(index=df_buy_bids_full.index,columns=df_hvac_load.columns,data=df_buy_bids_full.values) #Change column names


# df_diff_long = pd.DataFrame(columns=['min','diff'])
# for col in df_hvac_load.columns:
# 	for i in df_hvac_load.index:
# 		if df_hvac_load[col].loc[i] > 0:
# 			i_min = i.minute%5
# 			delta = df_hvac_load[col].loc[i] - df_buy_bids_full[col].loc[i]
# 			df_diff_i = pd.DataFrame(index=[0],columns=['min','diff'],data=[[i_min,delta]])
# 			df_diff_long = df_diff_long.append(df_diff_i,ignore_index=True)

# #Save
# df_diff_long.to_csv(run+'/'+run + '_' + ind + '_vis/df_diff_long.csv')


#Read
df_diff_long = pd.read_csv(run+'/'+run + '_' + ind + '_vis/df_diff_long.csv',index_col=[0])
import pdb; pdb.set_trace()


xlabel = 'Difference dispatch vs. bid [kW]'
ymax = 25.
ax = df_diff_long['diff'].hist(bins=20,histtype='step',normed=True,linewidth=2,color='orange')
ax.vlines(df_diff_long['diff'].median(),0.,ymax,color='orange',linestyles='dashed') #dashes=[5, 5])
print('Median: '+str(df_diff_long.median()))

fig = ax.get_figure()
ax.set(xlabel=xlabel,ylabel='Density of time periods')
ax.set_ylim(0.,ymax)
#ax.annotate('Median cost changes',xy=(-0.025,18.))

L = ax.legend(bbox_to_anchor=(0.5, -0.25), loc='lower center', ncol=3)

fig.savefig(run+'/'+run + '_' + ind + '_vis/' +'_16_bids_vs_dispatch_'+ind+'.png', bbox_inches='tight',dpi=300)


#import pdb; pdb.set_trace()
#Histogram for different minutes

#ymax = 2.
# for m in range(5):
# 	ax2 = df_diff_long['diff'].loc[df_diff_long['min'] == m].hist(bins=20,histtype='step',normed=True,linewidth=2,label=str(m)) #,color='orange')
# 	print('Variance of minute '+str(m))
# 	print(df_diff_long['diff'].loc[df_diff_long['min'] == m].var())
# 	#ax.vlines(df_diff_long.median(),0.,ymax,color='orange',linestyles='dashed') #dashes=[5, 5])
# fig2 = ax2.get_figure()
# ax2.set(xlabel=xlabel,ylabel='Density of time periods')
# #ax2.set_ylim(0.,ymax)
# #ax.annotate('Median cost changes',xy=(-0.025,18.))

# L2 = ax2.legend(bbox_to_anchor=(0.5, -0.25), loc='lower center', ncol=5)

# fig2.savefig(run+'/'+run + '_' + ind + '_vis/' +'_16_bids_vs_dispatch_'+ind+'_minutes.png', bbox_inches='tight',dpi=300)

