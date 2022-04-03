#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 18:15:01 2022

@author: larsnolden
"""
import numpy as np
import math
from euler import euler_step

def particle_simulation(particle_diameter_init, v_init, pos_init, experiment_time, delta_t, air_velocity_field, air_pressure_field=None, collision_detection=None ):
    steps = np.arange(delta_t, experiment_time, delta_t)
    n_steps = math.ceil(experiment_time/delta_t)
    #print('experiment_time', experiment_time, 'delta_t', delta_t, 'steps', steps, 'n_steps', n_steps)
    v = np.zeros(shape=(n_steps + 1, 2))
    pos = np.zeros(shape=(n_steps + 1, 2))
    particle_diameter = np.zeros(shape=(n_steps + 1))
    
    v[0] = v_init
    pos[0] = pos_init
    particle_diameter[0] = particle_diameter_init
    
    for id, step in enumerate(steps):
        # id starts at 0
        has_colided = False
        t = steps[id]
        # compute new values
        #print('particle_diameter[id]', particle_diameter[id])
        new_values = euler_step(v[id], pos[id], particle_diameter[id], delta_t, air_velocity_field, air_pressure_field, t)
        
        if(collision_detection):
            has_colided=collision_detection(new_values['pos'])
    
        if(new_values['d'] <= 0 or has_colided):
            #print('has_colided', has_colided, 'pos', new_values['pos'])
            if(new_values['d'] <= 0):
                print('particle evaporated')
            elif(has_colided):
                print('particle collided')
            # particle evaporated fully => break iteration early
            # do not return the empty initialized zeroes
            return {
                'v': v[0:id],
                'pos': pos[0:id],
                'd': particle_diameter[0:id],
                't': steps[0:id]
            }

        # add new values
        v[id+1] = new_values['v']
        pos[id+1] = new_values['pos']
        particle_diameter[id+1] = new_values['d']
        
    return {
        'v': v,
        'pos': pos,
        'd': particle_diameter,
        't': steps
    }
