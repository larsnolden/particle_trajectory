#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 17:52:58 2022

@author: larsnolden
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
import math
from itertools import cycle
#from numpy import ma
from matplotlib import ticker, cm
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
import random


from constants import *
from passengers import passengers
from train import build_train_coordinates, collision_detection, collision_detection_init
from simulation import particle_simulation

# import openFOAM velocity/pressure field
stream_traces = pd.read_csv('./Steady Field/ClosedValves.csv')

experiment_time = 4
delta_t = 0.001
total_seats = 20
exhalation_height = 1.2

fig, ax = plt.subplots(figsize=(16,5))
fig.set_dpi(200)
ax.set_xlim([0, 24])
ax.set_ylim([0, 2.5])
ax.set_aspect('equal', adjustable='box')

[x_train, y_train] = build_train_coordinates(total_seats)
ax.plot(x_train,y_train, color='blue')
collision_detection_initialised = collision_detection_init(x_train, y_train)

def air_pressure_field(pos, speed):
    # find the closest available position from the openFoam data
    # http://www.wolfdynamics.com/wiki/tut_cavity.pdf
    p_relative = stream_traces.iloc[(stream_traces['Points:0']-pos[0]+stream_traces['Points:1']-pos[1]).abs().argsort()[:1]]['p'].values[0]*fluid_density
    #p = p_relative + 0.5*speed**2
    p = p_train + p_relative
    return p

def air_velocity_field(pos):
    # find the closest available position from the openFoam data
    u_x = stream_traces.iloc[(stream_traces['Points:0']-pos[0]).abs().argsort()[:1]]['U:0'].values[0]
    u_y = stream_traces.iloc[(stream_traces['Points:1']-pos[1]).abs().argsort()[:1]]['U:1'].values[0]
    return [u_x, u_y]
    
for passenger in passengers[:10]:
    for particle_diameter in passenger['d']:
        print('person: ', passenger['person'])
        x_exhaling = 1.1-0.1+1.1*passenger['person']
        pos_init = [x_exhaling, exhalation_height]
        res = particle_simulation(particle_diameter, passenger['v'], pos_init, experiment_time, delta_t, air_velocity_field, air_pressure_field, collision_detection_initialised)        
        # extract axes from position list
        pos_x = list(map(lambda xy: xy[0], res['pos']))
        pos_y = list(map(lambda xy: xy[1], res['pos']))
        print('diameter change: ', res['d'])
        print('time', res['t'])
        ax.plot(pos_x, pos_y, linestyle='dashed' if passenger['type'] == 'speech' else 'dotted', zorder=100)
        

stream_traces_downsampled = stream_traces[['Points:0', 'Points:1', 'U:0', 'U:1']].sample(n=1000)
#ax.quiver(stream_traces_downsampled['Points:0'], stream_traces_downsampled['Points:1'], stream_traces_downsampled['U:0'], stream_traces_downsampled['U:1'], color='#adadad', zorder=0)
ax.quiver(stream_traces['Points:0'], stream_traces['Points:1'], stream_traces['U:0'], stream_traces['U:1'], color='#adadad', zorder=0)