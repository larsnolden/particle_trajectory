#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 18:15:01 2022

@author: larsnolden
"""
import numpy as np
import math
from euler import euler_step
from constants import minimum_virus_particle_size

def particle_simulation(particle_diameter_init, v_init, pos_init, experiment_time, delta_t, air_velocity_field, bar, air_pressure_field=None, collision_detection=None):
    steps = np.arange(delta_t, experiment_time, delta_t)
    n_steps = round(experiment_time/delta_t)
    #print('experiment_time', experiment_time, 'delta_t', delta_t, 'steps', steps, 'n_steps', n_steps)
    v = np.zeros(shape=(n_steps, 2))
    pos = np.zeros(shape=(n_steps, 2))
    particle_diameter = np.zeros(shape=(n_steps))
    # just for debugging:
    a = np.zeros(shape=(n_steps, 2))
    
    v[0] = v_init
    pos[0] = pos_init
    particle_diameter[0] = particle_diameter_init
    a[0] = [0, 0]
    
    for id, step in enumerate(steps):
        bar.next()
        # id starts at 0
        has_colided = False
        has_evaporated = False
        t = steps[id]
        # compute new values
        #print('particle_diameter[id]', particle_diameter[id])
        new_values = euler_step(v[id], pos[id], particle_diameter[id], delta_t, air_velocity_field, air_pressure_field, t)
        
        if(new_values['d'] <= 0):
            has_evaporated = True
            new_values['d'] = minimum_virus_particle_size
            
        if(collision_detection):
            has_colided=collision_detection(new_values['pos'])
            if(has_colided):    
                # particle evaporated fully => break iteration early
                # do not return the empty initialized zeroes
                return {
                    'v': v[0:id],
                    'pos': pos[0:id],
                    'd': particle_diameter[0:id],
                    't': steps[0:id],
                    'a': steps[0:id],
                    'collided': True
                }

        # add new values
        v[id+1] = new_values['v']
        pos[id+1] = new_values['pos']
        particle_diameter[id+1] = new_values['d']
        a[id+1] = new_values['a']
        
    return {
        'v': v,
        'pos': pos,
        'd': particle_diameter,
        't': steps,
        'a': a,
        'collided': has_colided,
        'evaporated': has_evaporated
    }
