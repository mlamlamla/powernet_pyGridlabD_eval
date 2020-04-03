#Calculates up time of flexible and inflexible HVACs 
import pandas as pd
import matplotlib.pyplot as ppt

from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from numpy import arange 

run = 'FinalReport2' #'FinalReport_Jul1d'

start = pd.Timestamp(2015, 7, 16, 0)
end= pd.Timestamp(2015, 7, 16, 23, 59)
C = 1.6

#Detailed analysis
df_baseload = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/glm_generation_SanDiego/perfect_baseload_forecast.csv')
#import pdb; pdb.set_trace()
df_baseload['# timestamp'] = df_baseload['# timestamp'].str.replace(r' UTC$', '')
df_baseload['# timestamp'] = pd.to_datetime(df_baseload['# timestamp'])
df_baseload.set_index('# timestamp',inplace=True)

import pdb; pdb.set_trace()

fig = ppt.figure(figsize=(9,3),dpi=150)   
ppt.ioff()
ax = fig.add_subplot(111)

#Clearing quantity
lns1 = ax.plot(df_baseload.index,df_baseload['baseload']/1000,'b',label='baseload') 
ax.vlines(pd.Timestamp(2015, 7, 16, 15, 45),0.0,C*1.1,linestyles='dashed')

#ax.plot(df_baseload.index,[0.0]*len(df_baseload.index),'k')
lns2 = ax.plot(df_baseload.index,[C]*len(df_baseload.index),'r',dashes=[5,5], label='capacity constraint')

ax.set_ylabel('Measured system load [MW]')
ax.set_xlim(xmin=start, xmax=end)
ax.set_ylim(ymin=0.0,ymax=C*1.1)
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

lns = lns1 + lns2
labs = [l.get_label() for l in lns]
L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=len(labs))

ppt.savefig(run+'/'+'08_baseload.png', bbox_inches='tight')


