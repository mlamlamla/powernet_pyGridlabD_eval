#Compare 
#duty cycles of HVACs
#average price at up-time
#temperature variation

import pandas as pd

# 0064 - no market (Jan)
# 0106 - market, no constraint (Jan)

run = 'FinalReport2'

#No market
ind = '0001'
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind
df_system = pd.read_csv(run + '/' + run + '_' + ind + '_vis/df_system.csv',index_col=[0],parse_dates=True)

df_hvac_load_nom = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8))
df_hvac_load_nom['# timestamp'] = df_hvac_load_nom['# timestamp'].map(lambda x: str(x)[:-4])
df_hvac_load_nom = df_hvac_load_nom.iloc[:-1]
df_hvac_load_nom['# timestamp'] = pd.to_datetime(df_hvac_load_nom['# timestamp'])
df_hvac_load_nom.set_index('# timestamp',inplace=True)        

df_hvac_on_nom = df_hvac_load_nom.copy()
df_hvac_on_nom[df_hvac_on_nom > 0.0] = 1                

# df_cycles = pd.DataFrame(index=df_hvac_on_nom.columns,columns=['#cycles nom','#cycles wm'],data=0)
# for col in df_hvac_on_nom.columns:
# 	prev = 0
# 	no_cycles = 0
# 	for ind in df_hvac_on_nom.index:
# 		if (prev == 0) and (df_hvac_on_nom[col].loc[ind] == 1):
# 			no_cycles += 1
# 			prev = 1
# 		elif (prev > 0) and (df_hvac_on_nom[col].loc[ind] == 1):
# 			prev += 1
# 			df_hvac_on_nom[col].loc[ind] = prev
# 		else:
# 			prev = 0
# 	df_cycles['#cycles nom'].loc[col] = no_cycles

#With market
ind = '0013'
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind

df_hvac_load_wm1 = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8))
df_hvac_load_wm1['# timestamp'] = df_hvac_load_wm1['# timestamp'].map(lambda x: str(x)[:-4])
df_hvac_load_wm1 = df_hvac_load_wm1.iloc[:-1]
df_hvac_load_wm1['# timestamp'] = pd.to_datetime(df_hvac_load_wm1['# timestamp'])
df_hvac_load_wm1.set_index('# timestamp',inplace=True)                           

#df_hvac_on_wm1 = df_hvac_load_wm.copy()
#df_hvac_on_wm1[df_hvac_on_wm1 > 0.0] = 1

#With market
ind = '0113'
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind

df_hvac_load_wm2 = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8))
df_hvac_load_wm2['# timestamp'] = df_hvac_load_wm2['# timestamp'].map(lambda x: str(x)[:-4])
df_hvac_load_wm2 = df_hvac_load_wm2.iloc[:-1]
df_hvac_load_wm2['# timestamp'] = pd.to_datetime(df_hvac_load_wm2['# timestamp'])
df_hvac_load_wm2.set_index('# timestamp',inplace=True)                           

#With market
ind = '0112'
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind

df_hvac_load_wm3 = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8))
df_hvac_load_wm3['# timestamp'] = df_hvac_load_wm3['# timestamp'].map(lambda x: str(x)[:-4])
df_hvac_load_wm3 = df_hvac_load_wm3.iloc[:-1]
df_hvac_load_wm3['# timestamp'] = pd.to_datetime(df_hvac_load_wm3['# timestamp'])
df_hvac_load_wm3.set_index('# timestamp',inplace=True)

# for col in df_hvac_on_wm.columns:
# 	prev = 0
# 	no_cycles = 0
# 	for ind in df_hvac_on_wm.index:
# 		if (prev == 0) and (df_hvac_on_wm[col].loc[ind] == 1):
# 			no_cycles += 1
# 			prev = 1
# 		elif (prev > 0) and (df_hvac_on_wm[col].loc[ind] == 1):
# 			prev += 1
# 			df_hvac_on_wm[col].loc[ind] = prev
# 		else:
# 			prev = 0
# 	df_cycles['#cycles wm'].loc[col] = no_cycles

import matplotlib.pyplot as ppt

# fig = ppt.figure(figsize=(9,3),dpi=150)   
# ppt.ioff()
# ax = fig.add_subplot(111)

# #Clearing quantity
# lns1 = ax.plot(df_hvac_on_nom.sum(axis=1),'b',label='no market') 
# lns2 = ax.plot(df_hvac_on_wm.sum(axis=1),'r',label='market')

# ax.set_ylabel('Number of HVAC systems on')

# lns = lns1 + lns2
# labs = [l.get_label() for l in lns]
# L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=len(labs))

# ppt.savefig(run+'/'+'22_HVACs_on.png', bbox_inches='tight')

fig = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
ax = fig.add_subplot(111)

#Clearing quantity
lns1 = ax.plot(df_hvac_load_nom.sum(axis=1),'k',label='no market') 
lns2 = ax.plot(df_hvac_load_wm1.sum(axis=1),'r',label='historical ref price (12)')
lns3 = ax.plot(df_hvac_load_wm2.sum(axis=1),'g',label='forward ref price (24)')
lns4 = ax.plot(df_hvac_load_wm3.sum(axis=1),'b',label='forward ref price (36)')

ax.set_xlim(pd.Timestamp(2015,7,16),pd.Timestamp(2015,7,17))
#ax.set_ylim(0,1600)
ax.set_ylabel('HVAC power')

#import pdb; pdb.set_trace()
ax2 = ax.twinx()
lnsCP = ax2.plot(df_system.index,df_system['clearing_price'])
lnsWS = ax2.plot(df_system.index,df_system['WS'])
#import pdb; pdb.set_trace()

lns = lns1 + lns2  + lnsCP + lnsWS + lns3 + lns4
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.4), loc='lower center', ncol=4)

ppt.savefig(run+'/'+'22_HVACs_load.png', bbox_inches='tight')

#import pdb; pdb.set_trace()


# fig = ppt.figure(figsize=(9,3),dpi=150)   
# ppt.ioff()
# ax = fig.add_subplot(111)

# #Clearing quantity
# lns1 = ax.plot(df_agg_load['measured_real_power'],'b',label='no market') 

# ax.set_ylabel('Agg load at slack bus')

# lns = lns1 + lns2
# labs = [l.get_label() for l in lns]
# L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=len(labs))

# ppt.savefig(run+'/'+'22_agg_load.png', bbox_inches='tight')
