#Calculates up time of flexible and inflexible HVACs 
import pandas as pd
import matplotlib.pyplot as ppt

from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from numpy import arange 

run = 'FinalReport2' #'FinalReport_Jul1d'

start = pd.Timestamp(2015, 7, 16, 15)
end= pd.Timestamp(2015, 7, 16, 18)

#Detailed analysis
ind = '0018'
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run + '_' + ind
directory = run + '/' + run + '_' + ind + '_vis'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_final2.csv'
df_settings = pd.read_csv(settings_file)
C = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(ind))]['line_capacity'].iloc[0]/1000
no_houses = df_settings.loc[(df_settings['run'] == run) & (df_settings['id'] == int(ind))]['flexible_houses'].iloc[0]

fig = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
ax = fig.add_subplot(111)

df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True)

#Clearing quantity
lns1 = ax.step(df_system.index,df_system['clearing_quantity'],'r',where='post',label='clearing quantity') 

#Measured real power
lns2 = ax.plot(df_system.index,df_system['measured_real_power'],'g',label='measured real power') 

#Unresp load
lns3 = ax.step(df_system.index,df_system['unresponsive_loads'],'b',where='post',label='estimate unresp. load') 

#Total load
lns4 = ax.plot(df_system.index,(df_system['total_load_houses']-df_system['flex_hvac']),'y',label='actual inflexible load') 
#lns5 = ax.plot(df_total_load.index,(df_total_load)/1000.,'y',label='total load') 

ax.plot(df_system.index,[C]*len(df_system.index),'r',dashes=[5,5])

ax.set_ylabel('Measured system load [MW]')
ax.set_xlim(xmin=start, xmax=end)
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

lns = lns1 + lns2 + lns3 + lns4 #+ lns5
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=len(labs))

ppt.savefig(run+'/'+'06_load_diff_cleared_vs_measured_'+ind+'.png', bbox_inches='tight')

#Forecasting error
df_system['abs_error'] = (df_system['total_load_houses']-df_system['flex_hvac']) - df_system['unresponsive_loads']
df_system['rel_error'] = df_system['abs_error']/df_system['unresponsive_loads']*100

fig = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
ax = fig.add_subplot(111)

lns1 = ax.step(df_system.index,df_system['abs_error']*1000.,'r',where='post',label='forecasting error') 
ax.plot(df_system.index,[0.0]*len(df_system.index),'k')

ax.set_ylabel('Forecasting error [kW]')
ax.set_xlim(xmin=start, xmax=end)
#ax.set_ylim(ymin=-75., ymax=75)
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

lns = lns1
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=len(labs))

ppt.savefig(run+'/'+'06_abs_error_'+ind+'.png', bbox_inches='tight')


