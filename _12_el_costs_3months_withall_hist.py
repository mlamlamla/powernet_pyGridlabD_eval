import pandas as pd

run = 'FinalReport2' #'FinalReport_Jul1d'
risk_prem = '2.5'
ymax = 0.014

df_cost = pd.read_csv(run+'/cost_changes_procneutral_1600_all.csv')

#df_cost['abs_change_newRR_riskprem5'] = df_cost['abs_change_newRR_riskprem5']/18*365 #yearly savings
xlabel = 'Estimated yearly absolute cost change [USD]'
xlabel = 'Estimated daily absolute cost change [USD]'

df_cost['abs_change_oldRR'] = df_cost['abs_change_oldRR']/18*365 #yearly savings

ax = df_cost['abs_change_oldRR'].hist(bins=20,histtype='step',label='retail rate without TS',normed=True,linewidth=2,color='orange')
ax.vlines(df_cost['abs_change_oldRR'].median(),0.,ymax,color='orange',linestyles='dashed') #dashes=[5, 5])

df_cost['abs_change_newRR'] = df_cost['abs_change_newRR']/18*365 #yearly savings

ax = df_cost['abs_change_newRR'].hist(bins=20,histtype='step',label='retail rate with TS',normed=True,linewidth=2,color='green')
ax.vlines(df_cost['abs_change_newRR'].median(),0.,ymax,color='green',linestyles='dashed') #dashes=[5, 5])

#import pdb; pdb.set_trace()


# ax = df_cost['abs_change_1600_riskprem5'].hist(bins=20,histtype='step',label='C = 1.6 MW, '+risk_prem+'% risk premium',normed=True,linewidth=2,color='green')
# ax.vlines(df_cost['abs_change_1600_riskprem5'].median(),0.,ymax,color='green',linestyles='dashed')

fig = ax.get_figure()
ax.set(xlabel=xlabel,ylabel='Density of households')
ax.set_ylim(0.,ymax)
ax.annotate('Median cost changes',xy=(-400.,0.013))

L = ax.legend(bbox_to_anchor=(0.5, -0.25), loc='lower center', ncol=3)

fig.savefig(run+'/hist_prices_procneutral_all_year_oldnewRR.png', bbox_inches='tight',dpi=300)
