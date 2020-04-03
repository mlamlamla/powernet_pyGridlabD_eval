# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 04:09:07 2019

@author: MLA
"""
import pandas as pd
import numpy as np
from numpy import arange 
import matplotlib
import matplotlib.pyplot as ppt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import pylab
import datetime as dt
import matplotlib.dates as mdates
from datetime import timedelta
from math import sqrt

def latexify(fig_width=None, fig_height=None, columns=1):
    """Set up matplotlib's RC params for LaTeX plotting.
    Call this before plotting a figure.

    Parameters
    ----------
    fig_width : float, optional, inches
    fig_height : float,  optional, inches
    columns : {1, 2}
    """

    # code adapted from http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples

    # Width and max height in inches for IEEE journals taken from
    # computer.org/cms/Computer.org/Journal%20templates/transactions_art_guide.pdf

    assert(columns in [1,2])

    if fig_width is None:
        fig_width = 3.39 if columns==1 else 6.9 # width in inches

    if fig_height is None:
        golden_mean = (sqrt(5)-1.0)/2.0    # Aesthetic ratio
        fig_height = fig_width*golden_mean # height in inches

    MAX_HEIGHT_INCHES = 8.0
    if fig_height > MAX_HEIGHT_INCHES:
        print("WARNING: fig_height too large:" + fig_height + 
              "so will reduce to" + MAX_HEIGHT_INCHES + "inches.")
        fig_height = MAX_HEIGHT_INCHES

    params = {'backend': 'ps',
              'text.latex.preamble': ['\\usepackage{gensymb}'],
              'axes.labelsize': 8, # fontsize for x and y labels (was 10)
              'axes.titlesize': 8,
              #'text.fontsize': 8, # was 10
              'font.size': 8, # was 10
              'legend.fontsize': 8, # was 10
              'xtick.labelsize': 8,
              'ytick.labelsize': 8,
              #'text.usetex': True,
              'figure.figsize': [fig_width,fig_height],
              'font.family': 'serif',
              'image.cmap' : 'gray'
    }

    matplotlib.rcParams.update(params)


def format_axes(ax):

    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)

    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color(SPINE_COLOR)
        ax.spines[spine].set_linewidth(0.5)

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_tick_params(direction='out', color=SPINE_COLOR)

    return ax

def plot_systemload(results,df_systemdata,s_settings):
    #Get settings
    no_houses = s_settings['flexible_houses'].iloc[0]
    C = float(s_settings['line_capacity'].iloc[0])
    p_max = float(s_settings['p_max'].iloc[0])
    interval = int(s_settings['interval'].iloc[0])
    PV_share = s_settings['PV_share'].iloc[0]
    EV_share = s_settings['EV_share'].iloc[0]
    Batt_share = s_settings['Batt_share'].iloc[0]
    city = s_settings['city'].iloc[0]
    market_file = s_settings['market_data'].iloc[0]
    which_price = s_settings['which_price'].iloc[0]

    fig = ppt.figure(figsize=(12,4),dpi=150)   
    ppt.ioff()
    #House load
    ax = fig.add_subplot(111)
    lns1 = ax.plot(df_systemdata.index,df_systemdata['measured_real_power'],label='Measured system load')
    if 'all_flexload' in df_systemdata.columns:
        lns1b = ax.plot(df_systemdata.index,df_systemdata['measured_real_power']-df_systemdata['all_flexload'],label='Measured inflexible system load')
    lns2 = ax.plot(df_systemdata.index,df_systemdata['unresp_load'],label='Unresponsive system load (market)')
    lns3 = ax.plot(df_systemdata.index,df_systemdata['clearing_quantity'],label='Total clearing quantity (market)')
    ax.set_ylabel('MW')
    ax.set_xlim(xmin=df_systemdata.index[0], xmax=df_systemdata.index[-1])
    
    ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
    ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
    #ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    
    max_load = df_systemdata['cap_rest'].max()
    ppt.hlines(max_load, df_systemdata.index[0], df_systemdata.index[-1], colors='r', linestyles='dashed')
    
    #Legend
    if 'all_flexload' in df_systemdata.columns:
        lns = lns1 + lns1b + lns2 + lns3
    else:
        lns = lns1 + lns2 + lns3
    labs = [l.get_label() for l in lns]
    L = ax.legend(lns, labs, bbox_to_anchor=(0.3, -0.4), loc='lower left', ncol=1)
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    ppt.savefig(results+'/system_total_load.png', bbox_inches='tight')
    return

def plot_systemload_womarkets(results,df_systemdata,df_systemdata_nomarket,s_settings):
    #Get settings
    no_houses = s_settings['flexible_houses'].iloc[0]
    C = float(s_settings['line_capacity'].iloc[0])
    p_max = float(s_settings['p_max'].iloc[0])
    interval = int(s_settings['interval'].iloc[0])
    PV_share = s_settings['PV_share'].iloc[0]
    EV_share = s_settings['EV_share'].iloc[0]
    Batt_share = s_settings['Batt_share'].iloc[0]
    city = s_settings['city'].iloc[0]
    market_file = s_settings['market_data'].iloc[0]
    which_price = s_settings['which_price'].iloc[0]

    fig = ppt.figure(figsize=(12,4),dpi=150)   
    ppt.ioff()
    #House load
    ax = fig.add_subplot(111)
    lns1 = ax.plot(df_systemdata['measured_real_power'],label='Measured system load with market')
    lns2 = ax.plot(df_systemdata_nomarket['measured_real_power'],label='Measured system load without market')
    #lns3 = ax.plot(df_systemdata['clearing_quantity'],label='Total clearing quantity (market)')
    ax.set_ylabel('MW')
    ax.set_xlim(xmin=df_systemdata.index[0], xmax=df_systemdata.index[-1])
    
    ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
    #ax.xaxis.set_minor_locator(HourLocator(drange(0, 25, 6)))
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
    
    max_load = df_systemdata['cap_rest'].max()
    ppt.hlines(max_load, df_systemdata.index[0], df_systemdata.index[-1], colors='r', linestyles='dashed')
    
    #Legend
    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]
    L = ax.legend(lns, labs, bbox_to_anchor=(0.3, -0.4), loc='lower left', ncol=1)
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    ppt.savefig(results+'/system_total_load_womarkets.png', bbox_inches='tight')
    return

def plot_systemload_short(results,df_systemdata,s_settings):
    #Get settings
    no_houses = s_settings['flexible_houses'].iloc[0]
    C = float(s_settings['line_capacity'].iloc[0])
    p_max = float(s_settings['p_max'].iloc[0])
    interval = int(s_settings['interval'].iloc[0])    
    PV_share = s_settings['PV_share'].iloc[0]
    EV_share = s_settings['EV_share'].iloc[0]
    Batt_share = s_settings['Batt_share'].iloc[0]
    city = s_settings['city'].iloc[0]
    market_file = s_settings['market_data'].iloc[0]
    which_price = s_settings['which_price'].iloc[0]

    fig = ppt.figure(figsize=(12,4),dpi=150)   
    ppt.ioff()
    #House load
    ax = fig.add_subplot(111)
    lns1 = ax.plot(df_systemdata.index,df_systemdata['measured_real_power'],label='Measured system load')
    #include losses
    lns2 = ax.plot(df_systemdata.index,df_systemdata['unresp_load'],label='Unresponsive system load (market)')
    
    ax.set_xlim(xmin=df_systemdata.index[0], xmax=df_systemdata.index[-1])
    ax.set_ylim(ymin=0.0, ymax=max(df_systemdata['measured_real_power'].max(),C/1000.)*1.05)

    ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
    ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
    #ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))

    ax.set_ylabel('MW')
    
    max_load = df_systemdata['cap_rest'].max()
    #ppt.hlines(max_load, df_systemdata.index[0], df_systemdata.index[-1], colors='r', linestyles='dashed')
    
    #Legend
    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]
    L = ax.legend(lns, labs, bbox_to_anchor=(0.3, -0.4), loc='lower left', ncol=1)
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    ppt.savefig(results+'/system_total_load_short.png', bbox_inches='tight')
    return

def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)

def plot_system_prices_week(directory,df_systemdata,s_settings,start=None,end=None):
    #Get settings
    no_houses = s_settings['flexible_houses'].iloc[0]
    C = float(s_settings['line_capacity'].iloc[0])
    p_max = float(s_settings['p_max'].iloc[0])
    import pdb; pdb.set_trace()
    interval = int(s_settings['interval'].iloc[0])
    PV_share = s_settings['PV_share'].iloc[0]
    EV_share = s_settings['EV_share'].iloc[0]
    Batt_share = s_settings['Batt_share'].iloc[0]
    city = s_settings['city'].iloc[0]
    market_file = s_settings['market_data'].iloc[0]
    which_price = s_settings['which_price'].iloc[0]

    if not start:
        start = df_systemdata.index[0]
    if not end:
        end = df_systemdata.index[-1]
    if start > df_systemdata.index[-1] or start < df_systemdata.index[0]:
        print('Given start and end date do not overlap with indices')
        start = df_systemdata.index[0]
    if end < df_systemdata.index[0] or end > df_systemdata.index[-1]:
        end = df_systemdata.index[-1]

    latexify()
    ppt.gray()
    fig = ppt.figure(figsize=(9,3),dpi=150)   

    #House load
    ax = fig.add_subplot(111)
    #lns1 = ax.plot(df_systemdata.index,df_systemdata['measured_real_power'],'#1f77b4',label='Measured system load')
    lns1 = ax.plot(df_systemdata.index,df_systemdata['measured_real_power'],label='Measured system load')
    
    ax.plot(df_systemdata.index,[0.0]*len(df_systemdata.index),'k',lw=1)
    
    ax.set_xlim(xmin=start, xmax=end)
    #ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 24)))
    #ax.xaxis.set_major_formatter(DateFormatter('%m-%d'))
    ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    #ax.xaxis.set_major_formatter(DateFormatter('%d:%m %H:%M'))

    ax.set_ylim(ymin=min(df_systemdata['measured_real_power'].min()*1.05,0.0))
    ax.set_ylabel('Measured system load [MW]')
    
    ax2 = ax.twinx()
    ax2.set_ylabel('Price [USD/MW]')
    #lns2 = ax2.plot(df_systemdata['clearing_price'],'#2ca02c',label='LEM price')    
    lns3 = ax2.plot(df_systemdata.index,df_systemdata['WS'],linestyle='dashed',label='WS prices') 
    #lns3 = ax2.plot(df_systemdata.index,df_systemdata['WS'],'#2ca02c', linestyle='dashed',label='WS prices') 
    #ax2.plot(df_systemdata.index,[0.0]*len(df_systemdata.index),'k',label='WS prices') 
    ax2.set_ylim(ymin=min(df_systemdata['WS'].min()*1.05,0.0),ymax=df_systemdata['WS'].max()*1.05)
    #ax2.axhline(y=0,xmin=start, xmax=end)

    #ppt.hlines(max_load, df_systemdata.index[0], df_systemdata.index[-1], colors='r', linestyles='dashed') 
    ax2.set_xlim(xmin=start, xmax=end)
    #ax2.set_ylim(ymin=0.0)
    ax2.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
    ax2.xaxis.set_major_formatter(DateFormatter('%H:%M'))

    align_yaxis(ax, 0, ax2, 0)
    
    #Legend
    lns = lns1 + lns3 #lns2 + lns3 #+ lns2a+ lns2b 
    labs = [l.get_label() for l in lns]
    L = ax.legend(lns, labs, bbox_to_anchor=(0.5, -0.3), loc='lower center', ncol=3)
    #ppt.title('Measured real power vs. wholesale market prices')
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    ppt.gray()
    ppt.savefig(directory+'/01_system_total_load_vs_prices_week.pdf', bbox_inches='tight')
    print(directory+'/01_system_total_load_vs_prices.png')
    return

def plot_system_prices(directory,df_systemdata,s_settings,start=None,end=None):
    #Get settings
    no_houses = s_settings['flexible_houses'].iloc[0]
    C = float(s_settings['line_capacity'].iloc[0])
    p_max = float(s_settings['p_max'].iloc[0])
    interval = int(s_settings['interval'].iloc[0])
    PV_share = s_settings['PV_share'].iloc[0]
    EV_share = s_settings['EV_share'].iloc[0]
    Batt_share = s_settings['Batt_share'].iloc[0]
    city = s_settings['city'].iloc[0]
    market_file = s_settings['market_data'].iloc[0]
    which_price = s_settings['which_price'].iloc[0]

    if not start:
        start = df_systemdata.index[0]
    if not end:
        end = df_systemdata.index[-1]
    if start > df_systemdata.index[-1] or end < df_systemdata.index[0] or start < df_systemdata.index[0] or end > df_systemdata.index[-1]:
        print('Given start and end date do not overlap with indices')
        start = df_systemdata.index[0]
        end = df_systemdata.index[-1]

    fig = ppt.figure(figsize=(12,4),dpi=150)   
    #ppt.ioff()
    #House load
    ax = fig.add_subplot(111)
    lns1 = ax.plot(df_systemdata.index,df_systemdata['measured_real_power'],'b',label='Measured system load')
    ax.set_ylabel('MW')
    ax.set_xlim(xmin=df_systemdata.index[0], xmax=df_systemdata.index[-1])
    
    ax.set_xlim(xmin=start, xmax=end)
    ax.set_ylim(ymin=0.0)
    ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
    ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
    #ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    
    max_load = C/1000.#df_systemdata['cap_rest'].max()
    ppt.hlines(max_load, start, end, colors='r', linestyles='dashed')
    
    ax2 = ax.twinx()
    ax2.set_ylabel('Price [USD/MWh]')
    #lns2 = ax2.plot(df_systemdata['clearing_price'],'r',label='Local market price')    
    lns3 = ax2.plot(df_systemdata.index,df_systemdata['WS'],'g',label='WS prices') 
    ax2.plot(df_systemdata.index,[0.0]*len(df_systemdata.index),'k',label='WS prices') 
    ax2.axhline(y=0,xmin=start, xmax=end)

    #ppt.hlines(max_load, df_systemdata.index[0], df_systemdata.index[-1], colors='r', linestyles='dashed') 
    ax2.set_xlim(xmin=start, xmax=end)
    #ax2.set_ylim(ymin=0.0)
    
    #Legend
    lns = lns1 + lns3 #+ lns2 
    labs = [l.get_label() for l in lns]
    L = ax.legend(lns, labs, bbox_to_anchor=(0.3, -0.4), loc='lower left', ncol=1)
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    ppt.savefig(directory+'/system_total_load_vs_prices.png', bbox_inches='tight')
    print(directory+'/system_total_load_vs_prices.png')
    return

def plot_load_curve(directory,df_system,s_settings,values=100, set_max_load=True, perc_max=1.05,perc_min=0.95):
    #Get settings
    no_houses = s_settings['flexible_houses'].iloc[0]
    C = float(s_settings['line_capacity'].iloc[0])
    p_max = float(s_settings['p_max'].iloc[0])
    interval = int(s_settings['interval'].iloc[0])
    PV_share = s_settings['PV_share'].iloc[0]
    EV_share = s_settings['EV_share'].iloc[0]
    Batt_share = s_settings['Batt_share'].iloc[0]
    city = s_settings['city'].iloc[0]
    market_file = s_settings['market_data'].iloc[0]
    which_price = s_settings['which_price'].iloc[0]
    
    df_load_curve = pd.DataFrame(index=df_system.index,columns=['measured_real_power'],data=df_system['measured_real_power'])
    max_load = df_system['cap_rest'].iloc[0]
    df_load_curve.sort_values('measured_real_power',axis=0,ascending=False,inplace=True)
    df_load_curve = df_load_curve.iloc[:values]
    df_load_curve['indices'] = range(len(df_load_curve)) 
    df_load_curve.set_index('indices',inplace=True)
    
    fig = ppt.figure(figsize=(8,4),dpi=150)   
    ppt.ioff()
    #House load
    ax = fig.add_subplot(111)
    ppt.bar(df_load_curve.index,df_load_curve['measured_real_power'])
    
    ax.set_xlabel('Ranking of max measured real power')
    ax.set_ylabel('MW')
    ax.set_ylim(ymin = df_load_curve['measured_real_power'].min()*perc_min,ymax = df_load_curve['measured_real_power'].max()*perc_max)
    ax.set_xlim(xmin=-1, xmax=values+1)
    
    #ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
    #ax.xaxis.set_minor_locator(HourLocator(drange(0, 25, 6)))
    #ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
    
    if set_max_load == True:
        ppt.hlines(max_load, -1, values+1, colors='r', linestyles='dashed')
        
    #Legend
    #labs = [l.get_label() for l in lns]
    #L = ax.legend(lns, labs, bbox_to_anchor=(0.3, -0.4), loc='lower left', ncol=1)
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    print('Maximum value: '+str(df_load_curve['measured_real_power'].max()))
    print('Minimum value: '+str(df_load_curve['measured_real_power'].min()))
    ppt.savefig(directory+'/system_load_curve.png', bbox_inches='tight')
    return

def plot_load_disagg(directory,df_systemdata,s_settings,start=None,end=None):
    #Get settings
    no_houses = s_settings['flexible_houses'].iloc[0]
    C = float(s_settings['line_capacity'].iloc[0])
    p_max = float(s_settings['p_max'].iloc[0])
    interval = int(s_settings['interval'].iloc[0])
    PV_share = s_settings['PV_share'].iloc[0]
    EV_share = s_settings['EV_share'].iloc[0]
    Batt_share = s_settings['Batt_share'].iloc[0]
    city = s_settings['city'].iloc[0]
    market_file = s_settings['market_data'].iloc[0]
    which_price = s_settings['which_price'].iloc[0]

    fig = ppt.figure(figsize=(12,4),dpi=150)   
    ppt.ioff()
    #House load
    ax = fig.add_subplot(111)
    lns1 = ax.plot(df_systemdata['measured_real_power'],'r-',label='Measured system load', linewidth=0.5)
    
    df_systemdata['cumulated'] = df_systemdata['all_inflexload']
    lns2 = ax.plot(df_systemdata['all_inflexload'],'b-',label='Inflexible load', linewidth=0.5)
    ax.fill_between(np.array(df_systemdata['cumulated'].index), np.array(df_systemdata['cumulated']), facecolor='b', alpha = 0.5)
    
    if no_houses > 0:
        df_systemdata['cumulated'] += df_systemdata['flex_hvac']
        lns3 = ax.plot(df_systemdata['cumulated'],'g-',label='Flexible HVAC load', linewidth=0.5)
        ax.fill_between(np.array(df_systemdata['cumulated'].index), np.array(df_systemdata['cumulated']), np.array(df_systemdata['all_inflexload']), facecolor='g', alpha = 0.5)
    
    if Batt_share > 0.0:
        df_systemdata['cumulated'] -= df_systemdata['flex_batt'] #Load is negative, supply positive
        lns4 = ax.plot(df_systemdata['cumulated'],'m-',label='Flexible battery load', linewidth=0.5)
        ax.fill_between(np.array(df_systemdata['cumulated'].index), np.array(df_systemdata['cumulated']), np.array(df_systemdata['cumulated'] + df_systemdata['flex_batt']), facecolor='m', alpha = 0.5)
    
    if PV_share > 0.0:
        df_systemdata['cumulated'] -= df_systemdata['flex_pv'] #Load is negative, supply positive
        lns5 = ax.plot(df_systemdata['cumulated'],'y-',label='PV generation', linewidth=0.5)
        ax.fill_between(np.array(df_systemdata['cumulated'].index), np.array(df_systemdata['cumulated']), np.array(df_systemdata['cumulated'] + df_systemdata['flex_pv']), facecolor='y', alpha = 0.5)
    
    ax.set_ylabel('MW')
    if not start:
        start = df_systemdata.index[0]
    if not end:
        end = df_systemdata.index[-1]
    ax.set_xlim(xmin=start, xmax=end)
    ax.set_ylim(ymin=0.0)
    
    ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 1)))
    #ax.xaxis.set_minor_locator(HourLocator(drange(0, 25, 6)))
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M')) #'%m-%d %H:%M'
    
    max_load = df_systemdata['cap_rest'].max()
    ppt.hlines(max_load, df_systemdata.index[0], df_systemdata.index[-1], colors='r', linestyles='dashed')
    
    #Legend
    #lns = lns1 + lns2 + lns3 + lns4 + lns5
    #labs = [l.get_label() for l in lns]
    #L = ax.legend(lns, labs, bbox_to_anchor=(0.3, -0.4), loc='lower left', ncol=1)
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    ppt.savefig(directory+'/system_load_disaggregated.png', bbox_inches='tight')
    return

#Bar plot for each full hour (except for first)
def plot_load_disaggbars(directory,df_systemdata,s_settings,start=None,end=None, interval=5):
    #Get settings
    no_houses = s_settings['flexible_houses'].iloc[0]
    C = float(s_settings['line_capacity'].iloc[0])
    p_max = float(s_settings['p_max'].iloc[0])
    interval = int(s_settings['interval'].iloc[0])
    PV_share = s_settings['PV_share'].iloc[0]
    EV_share = s_settings['EV_share'].iloc[0]
    Batt_share = s_settings['Batt_share'].iloc[0]
    city = s_settings['city'].iloc[0]
    market_file = s_settings['market_data'].iloc[0]
    which_price = s_settings['which_price'].iloc[0]

    fig = ppt.figure(figsize=(12,4),dpi=150)   
    ppt.ioff()
    #df_systemdata_full = df_systemdata.loc[df_systemdata.index.minute == 0]
    #df_systemdata_full = df_systemdata_full[1:]
    df_systemdata_full = df_systemdata.loc[(df_systemdata.index.minute%5) == 0]
    
    #House load
    ax = fig.add_subplot(111)
    
    part = 3
    w =  (mdates.date2num(start+timedelta(minutes=interval)) - mdates.date2num(start))/part
    
    lns1 = ppt.bar(df_systemdata_full['all_inflexload'].index-dt.timedelta(minutes=interval/part), df_systemdata_full['all_inflexload'], w,color='b',align='edge',label='test')
    lns2 = ppt.bar(df_systemdata_full['all_inflexload'].index-dt.timedelta(minutes=interval/part), df_systemdata_full['flex_hvac'], w, bottom=df_systemdata_full['all_inflexload'],color='g',align='edge')
    lns3 = ppt.bar(df_systemdata_full['all_inflexload'].index-dt.timedelta(minutes=interval/part), 
                   df_systemdata_full['flex_batt_demand'], w, bottom=df_systemdata_full['all_inflexload']+df_systemdata_full['flex_hvac'],color='m',align='edge')
    
    df_systemdata_full['C_max'] = 1.0
    #total demand minus non-WS market supply
    df_systemdata_full['WS_q'] = df_systemdata_full['total_load_houses'] + df_systemdata_full['flex_batt_demand'] - df_systemdata_full['flex_pv'] - df_systemdata_full['flex_batt_supply']
    df_systemdata_full['WS_q'] = df_systemdata_full[['WS_q','C_max']].min(axis=1)
    lns4 = ppt.bar(df_systemdata_full['WS_q'].index, df_systemdata_full['WS_q'], w,color='k',align='edge')
    lns5 = ppt.bar(df_systemdata_full['flex_pv'].index, df_systemdata_full['flex_pv'], w, bottom=df_systemdata_full['WS_q'],color='y',align='edge')
    lns6 = ppt.bar(df_systemdata_full['flex_batt_supply'].index, df_systemdata_full['flex_batt_supply'], w, bottom=df_systemdata_full['WS_q']+df_systemdata_full['flex_pv'],color='m',align='edge')
    
    
    ax.set_ylabel('MW')
    if not start:
        start = df_systemdata.index[0]
    if not end:
        end = df_systemdata.index[-1]
    ax.set_xlim(xmin=start-timedelta(minutes=interval)/2, xmax=end+timedelta(minutes=interval)/2)
    ax.set_ylim(ymin=0.0,ymax=1.2)
    
    ax.xaxis.set_major_locator(HourLocator(interval=1)) #arange(0, 25, 1)
    #ax.xaxis.set_minor_locator(HourLocator(interval=0.25))
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M')) #'%m-%d %H:%M'
    
    max_load = df_systemdata['cap_rest'].max()
    ppt.hlines(max_load, df_systemdata.index[0], df_systemdata.index[-1], colors='r', linestyles='dashed')
    
    #Legend
    ppt.legend((lns1[0],lns2[0],lns3[0],lns4[0],lns5[0],lns6[0]), 
               ('Inflexible Load', 'Flexible HVAC load','Battery load','WS supply','PV supply','Battery supply'),
               loc='lower center', bbox_to_anchor=(0.5, -0.4), ncol=2)
    #lns = lns1 + lns2 + lns3 + lns4 + lns5 + lns6
    #labs = [l.get_label() for l in lns]
    #L = ax.legend(lns, labs, bbox_to_anchor=(0.3, 0.0), loc='lower left', ncol=1)
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    ppt.savefig(directory+'/system_load_disaggregated_bars.png', bbox_inches='tight') #, bbox_extra_artist=[L]
    return

def plot_sysop(folder,df_systemdata,s_settings,start=None,end=None):
    #Get settings
    no_houses = s_settings['flexible_houses'].iloc[0]
    C = float(s_settings['line_capacity'].iloc[0])
    p_max = float(s_settings['p_max'].iloc[0])
    interval = int(s_settings['interval'].iloc[0])
    PV_share = s_settings['PV_share'].iloc[0]
    EV_share = s_settings['EV_share'].iloc[0]
    Batt_share = s_settings['Batt_share'].iloc[0]
    city = s_settings['city'].iloc[0]
    market_file = s_settings['market_data'].iloc[0]
    which_price = s_settings['which_price'].iloc[0]

    #Get data
    df_sysop = pd.read_csv(folder+'/system_operations.csv',parse_dates=['timedate'],dtype={'bid_quantity': float, 'bid_price': float} )
    df_awarded = pd.read_csv(folder+'/awarded_bids.csv',parse_dates=['timedate'],dtype={'unresp_load': float})
    max_load = df_systemdata['cap_rest'].max()
    
    #Re-organize and merge
    df_total_load = pd.DataFrame(index=df_systemdata.index,columns=['measured_real_power'],data=df_systemdata['measured_real_power'])
    df_total_load['SO'] = 0.0 #flexible loads
    df_total_load['curtailed'] = 0.0 #inflexible loads
    for t in df_total_load.index:
        if t == pd.Timestamp(year=2015, month=7, day=1, hour=14, minute=51):
            print('')
        df_sysop_t = df_sysop.loc[df_sysop['timedate'] == t]
        df_awarded_t = df_awarded.loc[df_awarded['timedate'] == t.floor('5min')]
        q_SO_t = 0.0
        q_curt_t = 0.0
        for app in df_sysop_t['appliance_name']:
            if app in df_awarded_t['appliance_name'].tolist():
                q_SO_t += df_sysop_t['q'].loc[df_sysop_t['appliance_name'] == app].sum()
            else:
                q_curt_t += df_sysop_t['q'].loc[df_sysop_t['appliance_name'] == app].sum()
        df_total_load.at[t,'SO'] = q_SO_t/1000 #flexible loads
        df_total_load.at[t,'curtailed'] = q_curt_t/1000 #inflexible loads
    
    df_total_load['SO_all'] = df_total_load['SO'] + df_total_load['curtailed']
    df_total_load['temp1'] = df_total_load['measured_real_power'] - max_load
    df_total_load['temp2'] = 0.0
    df_total_load['violations'] = df_total_load[['temp1','temp2']].max(axis=1)
    
    #Plot 1: Delta control
    fig = ppt.figure(figsize=(12,4),dpi=150)   
    ppt.ioff()
    #Delta
    ax = fig.add_subplot(111)
    lns1 = ax.plot(df_total_load['SO_all'],label='Control (P_tot_(t-1) - C)')
    lns2 = ax.plot(df_total_load['SO'],label='Curtailment of flexible loads')
    #lns3 = ax.plot(df_total_load['SO'],label='Curtailment of flexible loads')
    ax.set_ylabel('MW')
    if not start:
        start = df_total_load.index[0]
    if not end:
        end = df_total_load.index[-1]
    ax.set_xlim(xmin=start, xmax=end)    
    ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
    #Legend
    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]
    L = ax.legend(lns, labs, bbox_to_anchor=(0.3, -0.4), loc='lower left', ncol=1)
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    ppt.savefig(folder+'_vis/system_SO_vs_curtailed.png', bbox_inches='tight')
    
    #Plot 2: Delta from control (t-1) versus actual delta (t)
    fig = ppt.figure(figsize=(12,4),dpi=150)   
    ppt.ioff()
    #Delta
    ax = fig.add_subplot(111)
    lns1 = ax.plot(df_total_load['SO_all'],label='Control (P_tot_(t-1) - C)')
    lns2 = ax.plot(df_total_load['violations'],label='Actual capacity violation in t')
    ax.set_ylabel('MW')
    if not start:
        start = df_total_load.index[0]
    if not end:
        end = df_total_load.index[-1]
    ax.set_xlim(xmin=start, xmax=end)    
    ax.xaxis.set_major_locator(HourLocator(arange(0, 25, 3)))
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
    #Legend
    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]
    L = ax.legend(lns, labs, bbox_to_anchor=(0.3, -0.4), loc='lower left', ncol=1)
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    ppt.savefig(folder+'_vis/system_SO_error.png', bbox_inches='tight')
    
    return df_total_load

def plot_flex_HVAC(folder,directory,values,s_settings,perc_min=0.9,perc_max = 1.1):
    #Get settings
    no_houses = s_settings['flexible_houses'].iloc[0]
    C = float(s_settings['line_capacity'].iloc[0])
    p_max = float(s_settings['p_max'].iloc[0])
    interval = int(s_settings['interval'].iloc[0])
    PV_share = s_settings['PV_share'].iloc[0]
    EV_share = s_settings['EV_share'].iloc[0]
    Batt_share = s_settings['Batt_share'].iloc[0]
    city = s_settings['city'].iloc[0]
    market_file = s_settings['market_data'].iloc[0]
    which_price = s_settings['which_price'].iloc[0]

    global_par = open(folder+'/HH_global.py','r')
    for i in global_par:
        if '=' in i and 'flexible_houses' in i:
            no_houses = int(i.split(' ')[2])
        
    df_hvac_load = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8))
    df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
    df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
    df_hvac_load.set_index('# timestamp',inplace=True)
    sum_hvac_load = df_hvac_load[:no_houses].sum(axis=1)
    
    df_hvac_flex = pd.DataFrame(index=df_hvac_load.index,columns=['sum_flex_hvac'],data=sum_hvac_load)
    df_hvac_flex.sort_values('sum_flex_hvac',axis=0,ascending=False,inplace=True)
    df_hvac_flex = df_hvac_flex.iloc[:values] #number of houses to be displayed
    df_hvac_flex['indices'] = range(len(df_hvac_flex)) 
    df_hvac_flex.set_index('indices',inplace=True)
    
    fig = ppt.figure(figsize=(8,4),dpi=150)   
    ppt.ioff()
    #House load
    ax = fig.add_subplot(111)
    ppt.bar(df_hvac_flex.index,df_hvac_flex['sum_flex_hvac'])
    
    ax.set_xlabel('Ranking of max measured flex hvac power')
    ax.set_ylabel('MW')
    ax.set_ylim(ymin = df_hvac_flex['sum_flex_hvac'].min()*perc_min,ymax = df_hvac_flex['sum_flex_hvac'].max()*perc_max)
    ax.set_xlim(xmin=-1, xmax=values+1)
        
    #Legend
    #labs = [l.get_label() for l in lns]
    #L = ax.legend(lns, labs, bbox_to_anchor=(0.3, -0.4), loc='lower left', ncol=1)
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    print('Maximum value: '+str(df_hvac_flex['sum_flex_hvac'].max()))
    print('Minimum value: '+str(df_hvac_flex['sum_flex_hvac'].min()))
    ppt.savefig(directory+'/system_flex_hvac_load_curve.png', bbox_inches='tight')
    return df_hvac_load

def plot_inflex_HVAC(folder,directory,values,s_settings,perc_min=0.9,perc_max = 1.1):
    #Get settings
    no_houses = s_settings['flexible_houses'].iloc[0]
    C = float(s_settings['line_capacity'].iloc[0])
    p_max = float(s_settings['p_max'].iloc[0])
    interval = int(s_settings['interval'].iloc[0])
    PV_share = s_settings['PV_share'].iloc[0]
    EV_share = s_settings['EV_share'].iloc[0]
    Batt_share = s_settings['Batt_share'].iloc[0]
    city = s_settings['city'].iloc[0]
    market_file = s_settings['market_data'].iloc[0]
    which_price = s_settings['which_price'].iloc[0]

    global_par = open(folder+'/HH_global.py','r')
    for i in global_par:
        if '=' in i and 'flexible_houses' in i:
            no_houses = int(i.split(' ')[2])
        
    df_hvac_load = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8))
    df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
    df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
    df_hvac_load.set_index('# timestamp',inplace=True)
    sum_hvac_load = df_hvac_load[no_houses:].sum(axis=1)
    
    df_hvac_flex = pd.DataFrame(index=df_hvac_load.index,columns=['sum_flex_hvac'],data=sum_hvac_load)
    df_hvac_flex.sort_values('sum_flex_hvac',axis=0,ascending=False,inplace=True)
    df_hvac_flex = df_hvac_flex.iloc[:values]
    df_hvac_flex['indices'] = range(len(df_hvac_flex)) 
    df_hvac_flex.set_index('indices',inplace=True)
    
    fig = ppt.figure(figsize=(8,4),dpi=150)   
    ppt.ioff()
    #House load
    ax = fig.add_subplot(111)
    ppt.bar(df_hvac_flex.index,df_hvac_flex['sum_flex_hvac'])
    
    ax.set_xlabel('Ranking of max measured flex hvac power')
    ax.set_ylabel('MW')
    ax.set_ylim(ymin = df_hvac_flex['sum_flex_hvac'].min()*perc_min,ymax = df_hvac_flex['sum_flex_hvac'].max()*perc_max)
    ax.set_xlim(xmin=-1, xmax=values+1)
        
    #Legend
    #labs = [l.get_label() for l in lns]
    #L = ax.legend(lns, labs, bbox_to_anchor=(0.3, -0.4), loc='lower left', ncol=1)
    #L.get_texts()[0].set_text('Total system load')
    #L.get_texts()[1].set_text('Total unresponsive system load')
    print('Maximum value: '+str(df_hvac_flex['sum_flex_hvac'].max()))
    print('Minimum value: '+str(df_hvac_flex['sum_flex_hvac'].min()))
    ppt.savefig(directory+'/system_inflex_hvac_load_curve.png', bbox_inches='tight')
    return df_hvac_load

#Creates master table for non market data
def get_nomarketdata(folder,s_settings):
    print('Data without market')

    #Get settings
    no_houses = s_settings['flexible_houses'].iloc[0]
    C = float(s_settings['line_capacity'].iloc[0])
    p_max = float(s_settings['p_max'].iloc[0])
    interval = int(s_settings['interval'].iloc[0])    
    PV_share = s_settings['PV_share'].iloc[0]
    EV_share = s_settings['EV_share'].iloc[0]
    Batt_share = s_settings['Batt_share'].iloc[0]
    city = s_settings['city'].iloc[0]
    market_file = s_settings['market_data'].iloc[0]
    which_price = s_settings['which_price'].iloc[0]

    #Physical: total system load at slack bus (node 149 in IEEE123)
    df_nomarket = pd.read_csv(folder+'/load_node_149.csv',skiprows=range(8))
    df_nomarket['# timestamp'] = df_nomarket['# timestamp'].map(lambda x: str(x)[:-4])
    df_nomarket = df_nomarket.iloc[:-1]
    df_nomarket['# timestamp'] = pd.to_datetime(df_nomarket['# timestamp'])
    df_nomarket.set_index('# timestamp',inplace=True)
    df_nomarket['measured_real_power'] = df_nomarket['measured_real_power']/1000000
    print('Max measured real power: '+str(df_nomarket['measured_real_power'].max()))
    
    df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8))
    df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
    df_total_load = df_total_load.iloc[:-1]
    df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
    df_total_load.set_index('# timestamp',inplace=True)
    df_total_load = pd.DataFrame(index=df_total_load.index,columns=['total_load_houses'],data=df_total_load.sum(axis=1))
    print('Max total load: '+str(df_total_load['total_load_houses'].max()))
    
    df_hvac_load = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8))
    df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
    df_hvac_load = df_hvac_load.iloc[:-1]
    df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
    df_hvac_load.set_index('# timestamp',inplace=True)                           
    print('Max flexible hvac load: '+str(0.0))
    
    df_T = pd.read_csv(folder+'/T_all.csv',skiprows=range(8))
    df_T['# timestamp'] = df_T['# timestamp'].map(lambda x: str(x)[:-4])
    df_T['# timestamp'] = pd.to_datetime(df_T['# timestamp'])
    df_T.set_index('# timestamp',inplace=True)

    if PV_share + Batt_share + EV_share > 0.0:
        df_P_out = pd.read_csv(folder+'/total_P_Out.csv',skiprows=range(8))
        df_P_out['# timestamp'] = df_P_out['# timestamp'].map(lambda x: str(x)[:-4])
        df_P_out['# timestamp'] = pd.to_datetime(df_P_out['# timestamp'])
        df_P_out = df_P_out[df_P_out.columns[~df_P_out.columns.str.contains('EV')]]
        df_P_out = df_P_out[df_P_out.columns[~df_P_out.columns.str.contains('Batt')]]
        df_P_out.set_index('# timestamp',inplace=True)      
                       
    #Merge: total load, av_HVAC, av_T, PV generation
    df_nomarket = df_nomarket.merge(df_total_load/1000, how='outer', left_index=True, right_index=True)
    df = pd.DataFrame(index=df_total_load.index, columns=['sum_houseload'], data = df_total_load.sum(axis=1))
    df_nomarket = df_nomarket.merge(df/1000, how='outer', left_index=True, right_index=True)
    df = pd.DataFrame(index=df_hvac_load.index, columns=['sum_HVAC'], data = df_hvac_load.sum(axis=1))
    df_nomarket = df_nomarket.merge(df/1000, how='outer', left_index=True, right_index=True)
    df = pd.DataFrame(index=df_T.index, columns=['av_T'], data = df_T.mean(axis=1))
    df_nomarket = df_nomarket.merge(df, how='outer', left_index=True, right_index=True)
    if PV_share + Batt_share + EV_share > 0.0:
        df = pd.DataFrame(index=df_P_out.index, columns=['sum_PV'], data = df_P_out.mean(axis=1))
        df_nomarket = df_nomarket.merge(df/1000, how='outer', left_index=True, right_index=True)

    return df_nomarket, df_T

#Creates master table for system data
def get_systemdata(folder,s_settings,df_results,ind):
    #import pdb; pdb.set_trace()
    start = pd.to_datetime(s_settings['start_time'].iloc[0]) + pd.Timedelta(days=1) #pd.Timestamp(2015, 7, 16)
    end = pd.to_datetime(s_settings['end_time'].iloc[0])

    #Get settings
    no_houses = s_settings['flexible_houses'].iloc[0]
    C = float(s_settings['line_capacity'].iloc[0])
    p_max = float(s_settings['p_max'].iloc[0])
    interval = int(s_settings['interval'].iloc[0])
    PV_share = s_settings['PV_share'].iloc[0]
    EV_share = s_settings['EV_share'].iloc[0]
    Batt_share = s_settings['Batt_share'].iloc[0]
    city = s_settings['city'].iloc[0]
    market_file = s_settings['market_data'].iloc[0]
    which_price = s_settings['which_price'].iloc[0]

    #Physical: total system load at slack bus (node 149 in IEEE123)
    df_slack = pd.read_csv(folder+'/load_node_149.csv',skiprows=range(8))
    df_slack['# timestamp'] = df_slack['# timestamp'].map(lambda x: str(x)[:-4])
    df_slack = df_slack.iloc[:-1]
    df_slack['# timestamp'] = pd.to_datetime(df_slack['# timestamp'])
    df_slack.set_index('# timestamp',inplace=True)
    df_slack['measured_real_power'] = df_slack['measured_real_power']/1000
    df_slack['cap_rest'] = C
    print('Max measured real power: '+str(df_slack['measured_real_power'].iloc[15:].max()))
    
    #Total house load
    df_total_load = pd.read_csv(folder+'/total_load_all.csv',skiprows=range(8))
    df_total_load['# timestamp'] = df_total_load['# timestamp'].map(lambda x: str(x)[:-4])
    df_total_load = df_total_load.iloc[:-1]
    df_total_load['# timestamp'] = pd.to_datetime(df_total_load['# timestamp'])
    df_total_load.set_index('# timestamp',inplace=True)
    df_total_load = pd.DataFrame(index=df_total_load.index,columns=['total_load_houses'],data=df_total_load.sum(axis=1))
    print('Max total residential load: '+str(df_total_load['total_load_houses'].iloc[15:].max()))

    df_systemdata = df_slack.merge(df_total_load, how='outer', left_index=True, right_index=True)
    
    #Total hvac load
    df_hvac_load = pd.read_csv(folder+'/hvac_load_all.csv',skiprows=range(8))
    df_hvac_load['# timestamp'] = df_hvac_load['# timestamp'].map(lambda x: str(x)[:-4])
    df_hvac_load = df_hvac_load.iloc[:-1]
    df_hvac_load['# timestamp'] = pd.to_datetime(df_hvac_load['# timestamp'])
    df_hvac_load.set_index('# timestamp',inplace=True)                           
    all_flexhvac = df_hvac_load.iloc[:,:no_houses].sum(axis=1)
    df_all_flexhvac = pd.DataFrame(index=all_flexhvac.index,columns=['flex_hvac'],data=all_flexhvac)
    all_inflexhvac = df_hvac_load.iloc[:,no_houses:].sum(axis=1)
    df_all_inflexhvac = pd.DataFrame(index=all_inflexhvac.index,columns=['inflex_hvac'],data=all_inflexhvac)
    print('Max flexible hvac load: '+str(df_all_flexhvac['flex_hvac'].iloc[15:].max()))
    print('Max inflexible hvac load: '+str(df_all_inflexhvac['inflex_hvac'].iloc[15:].max()))
    share_hvac_energy = (df_all_flexhvac['flex_hvac'].sum() + df_all_inflexhvac['inflex_hvac'].sum())/df_total_load['total_load_houses'].sum()
    
    df_systemdata = df_systemdata.merge(df_all_flexhvac, how='outer', left_index=True, right_index=True)
    df_systemdata = df_systemdata.merge(df_all_inflexhvac, how='outer', left_index=True, right_index=True)

    #Inverter devices
    list_PV = list(pd.read_csv(folder+'/df_PV_state.csv')['PV_name'])
    list_PV_inv = list(pd.read_csv(folder+'/df_PV_state.csv')['inverter_name'])    
    list_batt = list(pd.read_csv(folder+'/df_battery_state.csv')['battery_name'])
    list_batt_inv = []
    for batt in list_batt:
        list_batt_inv += ['Bat_inverter_'+batt[8:]]
    list_EV = list(pd.read_csv(folder+'/df_EV_state.csv')['EV_name'])
    list_EV_inv = []
    for EV in list_EV:
        list_EV_inv += ['EV_inverter_'+EV[3:]]
    
    #Inverter infeed/outfeed
    if PV_share + EV_share + Batt_share > 0.0:
        df_inv_load = pd.read_csv(folder+'/total_P_Out.csv',skiprows=range(8))
        df_inv_load['# timestamp'] = df_inv_load['# timestamp'].map(lambda x: str(x)[:-4])
        df_inv_load = df_inv_load.iloc[:-1]
        df_inv_load['# timestamp'] = pd.to_datetime(df_inv_load['# timestamp'])
        df_inv_load.set_index('# timestamp',inplace=True)                           
    
        if PV_share > 0.0:
            all_pv =  df_inv_load[list_PV_inv].sum(axis=1)/1000 #W -> kW (comes from GridlabD)
            df_all_pv = pd.DataFrame(index=all_pv.index,columns=['flex_pv'],data=all_pv)
            print('Max flexible pv infeed: '+str(df_all_pv['flex_pv'].max()))
            #Merge PV data
            df_systemdata = df_systemdata.merge(df_all_pv, how='outer', left_index=True, right_index=True)

        if Batt_share > 0.0:
            all_batt = df_inv_load[list_batt_inv].sum(axis=1)/1000 #W -> kW (comes from GridlabD)
            df_all_batt = pd.DataFrame(index=all_batt.index,columns=['flex_batt'],data=all_batt)
            print('Max flexible batt load: '+str(df_all_batt['flex_batt'].max()))
            #Merge battery data
            df_systemdata = df_systemdata.merge(df_all_batt, how='outer', left_index=True, right_index=True)
            df_systemdata['flex_batt_supply'] = 0.0
            df_systemdata['flex_batt_supply'].loc[df_systemdata['flex_batt'] > 0] = df_systemdata['flex_batt'].loc[df_systemdata['flex_batt'] > 0]
            df_systemdata['flex_batt_demand'] = 0.0
            df_systemdata['flex_batt_demand'].loc[df_systemdata['flex_batt'] < 0] = -df_systemdata['flex_batt'].loc[df_systemdata['flex_batt'] < 0]
    
        if EV_share > 0.0:
            #Retrieve battery data from inverter data
            all_EV = -df_inv_load[list_EV_inv].sum(axis=1)/1000 #W -> kW (comes from GridlabD)
            df_all_EV = pd.DataFrame(index=all_EV.index,columns=['flex_EV'],data=all_EV)
            #Merge EV data
            df_systemdata = df_systemdata.merge(df_all_EV, how='outer', left_index=True, right_index=True)

    total_supply = df_slack['measured_real_power'].sum()
    if PV_share > 0.0:
        total_PV_supply = df_all_pv['flex_pv'].sum()
        total_supply += total_PV_supply
    if Batt_share > 0.0:
        total_Batt_supply = df_systemdata['flex_batt_supply'].sum()
        total_supply += total_Batt_supply
    if PV_share > 0.0:
        PV_energy_share = total_PV_supply/total_supply*100
    else:
        PV_energy_share = 0.0
    if Batt_share > 0.0:
        Batt_energy_share = total_Batt_supply/total_supply*100
    else:
        Batt_energy_share = 0.0

    #Market: only to get unresponsive load
    df_unresp = pd.read_csv(folder+'/df_buy_bids.csv')
    df_unresp = df_unresp.loc[df_unresp['appliance_name'] == 'unresponsive_loads']
    df_unresp.drop(['appliance_name','Unnamed: 0'],axis=1,inplace=True)
    df_unresp.rename(columns={'bid_quantity': 'unresp_load'}, inplace=True)
    try:
        df_unresp.rename(columns={'timedate':'timestamp'},inplace=True)
    except:
        pass
    df_unresp.set_index('timestamp',inplace=True)
    print('Max unresponsive load: '+str(df_unresp['unresp_load'].max()))
    df_systemdata = df_systemdata.merge(df_unresp, how='outer', left_index=True, right_index=True)
    
    #Prices
    df_WS = pd.read_csv('/Users/admin/Documents/powernet/powernet_markets_mysql/glm_generation_'+city+'/'+market_file,parse_dates=[0])
    df_WS.rename(columns={'Unnamed: 0':'timestamp'},inplace=True)
    df_WS.set_index('timestamp',inplace=True)
    df_WS['P_cap'] = p_max
    df_WS['WS'] = df_WS[[which_price, 'P_cap']].min(axis=1)
    print('Max WS price: '+str(df_WS[which_price].max()))
    
    df_cleared = pd.read_csv(folder+'/df_prices.csv',parse_dates=[0])
    df_cleared.rename(columns={'Unnamed: 0':'timedate'},inplace=True)
    df_cleared.set_index('timedate',inplace=True)
    print('Max clearing capacity: '+str(df_cleared['clearing_quantity'].max()))
    
    df_market = df_cleared.merge(df_WS, how='inner', left_index=True, right_index=True)
    df_systemdata = df_systemdata.merge(df_market, how='outer', left_index=True, right_index=True)
    df_systemdata.fillna(method='ffill',inplace=True)

    #Calculate 
    df_systemdata['all_inflexload'] = df_systemdata['measured_real_power']
    if PV_share > 0.0:
        df_systemdata['all_inflexload'] = df_systemdata['all_inflexload'] + df_systemdata['flex_pv']
    if Batt_share > 0.0:
        df_systemdata['all_inflexload'] = df_systemdata['all_inflexload'] + df_systemdata['flex_batt_supply'] - df_systemdata['flex_batt_demand']
    if EV_share > 0.0:
        df_systemdata['all_inflexload'] = df_systemdata['all_inflexload'] - df_systemdata['flex_EV']
    
    #Clean up
    df_systemdata = df_systemdata/1000 #into MW
    df_systemdata['clearing_price'] = df_systemdata['clearing_price']*1000
    df_systemdata[which_price] = df_systemdata[which_price]*1000
    df_systemdata['WS'] = df_systemdata['WS']*1000
    df_systemdata['P_cap'] = df_systemdata['P_cap']*1000

    #Get max and mean
    max_real_power = df_systemdata['measured_real_power'].loc[start:end].max() #Exclude first 15min
    mean_real_power = df_systemdata['measured_real_power'].loc[start:end].mean()
    max_res_load = df_systemdata['total_load_houses'].loc[start:end].max()
    mean_res_load = df_systemdata['total_load_houses'].loc[start:end].mean()
    max_flex_hvac = df_systemdata['flex_hvac'].loc[start:end].max()
    mean_flex_hvac = df_systemdata['flex_hvac'].loc[start:end].mean()
    max_inflex_hvac = df_systemdata['inflex_hvac'].loc[start:end].max()
    mean_inflex_hvac = df_systemdata['inflex_hvac'].loc[start:end].mean()
    mean_p = df_systemdata['clearing_price'].loc[start:end].mean()
    if PV_share > 0.0:
        max_pv = df_systemdata['flex_pv'].loc[start:end].max()
        mean_pv = df_systemdata['flex_pv'].loc[start:end].mean()
    else:
        max_pv = 0.0
        mean_pv = 0.0
    if Batt_share > 0.0:
        max_batt_demand = df_systemdata['flex_batt_demand'].loc[start:end].max()
        mean_batt_demand = df_systemdata['flex_batt_demand'].loc[start:end].mean()
        max_batt_supply = df_systemdata['flex_batt_supply'].loc[start:end].max()
        mean_batt_supply = df_systemdata['flex_batt_supply'].loc[start:end].mean()
    else:
        max_batt_demand = 0.0
        mean_batt_demand = 0.0
        max_batt_supply = 0.0
        mean_batt_supply = 0.0
    if EV_share > 0.0:
        max_EV = df_systemdata['flex_EV'].loc[start:end].max()
        mean_EV = df_systemdata['flex_EV'].loc[start:end].mean()
    else:
        max_EV = 0.0
        mean_EV = 0.0
    max_unresp = df_systemdata['unresp_load'].loc[start:end].max()
    mean_unresp = df_systemdata['unresp_load'].loc[start:end].mean()
    max_cleared = df_systemdata['clearing_quantity'].loc[start:end].max()
    mean_cleared = df_systemdata['clearing_quantity'].loc[start:end].mean()

    #T
    df_T = pd.read_csv(folder+'/T_all.csv',skiprows=range(8))
    df_T['# timestamp'] = df_T['# timestamp'].map(lambda x: str(x)[:-4])
    df_T = df_T.iloc[:-1]
    df_T['# timestamp'] = pd.to_datetime(df_T['# timestamp'])
    df_T.set_index('# timestamp',inplace=True)
    if no_houses > 0:
        df_T = df_T[df_T.columns[:no_houses]]
    df_T_mean = pd.DataFrame(index=df_T.index,columns=['mean_T'],data=df_T.mean(axis=1))
    mean_T = df_T_mean['mean_T'].loc[start:end].mean() #Mean T over all flexible houses in relevant period
    df_T_max = pd.DataFrame(index=df_T.index,columns=['max_T'],data=df_T.max(axis=1))
    max_T = df_T_max['max_T'].loc[start:end].max() 
    max_T = df_T.max(axis=0).mean() #Mean of max T over all flexible houses in relevant period

    #df_nomarket, df_T = get_nomarketdata(folder_nomarket,s_settings)
    #
    df_results_temp = pd.DataFrame(columns=df_results.columns,data=[[ind,no_houses,PV_share,EV_share,Batt_share,max_real_power,mean_real_power,max_res_load,mean_res_load,max_flex_hvac,mean_flex_hvac,max_inflex_hvac,mean_inflex_hvac,share_hvac_energy,max_pv,mean_pv,PV_energy_share,max_batt_supply,mean_batt_supply,max_batt_demand,mean_batt_demand,Batt_energy_share,max_EV,mean_EV,max_unresp,mean_unresp,max_cleared,mean_cleared,mean_p,mean_T,max_T]])
    df_results = df_results.append(df_results_temp,ignore_index=True)

    #df_systemdata = df_systemdata.loc[start:end]
    return df_systemdata, df_results
    