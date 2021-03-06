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
import os
from multiprocessing import Pool

from constants import *
from passengers import passengers
from train import build_train_coordinates, collision_detection, collision_detection_init
from simulation import particle_simulation
from experiment_files import files
from progress.bar import Bar

experiment_time = 10
delta_t = 1e-3

color_map = plt.cm.ScalarMappable(cmap=cm.tab10, norm=plt.Normalize(0, len(passengers)))

debug_results = []

def air_pressure_field(pos, speed, stream_traces):
    # find the closest available position from the openFoam data
    # http://www.wolfdynamics.com/wiki/tut_cavity.pdf
    p_relative = stream_traces.iloc[(stream_traces['Points:0']-pos[0]+stream_traces['Points:1']-pos[1]).abs().argsort()[:1]]['p'].values[0]*fluid_density
    #p = p_relative + 0.5*speed**2
    p = p_train + p_relative
    return p

def air_velocity_field(pos, stream_traces):
    possible_x = stream_traces.iloc[(stream_traces['Points:0']-pos[0]).abs().argsort()[:100]]
    match = possible_x.iloc[(possible_x['Points:1']-pos[1]).abs().argsort()[:1]]
    u_x = match['U:0'].values[0]
    u_y = match['U:1'].values[0]
    # find the closest available position from the openFoam data
    #u_x = stream_traces.iloc[(stream_traces['Points:0']-pos[0]).abs().argsort()[:1]]['U:0'].values[0]
    #u_y = stream_traces.iloc[(stream_traces['Points:1']-pos[1]).abs().argsort()[:1]]['U:1'].values[0]
    return [u_x, u_y]
 
# determine all trajectories to calculate for progress bar
n_trajectiories = len(files) * len(passengers) * len(passengers[0]['v']) * len(passengers[0]['d']) * experiment_time/delta_t
bar = Bar('Processing', max=n_trajectiories, suffix='%(percent)d%%; %(eta_td)s hours remaining')

def simulation(velocity_profile_file):
    fig, ax = plt.subplots(figsize=(16,5))
    fig.set_dpi(400)
    ax.set_xlim([0, 24])
    ax.set_ylim([0, train_height])
    ax.set_aspect('equal', adjustable='box')
    
    [x_train, y_train] = build_train_coordinates(len(passengers))
    ax.plot(x_train,y_train, color='blue')
    collision_detection_initialised = collision_detection_init(x_train, y_train)
    
    # import openFOAM velocity/pressure field
    stream_traces = pd.read_csv(velocity_profile_file['path'])
    print(velocity_profile_file['name'])

    for passenger_id, passenger in enumerate(passengers):
        active_passenger = passenger['type'] != 'inhale'
  
        x_exhaling = 1.1-0.3+1.1*passenger['person']
        x_label =  1.1-0.4+1.1*passenger['person']
        pos_init = [x_exhaling, exhalation_height]
        # add passenger label
        plt.text(x_label, 0.2, passenger_id+1, color=color_map.to_rgba(passenger_id) if active_passenger else 'black')
        if(active_passenger):
            for particle_diameter in passenger['d']:
                for ejection_velocity in passenger['v']:
                        #res = particle_simulation(particle_diameter, passenger['v'], pos_init, experiment_time, delta_t, air_velocity_field, bar, air_pressure_field, collision_detection_initialised)
                        res = particle_simulation(particle_diameter, ejection_velocity, pos_init, experiment_time, delta_t, air_velocity_field, bar, stream_traces, air_pressure_field, collision_detection_initialised)        
                        # extract axes from position list
                        pos_x = list(map(lambda xy: xy[0], res['pos']))
                        pos_y = list(map(lambda xy: xy[1], res['pos']))
                        #print('diameter change: ', res['d'])
                        #print('time', res['t'])
                        speed = (ejection_velocity[0]**2+ejection_velocity[1]**2)**(1/2)
                        ax.plot(pos_x, pos_y, zorder=100, color=color_map.to_rgba(passenger_id), label=f'{passenger_id+1} - d: {round(particle_diameter/1e-6, 2)} ??m; v: {speed} m/s', alpha=0.1)
                        v_x = list(map(lambda xy: xy[0], res['v']))
                        v_y = list(map(lambda xy: xy[1], res['v']))
                        # add to debugging results
                        debug_results.append({
                            'res': res,
                            'passenger': passenger_id+1
                            })
                        # plot arrow at start and end of trajecotory
                        #if(res['collided']):
                            #print('\n particle collided')
                        for id in [0, len(v_x) - 2]:
                            # make arrow length extremly small (/100000)
                            plt.arrow(pos_x[id], pos_y[id], v_x[id]/100000, v_y[id]/100000, head_width=0.1, color=color_map.to_rgba(passenger_id), length_includes_head=True)
                        bar.finish()
        
    stream_traces_downsampled = stream_traces[['Points:0', 'Points:1', 'U:0', 'U:1']].sample(n=1000)
    #ax.quiver(stream_traces_downsampled['Points:0'], stream_traces_downsampled['Points:1'], stream_traces_downsampled['U:0'], stream_traces_downsampled['U:1'], color='#adadad', zorder=0)
    ax.quiver(stream_traces['Points:0'], stream_traces['Points:1'], stream_traces['U:0'], stream_traces['U:1'], color='#ededed', zorder=0)
    #ax.legend(loc='upper left', bbox_to_anchor=(0, -0.5), ncol=5)
    plt.savefig('./output/'+file['name'] + '_' + str(delta_t) +'.png',  bbox_inches="tight")


if __name__ ==  '__main__':
    try:
        pool = Pool(8)
        pool.map(simulation, files)
    except Exception as e:
        print(e)
        pool.close()
        pool.join()
    finally: # To make sure processes are closed in the end, even if errors happen
        pool.close()
        pool.join()
