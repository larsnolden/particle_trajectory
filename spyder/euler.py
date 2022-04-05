#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 18:16:43 2022

@author: larsnolden
"""
import numpy as np
from evaporation import diameter_change_due_to_evaporation
from acceleration import acceleration

def euler(xy_n, delta_t, funcs):
    # 2D euler
    x_n = xy_n[0] + delta_t*funcs[0]
    y_n = xy_n[1] + delta_t*funcs[1]
    return [x_n, y_n]


def euler_step(v, pos, particle_diameter, delta_t, air_velocity_field, air_pressure_field, t, stream_traces):
    # velocity field
    v_air =  air_velocity_field(pos, stream_traces)
    v_actual = np.add(v, v_air)
    speed = (v_actual[0]**2+v_actual[1]**2)**(1/2)
    
    if(air_pressure_field):
        pressure = air_pressure_field(pos, speed, stream_traces)
        particle_diameter_new = particle_diameter + diameter_change_due_to_evaporation(delta_t, particle_diameter, pressure, speed)
        #print('v_air', v_air, 'v_actual', v_actual, 'speed', speed, 'v', v, 't', t, 'particle_diameter', particle_diameter, 'pressure', pressure, 'particle_diameter_new', particle_diameter_new)
    else:
        particle_diameter_new = particle_diameter # no evaporation case
    
    pos_new = euler(pos, delta_t, v_actual)
    a_new = acceleration(v_actual, speed, particle_diameter_new)
    v_new = euler(v_actual, delta_t, a_new)
        
    return {
        'a': a_new,
        'v': v_new,
        'pos': pos_new,
        'd': particle_diameter_new
    }


