#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 17:54:53 2022

@author: larsnolden
"""
from math import log, e
from constants import *
from acceleration import Re
import numpy as np
import matplotlib.pyplot as plt
import math

S_c = dynamic_viscosity_air_25C/(fluid_density*diffusion_coefficient_water_in_air) # Elana notes
sherwood2 = lambda particle_diameter: k_m*particle_diameter/diffusion_coefficient_water_in_air #33
sherwood = lambda v, particle_diameter: 2+0.6*Re(v, particle_diameter)**(1/2)*S_c**(1/3) #34
vapour_pressure = lambda particle_diameter: saturation_pressure_water_1atm_25C*e**(2*surf_tension_water/(particle_density*R_v*temp*particle_diameter/2)) #32
vapor_mass_frac_r = lambda particle_diameter, pressure: vapour_pressure(particle_diameter)*M_v/(vapour_pressure(particle_diameter)*M_v + (pressure - vapour_pressure(particle_diameter))*M_g) #31
y_m = lambda particle_diameter, pressure: 2/3*vapor_mass_frac_r(particle_diameter, pressure)+1/3*vapor_mass_frac_inf
density_mixture = lambda particle_diameter, pressure: fluid_density*(y_m(particle_diameter, pressure)*vapor_mass_frac_r(particle_diameter, pressure)+1-y_m(particle_diameter, pressure))

diameter_change_due_to_evaporation = lambda dt, particle_diameter, pressure, v: 2*dt*(-1*fluid_density*diffusion_coefficient_water_in_air*sherwood(v, particle_diameter)/
                                                                      (2*particle_density*particle_diameter/2)*log((1-vapor_mass_frac_inf)/(1-vapor_mass_frac_r(particle_diameter, pressure)))) #41

diameter_change_due_to_evaporation_updated = lambda dt, particle_diameter, pressure, v: 2*dt*(-1*density_mixture(particle_diameter, pressure)*diffusion_coefficient_water_in_air*sherwood(v, particle_diameter)/
                                                                      (2*particle_density*particle_diameter/2)*log((1-vapor_mass_frac_inf)/(1-vapor_mass_frac_r(particle_diameter, pressure)))) #41

p_size = 10e-6

p_size_final = p_size + diameter_change_due_to_evaporation(1, p_size, p_train, 10) #this is too fast?


#with evaporation sneezing, breathing, coughing diameter change over time
evaporation_plots_v = [20, 10, 1]
evaporation_plots_d = [1000e-6, 100e-6, 10e-6]

total_time = 20
dt = 0.001
x_time = np.arange(0, total_time, dt)

fig, ax = plt.subplots(figsize=(16,5))
fig.set_dpi(200)
ax.set_ylabel('diameter [μm]')
ax.set_xlabel('t [s]')
ax.set_yscale('log')
ax.set_xscale('log')
#ax.set_ylim([0, 10e2])



for d in evaporation_plots_d:
    for v in evaporation_plots_v:    
        y_d = np.zeros(shape=(len(x_time)))
        y_d[0] = d
        for id, t in enumerate(x_time):
            if(y_d[id] <= 0):
                new_d = 0
            else:
                new_d = y_d[id] + diameter_change_due_to_evaporation_updated(dt, y_d[id], p_train, v)
                if(id +2 <= len(x_time)):
                    y_d[id+1] = new_d
               
        ax.plot(x_time, y_d/1e-6, label=f'd: {math.floor(d/1e-6)}μm; v={v}m/s') #diameter change

ax.legend()
