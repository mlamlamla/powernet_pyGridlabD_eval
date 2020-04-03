import pandas as pd

run = 'FinalReport2' #'FinalReport_Jul1d'
risk_prem = '2.5'
ymax = 0.1

df_cost = pd.read_csv(run+'/cost_changes_procneutral_1600_PV.csv')

df_cost['abs_change_1600'] = df_cost['abs_change_1600']/18*365 #yearly savings
df_cost['abs_change_1600_riskprem5'] = df_cost['abs_change_1600_riskprem5']/18*365 #yearly savings
xlabel = 'Estimated yearly absolute cost change [USD]'
xlabel = 'Estimated daily absolute cost change [USD]'

ax = df_cost['abs_change_1600'].loc[df_cost['PV_exists'] == 1].hist(bins=20,histtype='step',label='C = 1.6 MW, with PV',normed=True,linewidth=2,color='orange')
ax.vlines(df_cost['abs_change_1600'].loc[df_cost['PV_exists'] == 1].median(),0.,ymax,color='orange',linestyles='dashed') #dashes=[5, 5])

print('Median with PV')
print(df_cost['abs_change_1600'].loc[df_cost['PV_exists'] == 1].median())

ax = df_cost['abs_change_1600'].loc[df_cost['PV_exists'] == 0].hist(bins=20,histtype='step',label='C = 1.6 MW, without PV',normed=True,linewidth=2,color='green')
ax.vlines(df_cost['abs_change_1600'].loc[df_cost['PV_exists'] == 0].median(),0.,ymax,color='green',linestyles='dashed') #dashes=[5, 5])

print('Median without PV')
print(df_cost['abs_change_1600'].loc[df_cost['PV_exists'] == 0].median())

# ax = df_cost['abs_change_1600_riskprem5'].hist(bins=20,histtype='step',label='C = 1.6 MW, '+risk_prem+'% risk premium',normed=True,linewidth=2,color='green')
# ax.vlines(df_cost['abs_change_1600_riskprem5'].median(),0.,ymax,color='green',linestyles='dashed')

fig = ax.get_figure()
ax.set(xlabel=xlabel,ylabel='Density of households')
ax.set_ylim(0.,ymax)
ax.annotate('Median cost changes',xy=(-12.,0.09))

L = ax.legend(bbox_to_anchor=(0.5, -0.25), loc='lower center', ncol=3)

fig.savefig(run+'/hist_prices_procneutral_PV_sep_year.png', bbox_inches='tight',dpi=300)
