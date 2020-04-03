# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 03:17:53 2018

@author: MLA

Goes through all evaluations
"""
import os
import plt_total_system_load_SLACK as sysload
import residual_unresp_capacity_constraint as resload
import bids_versus_dispatch as biddis
import T_vs_bids as Tbid
import bids_versus_dispatch_house as biddish
import bids_versus_dispatch_allhouses


results = 'Results_100_EVs'
capacity = 1000
house_no = 60

directory = results+'_vis'
if not os.path.exists(directory):
    os.makedirs(directory)

#Plot total system load versus capacity constraint
sysload.plot_total_load(results,directory,capacity,house_no)
sysload.table_bids(results,directory,capacity)

#Plot size of flexible load versus available capacity
resload.plot_residual_load(results,directory,capacity)

#Plots awarded bid versus actual dispatch
biddis.plot_bid_vs_dispatch(results,directory,house_name=None)
biddish.plot_bid_vs_dispatch_house(results,directory,house_name=None)

#Plots temperature versus actual bids
Tbid.plot_T_vis_bid(results,directory,house_name=None)

#Plots actual load for all houses
# !!!! Only for the ones included into hvac_load.csv so far !!!!
plot_bid_vs_dispatch_all(results,directory)
