#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 14:10:11 2022

@author: larsnolden
"""
import matplotlib.pyplot as plt
from simulation import particle_simulation

fluid_density = 1030 # [kg/m3]
particle_density = 2600 # density marble [kg/m3]
particle_diameter = 0.01 # [m]
experiment_time = 4
delta_t = 0.01

velocity_field = lambda pos: [0, 0]

# velocity over time
res = particle_simulation(particle_diameter, [0, 1], [0, 1], experiment_time, delta_t, velocity_field )
fig, ax = plt.subplots(figsize=(16,5))
fig.set_dpi(200)
#ax.set_ylabel('diameter [μm]')
#ax.set_xlabel('t [s]')
ax.plot(res['pos'][0], res['pos'][1])
#ax.plot(res['t'], res['v'][:len(res['t'])])
# fall distance over time