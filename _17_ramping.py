import os
import pandas as pd
import system_analyses as sysev
import house_analyses as hev
import battery_analyses as bev
import EV_analyses as EVev
import market_analyses as mev
import welfare_analyses as wev
from numpy import arange 

import matplotlib.pyplot as ppt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange

def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)

#Which run
run = 'Paper'
settings_file = '/Users/admin/Documents/powernet/powernet_markets_mysql/settings_paper.csv'
df_settings = pd.read_csv(settings_file)
ind = '0006'
interval= 5

#Prepare data
folder = '/Users/admin/Documents/powernet/powernet_markets_mysql/'+run+'/'+run + '_' + ind
directory = run + '/' + run + '_' + ind + '_vis'
df_system = pd.read_csv(directory+'/df_system.csv',index_col=[0], parse_dates=True).iloc[(24*60):]
df_system['baseload'] = df_system['total_load_houses'] - df_system['flex_hvac'] - df_system['inflex_hvac']
df_system['baseload_t-1'] = df_system['baseload'].shift(interval)
df_system = df_system.iloc[interval:]
df_system['baseload_ramp'] = (df_system['baseload_t-1'] - df_system['baseload'])*1000 #to kW

#Figure
xlabel = 'Ramp [kW]'
#ymax = 25.
ax = df_system['baseload_ramp'].hist(bins=20,histtype='step',normed=True,linewidth=2,color='orange')
#ax.vlines(df_system['baseload_ramp'].median(),0.,ymax,color='orange',linestyles='dashed') #dashes=[5, 5])

fig = ax.get_figure()
ax.set(xlabel=xlabel,ylabel='Density of time periods')
#ax.set_ylim(0.,ymax)
#ax.annotate('Median cost changes',xy=(-0.025,18.))

L = ax.legend(bbox_to_anchor=(0.5, -0.25), loc='lower center', ncol=3)

fig.savefig(run+'/'+run + '_' + ind + '_vis/' +'_17_ramping_baseload_'+ind+'_'+str(interval)+'min.png', bbox_inches='tight',dpi=300)

