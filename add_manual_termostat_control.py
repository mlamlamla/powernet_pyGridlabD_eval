# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 02:39:26 2019

@author: MLA
"""



file = 'IEEE_123_homes_5min.glm'
new_file = 'test.glm'
no_houses = 5

glm = open(file,'r') 
new_glm = open(new_file,'w') 
j = 0

for line in glm:
    new_glm.write(line)
    if 'heating_system_type' in line and j < (no_houses-1):
        new_glm.write('    thermostat_control NONE; \n')
        j += 1

glm.close()
new_glm.close()