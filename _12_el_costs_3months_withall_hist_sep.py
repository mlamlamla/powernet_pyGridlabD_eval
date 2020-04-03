import pandas as pd

run = 'FinalReport2' #'FinalReport_Jul1d'
risk_prem = '2.5'
ymax = 0.07

df_cost = pd.read_csv(run+'/cost_changes_procneutral_1600_all_200225.csv')
#import pdb; pdb.set_trace()

#df_cost['abs_change_newRR_riskprem5'] = df_cost['abs_change_newRR_riskprem5']/18*365 #yearly savings
import matplotlib.pyplot as ppt
fig = ppt.figure(figsize=(8,4),dpi=150)  
ax = fig.add_subplot(111) 
xlabel = 'Estimated yearly absolute cost change [USD]'
#xlabel = 'Estimated daily absolute cost change [USD]'

df_cost['abs_change_newRR'] = df_cost['abs_change_newRR']/18*365 #yearly savings
df_cost['cost_market_newRR'] = df_cost['cost_market_newRR']/18*365 #yearly savings
df_cost['costs_nomarket'] = df_cost['costs_nomarket']/18*365 #yearly savings
df_cost['costs_nomarket_riskprem5'] = df_cost['costs_nomarket_riskprem5']/18*365 #yearly savings

ax = df_cost['abs_change_newRR'].loc[(df_cost['PV_exists'] == 0) & (df_cost['Bat_exists'] == 0) & (df_cost['EV_exists'] == 0)].hist(bins=20,histtype='step',label='without DER',normed=True,linewidth=2,color='green')
ax.vlines(df_cost['abs_change_newRR'].loc[(df_cost['PV_exists'] == 0) & (df_cost['Bat_exists'] == 0) & (df_cost['EV_exists'] == 0)].median(),0.,ymax,color='green',linestyles='dashed') #dashes=[5, 5])
print('No DER: Median change / median abs')
print(df_cost['abs_change_newRR'].loc[(df_cost['PV_exists'] == 0) & (df_cost['Bat_exists'] == 0) & (df_cost['EV_exists'] == 0)].median())
print(df_cost['cost_market_newRR'].loc[(df_cost['PV_exists'] == 0) & (df_cost['Bat_exists'] == 0) & (df_cost['EV_exists'] == 0)].median())
print(df_cost['costs_nomarket'].loc[(df_cost['PV_exists'] == 0) & (df_cost['Bat_exists'] == 0) & (df_cost['EV_exists'] == 0)].median())
print(df_cost['costs_nomarket_riskprem5'].loc[(df_cost['PV_exists'] == 0) & (df_cost['Bat_exists'] == 0) & (df_cost['EV_exists'] == 0)].median())

ax = df_cost['abs_change_newRR'].loc[(df_cost['PV_exists'] == 1) & (df_cost['Bat_exists'] == 0) & (df_cost['EV_exists'] == 0)].hist(bins=20,histtype='step',label='with PV',normed=True,linewidth=2,color='blue')
ax.vlines(df_cost['abs_change_newRR'].loc[(df_cost['PV_exists'] == 1) & (df_cost['Bat_exists'] == 0) & (df_cost['EV_exists'] == 0)].median(),0.,ymax,color='blue',linestyles='dashed') #dashes=[5, 5])
print('PV only')
print(df_cost['abs_change_newRR'].loc[(df_cost['PV_exists'] == 1) & (df_cost['Bat_exists'] == 0) & (df_cost['EV_exists'] == 0)].median())
print(df_cost['cost_market_newRR'].loc[(df_cost['PV_exists'] == 1) & (df_cost['Bat_exists'] == 0) & (df_cost['EV_exists'] == 0)].median())
print(df_cost['costs_nomarket'].loc[(df_cost['PV_exists'] == 1) & (df_cost['Bat_exists'] == 0) & (df_cost['EV_exists'] == 0)].median())
print(df_cost['costs_nomarket_riskprem5'].loc[(df_cost['PV_exists'] == 1) & (df_cost['Bat_exists'] == 0) & (df_cost['EV_exists'] == 0)].median())

ax = df_cost['abs_change_newRR'].loc[(df_cost['PV_exists'] == 1) & (df_cost['Bat_exists'] == 1) & (df_cost['EV_exists'] == 1)].hist(bins=20,histtype='step',label='with all DER',normed=True,linewidth=2,color='orange')
ax.vlines(df_cost['abs_change_newRR'].loc[(df_cost['PV_exists'] == 1) & (df_cost['Bat_exists'] == 1) & (df_cost['EV_exists'] == 1)].median(),0.,ymax,color='orange',linestyles='dashed') #dashes=[5, 5])
print('All DER')
print(df_cost['abs_change_newRR'].loc[(df_cost['PV_exists'] == 1) & (df_cost['Bat_exists'] == 1) & (df_cost['EV_exists'] == 1)].median())
print(df_cost['cost_market_newRR'].loc[(df_cost['PV_exists'] == 1) & (df_cost['Bat_exists'] == 1) & (df_cost['EV_exists'] == 1)].median())
print(df_cost['costs_nomarket'].loc[(df_cost['PV_exists'] == 1) & (df_cost['Bat_exists'] == 1) & (df_cost['EV_exists'] == 1)].median())
print(df_cost['costs_nomarket_riskprem5'].loc[(df_cost['PV_exists'] == 1) & (df_cost['Bat_exists'] == 1) & (df_cost['EV_exists'] == 1)].median())

# ax = df_cost['abs_change_1600_riskprem5'].hist(bins=20,histtype='step',label='C = 1.6 MW, '+risk_prem+'% risk premium',normed=True,linewidth=2,color='green')
# ax.vlines(df_cost['abs_change_1600_riskprem5'].median(),0.,ymax,color='green',linestyles='dashed')
#import pdb; pdb.set_trace()


#fig = ax.get_figure(figsize=(12,4),dpi=150)
ax.set(xlabel=xlabel,ylabel='Density of households')
ax.set_ylim(0.,ymax)
#ax.annotate('Median cost changes',xy=(-12.,0.09))

L = ax.legend(bbox_to_anchor=(0.5, -0.25), loc='lower center', ncol=3)

fig.savefig(run+'/hist_prices_procneutral_all_sep_year_200225.png', bbox_inches='tight',dpi=300)
