import pandas as pd

run = 'FinalReport2' #'FinalReport_Jul1d'
risk_prem = '2.5'

df_cost = pd.read_csv(run+'/cost_changes_procneutral_1600.csv')

ax = df_cost['change_5000'].hist(bins=20,histtype='step',label='No capacity constraint',normed=True,linewidth=2,color='orange')
ax.vlines(df_cost['change_5000'].median(),0.,0.1,color='orange',linestyles='dashed') #dashes=[5, 5])

ax = df_cost['change_5000_riskprem5'].hist(bins=20,histtype='step',label='No capacity constraint, '+risk_prem+'% risk premium',normed=True,linewidth=2,color='green')
ax.vlines(df_cost['change_5000_riskprem5'].median(),0.,0.1,color='green',linestyles='dashed')

#ax = df_cost['change_1600'].hist(bins=20,histtype='step',label='x',normed=True)
ax = df_cost['change_1600_riskprem5'].hist(bins=20,histtype='step',label='C = 1.6 MW, '+risk_prem+'% risk premium',normed=True,linewidth=2,color='blue')
ax.vlines(df_cost['change_1600_riskprem5'].median(),0.,0.1,color='blue',linestyles='dashed')

fig = ax.get_figure()
ax.set(xlabel='Cost change in [%]',ylabel='Density of households')
ax.set_ylim(0.,0.035)
ax.annotate('Median cost changes',xy=(2.,0.032))

L = ax.legend(bbox_to_anchor=(0.5, -0.25), loc='lower center', ncol=3)

fig.savefig(run+'/hist_prices_procneutral_all.png', bbox_inches='tight',dpi=300)
